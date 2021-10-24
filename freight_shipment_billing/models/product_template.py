# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    transport = fields.Selection([('air', 'Air'),
                                  ('ocean', 'Ocean'),
                                  ('land', 'Road'),
                                  ('sea_then_air', 'Sea then Air'),
                                  ('air_then_sea', 'Air then Sea'),
                                  ('rail', 'Rail'),
                                  ('courier', 'Courier'),
                                  ('documentation', 'Documentation'),
                                  ('all', 'All'),], string='Transport', default='all')
