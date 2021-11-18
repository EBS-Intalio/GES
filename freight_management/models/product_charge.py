from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductCharge(models.Model):
    _name = 'product.charge'

    name = fields.Char(string="Product/Charge Code")
    invoice_type = fields.Selection(selection=[
        ('local_individual', 'Local Individual'),
        ('foreign_individual', 'Foreign Individual'),
        ('consolidated_local', 'Consolidated Local'),
        ('consolidated_foreign', 'Consolidated Foreign'),
    ], string=' Invoicing Type', default='local_individual', required=True)

    partner_id = fields.Many2one('res.partner')
