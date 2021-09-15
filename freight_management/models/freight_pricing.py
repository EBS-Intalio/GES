# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FreightPricing(models.Model):
    _inherit = 'freight.pricing'
    _description = 'Freight Pricing'
    _order = 'name desc, id desc'

    freight_request_id = fields.Many2one('freight.job.request', 'Freight Request')

    currency_id = fields.Many2one('res.currency', string="Currency", domain="[('active', '=', True)]")
    different_amount = fields.Selection([('price_1', 'Carrier 1'), ('price_2', 'Carrier 2'), ('price_3', 'Carrier 3')],
                                           string='Select Carrier')

    freight_transport = fields.Selection(related='freight_request_id.mode_of_transport')

    # See Fields
    freight_shipping_line_id = fields.Many2one(related='freight_request_id.shipping_line_id', readonly=False)
    freight_vessel_id = fields.Many2one(related='freight_request_id.vessel_id', readonly=False)

    # Land Fields
    freight_trucker = fields.Many2one(related='freight_request_id.trucker', readonly=False)
    freight_trucker_number = fields.Char(related='freight_request_id.trucker_number', readonly=False)

    preferred_airline_id = fields.Many2one(related='freight_request_id.preferred_airline_id', readonly=False)
    freight_flight_no = fields.Char(related='freight_request_id.flight_no', readonly=False)

    freight_additional_comments = fields.Text(related='freight_request_id.additional_comments', readonly=False)

    freight_target_etd = fields.Date(related='freight_request_id.target_etd', readonly=False)
    freight_target_eta = fields.Date(related='freight_request_id.target_eta', readonly=False)

    sales_count = fields.Integer(string='Total Orders', compute='_compute_sales_orders')
    order_ids = fields.One2many('sale.order', 'pricing_id', string='Orders', copy=False)

    # carrier_ids = fields.Many2many('res.partner', 'Carrier')
    carrier_ids = fields.Many2many('res.partner', string="Carrier")

    total_charges_amount_usd = fields.Float(string='Total Charge Amount USD', compute='_compute_total_charges_usd_eur_aed')
    total_charges_amount_aed = fields.Float(string='Total Charge Amount AED', compute='_compute_total_charges_usd_eur_aed')
    total_charges_amount_eur = fields.Float(string='Total Charge Amount EUR', compute='_compute_total_charges_usd_eur_aed')

    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        readonly=True, check_company=True,
        domain=lambda self: [(1, '=', 1)],
        states={'draft': [('readonly', False)]})

    def _compute_total_charges_usd_eur_aed(self):
        """
        Compute total charge amount in USD, EUR and AED
        :return:
        """
        for line in self:
            if line.different_amount == 'price_1':
                total_charges_amount_usd = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'USD').mapped('charge_amount'))
                total_charges_amount_aed = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'AED').mapped('charge_amount'))
                total_charges_amount_eur = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'EUR').mapped('charge_amount'))
            elif line.different_amount == 'price_2':
                total_charges_amount_usd = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'USD').mapped('charge_amount_price_2'))
                total_charges_amount_aed = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'AED').mapped('charge_amount_price_2'))
                total_charges_amount_eur = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'EUR').mapped('charge_amount_price_2'))
            else:
                total_charges_amount_usd = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'USD').mapped('charge_amount_price_3'))
                total_charges_amount_aed = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'AED').mapped('charge_amount_price_3'))
                total_charges_amount_eur = sum(line.charges_ids.filtered(lambda charge: charge.currency_id.name == 'EUR').mapped('charge_amount_price_3'))
            line.total_charges_amount_usd = total_charges_amount_usd
            line.total_charges_amount_aed = total_charges_amount_aed
            line.total_charges_amount_eur = total_charges_amount_eur

    def action_done(self):
        """
        DOne Request and Create Mail Activity
        :return:
        """
        res = super(FreightPricing, self).action_done()
        activity_type = self.env.ref('mail.mail_activity_data_todo').id

        activity = self.env['mail.activity'].create({
            'summary': 'Check Pricing',
            'activity_type_id': activity_type,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'freight.pricing')], limit=1).id,
            'res_id': self.id,
        })
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
        """
        Count total pricing sales order
        :return:
        """
        for pricing in self:
            pricing.sales_count = len(pricing.order_ids)

    def _compute_total_charges(self):
        """
        Compute total charges set based on Converted Amount (Currency Amount)
        :return:
        """
        self.total_charges = sum(self.charges_ids.mapped('converted_amount'))

    def create_quotations(self):
        """
        Create a sales Quotations
        :return:
        """
        if not self.freight_request_id:
            raise ValidationError('Request not found.')
        if not self.freight_request_id.partner_id:
            raise ValidationError('Customer Not set in the Request.')

        vals = []
        count = 10
        for charges in self.charges_ids.filtered(lambda x: x.product_id and not x.freight_line_section_id):
            description = self.env['sale.order.line'].get_sale_order_line_multiline_description_sale(charges.product_id)

            vals.append((0, 0, {'name': description,
                                'product_id': charges.product_id.id,
                                'product_uom_qty': 1,
                                'sequence': count,
                                'price_unit': charges.converted_amount}))
            count += 1

        section_ids = self.charges_ids.filtered(lambda x: x.product_id).mapped('freight_line_section_id')
        for section in section_ids:
            vals.append((0, 0, {'name': '%s'%section.name,
                                'sequence': count,
                                'display_type': 'line_section'}))
            count += 1

            for charges in self.charges_ids.filtered(lambda x: x.product_id and x.freight_line_section_id.id == section.id):
                description = self.env['sale.order.line'].get_sale_order_line_multiline_description_sale(charges.product_id)
                vals.append((0, 0, {'name': description,
                                    'product_id': charges.product_id.id,
                                    'product_uom_qty': 1,
                                    'sequence': count,
                                    'price_unit': charges.converted_amount}))
                count += 1

        freight_request_id = self.freight_request_id
        if freight_request_id:
            vals = {
                'freight_request_id': freight_request_id.id,
                'pricing_id': self.id,
                'partner_id': freight_request_id and freight_request_id.partner_id.id or False,
                'order_line': vals
            }
            if self.currency_id:
                price_list_id = self.env['product.pricelist'].search([('currency_id','=',self.currency_id.id)])
                if price_list_id:
                    vals.update({'pricelist_id': price_list_id[0].id})
                else:
                    price_list_id = self.env['product.pricelist'].create({'name':'Default '+ self.currency_id.name+ ' Pricelist','currency_id':self.currency_id.id})
                    vals.update({'pricelist_id': price_list_id.id})
            order_quotation = self.env['sale.order'].create(vals)
            print("order_quotationorder_quotationorder_quotationorder_quotationorder_quotation", order_quotation)
        return True

    def button_request(self):
        """
        View Freight Request
        :return:
        """
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

