#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from uuid import UUID

from odoo.tests.common import SingleTransactionCase
from uuid6 import uuid7


class TestUUID7(SingleTransactionCase):
    def test_create_with_default(self):
        model = self.env["test.uuid.field"].create({})
        self.assertIsInstance(model.v7, UUID)

    def test_create_with_uuid(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": uuid})
        self.assertEqual(model.uuid, uuid)

    def test_create_with_uuid_string(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": str(uuid)})
        self.assertEqual(model.uuid, uuid)

    def test_write_with_uuid(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({})
        model.write({"uuid": uuid})
        self.assertEqual(model.uuid, uuid)

    def test_write_with_uuid_string(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({})
        model.write({"uuid": str(uuid)})
        self.assertEqual(model.uuid, uuid)

    def test_assign_uuid(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({})
        model.uuid = uuid
        self.assertEqual(model.uuid, uuid)

    def test_assign_uuid_string(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({})
        model.uuid = str(uuid)
        self.assertEqual(model.uuid, uuid)

    def test_reads_is_always_string(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": uuid})
        [result] = model.read(["uuid"])
        self.assertEqual(result["uuid"], str(uuid))

    def test_search_read_is_always_string(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": uuid})
        result = self.env["test.uuid.field"].search_read([("uuid", "=", uuid)], ["uuid"])
        self.assertEqual(result, [{"id": model.id, "uuid": str(uuid)}])

    def test_search_read_is_always_string_searching_by_str(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": uuid})
        result = self.env["test.uuid.field"].search_read([("uuid", "=", str(uuid))], ["uuid"])
        self.assertEqual(result, [{"id": model.id, "uuid": str(uuid)}])

    def test_search_by_string(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": uuid})
        result = self.env["test.uuid.field"].search([("uuid", "=", str(uuid))])
        self.assertEqual(result, model)

    def test_search_by_uuid(self):
        uuid = uuid7()
        model = self.env["test.uuid.field"].create({"uuid": uuid})
        result = self.env["test.uuid.field"].search([("uuid", "=", uuid)])
        self.assertEqual(result, model)

    def test_null_value_in_record_none(self):
        model = self.env["test.uuid.field"].create({})
        self.assertIsNone(model.uuid)

    def test_null_value_in_read_false(self):
        model = self.env["test.uuid.field"].create({})
        [result] = model.read(["uuid"])
        self.assertIs(result["uuid"], False)
