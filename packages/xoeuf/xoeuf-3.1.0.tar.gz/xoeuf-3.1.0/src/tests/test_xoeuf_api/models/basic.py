#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xoeuf import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    text_field = fields.Char()

    # 'name' and 'partner_id.name' are the same thing.
    @api.onupdate("partner_id", "name", "partner_id.name")
    def update_text_field(self):
        for record in self:
            record.text_field = record.get_text_field()

    @api.requires_singleton
    def get_text_field(self):
        return "s2 %s" % self.name


class TextOnUpdateMixin(models.AbstractModel):
    _name = "test.onupdate.mixin"

    user_id = fields.Many2one("res.users")
    name = fields.Char()

    @api.onupdate("user_id", "user_id.partner_id.name")
    def test_mixin_onupdate(self):
        for record in self:
            record.name = "Updated: {name}".format(name=record.user_id.name)


class Model(models.Model):
    _name = "test.onupdate.big.model"
    _inherit = TextOnUpdateMixin._name
