# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ExportProcessLine(models.Model):
    _name = 'export.process.line'
    _description = 'Export Process Line'

    export_container_id = fields.Many2one('freight.container', string="Export container")
    penalty = fields.Selection([
        ('det', 'Detention'),
        ('sto', 'Storage'),
        ('twt', 'Truck Wait Time'),
    ], default='det', string="Penalty")

    penalty_desc = fields.Char('Penalty Description')
    credit_type = fields.Selection([
        ('car', 'Carrier'),
        ('cto', 'CTO'),
        ('trs', 'Transfer'),
    ], string="Cred Type")
    creditor = fields.Many2one('res.partner', string="Creditor")
    location = fields.Many2one('freight.port', string="Location")
    free_time = fields.Integer(string='Free Time')
    duration = fields.Integer(string='Duration')
    unit = fields.Selection([
        ('d', 'Days'),
        ('h', 'Hours')
    ], string="Unit")
    override_co = fields.Float(string='Override Co')
    override = fields.Float(string='Override')
    currency = fields.Many2one('res.currency', string="Currency")
