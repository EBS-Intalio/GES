# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class FreightOperationInherit(models.Model):
    _inherit = "freight.operation"

    operating_unit_id = fields.Many2one('operating.unit', string='Branch')
    analytic_account_id = fields.Many2one('account.analytic.account',string='Department')

    account_operation_lines = fields.One2many(comodel_name='freight.operation.billing', inverse_name='operation_billing_id')


class FreightOperationBilling(models.Model):
    _name = "freight.operation.billing"

    charge_code_sequence = fields.Integer("Sequence")
    charge_code = fields.Many2one('product.product', 'Charge Code')
    description = fields.Char(compute='_default_description', string="Description", readonly=False)
    product_categ_id = fields.Many2one('product.category', string='Product Type', related='charge_code.categ_id')
    operating_unit_id = fields.Many2one('operating.unit', compute='_default_operating_unit_id', readonly=False , string='Branch')
    analytic_account_id = fields.Many2one('account.analytic.account', compute='_default_analytic_account_id', readonly=False, string='Department')
    cost_currency_id = fields.Many2one('res.currency', string='Cost Currency')
    os_cost_amount = fields.Monetary(string="OS Cost Amount", currency_field='cost_currency_id')
    company_currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)
    estimated_cost = fields.Monetary(string="Estimated Cost", currency_field='company_currency_id')
    local_cost_amount = fields.Monetary(string="Local Cost Amount", currency_field='company_currency_id', compute='_compute_local_cost_amount')
    vendor = fields.Many2one("res.partner", string="Vendor", domain="[('is_payable', '=', True)]")
    cost_recognition = fields.Selection(([('imm', 'IMM')]), string='Cost Recognition', default='imm')
    posted_cost = fields.Boolean("Posted Cost", default=False)
    cost_tax_ids = fields.Many2many('account.tax', string="Tax")
    sell_currency_id = fields.Many2one('res.currency', string='Sell Currency')
    os_sell_amount = fields.Monetary(string="OS Sell Amount", currency_field='sell_currency_id')
    estimated_revenue = fields.Monetary(string="Estimated Revenue", currency_field='company_currency_id')
    local_sell_amount = fields.Monetary(string="Local Sell Amount", currency_field='company_currency_id',
                                        compute='_compute_local_sell_amount')
    debtor = fields.Many2one('res.partner', string='Debtor', related='operation_billing_id.agent_id')
    sell_recognition = fields.Selection(([('imm', 'IMM')]), string='Sell Recognition', default='imm')
    posted_revenue = fields.Boolean("Posted Revenue", default=False)
    sell_reference = fields.Char("Sell Reference")
    cost_exchange_rate = fields.Float("Cost Exchange Rate")
    sell_exchange_rate = fields.Float("Sell Exchange Rate")
    reference = fields.Char("Ref")
    ar_invoice_number = fields.Many2one('account.move',"AR Invoice Number")
    invoice_type = fields.Selection(related='ar_invoice_number.invoice_type', string='Inv. Type')
    invoice_date = fields.Date(related='ar_invoice_number.invoice_date', string='Inv. Date')
    invoice_currency_id = fields.Many2one('res.currency', string='Invoice Currency', related='ar_invoice_number.currency_id')
    invoice_line_id = fields.Many2one('account.move.line')
    sell_invoice_amount = fields.Monetary(string="Sell Inv. Amount", currency_field='invoice_currency_id', related='invoice_line_id.price_subtotal')
    local_sell_invoice_amount = fields.Monetary(string="Local Sell Invoice Amount", currency_field='company_currency_id',
                                        compute='_compute_local_sell_invoice_amount')


    sell_invoice_tax_amount = fields.Monetary(string="Sell Inv. Tax Amount", currency_field='invoice_currency_id', related='invoice_line_id.tax_base_amount')

    operation_billing_id = fields.Many2one('freight.operation', readonly=True)

    @api.depends('charge_code')
    def _default_description(self):
        self.description = self.charge_code.name

    @api.depends('operation_billing_id')
    def _default_operating_unit_id(self):
        self.operating_unit_id = self.operation_billing_id.operating_unit_id.id

    @api.depends('operation_billing_id')
    def _default_analytic_account_id(self):
        self.analytic_account_id = self.operation_billing_id.analytic_account_id.id

    @api.depends('cost_currency_id', 'os_cost_amount')
    def _compute_local_cost_amount(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        for rec in self:
            if rec.cost_currency_id and rec.os_cost_amount:
                rec.local_cost_amount = rec.cost_currency_id._convert(rec.os_cost_amount, rec.company_currency_id, company, date)
            else:
                rec.local_cost_amount = 0


    @api.depends('sell_currency_id', 'os_sell_amount')
    def _compute_local_sell_amount(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        for rec in self:
            if rec.sell_currency_id and rec.os_sell_amount:
                rec.local_sell_amount = rec.sell_currency_id._convert(rec.os_sell_amount, rec.company_currency_id, company, date)
            else:
                rec.local_sell_amount = 0

    @api.depends('invoice_currency_id', 'sell_invoice_amount')
    def _compute_local_sell_invoice_amount(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        for rec in self:
            if rec.invoice_currency_id and rec.sell_invoice_amount:
                rec.local_sell_invoice_amount = rec.invoice_currency_id._convert(rec.sell_invoice_amount, rec.company_currency_id, company, date)
            else:
                rec.local_sell_invoice_amount = 0