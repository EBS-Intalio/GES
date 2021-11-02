# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class TrackingDetails(models.Model):
    _name = 'tracking.dates'
    _description = 'Tracking Dates'

    name = fields.Char('Description')
    estimated = fields.Date('Estimated')
    actual_start = fields.Date('Actual Start')
    order_id = fields.Many2one('freight.order','Order ID')

