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


    created_from_shipment = fields.Boolean("Shipment Invoice", default=False, readonly=True,  inverse='compute_shipment_requested_by')
    requested_by = fields.Date("Requested By", compute='compute_shipment_requested_by')
    requested_stored= fields.Date("Requested By")

    def compute_shipment_requested_by(self):
        for rec in self:
            rec.requested_by = False
            if rec.created_from_shipment:
                shipment = rec.invoice_line_ids.search(
                    [('created_from_shipment', '=', True), ('move_id', '=', rec.id)]).shipment_line
                if len(shipment) == 1:
                    rec.requested_by = shipment.requested_by
                    rec.requested_stored = rec.requested_by

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

    invoice_shipment = fields.Many2one('freight.operation', string="invoice Shipment", inverse='_inverse_invoice_shipment')

    bill_shipment = fields.Many2one('freight.operation', string="bill Shipment", inverse='_inverse_bill_shipment')

    created_from_shipment = fields.Boolean(default=False, readonly=True)

    def _inverse_invoice_line_ids(self):
        for rec in self:
            if rec.move_id.move_type == 'out_invoice':
                rec.billing_line_id.invoice_line_id = rec.id
            if rec.move_id.move_type == 'in_invoice':
                rec.billing_line_id.bill_line_id = rec.id


    def _inverse_invoice_shipment(self):
        for rec in self:
            if rec.invoice_shipment:
                rec.direction = rec.invoice_shipment.direction
                rec.transport = rec.invoice_shipment.transport
                rec.service_type = rec.invoice_shipment.service_level
                rec.line_of_service_id = rec.invoice_shipment.line_of_service_id.id
                if rec.line_of_service_id:
                    account_matrix_line_id = rec.line_of_service_id.matrix_line_ids.search([('charge_code', '=', rec.product_id.id)], limit=1)
                    if account_matrix_line_id:
                        rec.account_id = account_matrix_line_id.income_account.id
                    else:
                        rec.account_id = rec.invoice_shipment.line_of_service_id.income_account.id

    def _inverse_bill_shipment(self):
        for rec in self:
            if rec.bill_shipment:
                rec.direction = rec.bill_shipment.direction
                rec.transport = rec.bill_shipment.transport
                rec.service_type = rec.bill_shipment.service_level
                rec.line_of_service_id = rec.bill_shipment.line_of_service_id.id
                if rec.line_of_service_id:
                    account_matrix_line_id = rec.line_of_service_id.matrix_line_ids.search([('charge_code', '=', rec.product_id.id)], limit=1)
                    if account_matrix_line_id:
                        rec.account_id = account_matrix_line_id.expense_account.id
                    else:
                        rec.account_id = rec.bill_shipment.line_of_service_id.expense_account.id

    @api.onchange('price_unit')
    def on_change_price_unit_field(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        for rec in self:
            if rec.created_from_shipment:
                if rec.move_id.move_type == 'in_invoice':
                    if rec.move_id.currency_id == rec.billing_line_id.cost_currency_id:
                        rec.billing_line_id.os_cost_amount = rec.price_unit
                    else:
                        rec.billing_line_id.os_cost_amount = rec.move_id.currency_id._convert(rec.price_unit,
                                                                                              rec.billing_line_id.cost_currency_id,
                                                                                              company, date)

                elif rec.move_id.move_type == 'out_invoice':
                    if rec.move_id.currency_id == rec.billing_line_id.sell_currency_id:
                        rec.billing_line_id.os_sell_amount = rec.price_unit
                    else:
                        rec.billing_line_id.os_sell_amount = rec.move_id.currency_id._convert(rec.price_unit,
                                                                                              rec.billing_line_id.sell_currency_id,
                                                                                              company, date)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountMoveLineinherit, self).create(vals_list)
        move = self.env['account.move'].browse(vals_list[0]['move_id'])
        if move.move_type == 'out_invoice':
            for invoice_line in move.invoice_line_ids:
                if invoice_line.invoice_shipment:
                    invoice_line.invoice_shipment.write({'account_operation_lines': [
                        (0, 0, {
                            'charge_code': invoice_line.product_id.id,
                            'operating_unit_id': invoice_line.operating_unit_id.id,
                            'ar_invoice_number': move.id,
                            'debtor': move.partner_id.id,
                            'sell_currency_id': move.currency_id.id,
                            'sell_tax_ids': [(6, 0, invoice_line.tax_ids.ids)],
                            'os_sell_amount': invoice_line.price_unit,
                            'analytic_account_id': invoice_line.analytic_account_id.id,
                            'operation_billing_id': invoice_line.invoice_shipment.id,
                            'invoice_line_id': invoice_line.id,
                            'invoice_created': True,
                        }),
                    ]})
                    invoice_line.created_from_shipment = True
                    for record in res:
                        billing_line = invoice_line.invoice_shipment.account_operation_lines.search([('invoice_line_id', '=', record.id)])
                        record.billing_line_id = billing_line.id
        if move.move_type == 'in_invoice':
            for invoice_line in move.invoice_line_ids:
                if invoice_line.bill_shipment:
                    invoice_line.bill_shipment.write({'account_operation_lines': [
                        (0, 0, {
                            'charge_code': invoice_line.product_id.id,
                            'operating_unit_id': invoice_line.operating_unit_id.id,
                            'ar_bill_number': move.id,
                            'vendor': move.partner_id.id,
                            'cost_currency_id': move.currency_id.id,
                            'cost_tax_ids': [(6, 0, invoice_line.tax_ids.ids)],
                            'os_cost_amount': invoice_line.price_unit,
                            'analytic_account_id': invoice_line.analytic_account_id.id,
                            'operation_billing_id': invoice_line.invoice_shipment.id,
                            'bill_line_id': invoice_line.id,
                            'bill_created': True,
                        }),
                    ]})
                    invoice_line.created_from_shipment = True
                    for record in res:
                        billing_line = invoice_line.bill_shipment.account_operation_lines.search(
                            [('bill_line_id', '=', record.id)])
                        record.billing_line_id = billing_line.id
        return res
