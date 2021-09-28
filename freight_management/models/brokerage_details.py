# -*- coding: utf-8 -*-
import datetime
from odoo import api, fields, models, _


class BrokerageDetails(models.Model):
    _name = 'brokerage.details'

    name = fields.Many2one('freight.job.request', string="Request")
    type = fields.Selection([('pmt', 'Customers Permit /Clearance Number',),
                             ('tsn', 'Transhipment Number',),
                             ('ata', 'ATA Carnet Number',)], string='Type')
