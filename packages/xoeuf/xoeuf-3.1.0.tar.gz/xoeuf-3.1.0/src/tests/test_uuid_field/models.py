#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from xoeuf import fields, models


class Model(models.Model):
    _name = "test.uuid.field"
    uuid = fields.UUID()
    v7 = fields.UUID(default=fields.UUID.uuid7)
