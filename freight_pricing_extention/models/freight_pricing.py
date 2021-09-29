# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FreightPricingInherit(models.Model):
    _inherit = 'freight.pricing'
    _description = 'Freight Pricing'
    _order = 'name desc, id desc'

    first_carrier_id = fields.Many2one('res.partner', string="Carrier 1")
    second_carrier_id = fields.Many2one('res.partner', string="Carrier 2")
    third_carrier_id = fields.Many2one('res.partner', string="Carrier 3")
    first_flight_no = fields.Char("Flight No")
    second_flight_no = fields.Char("Flight No")
    third_flight_no = fields.Char("Flight No")
    first_vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    second_vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    third_vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    first_rout = fields.Char('Rout')
    second_rout = fields.Char('Rout')
    third_rout = fields.Char('Rout')

    # carrier_count = fields.Integer(string='Total carrier', compute='count_carriers', default=0)

    # @api.depends('carrier_ids')
    # def count_carriers(self):
    #     self.carrier_count = len(self.carrier_ids)