from xoeuf import api, fields, models


class Model(models.AbstractModel):
    _name = "xoeuf.test_api.model1"

    @api.model
    def modelized(self): ...

    @api.multi
    def multized(self): ...

    @api.one
    def oneized(self): ...

    @api.mimic(oneized)
    def mimiquing(self): ...

    @api.constrains
    def constraining(self): ...

    field1 = fields.Char()
    field2 = fields.Char(compute="_compute_field2")

    @api.depends("field1")
    def _compute_field2(self): ...

    @api.onchange("field1")
    def _on_change_field1(self): ...


@api.contextual
def run(): ...
