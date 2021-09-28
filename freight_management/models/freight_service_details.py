# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightServiceDetails(models.Model):
    _name = 'freight.service.details'

    service_type = fields.Selection([('fum', 'Fumigation'),
                                   ('qin', 'Quarantine Inspection'),
                                   ('cho', 'Customs Hold'),
                                   ('qup', 'Quarantine Unpack'),
                                   ('tai', 'Tailgate'),
                                   ('xin', 'Extra Inspection'),
                                   ('svy', 'Survey'),
                                   ('cln', 'Cleaning'),
                                   ('wsh', 'Washing'),
                                   ('fcs', 'FCL Free Storage'),
                                   ('fus', 'FCL Underbond Storage'),
                                   ('ste', 'Steam Cleaning')], string='Type')
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')

