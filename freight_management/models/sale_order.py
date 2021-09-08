# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    freight_request_id = fields.Many2one('freight.job.request', string="Freight Request")
    pricing_id = fields.Many2one('freight.pricing', 'Freight Pricing')

    def action_confirm(self):
        res = super(SalesOrder, self).action_confirm()
        if self.freight_request_id:
            self.freight_request_id.create_booking()
        return res
