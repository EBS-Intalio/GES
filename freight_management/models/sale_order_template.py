# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    transport = fields.Selection([('air', 'Air'),
                                   ('ocean', 'Ocean'),
                                   ('land', 'Land'),
                                   ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'),
                                   ('rail', 'Rail'),
                                   ('courier', 'Courier'),
                                   ('documentation', 'Documentation')], string='Transport', required=False)
