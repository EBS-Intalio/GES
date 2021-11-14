from odoo import models, fields, api


class AccountCodeJournal(models.Model):
    _name = 'account.code.journal'

    name = fields.Char(string='Name', required=True, translate=True)
    french = fields.Char(string='French')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'name already exists!')
    ]
