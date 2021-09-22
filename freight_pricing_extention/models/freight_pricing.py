# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FreightPricingInherit(models.Model):
    _inherit = 'freight.pricing'
    _description = 'Freight Pricing'
    _order = 'name desc, id desc'

    carrier_count = fields.Integer(string='Total carrier', compute='count_carriers', default=0)

    @api.depends('carrier_ids')
    def count_carriers(self):
        self.carrier_count = len(self.carrier_ids)