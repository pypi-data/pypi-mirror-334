#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENSE file allows you to.
#
"""Allows Odoo methods to return Pydantic models directly."""

import pydantic


def setup_pydantic_adapter():
    """Patches Odoo's DataSet to allow returning Pydantic models from Odoo RPC calls."""
    from odoo.addons.web.controllers.main import DataSet

    if not getattr(DataSet, "_patched_with_xoeuf_pydantic", False):
        DataSet._patched_with_xoeuf_pydantic = True
        real_call_kw = DataSet._call_kw

        def _call_kw(self, model, method, args, kwargs):
            result = real_call_kw(self, model, method, args, kwargs)
            if isinstance(result, pydantic.BaseModel):
                return result.model_dump(mode="json")
            else:
                return result

        DataSet._call_kw = _call_kw
