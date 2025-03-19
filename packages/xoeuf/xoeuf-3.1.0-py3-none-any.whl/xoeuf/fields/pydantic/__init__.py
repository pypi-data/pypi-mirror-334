from typing import TYPE_CHECKING, Callable, Generic, Type, TypeVar, Union

from odoo import fields, models
from psycopg2.extras import Json
from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


class Pydantic(fields.Field, Generic[M]):
    """A field that uses Postgres JSONB type and a pydantic model to validate it.

    The argument `pydantic_model` must be either a Pydantic Model (static model), a string or a
    callable to get the (dynamic) Pydantic Model. If is a string the Odoo model should a have method
    that takes no arguments and returns the pydantic model. If is a callable it must take a single
    argument (the recordset) and return a pydantic model.

    """

    type = "pydantic"
    column_type = ("jsonb", "jsonb")

    _slots = {"pydantic_model": None}

    if TYPE_CHECKING:
        pydantic_model: Union[Type[M], str, Callable[[models.BaseModel], Type[M]]]

    @property
    def _description_searchable(self):
        return False

    @property
    def _description_sortable(self):
        return False

    def __init__(self, **kwargs):
        kwargs["readonly"] = True
        super().__init__(**kwargs)

    def new(self, **kwargs):
        # required to make it work on delegated fields.
        kwargs = dict(self.args, **kwargs)
        return super().new(**kwargs)

    def _get_pydantic_model(self, record) -> Type[BaseModel]:
        arg = self.pydantic_model
        if isinstance(arg, type) and issubclass(arg, BaseModel):
            result = arg
        elif isinstance(arg, str):
            result = getattr(record, arg)()
        else:
            result = arg(record)
        if not issubclass(result, BaseModel):
            raise TypeError(f"{arg} doesn't return a Pydantic Model")
        return result

    def convert_to_cache(self, value, record, validate=True):
        """Convert ``value`` to the cache format; ``value`` may come from an
        assignment, or have the format of methods :meth:`BaseModel.read` or
        :meth:`BaseModel.write`. If the value represents a recordset, it should
        be added for prefetching on ``record``.

        :param bool validate: when True, field-specific validation of ``value``
            will be performed
        """
        if not self.required and (value is False or value is None):
            return False
        if not isinstance(value, BaseModel):
            try:
                pydantic_model = self._get_pydantic_model(record)
                return pydantic_model.model_validate(value)
            except ValueError:
                if validate:
                    raise
                else:
                    return False
        else:
            return value

    def convert_to_column(self, value, record, values=None, validate=True):
        """Convert ``value`` from the ``write`` format to the SQL format."""
        if not self.required and (value is False or value is None):
            return None
        try:
            if isinstance(value, BaseModel):
                return Json(value.model_dump(mode="json"))
            elif validate:
                pydantic_model = self._get_pydantic_model(record)
                return Json(pydantic_model.model_validate(value).model_dump(mode="json"))
            else:
                return None
        except ValueError:
            if validate:
                raise
            else:
                return None

    def convert_to_record(self, value, record):
        """Convert ``value`` from the cache format to the record format.
        If the value represents a recordset, it should share the prefetching of
        ``record``.
        """
        # We test for BaseModel and not the pydantic model because dynamically created (per record
        # set) might not be the exact same class.
        assert not value or isinstance(value, BaseModel)
        return value

    def convert_to_read(self, value, record, use_name_get=True):
        """Convert ``value`` from the record format to the format returned by
        method :meth:`BaseModel.read`.

        :param bool use_name_get: when True, the value's display name will be
            computed using :meth:`BaseModel.name_get`, if relevant for the field
        """
        return False if not value else value.model_dump(mode="json")

    def convert_to_write(self, value, record):
        """Convert ``value`` from the record format to the format of method
        :meth:`BaseModel.write`.
        """
        # We test for BaseModel and not the pydantic model because dynamically created (per record
        # set) might not be the exact same class.
        assert not value or isinstance(value, BaseModel)
        return value.model_dump(mode="json") if isinstance(value, BaseModel) else None
