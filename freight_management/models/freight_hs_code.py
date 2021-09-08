# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightHSCode(models.Model):
    _name = 'freight.hs.code'
    _description = 'Freight HS-Code'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string="Active")
