from odoo import models, fields


class ConsolDerails(models.Model):
    _name = 'freight.doc.line'

    order_no = fields.Integer('Order')
    category = fields.Char('Category')
    name = fields.Char('Name')
    value = fields.Boolean('Value')
    console_id = fields.Many2one('consol.details', 'Consol ID')
