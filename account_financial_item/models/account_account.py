# -*- coding: utf-8 -*"-
from odoo import models, fields

class AccountAccountInherit(models.Model):
    _inherit = 'account.account'

    financial_line_item = fields.Many2one('account.financial.line.item', string="Financial Line Item")