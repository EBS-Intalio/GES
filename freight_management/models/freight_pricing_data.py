# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _

class FreightBookingData(models.Model):
    _name = 'freight.pricing.data'

    pricing_id = fields.Many2one('freight.pricing')
    freight_transport = fields.Selection([('air', 'Air'),
                                           ('ocean', 'Sea'),
                                           ('land', 'Road'),
                                           ('sea_then_air', 'Sea then Air'),
                                           ('air_then_sea', 'Air then Sea'),
                                           ('rail', 'Rail'),
                                           ('courier', 'Courier')], string='Transpotr')
    freight_target_eta = fields.Date('Target ETA')
    freight_target_etd = fields.Date('Target ETD')


    #air
    preferred_airline_id = fields.Many2one('freight.airline', readonly=False)
    freight_flight_no = fields.Char('Flight No')
    #sea
    freight_shipping_line_id  = fields.Many2one('res.partner','Shipping Line')
    freight_vessel_id  = fields.Many2one('freight.vessel','Vessel')
    origin_days = fields.Integer('Free days at Origin')
    port_days = fields.Integer('Free days at Destination')

    # Land
    origin_country = fields.Many2one('res.country', 'Origin Country')
    origin_country_border = fields.Many2one('res.country', 'Origin Country Border')
    transit_country = fields.Many2one('res.country', 'Transit Country')
    transit_country_border = fields.Many2one('res.country', 'Transit Country Border')
    rout = fields.Char('Rout')
    freight_trucker = fields.Many2one('freight.trucker', String='Trucker')
    freight_trucker_number = fields.Char('Trucker No')


    def send_data(self):
        for rec in self:
            pricing_data = {
                'freight_target_eta':rec.freight_target_eta,
                'freight_target_etd':rec.freight_target_etd,
            }
            if rec.freight_transport == 'air':
                pricing_data.update(
                    {
                        'preferred_airline_id':rec.preferred_airline_id and rec.preferred_airline_id.id,
                        'freight_flight_no':rec.freight_flight_no
                    }
                )
            elif rec.freight_transport == 'ocean':
                pricing_data.update(
                    {
                        'freight_shipping_line_id': rec.freight_shipping_line_id and rec.freight_shipping_line_id.id,
                        'freight_vessel_id': rec.freight_vessel_id and rec.freight_vessel_id.id,
                        'origin_days':rec.origin_days,
                        'Port_days':rec.port_days
                    }
                )
            elif rec.freight_transport == 'land':
                pricing_data.update(
                    {
                        'origin_country': rec.origin_country and rec.origin_country.id,
                        'origin_country_border': rec.origin_country_border and rec.origin_country_border.id,
                        'transit_country': rec.transit_country and rec.transit_country.id,
                        'transit_country_border': rec.transit_country_border and rec.transit_country_border.id,
                        'rout': rec.rout ,
                        'freight_trucker': rec.freight_trucker and rec.freight_trucker.id,
                        'freight_trucker_number': rec.freight_trucker_number
                    }
                )
            rec.pricing_id.with_context(from_history=True).write(pricing_data)