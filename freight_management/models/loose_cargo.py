# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightLooseCargo(models.Model):
    _name = 'freight.loose.cargo'
    # _rec_name = "number"

    packs = fields.Integer(string='Packs')
    weight = fields.Float(string='Weight')
    volume = fields.Float(string='Volume')
    length = fields.Float(string='Length')
    width = fields.Float(string='Width')
    height = fields.Float(string='Height')

    uw = fields.Many2one('uom.uom', string='UW')
    package_type = fields.Selection([('palatized', 'Palatized'),
                                        ('cartons', 'Cartons'),
                                        ('bulk', 'Bulk'),
                                        ('drums', 'Drums'),
                                        ('other', 'Others')], default='palatized', required=True, string='Pk. Type')

    uv = fields.Many2one('uom.uom', string='UV')
    ud = fields.Many2one('uom.uom', string='UD')
    commodity_id = fields.Many2one('freight.commodity', string='Commodity')
    # freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')
