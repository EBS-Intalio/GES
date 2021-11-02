# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ImportProcessLine(models.Model):
    _name = 'import.process.line'
    _description = 'Import Process Line'

    import_container_id = fields.Many2one('freight.container',string="Import Container")
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
    free_time = fields.Integer('Free Time')
    duration = fields.Integer('Duration')
    unit = fields.Selection([
        ('d', 'Days'),
        ('h', 'Hours')
    ], string="Unit")
    override_co = fields.Float('Override Co')
    override = fields.Float('Override')
    currency = fields.Many2one('res.currency', string="Currency")
