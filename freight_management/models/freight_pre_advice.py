# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightPreAdvice(models.Model):
    _name = 'freight.pre.advice'
    _rec_name = 'pre_advice_id'

    pre_advice_id = fields.Char(string="Pre-Advice Id")
    master_bill = fields.Char(string="Master Bill")
    house_bill = fields.Char(string="House Bill")
    load_port = fields.Many2one('unloco.data', string="Load Port")
    discharge_port = fields.Many2one('unloco.data', string="Discharge Port")
    carrier = fields.Many2one('res.partner', string="Carrier")
    sending_agent = fields.Many2one('res.partner', string="Sending Agent")
    receiving_agent = fields.Many2one('res.partner', string="Receiving Agent")
    buyer = fields.Many2one('res.partner', string="Buyer")
    buyer_address = fields.Many2one('res.partner', string="Buyer Address")

    shipment = fields.Many2one('freight.operation', string="Shipment")
    weight = fields.Float(string="Weight")
    volume = fields.Float(string="volume")
    weight_uom = fields.Many2one('uom.uom', string="Weight Uom")
    volume_uom = fields.Many2one('uom.uom', string="Volume Uom")
    packs = fields.Float(string="Packs")
    packs_uom = fields.Many2one('uom.uom', string="Packs Uom")
    order_ids = fields.Many2many('freight.order', string='Order', copy=False)
    container_ids = fields.Many2many('freight.container', string='Container', copy=False)
    is_canceled = fields.Boolean(string="Canceled")
    routing_ids = fields.One2many('freight.routing', 'pre_advice_id', string="Routing")


