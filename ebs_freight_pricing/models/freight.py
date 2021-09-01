# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
from json import dumps
import json


class FreightOperation(models.Model):
    _inherit = 'freight.operation'
    _description = 'Freight Operation'

    pricing_id = fields.Many2one('freight.pricing', string='Shipment Pricing')