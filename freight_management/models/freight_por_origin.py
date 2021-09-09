# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPorOrigin(models.Model):
    _name = 'freight.por.origin'
    _description = 'Freight Por Origin'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string="Active")
