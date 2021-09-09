# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPofdDestination(models.Model):
    _name = 'freight.pofd.destination'
    _description = 'Freight Pofd Destination'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string="Active")
