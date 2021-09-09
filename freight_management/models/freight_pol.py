# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPol(models.Model):
    _name = 'freight.pol'
    _description = 'Freight Pol'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string="Active")
