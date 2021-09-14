# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    freight_request_id = fields.Many2one('freight.job.request', string="Freight Request")
    pricing_id = fields.Many2one('freight.pricing', 'Freight Pricing')
    usd_total_price = fields.Float(string='Total amount in USD',
                                   compute='_compute_usd_aed_amount')
    aed_total_price = fields.Float(string='Total amount in AED',
                                   compute='_compute_usd_aed_amount')
    currency_name = fields.Char(related='currency_id.name')
    contact_id = fields.Many2one('res.partner', string='Contact')
    customer_representative_id = fields.Many2one('res.partner', string='Customer Representative')
    freight_note = fields.Text('Freight Note')

    @api.depends('amount_total')
    def _compute_usd_aed_amount(self):
        for rec in self:
            usd_total_price = 0
            aed_total_price = 0
            if rec.amount_total:
                company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
                usd_currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
                aed_currency = self.env['res.currency'].search([('name', '=', 'AED')], limit=1)
                if usd_currency:
                    usd_total_price = usd_currency._convert(rec.amount_total, rec.currency_id,
                                                            company, fields.Date.today())
                if aed_currency:
                    aed_total_price = aed_currency._convert(rec.amount_total, rec.currency_id,
                                                            company, fields.Date.today())
            rec.usd_total_price = usd_total_price
            rec.aed_total_price = aed_total_price

    def action_confirm(self):
        """
        Create booking based on freight request
        :return:
        """
        res = super(SalesOrder, self).action_confirm()
        if self.freight_request_id:
            self.freight_request_id.create_booking()
        return res
