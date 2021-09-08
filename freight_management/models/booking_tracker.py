# -*- coding: utf-8 -*-
import datetime
from odoo import api, fields, models, _


class BookingTracker(models.Model):
    _inherit = 'booking.tracker'

    freight_request_id = fields.Many2one('freight.job.request', string="Request")
