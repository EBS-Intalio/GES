# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightBooking(models.Model):
    _inherit = 'freight.booking'

    freight_request_id = fields.Many2one('freight.job.request','RequestID')
    hs_code = fields.Many2many('freight.hs.code', string="Hs-Codes")

    transport = fields.Selection([('air', 'Air'),
                                   ('ocean', 'Ocean'),
                                   ('land', 'Land'),
                                   ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'),
                                   ('rail', 'Rail'),
                                   ('courier', 'Courier')], string='Transport', required=False)

    ocean_shipment_type = fields.Selection(selection_add=[('breakbulk', 'Breakbulk'),
                                              ('liquid', 'Liquid'),
                                              ('bulk', 'Bulk'),
                                              ('roro', 'Roro')])

    # ADDED Field for booking cargo
    marks_and_num = fields.Char(string='Marks & Nums')
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
    # client_address_id = fields.Many2one('res.partner', string='Client Address')
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
    container_ids = fields.Many2many('freight.package', string='Container', copy=False)
    loose_cargo_ids = fields.Many2many('freight.loose.cargo', string='Loose Cargo', copy=False)
    job_management_ids = fields.One2many('job.management.link', 'freight_booking_id', string='Job Management Link', copy=False)
    reference_ids = fields.One2many('freight.reference.number', 'freight_booking_id', string='Reference Number', copy=False)
    service_details_ids = fields.One2many('freight.service.details', 'freight_booking_id', string='Commodity Details', copy=False)
    rail_shipment_type = fields.Selection([('fcl', 'FCL'), ('lcl', 'LCL'),
                                           ('breakbulk', 'Breakbulk'),
                                           ('liquid', 'Liquid'),
                                           ('bulk', 'Bulk'),
                                           ('roro', 'Roro')], string='Rail Shipment Type')

    sea_then_air_shipment = fields.Selection([('fcl', 'FCL'), ('lcl', 'LCL'),
                                              ('breakbulk', 'Breakbulk'),
                                              ('liquid', 'Liquid'),
                                              ('bulk', 'Bulk'),
                                              ('roro', 'Roro')], string='Sea then Air Shipment Type')

    air_then_sea_shipment = fields.Selection([('fcl', 'FCL'), ('lcl', 'LCL'),
                                              ('breakbulk', 'Breakbulk'),
                                              ('liquid', 'Liquid'),
                                              ('bulk', 'Bulk'),
                                              ('roro', 'Roro')], string='Air then Sea Shipment Type')
    dimensions_of_package_id = fields.Many2one('freight.package',
                                               string="Dimensions of each package /Pallets dimensions")

    bl_copy = fields.Boolean("BL Copy Available ?")
    shipping_documents = fields.Boolean("Shipping Documents")
    original_copy = fields.Selection(([('original', 'Original'), ('copy', 'Copy')]), string='Original/Copy')

    load_location_id = fields.Many2one('freight.port', 'Load', index=True)
    discharge_location_id = fields.Many2one('freight.port', 'Discharge', index=True)
    # hs_code = fields.Many2many('freight.hs.code', string="Hs-Codes")

    @api.onchange('consignee_id')
    def onchange_consignee_id(self):
        for rec in self:
            rec.write({'consignee_address_id': False})

    @api.onchange('shipper_id')
    def onchange_shipper_id(self):
        for rec in self:
            rec.write({'shipper_address_id': False})

    @api.onchange('shipper_address_id', 'consignee_address_id')
    def set_loading_delivery_address(self):
        for rec in self:
            shipper_address_id = rec.shipper_address_id
            consignee_address_id = rec.consignee_address_id
            rec.write({'area': False, 'street': False, 'city': False, 'zip_code': False, 'building': False, 'po_box': False, 'state_id': False, 'country_id': False,
                       'delivery_area': False, 'delivery_street': False, 'delivery_city': False, 'delivery_building': False,
                       'delivery_po_box': False, 'delivery_zip_code': False, 'delivery_state_id': False, 'delivery_country_id': False})
            if shipper_address_id:
                rec.area = shipper_address_id.street
                rec.street = shipper_address_id.street2
                rec.city = shipper_address_id.city
                rec.zip_code = shipper_address_id.zip
                rec.building = shipper_address_id.building
                rec.po_box = shipper_address_id.po_box
                rec.state_id = shipper_address_id.state_id and shipper_address_id.state_id.id
                rec.country_id = shipper_address_id.country_id and shipper_address_id.country_id.id
            if consignee_address_id:
                rec.delivery_area = consignee_address_id.street
                rec.delivery_street = consignee_address_id.street2
                rec.delivery_city = consignee_address_id.city
                rec.delivery_building = consignee_address_id.building
                rec.delivery_po_box = consignee_address_id.po_box
                rec.delivery_zip_code = consignee_address_id.zip
                rec.delivery_state_id = consignee_address_id.state_id and consignee_address_id.state_id.id
                rec.delivery_country_id = consignee_address_id.country_id and consignee_address_id.country_id.id

    @api.onchange('destination_location_id', 'source_location_id')
    def onchange_origin_destination(self):
        """
        Set Load and discharge according to the origin and destination
        :return:
        """
        load_location_id = False
        discharge_location_id = False
        if self.source_location_id:
            load_location_id = self.source_location_id.id
        if self.destination_location_id:
            discharge_location_id = self.destination_location_id.id
        self.write({'load_location_id': load_location_id,
                    'discharge_location_id': discharge_location_id})

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
