#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""Odoo API Extensons."""

import types

from odoo import api as _odoo_api
from odoo.api import (
    Environment,
    Meta,
    attrsetter,
    constrains,
    depends,
    guess,
    model,
    model_cr,
    model_create_multi,
    model_create_single,
    noguess,
    onchange,
)
from odoo.api import one as _one
from odoo.api import returns
from typing_extensions import deprecated

__all__ = (
    "Environment",
    "contextual",
    "guess",
    "mimic",
    "model",
    "model_cr",
    "model_create_multi",
    "model_create_single",
    "multi",
    "onupdate",
    "requires_singleton",
    "Meta",
    "guess",
    "noguess",
    "one",
    "constrains",
    "depends",
    "onchange",
    "returns",
    "attrsetter",
)

try:
    from odoo.api import multi
except ImportError:

    def multi(f):
        return f


@deprecated("Removed in future Odoo/xoeuf versions")
def one(f):
    return _one(f)


@deprecated("Removed in future xoeuf versions")
def contextual(func):
    """Decorate a function to run within a proper Odoo environment.

    You should decorate every function that represents an "entry point" for
    working with the ORM.  A proper `Environment`:class: is entered upon
    calling the function.

    .. deprecated:: 3.0.3

    """

    def inner(*args, **kwargs):
        with Environment.manage():
            return func(*args, **kwargs)

    return inner


@deprecated("Removed in future xoeuf versions")
def requires_singleton(f):
    """An idiomatic alias for `api.multi()`.

    This is exactly the same as `api.multi()`, however it's expected to be
    used when the code you're decorating requires a singleton recordset.

    Notice we don't fail at the method call, but only if the actual code
    executes a command that requires such a condition to be met (for instance,
    accessing a field in ``self``.)

    .. deprecated:: 3.0.3

    """
    return multi(f)


@deprecated("Removed in future xoeuf versions")
def mimic(original):
    """Apply the API guess of `original` to the decorated function.

    Usage::

       def f1(self, cr, uid, ids, context=None):
           # Actually any valid signature

       @api.mimic(f1)
       def f2(*args, **kwargs):
           pass

    .. deprecated:: 3.0.3

    """
    method = guess(original)
    # Odoo stores the decorator in the _api attribute.  But Odoo 10 only
    # stores the name of the API method.
    decorator = method._api
    if isinstance(decorator, types.FunctionType):
        return decorator
    else:
        return getattr(_odoo_api, decorator)


def onupdate(*args):
    """A decorator to trigger updates on dependencies.

    Return a decorator that specifies the field dependencies of an updater
    method.  Each argument must be a string that consists in a dot-separated
    sequence of field names::

        @api.onupdate('partner_id.name', 'partner_id.is_company')
        def update_pname(self):
            for record in self:
                if record.partner_id.is_company:
                    record.pname = (record.partner_id.name or "").upper()
                else:
                    record.pname = record.partner_id.name

    One may also pass a single function as argument. In that case, the
    dependencies are given by calling the function with the field's model.

    .. note:: ``@onupdate`` is very similar to ``@constraint`` but with just
       one key difference: It allow dot-separated fields in arguments.

    .. versionadded: 0.46.0

    """
    if args and callable(args[0]):
        args = args[0]
    elif any("id" in arg.split(".") for arg in args):
        raise NotImplementedError("Updater method cannot depend on field 'id'.")
    return _odoo_api.attrsetter("_onupdates", args)
