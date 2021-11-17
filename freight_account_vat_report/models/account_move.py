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
    price_subtotal_sign = fields.Float(string='Net Amount', readonly=True,compute='_recalculate_amount_in_sign')
    tax_amount_sign = fields.Float(string='TAX Amount', readonly=True,compute='_recalculate_amount_in_sign')
    gross_amount_sign = fields.Float(string='GROSS Amount',readonly=True, compute='_recalculate_amount_in_sign')

    @api.depends('move_id.invoice_date')
    def get_period_name(self):
        for rec in self:
            rec.invoice_date_period = rec.invoice_date.strftime("%b, %Y")

    @api.depends('price_subtotal', 'tax_amount', 'gross_amount','move_id.move_type')
    def _recalculate_amount_in_sign(self):
        for line in self:
            # here we get the sign= -1  in invoice if it out_refund or in_refund
            sign = -1 if line.move_id.move_type in ('out_refund', 'in_refund') else 1
            line.price_subtotal_sign = line.price_subtotal * sign
            line.tax_amount_sign = line.tax_amount * sign
            line.gross_amount_sign = line.gross_amount * sign
