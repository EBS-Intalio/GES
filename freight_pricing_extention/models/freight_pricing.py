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
    #Air
    first_flight_no = fields.Char("Flight No")
    second_flight_no = fields.Char("Flight No")
    third_flight_no = fields.Char("Flight No")
    #Sea
    first_vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    second_vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    third_vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    first_origin_days = fields.Integer('Free days at Origin')
    second_origin_days = fields.Integer('Free days at Origin')
    third_origin_days = fields.Integer('Free days at Origin')
    first_port_days = fields.Integer('Free days at Destination')
    second_port_days = fields.Integer('Free days at Destination')
    third_port_days = fields.Integer('Free days at Destination')
    #Land
    first_trucker = fields.Many2one('freight.trucker', String='Trucker')
    second_trucker = fields.Many2one('freight.trucker', String='Trucker')
    third_trucker = fields.Many2one('freight.trucker', String='Trucker')
    first_rout = fields.Char('Rout')
    second_rout = fields.Char('Rout')
    third_rout = fields.Char('Rout')
    first_origin_country = fields.Many2one('res.country', 'Origin Country')
    first_origin_country_border = fields.Many2one('res.country', 'Origin Country Border')
    first_transit_country = fields.Many2one('res.country', 'Transit Country')
    first_transit_country_border = fields.Many2one('res.country', 'Transit Country Border')
    second_origin_country = fields.Many2one('res.country', 'Origin Country')
    second_origin_country_border = fields.Many2one('res.country', 'Origin Country Border')
    second_transit_country = fields.Many2one('res.country', 'Transit Country')
    second_transit_country_border = fields.Many2one('res.country', 'Transit Country Border')
    third_origin_country = fields.Many2one('res.country', 'Origin Country')
    third_origin_country_border = fields.Many2one('res.country', 'Origin Country Border')
    third_transit_country = fields.Many2one('res.country', 'Transit Country')
    third_transit_country_border = fields.Many2one('res.country', 'Transit Country Border')

    @api.onchange('different_amount')
    def onchange_different_amount(self):
        for record in self:
            if record.different_amount == 'price_1':
                #Air
                # record.preferred_airline_id = record.first_carrier_id.id
                record.freight_flight_no = record.first_flight_no
                #sea
                record.freight_shipping_line_id = record.first_carrier_id.id
                record.freight_vessel_id = record.first_vessel_id.id
                record.origin_days = record.first_origin_days
                record.Port_days = record.first_port_days
                #land
                record.origin_country = record.first_origin_country.id
                record.origin_country_border = record.first_origin_country_border.id
                record.transit_country = record.first_transit_country.id
                record.transit_country_border = record.first_transit_country_border.id
                record.freight_trucker = record.first_trucker.id
                record.rout = record.first_rout
            elif record.different_amount == 'price_2':
                #Air
                # record.preferred_airline_id = record.second_carrier_id.id
                record.freight_flight_no = record.second_flight_no
                #Sea
                record.freight_shipping_line_id = record.second_carrier_id.id
                record.freight_vessel_id = record.second_vessel_id.id
                record.origin_days = record.second_origin_days
                record.Port_days = record.second_port_days
                #Land
                record.origin_country = record.second_origin_country.id
                record.origin_country_border = record.second_origin_country_border.id
                record.transit_country = record.second_transit_country.id
                record.transit_country_border = record.second_transit_country_border.id
                record.freight_trucker = record.third_trucker.id
                record.rout = record.second_rout
            elif record.different_amount == 'price_3':
                #Air
                # record.preferred_airline_id = record.third_carrier_id.id
                record.freight_flight_no = record.third_flight_no
                #Sea
                record.freight_shipping_line_id = record.third_carrier_id.id
                record.freight_vessel_id = record.third_vessel_id.id
                record.origin_days = record.third_origin_days
                record.Port_days = record.third_port_days
                #land
                record.origin_country = record.third_origin_country.id
                record.origin_country_border = record.third_origin_country_border.id
                record.transit_country = record.third_transit_country.id
                record.transit_country_border = record.third_transit_country_border.id
                record.freight_trucker = record.second_trucker.id
                record.rout = record.third_rout
