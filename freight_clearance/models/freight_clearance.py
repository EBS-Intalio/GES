# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightClearance(models.Model):
    _name = 'freight.clearance'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Freight Clearance'

    name = fields.Char(string='Name')

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('freight.clearance') or _('New')
        clearance = super(FreightClearance, self).create(values)
        return clearance

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft', string='Status', track_visibility='onchange')

    def action_confirm(self):
        self.state = 'confirm'

    clearance_type = fields.Selection(([('general', 'General'), ('indian', 'Indian')]), string='Clearance Type', default='general', required=True, track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, track_visibility='onchange')
    freight_related = fields.Boolean("related to a freight Job?", track_visibility='onchange')
    request_id = fields.Many2one('freight.job.request', track_visibility='onchange')
    pol_id = fields.Many2one('freight.pol', string="POL", required=True, track_visibility='onchange')
    pod_id = fields.Many2one('freight.pod', string="POD", required=True, track_visibility='onchange')
    eta = fields.Date("ETA", required=True, track_visibility='onchange')
    etd = fields.Date("ETD", required=True, track_visibility='onchange')
    bl_copy = fields.Boolean("BL Copy Available ?", track_visibility='onchange')
    shipping_documents = fields.Boolean("Shipping Documents", track_visibility='onchange')
    original_copy = fields.Boolean("Original/Copy", track_visibility='onchange')
    #contact person
    first_name = fields.Char("First Name", required=True)
    family_name = fields.Char("Family Name", required=True)
    email = fields.Char("Email Address", required=True)
    phone = fields.Char("Phone Number", required=True)
    #delivery address
    delivery_country_id = fields.Many2one('res.country', string='Country')
    delivery_state_id = fields.Many2one('res.country.state', string='State',
                                        domain="[('country_id', '=', delivery_country_id)]")
    delivery_city = fields.Char(string="City")
    delivery_area = fields.Char(string="Area")
    delivery_street = fields.Char(string="Street")
    delivery_building = fields.Char(string="Building")
    delivery_po_box = fields.Char(string="PO Box")
    delivery_zip_code = fields.Integer(string="Zip Code")
    #Indian fields
    consignee_id = fields.Many2one('res.partner', string="Consignee", track_visibility='onchange')
    transport = fields.Selection(([('air', 'Air'), ('sea', 'Sea'), ('road', 'Road'), ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'), ('rail', 'Rail'), ('courier', 'Courier')]), string='Transport', track_visibility='onchange')

    road_shipment_type = fields.Selection(([('ltl', 'LTL'), ('ftl', 'FTL')]), string='Road Shipment Type', track_visibility='onchange')
    shipment_type = fields.Selection(([('fcl', 'FCL'), ('roro', 'Roro'), ('liquid', 'Liquid'), ('bulk', 'Bulk'), ('breakbulk', 'Breakbulk')]), string='Ocean Shipment Type', track_visibility='onchange')
    pofd_destination_id = fields.Many2one('freight.pofd.destination', string="Final Destination", track_visibility='onchange')
    additional_comments = fields.Text("Additional Comments", track_visibility='onchange')