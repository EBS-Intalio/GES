# -*- coding: utf-8 -*"-
from odoo import models, fields

class ChinaAccount(models.Model):
    _name = 'china.account.type'
    _rec_name = 'code'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code", required=True)

    _sql_constraints = [
        ('_unique_code',
         'unique (code)',
         "A record with the Same Code cannot be created"),
    ]