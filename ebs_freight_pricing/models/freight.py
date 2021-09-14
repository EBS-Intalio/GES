# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
from json import dumps
import json


class FreightOperation(models.Model):
    _inherit = 'freight.operation'
    _description = 'Freight Operation'

    pricing_id = fields.Many2one('freight.pricing', string='Shipment Pricing')

    # checklist_id = fields.Many2one('processing.checklist', string='Processing Checklist', )

    show_create_processing_checklist = fields.Boolean(related='booking_id.show_create_processing_checklist')

    def button_processing_checklist(self):
        action = {
            'name': _('Processing Checklist'),
            'type': 'ir.actions.act_window',
            'res_model': 'processing.checklist',
            'target': 'current',
        }
        ope = self.env['processing.checklist'].search([('book_id', '=', self.booking_id.id)], limit=1)
        action['domain'] = [('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action