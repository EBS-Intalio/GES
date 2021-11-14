# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute='_default_operating_unit_id',
        readonly=False,
        store=True
    )

    memo = fields.Text("Memo")

    @api.depends("move_id.operating_unit_id")
    def _default_operating_unit_id(self):
        for rec in self:
            rec.operating_unit_id = rec.move_id.operating_unit_id.id