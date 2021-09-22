# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PartnerRelatedParties(models.Model):
    _name = 'partner.related.parties'
    _description = 'Related Parties'

    party_type = fields.Selection([('ccf', 'Client DFS'),
                                   ('ccb', 'Controlling Customer'),
                                   ('cab', 'Customs Agent Broker'),
                                   ('ict', 'Invoice Customs Jobs To'),
                                   ('ift','Invoice Freight Jobs To'),
                                   ('ltt', 'Local Transport Provider'),
                                   ('ltb', 'Local Transport Provider Bill To'),
                                   ('ndc', 'National Distribution Center'),
                                   ('pag', 'Pickup Agent'),
                                   ('jnp', 'Japan Notification Party'),
                                   ('agr', 'Receiving Agent'),
                                   ('ags', 'Sending Agent'),
                                   ('whs', 'warehouse'),
                                   ('waf', 'Warehouse Forwarder'),
                                   ('rrt', 'Report Revenue To')], default='ccf', required=True, string='Party Type')
    party_type_description = fields.Char(string='Party Type Description')
    for_address = fields.Char(string='For Address')
    transport_mode = fields.Char(string='Transport Mode')
    container_mode = fields.Char(string='Container Mode')
    related_partner_id = fields.Many2one('res.partner', string='Related Party')
    related_partner_name = fields.Char(string='Related Party Name')
    unloco_id = fields.Many2one('unloco.data', string='Unloco')
    company_system_level = fields.Selection([('ent', 'System Level - All Companies'),
                                             ('com', 'This Company Only')], string='Company /System Level')

