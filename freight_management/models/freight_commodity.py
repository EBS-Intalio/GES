# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class FreightCommodity(models.Model):
    _name = 'freight.commodity'
    _rec_name = 'commodity_code'

    # name = fields.Char(string='Name', required=True)
    commodity_code = fields.Char(string='Code', required=True)
    iata_commodity = fields.Char(string='IATA Commodity')
    commodity_description = fields.Char(string='Commodity Description')
    lang = fields.Selection(_lang_get, string='Language')
    # universal_group = fi

    is_system = fields.Boolean(string='Is System')
    is_land_transport = fields.Boolean(string='Is Land Transport')
    is_shipping = fields.Boolean(string='Is Shipping')
    is_forwarding = fields.Boolean(string='Is Forwarding')
    active = fields.Boolean(string='Is This Commodity Code Active', default=True)
    is_this_commodity_pershable = fields.Boolean(string='Is This Commodity Perishable')
    is_this_commodity_timber = fields.Boolean(string='Is This Commodity Timber')
    is_this_commodity_hazardous = fields.Boolean(string='Is This Commodity Hazardous')
    is_this_commodity_flammable = fields.Boolean(string='Is This Commodity Flammable')
    is_con_v_req_commodity = fields.Boolean(string='Is Container Vent Required For This Commodity')
    reefer_min_temp = fields.Float(string='Reefer Min. Temp')
    reefer_max_temp = fields.Float(string='Reefer Max. Temp')
    expiry_date_commodity = fields.Date(string='Expiry Date Of This Commodity')
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')
