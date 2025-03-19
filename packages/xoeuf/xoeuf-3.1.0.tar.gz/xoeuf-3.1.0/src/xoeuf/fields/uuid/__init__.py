from uuid import uuid4

from odoo import fields


class UUID(fields.Field):
    """A field that uses Postgres UUID type.

    It will accept both UUIDs and (valid) strings in any input.  The value of
    the record and cache will be an UUID instance.  The value for read, export
    and search_read is the string representation of the UUID.

    Null values are None in the record and cache, and False in the read, and
    search_read.  They are the empty string in export.

    """

    type = "uuid"
    column_type = ("uuid", "uuid")

    @staticmethod
    def uuid7(*_args):
        """Return a new uuid7 if package uuid6 is installed, otherwise fallback to uuid4"""
        try:
            from uuid6 import uuid7
        except ImportError:
            return uuid4()
        else:
            return uuid7()

    @staticmethod
    def uuid4(*_args):
        """Return a new uuid4"""
        return uuid4()

    def convert_to_column(self, value, record, values=None, validate=True):
        return str(self.convert_to_cache(value, record, validate=validate))

    def convert_to_cache(self, value, record, validate=True):
        from uuid import UUID

        if value is False or value is None:
            return None
        if isinstance(value, str):
            try:
                return UUID(value)
            except ValueError:
                if validate:
                    raise
                else:
                    return None
        elif isinstance(value, UUID):
            return value
        elif validate:
            raise ValueError(f"Invalid UUID {value}")

    def convert_to_record(self, value, record):
        return value

    def convert_to_read(self, value, record, use_name_get=True):
        return False if not value else str(value)

    def convert_to_write(self, value, record):
        return self.convert_to_read(value, record)

    def convert_to_onchange(self, value, record, names):
        return self.convert_to_read(value, record)

    def convert_to_export(self, value, record):
        if not value:
            return ""
        return str(value)

    def convert_to_display_name(self, value, record):
        if not value:
            return ""
        return str(value)
