from odoo import models, fields, api

class PaymentMode(models.Model):
    _name = 'payment.mode'

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('_unique_name',
         'unique (name)',
         "Name Of Payment Mode Must Be Unique!"),
    ]

