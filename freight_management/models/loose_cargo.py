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
    # uw = fields
    # commodity = fields
    # uv = fields
    # ud = fields
    uom_id = fields.Many2one('uom.uom', string='Pk. Type', required=True)
    dep_container_id = fields.Many2one('freight.port', string='Dep. Container')
    dep_container_yard_id = fields.Many2one('freight.port', string='Dep. Container Yard')
    arr_container_yard = fields.Many2one('freight.port', string='Arr. Container')
    arr_container_yard_id = fields.Many2one('freight.port', string='Arr. Container Yard')
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')
