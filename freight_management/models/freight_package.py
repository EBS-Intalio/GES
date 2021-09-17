# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPackageExt(models.Model):
    _inherit = 'freight.package'

    is_ltl = fields.Boolean(string='LTL')
    is_lcl = fields.Boolean(string='LCL')

