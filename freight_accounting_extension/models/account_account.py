# -*- coding: utf-8 -*"-
from odoo import models, fields

class AccountAccountInherit(models.Model):
    _inherit = 'account.account'

    china_account_type = fields.Many2one('china.account.type', string="China Account Type")