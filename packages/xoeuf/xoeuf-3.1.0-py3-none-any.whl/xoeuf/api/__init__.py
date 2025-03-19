# At the time of make this API it seems that usage of @api.X in our model is
# rather reduced.  Running:
#
#    rg -IN '@api.' | sed 's/[[:space:]]*//' | cut -d'(' -f1 | sort -u
#
# Yields this list:
#
#    @api.constrains
#    @api.depends
#    @api.model
#    @api.model_cr
#    @api.model_create_multi
#    @api.multi
#    @api.onchange
#    @api.one
#    @api.onupdate
#    @api.requires_singleton
#    @api.returns
#
#  To cover more space:
#
#    rg -IN '[^@]api(\.[\w_]+)+' --glob '*.py'
#    rg -IN 'api import' --glob '*.py'
#
#  Extends this list including:
#
#    api.Environment  (in some cases import directly from odoo.api)
#    api.attrsetter
#
# In Odoo 17, the list of functions in the __all__ of odoo.api is just:
#
#    Environment, Meta, model, constrains, depends, onchange, returns, and
#    call_kw.
#
# attrsetter is still implemented, but it seems an internal function.
#
# In future versions of xoeuf, we'll remove all non used.  As of now we'll
# deprecate of the unused ones that are implemented by us.


from odoo.release import version_info

__all__ = (  # noqa
    "Environment",
    "contextual",
    "guess",
    "mimic",
    "model",
    "model_cr",
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


if (12, 0) <= version_info < (13, 0):
    from ._api_12 import *  # noqa
else:
    raise ImportError("Invalid Odoo version")
