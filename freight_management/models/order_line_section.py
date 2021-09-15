# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class OrderLineSection(models.Model):
    _name = 'order.line.section'
    _description = 'Order Line Section'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string="Active")
