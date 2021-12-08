# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountAccountInherit(models.Model):
    _inherit = 'account.account'

    is_shipment_account = fields.Boolean('Shipment')