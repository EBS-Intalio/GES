# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConsoleProfitLossSummaryLines(models.Model):
    _name = 'console.profit.loss.summary.lines'

    job_number = fields.Many2one('freight.operation', string="Job Number")
    branch = fields.Many2one('operating.unit', string="Branch")
    department = fields.Many2one('hr.department', string="Department")
    invoice_date = fields.Date(string="Invoice Date")
    amount = fields.Float(string="Amount")
    console_id = fields.Many2one('consol.details', string="Console")
    post_date = fields.Date(string="Post Date")
    transaction_no = fields.Char(string="Transaction No")
    ledger = fields.Many2one('account.move', string="Ledger")
    job_local_ref = fields.Char(string="Job Local Reference")
    org = fields.Many2one('res.partner', string="Partner")
    recognized_date = fields.Date(string="Recognized Date")
    date_reversed = fields.Date(string="Date Reversed")
    audit_details = fields.Date(string="Audit Details")
    audited_by = fields.Many2one('res.users', string="Audited By")
    charge_code = fields.Many2one('product.product', string="Charge Code")
