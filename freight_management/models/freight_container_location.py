# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FreightContainerLocation(models.Model):
    _name = 'freight.container.location'
    _description = 'Freight Container Location'

    outturn_location_id = fields.Many2one('freight.container',string="Outturn location")
    packs = fields.Integer('Packs')
    location = fields.Char('Location')

    
