from odoo import models, fields


class FreightDocLine(models.Model):
    _name = 'freight.doc.line'

    order_no = fields.Integer('Order')
    category = fields.Char('Category')
    name = fields.Char('Name')
    value = fields.Boolean('Value')
    console_id = fields.Many2one('consol.details', 'Console Details')
    shipment_id = fields.Many2one('freight.operation', string="Shipment")
    freight_order_id = fields.Many2one('freight.order', string="Freight Order")
