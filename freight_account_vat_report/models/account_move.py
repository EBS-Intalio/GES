# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class AccountMove(models.Model):
    _inherit = 'account.move'


class AccountMoveLineVat(models.Model):
    _inherit = 'account.move.line'

    invoice_date = fields.Date(related='move_id.invoice_date', string="Transaction Date")
    branch_id = fields.Many2one('operating.unit', related='move_id.operating_unit_id', string="Location")
    partner_id = fields.Many2one('res.partner', related='move_id.partner_id', string="Customer Name")
    partner_id = fields.Many2one('res.partner', related='move_id.partner_id', string="Customer Name")
    move_type = fields.Selection(related='move_id.move_type', string="Transaction Type")
    invoice_date_period = fields.Char(string='Accounting period Name', compute='get_period_name')
    vat = fields.Char(string='Tax REG Number', related='partner_id.vat')

    @api.depends('move_id.invoice_date')
    def get_period_name(self):
        for rec in self:
            rec.invoice_date_period = rec.invoice_date.strftime("%b, %Y")
