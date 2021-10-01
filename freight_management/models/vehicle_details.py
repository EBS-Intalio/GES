# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightVehicleDetails(models.Model):
    _name = 'vehicle.details'

    name = fields.Char(string='Vehicle#', required=True)
    count = fields.Integer(string='Count')
    vehicle_type = fields.Selection([('15ft', '15FT'), ('12ft', '12FT')], string="Vehicle Type")
    commodity_id = fields.Many2one('freight.commodity', string='Commodity')
    way_bill = fields.Char(string='Way Bill')
    transporter_id = fields.Many2one('res.partner', string='Transporter')
    partner_driver_id = fields.Many2one('res.partner', string='Driver Name')
    driver_id = fields.Char(related='partner_driver_id.driver_id', readonly=False)
