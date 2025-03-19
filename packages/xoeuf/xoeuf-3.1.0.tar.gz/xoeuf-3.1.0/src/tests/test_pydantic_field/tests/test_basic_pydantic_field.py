#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENSE file allows you to.
#
from datetime import datetime
from decimal import Decimal

from odoo.tests.common import TransactionCase, tagged
from pytz import UTC

from ..models import Commodity, DatetimeAdapter, NumberAdapter, PriceAdapter, StringAdapter

COMMODITY = Commodity(
    name="Commodity",
    attributes={
        "start": DatetimeAdapter(value=datetime(2025, 3, 10, tzinfo=UTC)),
        "price": PriceAdapter(value=Decimal.from_float(100), currency_id=1, currency_name="EUR"),
        "regimen": StringAdapter(value="TI", display_name="All inclusive"),
        "travelers": NumberAdapter(value=3),
    },
)


@tagged("-at_install", "-post_install", "-standard")
class Base(TransactionCase):
    model_name: str

    def test_create_with_instance(self):
        res = self.env[self.model_name].create({"static_model": COMMODITY})
        self.assertEqual(res.static_model, COMMODITY)

    def test_create_with_dump(self):
        res = self.env[self.model_name].create({"static_model": COMMODITY.model_dump(mode="json")})
        self.assertEqual(res.static_model, COMMODITY)

    def test_write_with_instance(self):
        res = self.env[self.model_name].create({})
        self.assertEqual(res.static_model, False)
        res.write({"static_model": COMMODITY})
        self.assertEqual(res.static_model, COMMODITY)

    def test_write_with_dump(self):
        res = self.env[self.model_name].create({})
        self.assertEqual(res.static_model, False)
        res.write({"static_model": COMMODITY.model_dump(mode="json")})
        self.assertEqual(res.static_model, COMMODITY)

    def test_assignment_with_instance(self):
        res = self.env[self.model_name].create({})
        self.assertEqual(res.static_model, False)
        res.static_model = COMMODITY
        self.assertEqual(res.static_model, COMMODITY)

    def test_read(self):
        res = self.env[self.model_name].create({"static_model": COMMODITY})
        self.assertEqual(
            res.read(["static_model"]),
            [{"id": res.id, "static_model": COMMODITY.model_dump(mode="json")}],
        )

    def test_create_with_invalid_data(self):
        with self.assertRaises(ValueError):
            self.env[self.model_name].create({"static_model": [1]})

    def test_write_with_invalid_data(self):
        res = self.env[self.model_name].create({})
        with self.assertRaises(ValueError):
            res.write({"static_model": [1]})

    def test_assignment_with_invalid_data(self):
        res = self.env[self.model_name].create({})
        with self.assertRaises(ValueError):
            res.static_model = [1]


@tagged("at_install")
class TestPydanticField(Base):
    model_name: str = "test.pydantic.field"


@tagged("at_install")
class TestInheritedPydanticField(Base):
    model_name: str = "test.pydantic.field.inherited"


@tagged("at_install")
class TestDelegatedPydanticField(Base):
    model_name: str = "test.pydantic.field.delegated"
