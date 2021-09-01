# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
from json import dumps
import json


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    pricing_id = fields.Many2one('freight.pricing')
    

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'
    _description = 'Sale Order Template'

    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')
