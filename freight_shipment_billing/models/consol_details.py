# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ConsolDetailsInherit(models.Model):
    _inherit = 'consol.details'

    billing_lines = fields.One2many(comodel_name='console.details.billing.lines', inverse_name='freight_console_id')

    def create_billing_lines(self):
        for record in self.billing_lines:
            record.create_billing()

class ConsoleDetailsBillingLines(models.Model):
    _name = 'console.details.billing.lines'

    handler = fields.Integer("Handler")
    charge_code_sequence = fields.Integer("Sequence")
    charge_code = fields.Many2one('product.product', 'Charge Code', required=True)
    description = fields.Char(compute='_default_description', string="Description", readonly=False)
    operating_unit_id = fields.Many2one('operating.unit', compute='_default_operating_unit_id', readonly=False,
                                        string='Branch')

    analytic_account_id = fields.Many2one('account.analytic.account', readonly=False, string='Department')

    cost_currency_id = fields.Many2one('res.currency', string='Cost Currency',
                                       default=lambda self: self.env.company.currency_id.id)

    os_cost_amount = fields.Monetary(string="OS Cost Amount", currency_field='cost_currency_id', required=True)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          default=lambda self: self.env.company.currency_id.id)

    local_cost_amount = fields.Monetary(string="Local Cost Amount", currency_field='company_currency_id',
                                        compute='_compute_local_cost_amount')

    vendor = fields.Many2one("res.partner", string="Creditor", domain="[('is_payable', '=', True)]", required=True)

    cost_recognition = fields.Selection(([('imm', 'IMM')]), string='Cost Recognition', default='imm')

    app_method = fields.Many2one("app.method", string="App Method")

    sent_to_shipment = fields.Boolean("Sent to Shipment", default=False)


    freight_console_id = fields.Many2one('consol.details', string='Consol')

    @api.depends('charge_code')
    def _default_description(self):
        for rec in self:
            rec.description = rec.charge_code.name

    @api.depends('freight_console_id')
    def _default_operating_unit_id(self):
        uid2 = self._uid
        user = self.env["res.users"].browse(uid2)
        for rec in self:
            rec.operating_unit_id = user.default_operating_unit_id.id

    @api.depends('cost_currency_id', 'os_cost_amount')
    def _compute_local_cost_amount(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        for rec in self:
            if rec.cost_currency_id and rec.os_cost_amount:
                rec.local_cost_amount = rec.cost_currency_id._convert(rec.os_cost_amount, rec.company_currency_id,
                                                                      company, date)
            else:
                rec.local_cost_amount = 0

    def create_billing(self):
        for rec in self:
            if rec.freight_console_id.shipment_ids and not rec.sent_to_shipment:
                shipments_count = len(rec.freight_console_id.shipment_ids)
                for shipment_id in rec.freight_console_id.shipment_ids:
                    shipment_id.write({'account_operation_lines': [
                        (0, 0, {
                            'charge_code_sequence': rec.charge_code_sequence,
                            'charge_code': rec.charge_code.id,
                            'operating_unit_id': rec.operating_unit_id.id,
                            'analytic_account_id': rec.analytic_account_id.id,
                            'cost_currency_id': rec.cost_currency_id.id,
                            'os_cost_amount': rec.os_cost_amount / shipments_count,
                            'company_currency_id': rec.company_currency_id.id,
                            'local_cost_amount': rec.local_cost_amount,
                            'vendor': rec.vendor.id,
                            'cost_recognition': rec.cost_recognition,
                            'freight_console_id': rec.freight_console_id.id,
                        }),
                    ]})

                rec.sent_to_shipment = True

            else:
                raise ValidationError("No shipment existing")