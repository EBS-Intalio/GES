# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPod(models.Model):
    _name = 'freight.pod'
    _description = 'Freight Pod'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string="Active")
