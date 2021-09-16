# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightJobRequestInherit(models.Model):
    _inherit = 'freight.job.request'

    bl_copy = fields.Boolean("BL Copy Available ?")
    shipping_documents = fields.Boolean("Shipping Documents")
    original_copy = fields.Selection(([('original', 'Original'), ('copy', 'Copy')]), string='Original/Copy')