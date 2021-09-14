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
    checklist_id = fields.Many2one('processing.checklist', string='Processing Checklist')
    state = fields.Selection(([('draft', 'Draft'),
                               # ('processing_checklist', 'Processing Checklist'),
                               ('ship_order', 'Ship Order')]),
                             string='Status', default='draft')

    show_create_processing_checklist = fields.Boolean("Show create checklist", default=False)


    def create_processing_checklist(self):
        checklist_id = self.env['processing.checklist'].sudo().create({
            'state': 'draft',
            'transport': self.transport,
            'book_id': self.id,

        })
        if checklist_id:
            # self.state = 'processing_checklist'
            self.show_create_processing_checklist = True
            self.checklist_id = checklist_id.id,

    def button_processing_checklist(self):
        action = {
            'name': _('Processing Checklist'),
            'type': 'ir.actions.act_window',
            'res_model': 'processing.checklist',
            'target': 'current',
        }
        ope = self.env['processing.checklist'].search([('book_id', '=', self.id)], limit=1)
        action['domain'] = [('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action

    def convert_to_operation(self):
        name_act = ''
        for book in self:
            res = self.convert_fields_to_dict()
            if res.get('operation') == 'master':
                name_act = 'Master'
                res['name'] = self.env['ir.sequence'].next_by_code('operation.master') or _('New')
            elif res.get('operation') == 'house':
                name_act = 'House'
                res['name'] = self.env['ir.sequence'].next_by_code('operation.house') or _('New')
            elif res.get('operation') == 'direct':
                name_act = 'Direct'
                res['name'] = self.env['ir.sequence'].next_by_code('operation.direct') or _('New')
            form_view = self.env.ref('freight.view_freight_operation_form')
            res.update({'default_booking_id': book.id})
            book.write({'state':'ship_order'})
            return {
                'name': name_act,
                'res_model': 'freight.operation',
                'type': 'ir.actions.act_window',
                'views': [(form_view and form_view.id, 'form')],
                'context':res,
            }
    def create_booking_pricing(self):
        sale_order_template_id = self.env['sale.order.template'].search([('transport', '=', self.transport)], limit=1)

        pricing = self.env['freight.pricing'].create({
            'state': 'draft',
            'freight_id': self.freight_id.id,
            'sale_order_template_id': sale_order_template_id.id,
            'book_id': self.id})
        order_lines = []
        for line in sale_order_template_id.sale_order_template_line_ids:
            if line.product_id:
                order_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'pricing_id': pricing.id,
                }))
        pricing.update({'charges_ids': order_lines})
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
