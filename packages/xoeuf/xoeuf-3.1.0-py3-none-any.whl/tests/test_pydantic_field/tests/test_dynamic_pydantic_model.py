#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENSE file allows you to.
#

from odoo.tests.common import TransactionCase, tagged

from ..models import Commodity

COMMODITY_DUMP = {
    "name": "Commodity",
    "attributes": {
        "start": {"type": "datetime", "value": "2025-03-10T00:00:00Z"},
        "price": {"type": "price", "value": "100", "currency_name": "EUR", "currency_id": 1},
        "regimen": {"type": "str", "value": "TI", "display_name": "All inclusive"},
        "travelers": {"type": "number", "value": 1},
    },
}
COMMODITY = Commodity.model_validate(COMMODITY_DUMP)


@tagged("-at_install", "-post_install", "-standard")
class Base(TransactionCase):
    model_name: str

    def test_create_with_instance(self):
        res = self.env[self.model_name].create({"dynamic_model": COMMODITY})
        self.assertEqual(res.dynamic_model.model_dump(mode="json"), COMMODITY_DUMP)

    def test_create_with_dump(self):
        res = self.env[self.model_name].create({"dynamic_model": COMMODITY_DUMP})
        self.assertEqual(res.dynamic_model.model_dump(mode="json"), COMMODITY_DUMP)

    def test_write_with_instance(self):
        res = self.env[self.model_name].create({})
        self.assertEqual(res.dynamic_model, False)
        res.write({"dynamic_model": COMMODITY})
        self.assertEqual(res.dynamic_model.model_dump(mode="json"), COMMODITY_DUMP)

    def test_write_with_dump(self):
        res = self.env[self.model_name].create({})
        self.assertEqual(res.dynamic_model, False)
        res.write({"dynamic_model": COMMODITY_DUMP})
        self.assertEqual(res.dynamic_model.model_dump(mode="json"), COMMODITY_DUMP)

    def test_assignment_with_instance(self):
        res = self.env[self.model_name].create({})
        self.assertEqual(res.dynamic_model, False)
        res.dynamic_model = COMMODITY
        self.assertEqual(res.dynamic_model.model_dump(mode="json"), COMMODITY_DUMP)

    def test_read(self):
        res = self.env[self.model_name].create({"dynamic_model": COMMODITY_DUMP})
        self.assertEqual(
            res.read(["dynamic_model"]),
            [{"id": res.id, "dynamic_model": COMMODITY_DUMP}],
        )

    def test_create_with_invalid_data(self):
        with self.assertRaises(ValueError):
            self.env[self.model_name].create({"dynamic_model": [1]})

    def test_write_with_invalid_data(self):
        res = self.env[self.model_name].create({})
        with self.assertRaises(ValueError):
            res.write({"dynamic_model": [1]})

    def test_assignment_with_invalid_data(self):
        res = self.env[self.model_name].create({})
        with self.assertRaises(ValueError):
            res.dynamic_model = [1]


@tagged("at_install")
class TestDynamicPydanticField(Base):
    maxDiff = None
    model_name: str = "test.pydantic.field"


@tagged("at_install")
class TestInheritedDynamicPydanticField(Base):
    maxDiff = None
    model_name: str = "test.pydantic.field.inherited"


@tagged("at_install")
class TestDelegatedDynamicPydanticField(Base):
    maxDiff = None
    model_name: str = "test.pydantic.field.delegated"
