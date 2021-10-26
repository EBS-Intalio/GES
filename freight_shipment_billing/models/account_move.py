# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class AccountMoveinherit(models.Model):
    _inherit = "account.move"

    invoice_type = fields.Selection(selection=[
        ('local_individual', 'Local Individual'),
        ('foreign_individual', 'Foreign Individual'),
        ('consolidated_local', 'Consolidated Local'),
        ('consolidated_foreign', 'Consolidated Foreign'),
    ], string='Inv. Type', default='local_individual', required=True)


    def action_post(self):
        if self.move_type == 'out_invoice':
            for invoice_line in self.invoice_line_ids:
                invoice_line.billing_line_id.posted_revenue = True
                rate_id = self.env['res.currency.rate'].sudo().search([('currency_id', '=', invoice_line.move_id.currency_id.id)], order='name desc', limit=1)
                invoice_line.billing_line_id.sell_exchange_rate = rate_id.rate

        if self.move_type == 'in_invoice':
            for invoice_line in self.invoice_line_ids:
                invoice_line.billing_line_id.posted_cost = True
                rate_id = self.env['res.currency.rate'].sudo().search([('currency_id', '=', invoice_line.move_id.currency_id.id)], order='name desc', limit=1)
                invoice_line.billing_line_id.cost_exchange_rate = rate_id.rate



        return super(AccountMoveinherit, self).action_post()

class AccountMoveLineinherit(models.Model):
    _inherit = "account.move.line"

    billing_line_id = fields.Many2one('freight.operation.billing',string="Billing Line", inverse='_inverse_invoice_line_ids')

    shipment_line = fields.Many2one('freight.operation', string="shipment", related='billing_line_id.operation_billing_id')

    def _inverse_invoice_line_ids(self):
        for rec in self:
            if rec.move_id.move_type == 'out_invoice':
                rec.billing_line_id.invoice_line_id = rec.id
            if rec.move_id.move_type == 'in_invoice':
                rec.billing_line_id.bill_line_id = rec.id
