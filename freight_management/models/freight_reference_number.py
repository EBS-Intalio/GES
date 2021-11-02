# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightReferenceNumber(models.Model):
    _name = 'freight.reference.number'

    name = fields.Char(string='Reference Number', required=True)
    type = fields.Selection([('ble', 'Bill Of Entry Number'),
                           ('dlv', 'Delivery Order Number'),
                           ('mrn', 'Manifest Registration Number'),
                           ('noc', 'No Objections Certificate Number'),
                           ('ins', 'UAE Installment Number'),
                           ('coc', 'Custom Office Code (Override)'),
                           ('ams', 'AMS Number'),
                           ('ubr', 'Under Bond Approval Reference Number'),
                           ('con', 'Carrier Contract Number'),
                           ('bkg', 'Carrier Booking Reference'),
                           ('ams', 'Ams Number'),
                           ('car', 'Customs Authorization Reference'),
                           ('lcr', 'Letter Of Credit Number'),
                           ('frm', 'FIRMS Code'),
                           ('ccn', 'Cargo Control Number'),
                           ('pcn', 'Previous Cargo Control Number'),
                           ('ucr', 'External (3rd Party) unique Consignment Reference')], string='Type')
    country_id = fields.Many2one('res.country', string='Country Of Issue')
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')
    shipment_id = fields.Many2one('freight.operation', string='Shipment')
    freight_console_id = fields.Many2one('consol.details', string='Consol')
    information = fields.Char(string='Information')
    issue_date = fields.Date(string='Issue Date')
    freight_container_id = fields.Many2one('freight.container', string='Container')
