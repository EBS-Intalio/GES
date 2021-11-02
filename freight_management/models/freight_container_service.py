# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FreightContainerService(models.Model):
    _name = 'freight.container.service'
    _description = 'Freight Container Service'

    container_service_id = fields.Many2one('freight.container',string="Container Service")
    service_type = fields.Selection([
        ('fumigation','Fumigation'),
        ('qs','Quarantine Inspection'),
        ('ch','Customs Hold'),
        ('qu','Quarantine Unpack'),
        ('tg','Tailgate'),
        ('ei','Extra Inspection'),
        ('sr','Survey'),
        ('cn','Cleaning'),
        ('wh','Washing'),
        ('sc','Steam Cleaning'),
        ('ffs','FCL Free Storage'),
        ('fus','FCL Underbond Storage'),
    ],string="Service Type")
    date_booked = fields.Date('Date booked')
    reference = fields.Char('Reference')
    completed = fields.Date('Completed')
    contractor = fields.Many2one('res.partner', string='Contractor')
    srv_location = fields.Many2one('res.partner', string='Srv. Location')
    service_rate = fields.Float('Service rate')
    service_rate_uom_id = fields.Many2one('res.currency',string="Service rate uom")
    service_count = fields.Integer('Service count')
    service_duration = fields.Float(string='Service Duration')
    service_notes = fields.Text('Service notes')

