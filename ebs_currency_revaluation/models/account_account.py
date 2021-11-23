# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _inherit = 'account.account'

    currency_revaluation = fields.Boolean(default=True )
