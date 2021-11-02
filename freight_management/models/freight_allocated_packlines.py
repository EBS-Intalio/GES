# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FreightAllocatedPackLines(models.Model):
    _name = 'freight.allocated.packlines'
    _description = 'Freight Allocated PackLines'

    shipment_id = fields.Char('Shipment ID')
    house_bill = fields.Char('House Bill')
    shipper_id = fields.Many2one('res.partner',string="Shipper ")
    consignee_id = fields.Many2one('res.partner',string="Consignee")
    interim_receipt = fields.Char('Interim Receipt')
    packs = fields.Integer('Packs')
    pk_ty = fields.Selection([
        ('bag','Bag'),
        ('bbg','Bulk Bag'),
        ('bbk','Break Bulk'),
        ('blc','Bale Compressed'),
        ('blu','Bale Uncompressed'),
        ('bnd','Bundle'),
        ('bot','Bottle'),
        ('box','Box'),
        ('bsk','Basket'),
        ('cas','Case'),
        ('col','Col'),
        ('crd','Cradle'),
        ('crt','Crate'),
        ('ctn','Cylinder'),
        ('cyl','Case'),
        ('doz','Dozen'),
        ('drm','Drum'),
        ('env','Envelope'),
        ('grs','Gross'),
        ('keg','Keg'),
        ('mix','Mix'),
        ('pal','Pal'),
        ('piece','Piece'),
        ('pkg','Package'),
        ('plt','Pallet'),
        ('pnl','Panel'),
        ('rai','Rails'),
        ('rel','Reel'),
        ('rll','Roll'),
        ('sht','Sheet'),
        ('skd','Skid'),
        ('spl','Spool'),
        ('tot','Tote'),
        ('tub','Tube'),
        ('unt','Unit'),
    ], string='Pk. Ty')
    weight = fields.Many2one('uom.uom',string="Weight")
    uw = fields.Many2one('uom.uom',string="UW")
    volume = fields.Float('Volume')
    uv = fields.Many2one('uom.uom',string="UV")
    pack_order = fields.Integer('Pack Order')
    commodity = fields.Many2one('freight.commodity' ,string="Commodity")
    outturn = fields.Integer('Outturn')
    pillaged = fields.Integer('Pillaged')
    damaged = fields.Integer('Damaged')
    short = fields.Integer('Short')
    surplus = fields.Integer('Surplus')
    ot_weight = fields.Float('OT Weight')
    ot_volume = fields.Float('OT Volume')
    ot_uw = fields.Many2one('uom.uom',string="UW")
    ot_uv = fields.Many2one('uom.uom',string="UV")
