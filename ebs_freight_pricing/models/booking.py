# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
from json import dumps
import json


class FreightBooking(models.Model):
    _inherit = 'freight.booking'
    _description = 'Freight Booking'

    pricing_id = fields.Many2one('freight.pricing', string='Shipment Pricing')
    state = fields.Selection(([('draft', 'Draft'),
                               ('pricing', 'Pricing Progress'),
                               ('converted', 'Converted')]),
                             string='Status', default='draft')

    def create_booking_pricing(self):
        sale_order_template_id = self.env['sale.order.template'].search([('transport', '=', self.transport)], limit=1)

        pricing = self.env['freight.pricing'].create({
            'state': 'draft',
            'freight_id': self.freight_id.id,
            'sale_order_template_id': sale_order_template_id.id,
            'book_id': self.id})
        self.state = 'pricing'
        self.pricing_id = pricing.id
        return {
            'name': _('Freight pricing'),
            'view_mode': 'form',
            'view_id': self.env.ref('ebs_freight_pricing.view_freight_pricing_form').id,
            'res_model': 'freight.pricing',
            'type': 'ir.actions.act_window',
            'res_id': pricing.id,
        }

    def button_pricing(self):
        action = {
            'name': _('Freight Pricing'),
            'type': 'ir.actions.act_window',
            'res_model': 'freight.pricing',
            'target': 'current',
        }
        ope = self.env['freight.pricing'].search([('book_id', '=', self.id)], limit=1)
        action['domain'] = [('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action
