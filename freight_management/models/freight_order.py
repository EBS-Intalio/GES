# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightOrder(models.Model):
    _name = 'freight.order'
    _description = 'Freight Order'

    shipment_id = fields.Many2one('freight.operation', 'Shipment ID')
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')
    name = fields.Char(string='Description', required=True)
    package = fields.Many2one('freight.package', 'Package', required=True)
    type = fields.Selection(([('dry', 'Dry'), ('reefer', 'Reefer')]), string="Operation")
    volume = fields.Float('Volume (CBM)')
    gross_weight = fields.Float('Gross Weight (KG)')
    qty = fields.Float('Quantity')

    @api.onchange('package')
    def onchange_package_id(self):
        for line in self:
            if line.shipment_id.transport == 'air':
                return {'domain': {'package': [('air', '=', True)]}}
            if line.shipment_id.transport == 'ocean':
                return {'domain': {'package': [('ocean', '=', True)]}}
            if line.shipment_id.transport == 'land':
                return {'domain': {'package': [('land', '=', True)]}}
