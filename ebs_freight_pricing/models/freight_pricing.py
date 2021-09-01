# -*- coding: utf-8 -*"-

from odoo import models, fields, api, _
from datetime import timedelta, date, datetime


class ChargesList(models.Model):
    _name = 'charges.list'
    _description = 'Charges List'

    name = fields.Char()
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')


class FreightPricingCharges(models.Model):
    _name = 'freight.pricing.charges'
    _description = 'Freight Pricing Charges'

    pricing_id = fields.Many2one('freight.pricing', 'Freight Pricing')
    freight_id = fields.Many2one('freight.operation', 'Freight Operation')
    book_id = fields.Many2one('freight.booking', 'Freight Book')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda x: x.env.company.currency_id)
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport',
                                 related='pricing_id.transport')

    # Charges & Fees
    charges = fields.Many2one('charges.list', string='Charge')
    # ,
    # domain = lambda self: [('type', '=', self.transport)]
    charge_amount = fields.Monetary(currency_field='currency_id', string='Charge Amount')
    margin_per = fields.Float(string='Margin(%)')
    margin_amount = fields.Monetary(currency_field='currency_id', string='Margin Amount',
                                    compute='_compute_charge_total_amount')
    charge_total_amount = fields.Monetary(currency_field='currency_id', string='Charge Total Amount',
                                          compute='_compute_charge_total_amount')

    @api.depends('charge_amount', 'margin_per')
    def _compute_charge_total_amount(self):
        margin_amount = charge_total_amount = 0
        for line in self:
            if line.charge_amount and line.margin_per:
                margin_amount = (line.charge_amount * line.margin_per) / 100
                charge_total_amount = line.charge_amount + margin_amount
            line.margin_amount = margin_amount
            line.charge_total_amount = charge_total_amount


class FreightPricing(models.Model):
    _name = 'freight.pricing'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Freight Pricing'

    def _get_default_stage_id(self):
        return self.env['shipment.stage'].search([], order='sequence', limit=1)

    # Fields for all
    name = fields.Char(string='Name', copy=False)
    state = fields.Selection(([('draft', 'Draft'),
                               ('done', 'Done')]),
                             string='Status', default='draft')

    stage_id = fields.Many2one('shipment.stage', 'Stage', default=_get_default_stage_id,
                               group_expand='_read_group_stage_ids')

    freight_id = fields.Many2one('freight.operation', 'Freight Operation')
    book_id = fields.Many2one('freight.booking', 'Freight Book')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda x: x.env.company.currency_id)

    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport',
                                 related='book_id.transport')

    color = fields.Integer('Color')

    eta = fields.Datetime('ETA')
    etd = fields.Datetime('ETD')

    additional_comments = fields.Text('Additional Comments')

    charges_ids = fields.One2many('freight.pricing.charges', 'pricing_id', string='Freight Charges')

    total_charges = fields.Monetary(currency_field='currency_id', string='Total Charge Amount',
                                    compute='_compute_total_charges')

    # See Fields
    shipping_line_id = fields.Many2one('res.partner', 'Shipping Line', related='book_id.shipping_line_id')
    vessel_id = fields.Many2one('freight.vessel', 'Vessel', related='book_id.vessel_id')
    origin_days = fields.Integer('Free Days at Origin')
    Port_days = fields.Integer('Free Days at Port')

    # Land Fields
    trucker = fields.Many2one('freight.trucker', 'Trucker', related='book_id.trucker')
    origin_country = fields.Many2one('res.country', 'Origin Country')
    origin_country_border = fields.Many2one('res.country', 'Origin Country Border')
    transit_country = fields.Many2one('res.country', 'Transit Country')
    transit_country_border = fields.Many2one('res.country', 'Transit Country Border')
    trucker_number = fields.Char('Trucker No', related='book_id.trucker_number')
    rout = fields.Char('Rout')

    # Air Fields
    airline_id = fields.Many2one('freight.airline', 'Airline')
    flight_no = fields.Char('Flight No')

    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        readonly=True, check_company=True,
        domain=lambda self: [('type', '=', self.transport)],
        states={'draft': [('readonly', False)]}, )
    order_line = fields.One2many('sale.order.line', 'pricing_id', string='Order Lines',
                                 related='sale_order_template_id.sale_order_template_line_ids')

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('freight.pricing') or _('New')
        Pricing = super(FreightPricing, self).create(values)
        return Pricing

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['shipment.stage'].search([])
        return stage_ids

    def action_done(self):
        self.state = 'done'

    def _compute_total_charges(self):
        self.total_charges = sum(self.charges_ids.mapped('charge_total_amount'))

    def reset_pricing(self):
        self.state = 'draft'

    def button_shipping(self):
        action = {
            'name': _('Shipment'),
            'type': 'ir.actions.act_window',
            'res_model': 'freight.operation',
            'target': 'current',
        }
        ope = self.env['freight.operation'].search([('pricing_id', '=', self.id)], limit=1)
        action['domain'] = [('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action

    def button_booking(self):
        action = {
            'name': _('Booking'),
            'type': 'ir.actions.act_window',
            'res_model': 'freight.booking',
            'target': 'current',
        }
        ope = self.env['freight.booking'].search([('pricing_id', '=', self.id)], limit=1)
        action['domain'] = [('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action
