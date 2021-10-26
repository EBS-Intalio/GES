# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CustomerValuationCharge(models.Model):
    _name = 'customer.valuation.charge'
    _description = 'Customer Valuation Charge'

    freight_order_id = fields.Many2one('freight.order', string="Order")
    code = fields.Char(string="Code")
    amount= fields.Float('Amount')
    currency = fields.Many2one('res.currency',string="Currency")
    ex_rate = fields.Float('Ex Rate')
    dutiable = fields.Boolean('Dutiable')
    add_to_cif = fields.Boolean('Add To Cif ? ')
    inc_in_invoice_lines = fields.Boolean('Inc in invoice lines?')
    distribute_by = fields.Many2one('res.partner',string="distribute by")

