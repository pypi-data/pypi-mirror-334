#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from datetime import datetime
from decimal import Decimal
from typing import Dict, Literal, Optional, Union

import pydantic
from typing_extensions import Annotated

from xoeuf import api, fields, models


class PriceAdapter(pydantic.BaseModel):
    type: Literal["price"] = "price"
    value: Decimal
    currency_name: str
    currency_id: int


class DatetimeAdapter(pydantic.BaseModel):
    type: Literal["datetime"] = "datetime"
    value: datetime


class StringAdapter(pydantic.BaseModel):
    type: Literal["str"] = "str"
    value: str
    display_name: Optional[str] = None


class NumberAdapter(pydantic.BaseModel):
    type: Literal["number"] = "number"
    value: Union[int, float]


class Commodity(pydantic.BaseModel):
    name: str
    attributes: Dict[
        str,
        Optional[
            Annotated[
                Union[PriceAdapter, StringAdapter, DatetimeAdapter, NumberAdapter],
                pydantic.Field(discriminator="type"),
            ]
        ],
    ]


class Model(models.Model):
    _name = "test.pydantic.field"

    name = fields.Char()
    static_model = fields.Pydantic(pydantic_model=Commodity)
    dynamic_model = fields.Pydantic(pydantic_model="_get_dynamic_model")

    @api.multi
    def _get_dynamic_model(self):
        class DynamicCommodity(Commodity):
            pass

        return DynamicCommodity


class Inherited(models.Model):
    _name = "test.pydantic.field.inherited"
    _inherit = Model._name


class Delegated(models.Model):
    _name = "test.pydantic.field.delegated"
    _inherits = {Model._name: "model_id"}
    model_id = fields.Many2one(Model._name, ondelete="cascade")

    @api.multi
    def _get_dynamic_model(self):
        class DynamicCommodity(Commodity):
            pass

        return DynamicCommodity
