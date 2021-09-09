# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightPricing(models.Model):
    _inherit = 'freight.pricing'
    _description = 'Freight Pricing'

    freight_request_id = fields.Many2one('freight.job.request', 'Freight Request')

    currency_id = fields.Many2one('res.currency', string="Currency", domain="[('active', '=', True)]")
    different_amount = fields.Selection(([('price_1', 'Price 1'), ('price_2', 'Price 2'), ('price_3', 'Price 3')]),
                                           string='Select Charge Amount', default='price_1')

    freight_transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport',
                                 related='freight_request_id.mode_of_transport')

    # See Fields
    freight_shipping_line_id = fields.Many2one('res.partner', 'Shipping Line', related='freight_request_id.shipping_line_id')
    freight_vessel_id = fields.Many2one('freight.vessel', 'Vessel', related='freight_request_id.vessel_id')

    # Land Fields
    freight_trucker = fields.Many2one('freight.trucker', 'Trucker', related='freight_request_id.trucker')
    freight_trucker_number = fields.Char('Trucker No', related='freight_request_id.trucker_number')

    sales_count = fields.Integer(string='Total Orders', compute='_compute_sales_orders')
    order_ids = fields.One2many('sale.order', 'pricing_id', string='Orders', copy=False)

    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        readonly=True, check_company=True,
        domain=lambda self: [(1, '=', 1)],
        states={'draft': [('readonly', False)]}, )

    def action_done(self):
        res = super(FreightPricing, self).action_done()
        activity_type = self.env.ref('mail.mail_activity_data_todo').id

        activity = self.env['mail.activity'].create({
            'summary': 'Check Pricing',
            'activity_type_id': activity_type,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'freight.pricing')], limit=1).id,
            'res_id': self.create_uid.partner_id.id,
        })
        print("aaaaa", activity)
        return res

    def action_view_sales_order(self):
        """
        Prepare a action for the display sales order
        :return:
        """
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        orders = self.order_ids
        if len(orders) > 1:
            action['domain'] = [('id', 'in', orders.ids)]
        elif orders:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = orders.id

        return action

    @api.depends('order_ids')
    def _compute_sales_orders(self):
        for pricing in self:
            pricing.sales_count = len(pricing.order_ids)

    def _compute_total_charges(self):
        self.total_charges = sum(self.charges_ids.mapped('converted_amount'))

    def create_quotations(self):
        vals = []
        for charges in self.charges_ids:
            description = self.env['sale.order.line'].get_sale_order_line_multiline_description_sale(charges.product_id)
            vals.append((0, 0, {'name': description,
                                'product_id': charges.product_id.id,
                                'product_uom_qty': 1,
                                'price_unit': charges.converted_amount}))
        freight_request_id = self.freight_request_id
        if freight_request_id:
            vals = {
                'freight_request_id': freight_request_id.id,
                'pricing_id': self.id,
                'partner_id': freight_request_id and freight_request_id.partner_id.id or False,
                'order_line': vals
            }
            if self.currency_id:
                vals.update({'currency_id':self.currency_id.id})
            order_quotation = self.env['sale.order'].create(vals)
            # order_quotation.write({'order_line': vals})
            print("order_quotationorder_quotationorder_quotationorder_quotationorder_quotation", order_quotation)
        return True

    def button_request(self):
        action = {
            'name': _('Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'freight.job.request',
            'target': 'current',
        }
        ope = self.env['freight.job.request'].search([('pricing_id', '=', self.id)], limit=1)
        action['domain'] = [('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action

