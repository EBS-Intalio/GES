# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
from json import dumps
import json


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricing_id = fields.Many2one('freight.pricing')

    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True, copy=False)

    margin_per = fields.Float(string='Margin(%)',
                              compute='_compute_charge_total_amount', readonly=False)
    margin_amount = fields.Monetary(currency_field='currency_id', string='Margin Amount',
                                    compute='_compute_charge_total_amount', readonly=False)
    charge_total_amount = fields.Monetary(currency_field='currency_id', string='Charge Total Amount',
                                          compute='_compute_charge_total_amount')

    @api.depends('price_unit', 'margin_per', 'margin_amount')
    def _compute_charge_total_amount(self):
        margin_amount = charge_total_amount = margin_per = 0
        for line in self:
            if line.margin_per and not line.margin_amount:
                margin_amount = (line.price_unit * line.margin_per) / 100
                charge_total_amount = line.price_unit + margin_amount

            elif line.margin_amount and not line.margin_per:
                margin_per = (line.margin_amount * 100) / line.price_unit
                charge_total_amount = line.price_unit + margin_amount

            line.margin_amount = margin_amount
            line.margin_amount = margin_amount
            line.charge_total_amount = charge_total_amount


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'
    _description = 'Sale Order Template'

    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')
