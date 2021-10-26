# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductQuantitySummary(models.Model):
    _name = 'product.quantity.summary'
    _description = 'Product Quantity Summary'

    freight_order_id = fields.Many2one('freight.order', string="Order")
    part_no = fields.Many2one('product.product',string="Part No")
    description = fields.Char(string="Description")
    quantity_ordered = fields.Float(' Ordered Quantity')
    quantity_invoiced = fields.Float('Invoiced Quantity ')
    quantity_received = fields.Float('Received Quantity ')
    quantity_remaining = fields.Float('Remaining Quantity ')
