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


    created_from_shipment = fields.Boolean("Shipment Invoice", default=False, readonly=True)

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

    def open_related_shipment(self):
        shipment = self.invoice_line_ids.search([('created_from_shipment', '=', True), ('move_id', '=', self.id)]).shipment_line
        action = self.env["ir.actions.actions"]._for_xml_id("freight.view_freight_operation_all_action")
        if len(shipment) == 1:
            form_view = [(self.env.ref('freight.view_freight_operation_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = shipment.id
        else:
            action['domain'] = [('id', 'in', shipment.ids)]
        return action

    def open_related_shipment_billing_lines(self):
        billing_lines = self.invoice_line_ids.search([('created_from_shipment', '=', True), ('move_id', '=', self.id)]).billing_line_id
        action = self.env["ir.actions.actions"]._for_xml_id("freight_shipment_billing.action_freight_Billing")
        if billing_lines:
            action['domain'] = [('id', 'in', billing_lines.ids)]
        return action

class AccountMoveLineinherit(models.Model):
    _inherit = "account.move.line"

    billing_line_id = fields.Many2one('freight.operation.billing',string="Billing Line", inverse='_inverse_invoice_line_ids')

    shipment_line = fields.Many2one('freight.operation', string="shipment", related='billing_line_id.operation_billing_id')

    created_from_shipment = fields.Boolean(related='move_id.created_from_shipment')

    def _inverse_invoice_line_ids(self):
        for rec in self:
            if rec.move_id.move_type == 'out_invoice':
                rec.billing_line_id.invoice_line_id = rec.id
            if rec.move_id.move_type == 'in_invoice':
                rec.billing_line_id.bill_line_id = rec.id
