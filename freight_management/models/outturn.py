# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OutTurn(models.Model):
    _name = 'container.outturn.line'
    _description = 'OutTurn'

    outturn_container_id = fields.Many2one('freight.container',string="OutTurn Container")
    shipment_id = fields.Char('shipment ID')
    packs = fields.Integer('Packs')
    pk_ty = fields.Char('PK. TY')
    outturn = fields.Integer('OutTurn')
    damaged = fields.Integer('Damaged')
    pillaged = fields.Integer('Pillaged')

