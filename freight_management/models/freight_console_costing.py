# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FreightConsoleCosting(models.Model):
    _name = 'freight.console.costing'

    posted = fields.Boolean(string="Posted")
    include_on_collect_inv = fields.Boolean(string="Include On Collect Invoice")
    display_rated_shipment = fields.Boolean(string="Display Related Shipment")
    os_cost_amt = fields.Float(string="OS Cost Amt")
    os_cost_amt_currency = fields.Many2one('res.currency', string="OS Cost Amt Currency")
    local_cost_amt = fields.Float(string="Local Cost Amt")
    local_cost_amt_currency = fields.Many2one('res.currency', string="Local Cost Amt Currency")
    invoice_no = fields.Char(string="Invoice #")
    creditor = fields.Many2one('res.partner', string="Creditor")
    supply_cost_ref = fields.Char(string="Sup. Cost Ref.")
    cost_owner = fields.Many2one('res.partner', string="Cost Owner")
    invoice_date = fields.Date(string="Invoice Date")
    doc_rec_date = fields.Date(string="Doc Rec Date")
    due_date = fields.Date(string="Due Date")
    payment_type = fields.Selection([('check', 'Check'), ('cash', 'Cash'), ('credit_card', 'Credit Card'),
                                     ('direct_debit', 'Direct Debit'),
                                     ('electonic_funds_transfer', 'Electonic Funds Transfer'),
                                     ('scheduled_eft', 'Scheduled EFT'), ('collection_request', 'Collection Request'),
                                     ('pay_via_compay_direct_debit', 'Pay via ComPay Direct Debit'),
                                     ('pay_via_compay_credit_card', 'Pay via ComPay Credit Card'),
                                     ('account_maintenance_fee', 'Account Maintenance Fee'),
                                     ('bank_debit_tax', 'Bank Debit Tax'), ('bank_deposit_fee', 'Bank Deposit Fee'),
                                     ('interest_paid', 'Interest Paid'), ('interest_received', 'Interest Received'),
                                     ('periodic_payment', 'Periodic Payment'), ('stamp_duty', 'Stamp Duty'),
                                     ('miscellaneous_receipt', 'Miscellaneous Receipt'),
                                     ('miscellaneous_fees', 'Miscellaneous Fees')], string="Payment Type")
    bank_account = fields.Many2one('res.partner.bank', string="Bank Account")
    ref_number = fields.Char(string="Reference #")
    total = fields.Float(string="Total")
    tax_amt = fields.Float(string="Tax Amt")
    tax_date = fields.Date(string="Tax Date")
    total_currency = fields.Many2one('res.currency', string="Total Currency")
    tax_amt_currency = fields.Many2one('res.currency', string="Tax Amt Currency")
    override_tax_amt = fields.Boolean(string="Override Tax Amount")
    os_total = fields.Float(string="OS Total")
    os_total_currency = fields.Many2one('res.currency', string="OS Total Currency")
    os_tax = fields.Float(string="OS Tax")
    os_tax_currency = fields.Many2one('res.currency', string="OS Tax Currency")
    local_total = fields.Float(string="Local Total")
    local_total_currency = fields.Many2one('res.currency', string="Local Total Currency")
    local_tax = fields.Float(string="Local Tax Total")
    local_tax_currency = fields.Many2one('res.currency', string="Local Tax Currency")
    console_id = fields.Many2one('consol.details', string="Console")
    app_method = fields.Selection([('manual', 'Manual'), ('shipment', 'Shipment'), ('revenue', 'Revenue'),
                                   ('chargeable_units', 'Chargeable Units'),
                                   ('gross_weight', 'Gross Weight'), ('gross_volume', 'Gross Volume'),
                                   ('container_count', 'Container Count'), ('outer_pack_total', 'Outer Pack Total'),
                                   ('twenty_foot_equivalent_unit', 'Twenty-Foot Equivalent Unit'),
                                   ('capacity_per_container', 'Capacity Per Container'),
                                   ('free_space_contribution', 'Free Space Contribution')], string="App. Method")
    check_book = fields.Many2one('account.payment', string="Check Book")
    tax_rate = fields.Float(string="Tax Rate")
    tax_date = fields.Date(string="Tax Date")
