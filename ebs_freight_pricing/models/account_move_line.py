from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tax_amount = fields.Float(string='Tax Amount', readonly=True, compute='_get_tax_amount')
    gross_amount = fields.Float(string='Gross Amount', readonly=True, compute='_get_gross_amount')

    @api.depends('tax_ids', 'price_subtotal')
    def _get_tax_amount(self):
        for record in self:
            amount = 0.0
            if record.tax_ids:
                for tax in record.tax_ids:
                    amount += (tax.amount/100) * (record.price_subtotal)
            record.tax_amount = amount

    @api.depends('price_subtotal')
    def _get_gross_amount(self):
        for record in self:
            if record.tax_amount > 0.0:
                record.gross_amount = record.tax_amount + record.price_subtotal
            else:
                record.gross_amount = record.price_subtotal


