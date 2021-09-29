# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPackageExt(models.Model):
    _inherit = 'freight.package'

    is_ltl = fields.Boolean(string='LTL')
    is_lcl = fields.Boolean(string='LCL')

    number = fields.Char(string='Container#', required=False)
    count = fields.Integer(string='Count')
    humidity_percentage = fields.Float(string='Humidity Percentage')
    is_shipper_owned = fields.Boolean(string='Is Shipper Owned?')
    cont_type = fields.Many2one('container.type', string='Container Type')
    commodity = fields.Many2one('freight.commodity', string='Commodity')
    release = fields.Char(string='Release')
    delivery_mode = fields.Selection([('cfs_cfs', 'CFS/CFS'),
                                      ('cy_cy', 'CY/CY'),
                                      ('cy_cfs', 'CY/CFS'),
                                      ('cfs_cy', 'CFS/CY'),
                                      ('dr_cy', 'DR/CY'),
                                      ('cy_dr', 'CY/DR'),
                                      ('fcl_fcl', 'FCL/FCL')
                                      ], string='Delivery Mode')
    dep_container_id = fields.Many2one('res.partner', string='Dep. Container')
    arr_container_yard_id = fields.Many2one('res.partner', string='Arr. Container')
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')
