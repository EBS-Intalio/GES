# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FreightOperationInherit(models.Model):
    _inherit = "freight.operation"

    operating_unit_id = fields.Many2one('operating.unit', string='Branch')
    analytic_account_id = fields.Many2one('account.analytic.account',string='Department')

    account_operation_lines = fields.One2many(comodel_name='freight.operation.billing', inverse_name='operation_billing_id')

    total_revenue = fields.Monetary(string="Total Revenue", currency_field='company_currency_id',  compute="compute_data")
    total_cost = fields.Monetary(string="Total Cost", currency_field='company_currency_id',  compute="compute_data")
    profit = fields.Monetary(string="Profit", currency_field='company_currency_id',  compute="compute_data")
    company_currency_id = fields.Many2one('res.currency', string="Currency",default=lambda self: self.env.company.currency_id.id)

    line_of_service_id = fields.Many2one('account.operation.matrix', 'Line of Service', compute="compute_line_of_service")

    @api.depends('transport', 'direction', 'service_level')
    def compute_line_of_service(self):
        for rec in self:
            line_of_service = self.env['account.operation.matrix'].search([('transport', '=', rec.transport), ('direction', '=', rec.direction), ('service_type', '=', rec.service_level)], limit=1)
            if line_of_service:
                rec.line_of_service_id = line_of_service.id
            else:
                rec.line_of_service_id = False

    @api.depends('account_operation_lines')
    def compute_data(self):
        for rec in self:
            rec.total_revenue = sum(rec.account_operation_lines.mapped('local_sell_amount'))
            rec.total_cost = sum(rec.account_operation_lines.mapped('local_cost_amount'))
            rec.profit = rec.total_revenue - rec.total_cost

    def button_post_sell(self):
        debtors_data = self.env['freight.operation.billing'].read_group(domain=[(
            'debtor', 'in', self.account_operation_lines.debtor.ids), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0)], fields=['debtor'], groupby=['debtor'])
        mapped_data = list([(debtor['debtor'][0]) for debtor in debtors_data])
        for data in mapped_data:
            debtor_id = self.env['res.partner'].browse(data)
            local_billing_id = self.env['freight.operation.billing'].sudo().search([('debtor', '=', debtor_id.id), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0),
                                                                              ('operation_billing_id', '=', self.id), ('invoice_type', 'in', ['local_individual', 'consolidated_local'])])

            foreign_billing_id = self.env['freight.operation.billing'].sudo().search([('debtor', '=', debtor_id.id), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0),
                                                                              ('operation_billing_id', '=', self.id), ('invoice_type', 'in', ['foreign_individual', 'consolidated_foreign'])])
            if local_billing_id:
                date = self._context.get('date') or fields.Date.today()
                company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
                invoice_line_ids = []
                for record in local_billing_id:
                    invoice_line_ids.append((0, 0, {
                        'product_id': record.charge_code.id,
                        'transport': record.transport,
                        'direction': record.operation_billing_id.direction,
                        'service_type': record.operation_billing_id.service_level,
                        'operating_unit_id': record.operating_unit_id.id,
                        'analytic_account_id': record.analytic_account_id.id,
                        'quantity': 1,
                        'created_from_shipment': True,
                        'price_unit':record.sell_currency_id._convert(record.os_sell_amount, self.env.company.currency_id, company, date),
                        'billing_line_id': record.id,
                        'tax_ids': [(6, 0, record.sell_tax_ids.ids)],
                    }))
                    record.invoice_created = True
                invoice_id = self.env['account.move'].sudo().create({
                    'name': "/",
                    'move_type': 'out_invoice',
                    'partner_id': debtor_id.id,
                    'invoice_date': fields.Date.today(),
                    'operating_unit_id': local_billing_id.operating_unit_id,
                    'currency_id': self.env.company.currency_id.id,
                    'invoice_type': "local_individual",
                    'invoice_line_ids': invoice_line_ids,
                })
                local_billing_id.ar_invoice_number = invoice_id.id
                invoice_id.created_from_shipment = True
            if foreign_billing_id:
                currencies_grouped = foreign_billing_id.read_group(domain=[('debtor', '=', debtor_id.id), ('invoice_created', '=', False),
                                                                           ('os_sell_amount', '!=', 0),('operation_billing_id', '=', self.id),
                                                                           ('invoice_type', 'in', ['foreign_individual', 'consolidated_foreign'])],
                                                                   fields=['sell_currency_id'], groupby=['sell_currency_id'])
                mapped_currencies = list([(currency['sell_currency_id'][0]) for currency in currencies_grouped])
                for mapped_currency in mapped_currencies:
                    currency_id = self.env['res.currency'].browse(mapped_currency)
                    foreign_currency_billing_id = self.env['freight.operation.billing'].sudo().search(
                        [('debtor', '=', debtor_id.id), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0),('sell_currency_id', '=', currency_id.id),
                         ('operation_billing_id', '=', self.id),('invoice_type', 'in', ['foreign_individual', 'consolidated_foreign'])])
                    invoice_line_ids = []
                    for record in foreign_currency_billing_id:
                        invoice_line_ids.append((0, 0, {
                            'product_id': record.charge_code.id,
                            'transport': record.transport,
                            'direction': record.operation_billing_id.direction,
                            'service_type': record.operation_billing_id.service_level,
                            'operating_unit_id': record.operating_unit_id.id,
                            'analytic_account_id': record.analytic_account_id.id,
                            'quantity': 1,
                            'created_from_shipment': True,
                            'price_unit': record.os_sell_amount,
                            'billing_line_id': record.id,
                            'tax_ids': [(6, 0, record.sell_tax_ids.ids)],
                        }))
                        record.invoice_created = True
                    invoice_id = self.env['account.move'].sudo().create({
                        'name': "/",
                        'move_type': 'out_invoice',
                        'partner_id': debtor_id.id,
                        'invoice_date': fields.Date.today(),
                        'operating_unit_id': foreign_currency_billing_id.operating_unit_id,
                        'currency_id': currency_id.id,
                        'invoice_type': "foreign_individual",
                        'invoice_line_ids': invoice_line_ids,
                    })
                    foreign_currency_billing_id.ar_invoice_number = invoice_id.id
                    invoice_id.created_from_shipment = True

    def button_post_cost(self):
        vendors_data = self.env['freight.operation.billing'].read_group(domain=[(
            'vendor', 'in', self.account_operation_lines.vendor.ids), ('bill_created', '=', False), ('os_cost_amount', '!=', 0)],
            fields=['vendor'], groupby=['vendor'])
        mapped_data = list([(vendor['vendor'][0]) for vendor in vendors_data])
        for data in mapped_data:
            vendor_id = self.env['res.partner'].browse(data)
            billing_id = self.env['freight.operation.billing'].sudo().search([('vendor', '=', vendor_id.id), ('bill_created', '=', False), ('os_cost_amount', '!=', 0), ('operation_billing_id', '=', self.id)])
            # date = self._context.get('date') or fields.Date.today()
            # company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
            if billing_id:
                currencies_grouped = self.env['freight.operation.billing'].sudo().read_group(
                    domain=[('vendor', '=', vendor_id.id), ('bill_created', '=', False),
                            ('os_cost_amount', '!=', 0), ('operation_billing_id', '=', self.id)],
                    fields=['cost_currency_id'], groupby=['cost_currency_id'])
                mapped_currencies = list([(currency['cost_currency_id'][0]) for currency in currencies_grouped])
                for mapped_currency in mapped_currencies:
                    currency_id = self.env['res.currency'].browse(mapped_currency)
                    foreign_currency_billing_id = self.env['freight.operation.billing'].sudo().search(
                        [('vendor', '=', vendor_id.id), ('bill_created', '=', False), ('os_cost_amount', '!=', 0),
                         ('cost_currency_id', '=', currency_id.id),
                         ('operation_billing_id', '=', self.id),])
                    invoice_line_ids = []
                    for record in foreign_currency_billing_id:
                        invoice_line_ids.append((0, 0, {
                            'product_id': record.charge_code.id,
                            'transport': record.transport,
                            'direction': record.operation_billing_id.direction,
                            'service_type': record.operation_billing_id.service_level,
                            'operating_unit_id': record.operating_unit_id.id,
                            'analytic_account_id': record.analytic_account_id.id,
                            'quantity': 1,
                            'price_unit': record.os_cost_amount,
                            'billing_line_id': record.id,
                            'tax_ids': [(6, 0, record.cost_tax_ids.ids)],
                        }))
                        record.bill_created = True
                    bill_id = self.env['account.move'].sudo().create({
                        'name': "/",
                        'move_type': 'in_invoice',
                        'partner_id': vendor_id.id,
                        'invoice_date': fields.Date.today(),
                        'operating_unit_id': foreign_currency_billing_id.operating_unit_id,
                        'currency_id': currency_id.id,
                        'invoice_line_ids': invoice_line_ids,
                    })
                    foreign_currency_billing_id.ar_bill_number = bill_id.id
                    bill_id.created_from_shipment = True

    bill_count = fields.Integer('Bill Count', compute='_compute_invoice_bill')
    invoice_count = fields.Integer('Invoice Count', compute='_compute_invoice_bill')

    def _compute_invoice_bill(self):
        for record in self:
            record.bill_count = len(self.account_operation_lines.search([('bill_created', '=', True), ('operation_billing_id', '=', self.id)]).ar_bill_number)
            record.invoice_count = len(self.account_operation_lines.search([('invoice_created', '=', True), ('operation_billing_id', '=', self.id)]).ar_invoice_number)

    def button_invoices(self):
        invoices = self.account_operation_lines.search([('invoice_created', '=', True), ('operation_billing_id', '=', self.id)]).ar_invoice_number
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['context'] = {'default_freight_operation_id': self.id, 'default_move_type': 'out_invoice', }
        if len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action['domain'] = [('id', 'in', invoices.ids)]
        return action

    def button_billing(self):
        invoices = self.account_operation_lines.search([('bill_created', '=', True), ('operation_billing_id', '=', self.id)]).ar_bill_number
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_in_invoice_type")
        action['context'] = {'default_freight_operation_id': self.id, 'default_move_type': 'in_invoice', }
        if len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action['domain'] = [('id', 'in', invoices.ids)]
        return action

class FreightOperationBilling(models.Model):
    _name = "freight.operation.billing"

    handler = fields.Integer("Handler")
    charge_code_sequence = fields.Integer("Sequence")
    charge_code = fields.Many2one('product.product', 'Charge Code')
    description = fields.Char(compute='_default_description', string="Description", readonly=False)
    product_categ_id = fields.Many2one('product.category', string='Product Type', related='charge_code.categ_id')
    operating_unit_id = fields.Many2one('operating.unit', compute='_default_operating_unit_id', readonly=False , string='Branch', store=True)
    analytic_account_id = fields.Many2one('account.analytic.account', compute='_default_analytic_account_id', readonly=False, string='Department')
    cost_currency_id = fields.Many2one('res.currency', string='Cost Currency', default=lambda self: self.env.company.currency_id.id)
    os_cost_amount = fields.Monetary(string="OS Cost Amount", currency_field='cost_currency_id')
    company_currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)
    local_cost_amount = fields.Monetary(string="Local Cost Amount", currency_field='company_currency_id', compute='_compute_local_cost_amount')
    vendor = fields.Many2one("res.partner", string="Creditor", domain="[('is_payable', '=', True)]")
    cost_recognition = fields.Selection(([('imm', 'IMM')]), string='Cost Recognition', default='imm')
    posted_cost = fields.Boolean("Posted Cost", default=False)
    cost_tax_ids = fields.Many2many(comodel_name='account.tax', relation="billing_cost_tax_rel", string="Cost Tax", domain="[('type_tax_use', '=', 'purchase')]")
    sell_tax_ids = fields.Many2many(comodel_name='account.tax', relation="billing_sell_tax_rel", string="Sell Tax", domain="[('type_tax_use', '=', 'sale')]")
    sell_currency_id = fields.Many2one('res.currency', string='Sell Currency', default=lambda self: self.env.company.currency_id.id)
    os_sell_amount = fields.Monetary(string="OS Sell Amount", currency_field='sell_currency_id')
    local_sell_amount = fields.Monetary(string="Local Sell Amount", currency_field='company_currency_id',
                                        compute='_compute_local_sell_amount')
    # debtor = fields.Many2one('res.partner', string='Debtor', related='operation_billing_id.agent_id', store=True)
    debtor = fields.Many2one('res.partner', string='Debtor', compute='_compute_debtor', store=True)

    sell_recognition = fields.Selection(([('imm', 'IMM')]), string='Sell Recognition', default='imm')
    posted_revenue = fields.Boolean("Posted Revenue", default=False)
    sell_reference = fields.Char("Sell Reference")
    cost_exchange_rate = fields.Float("Cost Exchange Rate")
    sell_exchange_rate = fields.Float("Sell Exchange Rate")
    reference = fields.Char("Ref")
    ar_invoice_number = fields.Many2one('account.move',"AR Invoice Number")
    ar_bill_number = fields.Many2one('account.move',"AR Bill Number")
    invoice_type = fields.Selection(selection=[
        ('local_individual', 'Local Individual'),
        ('foreign_individual', 'Foreign Individual'),
        ('consolidated_local', 'Consolidated Local'),
        ('consolidated_foreign', 'Consolidated Foreign'),
    ], string='Inv. Type', default='local_individual')
    invoice_date = fields.Date(related='ar_invoice_number.invoice_date', string='Inv. Date')
    bill_date = fields.Date(related='ar_bill_number.invoice_date', string='Bill Date')
    invoice_currency_id = fields.Many2one('res.currency', string='Invoice Currency', related='ar_invoice_number.currency_id')
    bill_currency_id = fields.Many2one('res.currency', string='Bill Currency', related='ar_bill_number.currency_id')
    invoice_line_id = fields.Many2one('account.move.line')
    bill_line_id = fields.Many2one('account.move.line')
    # cost_invoice_no = fields.Char("Cost Inv No.")
    estimated_revenue = fields.Monetary(string="Estimated Revenue", currency_field='company_currency_id')
    estimated_cost = fields.Monetary(string="Estimated Cost", currency_field='company_currency_id')
    sell_invoice_amount = fields.Monetary(string="Sell Inv. Amount", currency_field='invoice_currency_id', related='invoice_line_id.price_subtotal')
    cost_bill_amount = fields.Monetary(string="Cost Bill Amount", currency_field='bill_currency_id', related='bill_line_id.price_subtotal')
    local_sell_invoice_amount = fields.Monetary(string="Local Sell Invoice Amount", currency_field='company_currency_id',
                                        compute='_compute_local_sell_invoice_amount')


    sell_invoice_with_tax_amount = fields.Monetary(string="Sell Inv. With Tax Amount", currency_field='invoice_currency_id', related='invoice_line_id.price_total')
    cost_bill_with_tax_amount = fields.Monetary(string="Cost Bill With Tax Amount", currency_field='bill_currency_id', related='bill_line_id.price_total')

    sell_invoice_tax_amount = fields.Monetary(string="Sell Tax Amount", currency_field='invoice_currency_id', compute='_get_tax_for_sell_line')
    cost_bill_tax_amount = fields.Monetary(string="Cost Tax Amount", currency_field='bill_currency_id', compute='_get_tax_for_cost_line')

    @api.depends('invoice_line_id','sell_invoice_amount','sell_invoice_with_tax_amount')
    def _get_tax_for_sell_line(self):
        for rec in self:
            rec.sell_invoice_tax_amount = rec.sell_invoice_with_tax_amount - rec.sell_invoice_amount

    @api.depends('bill_line_id','cost_bill_amount','cost_bill_with_tax_amount')
    def _get_tax_for_cost_line(self):
        for rec in self:
            rec.cost_bill_tax_amount = rec.cost_bill_with_tax_amount - rec.cost_bill_amount


    booking_id = fields.Many2one('freight.booking')
    freight_request_id = fields.Many2one('freight.job.request')
    operation_billing_id = fields.Many2one('freight.operation', readonly=True)
    freight_console_id = fields.Many2one('consol.details', string='Consol')
    source_location_id = fields.Many2one('freight.port', related='operation_billing_id.source_location_id', store=True)
    destination_location_id = fields.Many2one('freight.port', related='operation_billing_id.destination_location_id', store=True)
    transport = fields.Selection(related='operation_billing_id.transport', store=True)

    bill_created = fields.Boolean("Bill Created", default=False)
    invoice_created = fields.Boolean("Invoice Created", default=False, readonly=False)

    @api.depends('charge_code')
    def _default_description(self):
        for rec in self:
            rec.description = rec.charge_code.name

    @api.depends('operation_billing_id')
    def _compute_debtor(self):
        for rec in self:
            rec.debtor = rec.operation_billing_id.agent_id.id or rec.booking_id.agent_id.id or rec.freight_request_id.partner_id.id

    @api.depends('operation_billing_id')
    def _default_operating_unit_id(self):
        for rec in self:
            rec.operating_unit_id = rec.operation_billing_id.operating_unit_id.id or rec.booking_id.operating_unit_id.id or rec.freight_request_id.operating_unit_id.id

    @api.depends('operation_billing_id')
    def _default_analytic_account_id(self):
        for rec in self:
            rec.analytic_account_id = rec.operation_billing_id.analytic_account_id.id or rec.booking_id.analytic_account_id.id or rec.freight_request_id.analytic_account_id.id

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


    @api.onchange('os_sell_amount')
    def on_change_os_sell_amount_field(self):
        for rec in self:
            date = self._context.get('date') or fields.Date.today()
            company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
            if rec.invoice_created:
                if rec.ar_invoice_number and rec.invoice_line_id.move_id.state != 'posted':
                    if rec.ar_invoice_number.currency_id == rec.sell_currency_id:
                        price_unit = rec.os_sell_amount
                    else:
                        price_unit = rec.sell_currency_id._convert(rec.os_sell_amount,rec.ar_invoice_number.currency_id,
                                                                                              company, date)
                    record = rec.ar_invoice_number.with_context(check_move_validity=False)
                    record['line_ids'] = [
                        (1, rec.invoice_line_id.id, {'quantity': 1, 'price_unit': price_unit}),
                    ]
                    record._recompute_dynamic_lines(recompute_all_taxes=True, recompute_tax_base_amount=True)
                if rec.invoice_line_id.move_id.state == 'posted':
                    raise ValidationError("You cannot Update a posted invoice")

    @api.onchange('os_cost_amount')
    def on_change_os_cost_amount_field(self):
        for rec in self:
            if rec.bill_created:
                if rec.ar_bill_number and rec.bill_line_id.move_id.state != 'posted':
                    record = rec.ar_bill_number.with_context(check_move_validity=False)
                    record['line_ids'] = [
                        (1, rec.bill_line_id.id, {'quantity': 1, 'price_unit': rec.os_cost_amount}),
                    ]
                    record._recompute_dynamic_lines(recompute_all_taxes=True, recompute_tax_base_amount=True)
                if rec.bill_line_id.move_id.state == 'posted':
                    raise ValidationError("You cannot Update a posted Bill")

    def action_post_sell(self):
        active_ids = self.env.context.get('active_ids')
        debtors_data = self.env['freight.operation.billing'].read_group(domain=[(
            'debtor', 'in', self.debtor.ids), ('invoice_created', '=', False),  ('os_sell_amount', '!=', 0),('operation_billing_id', '!=', False), ('id', 'in', active_ids)], fields=['debtor'],groupby=['debtor'])
        mapped_data = list([(debtor['debtor'][0]) for debtor in debtors_data])
        for data in mapped_data:
            debtor_id = self.env['res.partner'].browse(data)
            local_billing_id = self.env['freight.operation.billing'].sudo().search(
                [('debtor', '=', debtor_id.id), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0),
                 ('operation_billing_id', '!=', False), ('id', 'in', active_ids),
                 ('invoice_type', 'in', ['local_individual', 'consolidated_local'])])

            foreign_billing_id = self.env['freight.operation.billing'].sudo().search(
                [('debtor', '=', debtor_id.id), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0),
                 ('operation_billing_id', '!=', False), ('id', 'in', active_ids),
                 ('invoice_type', 'in', ['foreign_individual', 'consolidated_foreign'])])

            # # billing_id = self.env['freight.operation.billing'].sudo().search([('debtor', '=', debtor_id.id), ('os_sell_amount', '!=', 0),('booking_id', '!=', False), ('operation_billing_id', '!=', False)], limit=1)
            if local_billing_id:
                date = self._context.get('date') or fields.Date.today()
                company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
                invoice_line_ids = []
                for record in local_billing_id:
                    invoice_line_ids.append((0, 0, {
                        'product_id': record.charge_code.id,
                        'transport': record.transport,
                        'direction': record.operation_billing_id.direction,
                        'service_type': record.operation_billing_id.service_level,
                        'operating_unit_id': record.operating_unit_id.id,
                        'analytic_account_id': record.analytic_account_id.id,
                        'quantity': 1,
                        'created_from_shipment': True,
                        'price_unit': record.sell_currency_id._convert(record.os_sell_amount, self.env.company.currency_id, company, date),
                        'billing_line_id': record.id,
                        'tax_ids': [(6, 0, record.sell_tax_ids.ids)],
                    }))
                    record.invoice_created = True
                invoice_id = self.env['account.move'].sudo().create({
                    'name': "/",
                    'move_type': 'out_invoice',
                    'partner_id': debtor_id.id,
                    'invoice_date': fields.Date.today(),
                    'operating_unit_id':local_billing_id.operating_unit_id,
                    'currency_id':self.env.company.currency_id.id,
                    'invoice_type': "local_individual",
                    'invoice_line_ids': invoice_line_ids,
                })
                local_billing_id.ar_invoice_number = invoice_id.id
                invoice_id.created_from_shipment = True
            if foreign_billing_id:
                currencies_grouped = foreign_billing_id.read_group(
                    domain=[('debtor', '=', debtor_id.id), ('invoice_created', '=', False),
                            ('os_sell_amount', '!=', 0), ('operation_billing_id', '!=', False), ('id', 'in', active_ids),
                            ('invoice_type', 'in', ['foreign_individual', 'consolidated_foreign'])],
                    fields=['sell_currency_id'], groupby=['sell_currency_id'])
                mapped_currencies = list([(currency['sell_currency_id'][0]) for currency in currencies_grouped])
                for mapped_currency in mapped_currencies:
                    currency_id = self.env['res.currency'].browse(mapped_currency)
                    foreign_currency_billing_id = self.env['freight.operation.billing'].sudo().search(
                        [('debtor', '=', debtor_id.id), ('invoice_created', '=', False), ('os_sell_amount', '!=', 0),
                         ('sell_currency_id', '=', currency_id.id),
                          ('operation_billing_id', '!=', False), ('id', 'in', active_ids),
                         ('invoice_type', 'in', ['foreign_individual', 'consolidated_foreign'])])
                    invoice_line_ids = []
                    for record in foreign_currency_billing_id:
                        invoice_line_ids.append((0, 0, {
                            'product_id': record.charge_code.id,
                            'transport': record.transport,
                            'direction': record.operation_billing_id.direction,
                            'service_type': record.operation_billing_id.service_level,
                            'operating_unit_id': record.operating_unit_id.id,
                            'analytic_account_id': record.analytic_account_id.id,
                            'quantity': 1,
                            'created_from_shipment': True,
                            'price_unit': record.os_sell_amount,
                            'billing_line_id': record.id,
                            'tax_ids': [(6, 0, record.sell_tax_ids.ids)],
                        }))
                        record.invoice_created = True
                    invoice_id = self.env['account.move'].sudo().create({
                        'name': "/",
                        'move_type': 'out_invoice',
                        'partner_id': debtor_id.id,
                        'invoice_date': fields.Date.today(),
                        'operating_unit_id': foreign_currency_billing_id.operating_unit_id,
                        'currency_id': currency_id.id,
                        'invoice_type': "foreign_individual",
                        'invoice_line_ids': invoice_line_ids,
                    })
                    foreign_currency_billing_id.ar_invoice_number = invoice_id.id
                    invoice_id.created_from_shipment = True



    def action_post_cost(self):
        active_ids = self.env.context.get('active_ids')
        vendors_data = self.env['freight.operation.billing'].read_group(domain=[(
            'vendor', 'in', self.vendor.ids), ('bill_created', '=', False), ('os_cost_amount', '!=', 0), ('operation_billing_id', '!=', False), ('id', 'in', active_ids)], fields=['vendor'],groupby=['vendor'])
        mapped_data = list([(vendor['vendor'][0]) for vendor in vendors_data])
        for data in mapped_data:
            vendor_id = self.env['res.partner'].browse(data)
            billing_id = self.env['freight.operation.billing'].sudo().search([('vendor', '=', vendor_id.id), ('bill_created', '=', False), ('operation_billing_id', '!=', False), ('os_cost_amount', '!=', 0), ('id', 'in', active_ids)])
            invoice_line_ids = []
            if billing_id:
                currencies_grouped = self.env['freight.operation.billing'].sudo().read_group(
                    domain=[('vendor', '=', vendor_id.id), ('bill_created', '=', False),('operation_billing_id', '!=', False),
                            ('os_cost_amount', '!=', 0), ('id', 'in', active_ids)],
                    fields=['cost_currency_id'], groupby=['cost_currency_id'])
                mapped_currencies = list([(currency['cost_currency_id'][0]) for currency in currencies_grouped])
                for mapped_currency in mapped_currencies:
                    currency_id = self.env['res.currency'].browse(mapped_currency)
                    foreign_currency_billing_id = self.env['freight.operation.billing'].sudo().search(
                        [('vendor', '=', vendor_id.id), ('bill_created', '=', False), ('operation_billing_id', '!=', False), ('os_cost_amount', '!=', 0),
                         ('cost_currency_id', '=', currency_id.id), ('id', 'in', active_ids) ])
                    invoice_line_ids = []
                    for record in foreign_currency_billing_id:
                        invoice_line_ids.append((0, 0, {
                            'product_id': record.charge_code.id,
                            'transport': record.transport,
                            'direction': record.operation_billing_id.direction,
                            'service_type': record.operation_billing_id.service_level,
                            'operating_unit_id': record.operating_unit_id.id,
                            'analytic_account_id': record.analytic_account_id.id,
                            'quantity': 1,
                            'created_from_shipment': True,
                            'price_unit': record.os_cost_amount,
                            'billing_line_id': record.id,
                            'tax_ids': [(6, 0, record.cost_tax_ids.ids)],
                        }))
                        record.bill_created = True
                    bill_id = self.env['account.move'].sudo().create({
                        'name': "/",
                        'move_type': 'in_invoice',
                        'partner_id': vendor_id.id,
                        'invoice_date': fields.Date.today(),
                        'operating_unit_id':foreign_currency_billing_id.operating_unit_id,
                        'currency_id':currency_id.id,
                        'invoice_line_ids': invoice_line_ids,
                    })
                    foreign_currency_billing_id.ar_bill_number = bill_id.id
                    bill_id.created_from_shipment = True