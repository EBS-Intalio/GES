# -*- coding: utf-8 -*"-
from odoo import models, fields

class AccountFinancialLineItem(models.Model):
    _name = 'account.financial.line.item'
    _description = 'Account Financial Line Item'

    code = fields.Char("Code")
    name = fields.Char("Name", required=True)
    account_ids = fields.One2many(comodel_name='account.account', inverse_name='financial_line_item')
    type = fields.Many2one('account.account.type', string='Type')