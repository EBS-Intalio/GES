# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute='_default_operating_unit_id',
        readonly=False,
    )

    memo = fields.Text("Memo")

    code_journal = fields.Selection(selection=[
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    ], string='CODE Journal',default='a')

    @api.depends('move_id.invoice_line_ids')
    def _default_operating_unit_id(self):
        self.operating_unit_id = self.move_id.operating_unit_id.id