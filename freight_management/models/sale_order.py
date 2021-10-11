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
    vehicle_size = fields.Selection([('3_ton', '3 Ton Truck'),
                                     ('7_ton', '7 Ton Truck'),
                                     ('10_ton', '10 Ton Truck'),
                                     ('12_ton', '12 Meter Trailer'),
                                     ('15_ton', '15 Meter Trailer')], string="Vehicle Size")
    vehicle_type = fields.Selection([('flat_bed', 'Flat Bed'),
                                     ('full_box', 'Full Box'),
                                     ('curtain_slider', 'Curtain Slider'),
                                     ('53', '53'),
                                     ('hot_shot', 'Hot Shot'),
                                     ('low_bed', 'Low Bed'), ('box_truck', 'Box Truck w/Liftgate')],
                                    string="Vehicle Type")

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
            self.freight_request_id.create_booking(amount_total=self.amount_total)
        return res

    @api.model
    def create(self, vals):
        res = super(SalesOrder, self).create(vals)
        res._compute_section_total_amount()
        return res

    def write(self, vals):
        res = super(SalesOrder, self).write(vals)
        self._compute_section_total_amount()
        return res

    def _compute_section_total_amount(self):
        """
        Compute total section amount
        :return:
        """
        for line in self.order_line:
            section_total = 0
            line_sequence = line.sequence
            if line.display_type == 'line_section':
                available_sequence_line = line.order_id.order_line.filtered(
                                                lambda ln: ln.display_type == 'line_section'
                                                           and ln.sequence > line_sequence
                                                           and ln.sequence != line_sequence).mapped('sequence')
                if available_sequence_line:
                    line_min_sections = min(available_sequence_line)
                    section_total = sum(line.order_id.order_line.filtered(
                                                lambda ln: ln.display_type == False and ln.sequence < line_min_sections
                                                           and ln.sequence > line_sequence).mapped('price_subtotal'))
                else:
                    section_total = sum(line.order_id.order_line.filtered(
                        lambda ln: ln.display_type == False and ln.sequence > line_sequence).mapped('price_subtotal'))
            line.section_total = section_total


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    visible_in_report = fields.Boolean('Visible', default=True)
    section_total = fields.Float(string='Section Total')
