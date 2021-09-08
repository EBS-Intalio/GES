# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
import json


class FreightOperation(models.Model):
    _name = 'freight.operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Freight Operation'

    def _get_default_stage_id(self):
        return self.env['shipment.stage'].search([], order='sequence', limit=1)

    def _default_random_barcode(self):
        return "".join(choice(digits) for i in range(8))

    barcode = fields.Char(string="Barcode", help="ID used for shipment identification.",
                          default=_default_random_barcode, copy=False)
    color = fields.Integer('Color')
    stage_id = fields.Many2one('shipment.stage', 'Stage', default=_get_default_stage_id,
                               group_expand='_read_group_stage_ids')
    name = fields.Char(string='Name', copy=False)
    direction = fields.Selection(([('import', 'Import'), ('export', 'Export')]), string='Direction')
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')
    operation = fields.Selection([('direct', 'Direct'), ('house', 'House'), ('master', 'Master')], string='Operation')
    ocean_shipment_type = fields.Selection(([('fcl', 'FCL'), ('lcl', 'LCL')]), string='Ocean Shipment Type')
    inland_shipment_type = fields.Selection(([('ftl', 'FTL'), ('ltl', 'LTL')]), string='Inland Shipment Type')
    shipper_id = fields.Many2one('res.partner', 'Shipper')
    consignee_id = fields.Many2one('res.partner', 'Consignee')
    source_location_id = fields.Many2one('freight.port', 'Source Location', index=True, required=True)
    destination_location_id = fields.Many2one('freight.port', 'Destination Location', index=True, required=True)
    obl = fields.Char('OBL', help='Original Bill Of Landing')
    shipping_line_id = fields.Many2one('res.partner', 'Shipping Line')
    voyage_no = fields.Char('Voyage No')
    vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    mawb_no = fields.Char('MAWB No')
    airline_id = fields.Many2one('freight.airline', 'Airline')
    flight_no = fields.Char('Flight No')
    datetime = fields.Datetime('Date')
    truck_ref = fields.Char('CMR/RWB#/PRO#:')
    trucker = fields.Many2one('freight.trucker', 'Trucker')
    trucker_number = fields.Char('Trucker No')
    agent_id = fields.Many2one('res.partner', 'Agent')
    operator_id = fields.Many2one('res.users', 'User')
    freight_pc = fields.Selection(([('collect', 'Collect'), ('prepaid', 'Prepaid')]), string="Freight PC")
    other_pc = fields.Selection(([('collect', 'Collect'), ('prepaid', 'Prepaid')]), string="Other PC")
    notes = fields.Text('Notes')
    dangerous_goods = fields.Boolean('Dangerous Goods')
    dangerous_goods_notes = fields.Text('Dangerous Goods Info')
    move_type = fields.Many2one('freight.move.type', 'Move Type')
    tracking_number = fields.Char('Tracking Number')
    declaration_number = fields.Char('Declaration Number')
    declaration_date = fields.Date('Declaration Date')
    custom_clearnce_date = fields.Datetime('Customs Clearance Date')
    freight_orders = fields.One2many('freight.order', 'shipment_id')
    freight_packages = fields.One2many('freight.package.line', 'shipment_id')
    freight_services = fields.One2many('freight.service', 'shipment_id')
    incoterm = fields.Many2one('freight.incoterms', 'Incoterm')
    freight_routes = fields.One2many('freight.route', 'shipment_id')
    freight_log = fields.One2many('shipment.log', 'shipment_id')
    parent_id = fields.Many2one('freight.operation', 'Parent')
    shipments_ids = fields.One2many('freight.operation', 'parent_id')
    service_count = fields.Float('Services Count', compute='_compute_invoice')
    invoice_count = fields.Float('Invoice Count', compute='_compute_invoice')
    vendor_bill_count = fields.Float('Vendor Bill Count', compute='_compute_invoice')
    total_invoiced = fields.Float('Total Invoiced(Receivables', compute='compute_total_amount')
    total_bills = fields.Float('Total Bills(Payables)', compute='compute_total_amount')
    margin = fields.Float("Margin", compute='compute_total_amount')
    invoice_residual = fields.Float('Invoice Residual', compute='compute_total_amount')
    bills_residual = fields.Float('Bills Residual', compute='compute_total_amount')
    invoice_paid_amount = fields.Float('Invoice', compute='compute_total_amount')
    bills_paid_amount = fields.Float('Bills', compute='compute_total_amount')
    actual_margin = fields.Float('Actual Margin', compute='compute_total_amount')
    sale_orders = fields.One2many('sale.order', 'freight_id')
    freight_request_id = fields.Many2one('freight.job.request', string="Freight request")
    service_quote_count = fields.Float('Quote Count', compute='_compute_invoice')
    freight_request_count = fields.Float('Request Count', compute='_compute_invoice')

    @api.depends('freight_services')
    def compute_total_amount(self):
        for order in self:
            invoices = self.env['account.move'].sudo().search(
                [('freight_operation_id', '=', order.id), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted')])
            invoice_amount = 0.0
            bill_amount = 0.0
            invoice_residual = 0.0
            bills_residual = 0.0
            invoice_paid_amount = 0.0
            bills_paid_amount = 0.0
            for invoice in invoices:
                invoice_amount += invoice.amount_total
                invoice_residual += invoice.amount_residual
                reconciled_payments_widget_vals = json.loads(invoice.invoice_payments_widget)
                if reconciled_payments_widget_vals:
                    paid_amount_dict = {vals['move_id']: vals['amount'] for vals in
                                        reconciled_payments_widget_vals['content']}
                else:
                    paid_amount_dict = 0.0
                invoice_paid_amount += sum(list(paid_amount_dict.values())) if type(paid_amount_dict) == dict else 0.0

            bills = self.env['account.move'].sudo().search(
                [('freight_operation_id', '=', order.id), ('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
            for bill in bills:
                bill_amount += bill.amount_total
                bills_residual += bill.amount_residual
                reconciled_payments_widget_vals_bill = json.loads(bill.invoice_payments_widget)
                if reconciled_payments_widget_vals_bill:
                    paid_bill_amount_dict = {vals['move_id']: vals['amount'] for vals in
                                             reconciled_payments_widget_vals_bill['content']}
                else:
                    paid_bill_amount_dict = 0.0
                bills_paid_amount += sum(list(paid_bill_amount_dict.values())) if type(
                    paid_bill_amount_dict) == dict else 0.0

            order.total_invoiced = invoice_amount
            order.total_bills = bill_amount
            order.margin = invoice_amount - bill_amount
            order.invoice_residual = invoice_residual
            order.invoice_paid_amount = invoice_paid_amount
            order.bills_residual = bills_residual
            order.bills_paid_amount = bills_paid_amount
            order.actual_margin = invoice_paid_amount - bills_paid_amount

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['shipment.stage'].search([])
        return stage_ids

    @api.depends('freight_services')
    def _compute_invoice(self):
        for order in self:
            order.service_count = len(order.freight_services)
            order.service_quote_count = len(order.sale_orders)
            order.invoice_count = self.env['account.move'].sudo().search_count(
                [('freight_operation_id', '=', order.id), ('move_type', '=', 'out_invoice')])
            order.vendor_bill_count = self.env['account.move'].sudo().search_count(
                [('freight_operation_id', '=', order.id), ('move_type', '=', 'in_invoice')])
            order.freight_request_count = 1 if self.freight_request_id else 0

    def button_services(self):
        services = self.mapped('freight_services')
        action = self.env["ir.actions.actions"]._for_xml_id("freight.view_freight_service_action")
        action['context'] = {'default_shipment_id': self.id}
        action['domain'] = [('id', 'in', services.ids)]
        return action

    def button_services_quotes(self):
        action = {
            'name': _('Sales Order(s)'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'target': 'current',
        }
        action['context'] = {'default_freight_id': self.id}
        sale_order_ids = self.sale_orders.ids
        if len(sale_order_ids) == 1:
            action['res_id'] = sale_order_ids[0]
            action['view_mode'] = 'form'
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', sale_order_ids)]
        return action

    def button_services_bookings(self):
        action = {
            'name': _('Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'freight.job.request',
            'target': 'current',
        }
        action['domain'] = [('id', '=', self.freight_request_id.id)]
        freight_request_id = self.freight_request_id.id
        action['res_id'] = freight_request_id
        action['view_mode'] = 'form'
        return action

    def button_customer_invoices(self):
        invoices = self.env['account.move'].sudo().search(
            [('freight_operation_id', '=', self.id), ('move_type', '=', 'out_invoice')])
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

    def button_vendor_bills(self):
        invoices = self.env['account.move'].sudo().search(
            [('freight_operation_id', '=', self.id), ('move_type', '=', 'in_invoice')])
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

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            if values.get('operation') == 'master':
                values['name'] = self.env['ir.sequence'].next_by_code('operation.master') or _('New')
            elif values.get('operation') == 'house':
                values['name'] = self.env['ir.sequence'].next_by_code('operation.house') or _('New')
            elif values.get('operation') == 'direct':
                values['name'] = self.env['ir.sequence'].next_by_code('operation.direct') or _('New')
        if values.get('name', False) and not values.get('tracking_number', False):
            values['tracking_number'] = values.get('name', False)
        id_data = super(FreightOperation, self).create(values).id
        id = self.env['freight.operation'].browse(id_data)
        if id.transport == 'air':
            self.env['freight.route'].create({'source_location_id': id.source_location_id.id,
                                              'destination_location_id': id.destination_location_id.id,
                                              'main_carriage': True,
                                              'transport': id.transport,
                                              'mawb_no': id.mawb_no,
                                              'airline_id': id.airline_id.id,
                                              'flight_no': id.flight_no,
                                              'shipment_id': id.id})
        if id.transport == 'ocean':
            self.env['freight.route'].create({'source_location_id': id.source_location_id.id,
                                              'destination_location_id': id.destination_location_id.id,
                                              'main_carriage': True,
                                              'transport': id.transport,
                                              'shipping_line_id': id.shipping_line_id.id,
                                              'vessel_id': id.vessel_id.id,
                                              'obl': id.obl,
                                              'shipment_id': id.id})
        if id.transport == 'land':
            self.env['freight.route'].create({'source_location_id': id.source_location_id.id,
                                              'destination_location_id': id.destination_location_id.id,
                                              'main_carriage': True,
                                              'transport': id.transport,
                                              'truck_ref': id.truck_ref,
                                              'trucker': id.trucker.id,
                                              'trucker_number': id.trucker_number,
                                              'shipment_id': id.id})
        if 'default_freight_request_id' in self._context.keys():
            book = self.env['freight.job.request'].browse(self._context.get('default_freight_request_id'))
            book.freight_id = id.id
        return id

    @api.depends('transport')
    @api.onchange('source_location_id')
    def onchange_source_location_id(self):
        for line in self:
            if line.transport == 'air':
                return {'domain': {'source_location_id': [('air', '=', True)]}}
            elif line.transport == 'ocean':
                return {'domain': {'source_location_id': [('ocean', '=', True)]}}
            elif line.transport == 'land':
                return {'domain': {'source_location_id': [('land', '=', True)]}}

    @api.depends('transport')
    @api.onchange('destination_location_id')
    def onchange_destination_location_id(self):
        for line in self:
            if line.transport == 'air':
                return {'domain': {'destination_location_id': [('air', '=', True)]}}
            elif line.transport == 'ocean':
                return {'domain': {'destination_location_id': [('ocean', '=', True)]}}
            elif line.transport == 'land':
                return {'domain': {'destination_location_id': [('land', '=', True)]}}

    def generate_from_the_orders(self):
        for line in self:
            packages = []
            for order in line.freight_orders:
                packages.append((0, 0, {'name': order.name,
                                        'package': order.package.id,
                                        'qty': order.qty,
                                        'volume': order.volume,
                                        'gross_weight': order.gross_weight,
                                        'shipment_id': line.id}))
            self.freight_packages.unlink()
            self.write({'freight_packages': packages})
