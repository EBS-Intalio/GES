# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConsoleProfitLossDetailLines(models.Model):
    _name = 'console.profit.loss.detail.lines'

    job_number = fields.Many2one('freight.operation', string="Job Number")
    branch = fields.Many2one('operating.unit', string="Branch")
    department = fields.Many2one('hr.department', string="Department")
    description = fields.Char(string="Description")
    job_local_ref = fields.Char(string="Job Local Reference")
    revenue = fields.Float(string="Revenue")
    wip = fields.Float(string="WIP")
    cost = fields.Float(string="Cost")
    accrual = fields.Float(string="Accrual")
    profit_loss = fields.Float(string="Profit/Loss")
    margin = fields.Float(string="Margin")
    console_id = fields.Many2one('consol.details', string="Console")
    trans_type = fields.Selection([('ar_invoice', 'AR'),
                                   ('ap_invoice', 'AP'),
                                   ('entry', 'Entry')], default='entry', string="Trans. Type")
    charge_code = fields.Many2one('product.product', string="Charge Code")

