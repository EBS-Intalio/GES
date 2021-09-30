# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FreightVessel(models.Model):
    _inherit = 'freight.vessel'

    screening_status = fields.Selection([('unk', 'Unknown')], string="Screening Status")
    agent_vessel_number = fields.Char(string="Agent Vessel Number")
    imo_number = fields.Char(string="IMO Number")
    radio_call_sign = fields.Char(string="Radio Call Sign")
    vessel_consortium = fields.Char(string="Vessel Consortium")
    shipping_provider_id = fields.Many2one('res.partner', string="Shipping Provider")
    net_register_ton = fields.Integer(string="Net Register Ton")
    vessel_ype = fields.Selection([('ba', 'Barge'),
                                   ('blk', 'Bulk Carrier'),
                                   ('cs', 'Cable Ship'),
                                   ('car', 'Car Caring Vessel'),
                                   ('cv', 'Cargo Vessel'),
                                   ('ds', 'Drill Ship'),
                                   ('dry', 'Dry Cargo Vessel'),
                                   ('fv', 'Fishing Vessel'),
                                   ('cnt', 'Containerized vessel'),
                                   ('dr', 'Dredger')], string="Vessel Type")

    @api.constrains('imo_number')
    def check_use_imo_number(self):
        for rec in self:
            if rec.imo_number and len(self.env['freight.vessel'].search([('imo_number', '=', rec.imo_number)])) > 1:
                raise ValidationError(_('IMO Number Already Used.'))
