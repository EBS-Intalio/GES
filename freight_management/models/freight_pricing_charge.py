# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightPricingCharges(models.Model):
    _inherit = 'freight.pricing.charges'
    _description = 'Freight Pricing Charges'

    freight_request_id = fields.Many2one('freight.job.request', 'Freight Request')
    # currency_type = fields.Selection(([('fc', 'FC'), ('lc', 'LC')]), string='Currency Type')
    # currency_id = fields.Many2one('res.currency', string="Currency", domain="[('active', '=', True)]")
    different_amount = fields.Selection(related='pricing_id.different_amount')
    charge_amount_price_2 = fields.Monetary(currency_field='currency_id', string='Charge Amount 2')
    charge_amount_price_3 = fields.Monetary(currency_field='currency_id', string='Charge Amount 3')
    converted_amount = fields.Float(string='Charge Total Amount', compute="_compute_converted_amount")

    @api.onchange('currency_id')
    def onchange_currency_id(self):
        for line in self:
            if line.pricing_id.currency_id != line.currency_id:
                date = fields.Date.today()
                company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
                multi_currency_amount = line.pricing_id.currency_id._convert(line.charge_total_amount, line.currency_id,
                                                                             company, date)
            else:
                multi_currency_amount = line.charge_total_amount
            line.converted_amount = multi_currency_amount

    @api.depends('charge_total_amount', 'different_amount', 'charge_amount_price_2', 'charge_amount_price_3')
    def _compute_converted_amount(self):
        for line in self:
            if line.pricing_id.currency_id != line.currency_id:
                date = fields.Date.today()
                company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
                multi_currency_amount = line.pricing_id.currency_id._convert(line.charge_total_amount, line.currency_id, company, date)
            else:
                multi_currency_amount = line.charge_total_amount

            line.converted_amount = multi_currency_amount

    @api.depends('charge_amount', 'charge_amount_price_2', 'charge_amount_price_3', 'margin_amount', 'different_amount')
    def _compute_charge_total_amount(self):
        for line in self:
            if line.different_amount == 'price_1':
                charge_total_amount = line.charge_amount + line.margin_amount
            elif line.different_amount == 'price_2':
                charge_total_amount = line.charge_amount_price_2 + line.margin_amount
            else:
                charge_total_amount = line.charge_amount_price_3 + line.margin_amount
            line.charge_total_amount = charge_total_amount

    @api.depends('charge_amount', 'margin_per','charge_amount_price_2','charge_amount_price_3')
    def _compute_charge_amount(self):
        for line in self:
            if line.different_amount == 'price_1':
                margin_amount = (line.charge_amount * line.margin_per) / 100
            elif line.different_amount == 'price_2':
                margin_amount = (line.charge_amount_price_2 * line.margin_per) / 100
            else:
                margin_amount = (line.charge_amount_price_3 * line.margin_per) / 100
            line.margin_amount = margin_amount

    @api.depends('charge_amount', 'margin_amount','charge_amount_price_2','charge_amount_price_3')
    def _inverse_charge_amount(self):
        for line in self:
            margin_per = 0
            if line.different_amount == 'price_1' and line.charge_amount:
                margin_per = (line.margin_amount * 100) / line.charge_amount
            elif line.different_amount == 'price_2' and line.charge_amount_price_2:
                margin_per = (line.margin_amount * 100) / line.charge_amount_price_2
            elif line.charge_amount_price_3 and line.different_amount == 'price_3':
                margin_per = (line.margin_amount * 100) / line.charge_amount_price_3
            line.margin_per = margin_per
