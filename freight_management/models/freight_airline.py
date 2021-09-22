# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _

class FreightAirline(models.Model):
    _inherit = 'freight.airline'

    three_char = fields.Char('Three Char')
    two_char = fields.Char('Two Char')
    airline2 = fields.Char('Airline Name2')
    addr_line_1 = fields.Char('Address Line1')
    addr_line_2 = fields.Char('Address Line2')
    airline_city = fields.Char('Airline City')
    airline_state = fields.Many2one('res.country.state','Airline State')
    zip = fields.Char('PostCode')
    cass_cont = fields.Boolean('Cass Controlled')
