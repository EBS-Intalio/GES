# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    freight_type = fields.Selection(([('shipper', 'Shipper'), ('consignee', 'Consignee')]), string='Freight Type')
