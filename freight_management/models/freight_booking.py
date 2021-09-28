# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightBooking(models.Model):
    _inherit = 'freight.booking'

    freight_request_id = fields.Many2one('freight.job.request','RequestID')
    hs_code = fields.Many2many('freight.hs.code', string="Freight Hs-Codes")

    transport = fields.Selection([('air', 'Air'),
                                   ('ocean', 'Ocean'),
                                   ('land', 'Land'),
                                   ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'),
                                   ('rail', 'Rail'),
                                   ('courier', 'Courier')], string='Transport', required=False)

    # ADDED Field for booking cargo
    add_terms = fields.Char(string="Add. Terms")
    service_level = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                      ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door')],
                                     string="Service Level")
    shippers_ref = fields.Char(string="Shipper's Ref")
    carrier_id = fields.Many2one('res.partner', string='Carrier')
    goods_vals = fields.Float(string='Goods Val')
    goods_vals_currency_id = fields.Many2one('res.currency', string='Goods Vals Currency')
    ins_vals = fields.Float(string='Ins Val')
    ins_vals_currency_id = fields.Many2one('res.currency', string='Ins Vals Currency')

    outers = fields.Float(string='Outers')
    outers_uom_id = fields.Many2one('uom.uom', string='Outers UOM')

    volume = fields.Float(string='Volume')
    volume_uom_id = fields.Many2one('uom.uom', string='Volume UOM')

    chargeable = fields.Float(string='Chargeable')
    chargeable_uom_id = fields.Many2one('uom.uom', string='Chargeable UOM')
    # weight = fields.Float(string='Weight')
    weight_uom_id = fields.Many2one('uom.uom', string='Outers UOM')

    pic_drop_id = fields.Selection([('any', 'Any'),
                                    ('hsl', 'Haulier Supplies Lift'),
                                    ('hul', 'Hand Upload /Load by Premise'),
                                    ('hwl', 'Hand Upload/ Load by Haulier'),
                                    ('psl', 'Premise Supplier Lift')], string='Pic. Drop')
    div_drop_id = fields.Selection([('any', 'Any'),
                                    ('hsl', 'Haulier Supplies Lift'),
                                    ('hul', 'Hand Upload /Load by Premise'),
                                    ('hwl', 'Hand Upload/ Load by Haulier'),
                                    ('psl', 'Premise Supplier Lift')], string='Dlv. Drop')

    brokerage_type = fields.Selection([('pmt', 'Customers Permit /Clearance Number',),
                                       ('tsn', 'Transhipment Number',),
                                       ('ata', 'ATA Carnet Number',)], string='Div. Drop')

    is_domestic = fields.Boolean(string='Is Domestic')
    is_insurance_required = fields.Boolean(string='Insurance Required')
    est_pickup_date = fields.Date(string="Est. Pickup")
    pickup_required_by_date = fields.Date(string="Required By")
    est_delivery_date = fields.Date(string="Est. Delivery")
    delivery_required_by_date = fields.Date(string="Required By")

    interim_receipt = fields.Char(string="Interim Receipt")
    cfs_cut_off = fields.Char(string="CFS CUt Off")
    cfs_ref = fields.Char(string="CFS Reference")
    cfs_id = fields.Many2one('res.partner', string='CFS')
    pickup_agent_id = fields.Many2one('res.partner', string='Pickup Agent')
    delivery_agent_id = fields.Many2one('res.partner', string='Delivery Agent')
    export_broker_id = fields.Many2one('res.partner', string='Export Broker')
    import_broker_id = fields.Many2one('res.partner', string='Import Broker')
    port_transport_id = fields.Many2one('res.partner', string='Port Transport')

    pickup_address_id = fields.Many2one('res.partner', string='Pickup Address')
    delivery_address_id = fields.Many2one('res.partner', string='Delivery Address')
    client_address_id = fields.Many2one('res.partner', string='Client Address')
    shipper_address_id = fields.Many2one('res.partner', string='Shipper Address')
    consignee_address_id = fields.Many2one('res.partner', string='Consignee Address')

    controlling_customer_id = fields.Many2one('res.partner', string='Controlling Customer')
    controlling_agent_id = fields.Many2one('res.partner', string='Controlling Agent')
    booking_party_id = fields.Many2one('res.partner', string='Booking Party')
    booked_date = fields.Date(string="Booked Date")
    client_req_eat_date = fields.Date(string="Client Req.EAT")
    warehouse_rec_date = fields.Date(string="Warehouse Rec")
    estimated_arrival_date = fields.Date(string="Estimated Arrival date")
    estimated_departure_date = fields.Date(string="Estimated Departure date")
    total_current_weight = fields.Float(string='Total current weight')
    weight_uom_id = fields.Many2one('uom.uom', string='Pk. Type')
    total_current_volume = fields.Float(string='Total current volume')
    volume_uom_id = fields.Many2one('uom.uom', string='Pk. Type')

    container_ids = fields.One2many('freight.container', 'freight_booking_id', string='Container', copy=False)
    loose_cargo_ids = fields.One2many('freight.loose.cargo', 'freight_booking_id', string='Loose Cargo', copy=False)
    job_management_ids = fields.One2many('job.management.link', 'freight_booking_id', string='Job Management Link', copy=False)
    reference_ids = fields.One2many('freight.reference.number', 'freight_booking_id', string='Reference Number', copy=False)
    commodity_ids = fields.One2many('freight.commodity', 'freight_booking_id', string='Commodity Details', copy=False)
    service_details_ids = fields.One2many('freight.service.details', 'freight_booking_id', string='Commodity Details', copy=False)

    def button_request(self):
        return {
            'name': _('Freight Request'),
            'view_mode': 'form',
            'res_model': 'freight.job.request',
            'type': 'ir.actions.act_window',
            'res_id': self.freight_request_id.id,
        }

    def button_add_new_sailings(self):
        return True

    def button_view_sailings(self):
        return True

    def button_clear_sailing(self):
        return True

    def button_lode_list(self):
        return True
