# -*- coding: utf-8 -*-
from docutils.nodes import field

from odoo import api, fields, models, _


class FreightOperation(models.Model):
    _inherit = 'freight.operation'

    transport = fields.Selection([('air', 'Air'),
                                  ('ocean', 'Ocean'),
                                  ('land', 'Road'),
                                  ('sea_then_air', 'Sea then Air'),
                                  ('air_then_sea', 'Air then Sea'),
                                  ('rail', 'Rail'),
                                  ('courier', 'Courier'),
                                  ('documentation', 'Documentation')], default='air', string='Transport')

    ocean_shipment_type = fields.Selection(selection_add=[('breakbulk', 'Breakbulk'),
                                              ('liquid', 'Liquid'),
                                              ('bulk', 'Bulk'),
                                              ('roro', 'Roro')])

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
    # move_type = fields.Many2one('freight.move.type', 'Service Type')
    service_level = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                      ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door'),
                                      ('custom_and_brokerage', 'Customs and Brokerage')],
                                     string="Service Level")

    is_admin = fields.Boolean('Is Admin',compute='check_admin')
    direction = fields.Selection(selection_add=[('cross_state', 'Cross Border State'), ('domestic', 'Domestic')], default='cross_state')
    incotearm_name = fields.Char(related='incoterm.code')
    add_terms = fields.Char(string="Add. Terms")#use this in details
    ata = fields.Date('ATA')
    atd = fields.Date('ATD')
    iss_date = fields.Date('Issue Date')
    exp_date = fields.Date('Expiry Date')
    shipper_address_id = fields.Many2one('res.partner', string='Shipper Address')
    consignee_address_id = fields.Many2one('res.partner', string='Consignee Address')

    equipment_type = fields.Selection(([('20', '20'), ('20_open_top', '20 Open Top'), ('40', '40'),
                                        ('40_hc', '40 HC'), ('40_open_top', '40 OPEN TOP'), ('45', '45'),
                                        ('53', '53'), ('goh_single', 'GOH (Single)'), ('goh_double', 'GOH (Double)'),
                                        ('open_top_gauge', 'Open Top in-gauge'),
                                        ('open_top_out_gauge', 'Open Top out-of-gauge'), ('isotank', 'Isotank'),
                                        ('shipper_own', 'Shipper Owned Container'),
                                        ('mafi_trailer', 'Mafi Trailer'), ('tank', 'Tank'), ('flexibag', 'Flexibag')]),
                                      string="Equipment Type")
    equipment_count = fields.Integer(string='Equipment Count')
    pol = fields.Many2one('freight.pol', string="POL")
    pod = fields.Many2one('freight.pod', string="POD")
    target_rate = fields.Float(string="Quotation Amount")
    weight_type = fields.Selection([('estimated', 'Estimated'), ('actual', 'Actual')], string="Weight Type")
    number_packages = fields.Integer("Number of packages / Pallets")
    stackability = fields.Selection([('stackable', 'Stackable'), ('no_stackable', 'No Stackable')], string="Stackability")
    release_type = fields.Selection([
        ('brr','Letter of Credit (Bank Release)'),
        ('bsd','Sign Draft (Bank Release)'),
        ('btd','Time Draft (Bank Release)'),
        ('csh','Company/Cashier Check'),
        ('cad','Cash Agent Documents'),
        ('ebl','Express Bill Of Landing'),
        ('loi','Letter of Indemnity'),
        ('non','Not Negotiable Unless Consigned to Order'),
        ('obo','Original Bill Surrendered at Origin'),
        ('obr','Original Bill Required at Destination'),
        ('swb','Sea Waybill'),
        ('tlx','Telex Release'),
        ('ob','Original Bill Of landing'),
        ('obd','Original Bill - Surrendered at Destination'),
    ], string='Release Type')
    house_bill_type = fields.Selection([
        ('iau','IT Club Australia'),
        ('iap','IT Club Australia Preprinted'),
        ('inz','IT Club New Zealand'),
        ('inp','IT Club New Zealand Preprinted'),
        ('tnz','IT Club Australia / NZ'),
        ('tnp','IT Club Australia / NZ Preprinted'),
        ('fia','FIATA HBL'),
        ('fip','FIATA HBL Preprinted'),
        ('tan','TAN HBL'),
        ('tap','TAN HBL Preprinted'),
        ('eag','Cargowise Bill'),
        ('dhk','Datahawk Bill'),
        ('tus','TT Club United States'),
        ('tup','TT Club United States Preprinted'),
    ], string='House Bill Type')
    on_board = fields.Selection([
        ('shp','Shipped'),
        ('cln','Clean'),
        ('ldn','Laden'),
        ('rfs','Received for Shipment'),
    ], string='Onboard')
    on_board_date = fields.Date()
    hbl_div_mode = fields.Selection([
        ('cfs_cfs','CFS/CFS'),
        ('cfs_cy','CFS/CY'),
        ('cfs_door','CFS/DOOR'),
        ('cy_cy','CY/CY'),
        ('cy_cfs','CY/CFS'),
        ('cy_door','CY/DOOR'),
        ('door_door','DOOR/DOOR'),
        ('door_cfs','DOOR/CFS'),
        ('door_cy','DOOR/CY'),
    ], string='HBL Div.Mode')
    iss_date_1 = fields.Date('Issue Date')
    org_bill = fields.Integer('Original Bills')
    copy_bill = fields.Integer('Copy Bills')
    charges_apply = fields.Selection([
        ('non','No Charges Showing'),
        ('shw','Show Collect Charges'),
        ('ppd','Show Prepaid Charges'),
        ('agr','Show "AS Agreed" in Charges Section'),
        ('all','Show Prepaid and Collect Charges'),
        ('ccl','Show Original "AS Agreed" and Copy with Collect Charges'),
        ('ccp','Show Original "AS Agreed" and Copy with Prepaid Charges'),
        ('cal','Show Original "AS Agreed" and Copy with Prepaid Charges and Collect Charges'),
    ],string='Charges Apply')
    phase = fields.Selection([('all','Open Security')],string='Phase')
    e_freight_status = fields.Selection([
        ('non','e-Freight Not Supported'),
        ('eap','e-Freight Consignment with Acompanying Paper Documents'),
        ('eaw','e-Freight Consignment with No Acompanying Paper Documents'),
    ],string='e-Freight Status')
    house_bill = fields.Char('House Bill')
    # custom fields
    buy_appr_ship_sched = fields.Date('Buyer Approval Shipment Schedule')
    buy_comm = fields.Char('Buyers Comments')
    frc_approval_ship_sch = fields.Date('FRC Approval Shipment Schedule')
    frc_comm = fields.Char('FRC Comments')
    in_dc_ex = fields.Date('IN DC EXPECTATION')
    own_office = fields.Selection([
        ('abu','Abu Dhabi'),
        ('aoi','Ancona'),
        ('bwi','Baltimore'),
        ('bkt','Bangkok'),
        ('dak','Bangladesh'),
        ('bri','Bari'),
        ('bjs','Beijing'),
        ('bey','Beirut'),
        ('bod','BORDEAUX'),
        ('bos','Boston'),
        ('bou','Boudry'),
        ('clt','Charlotte'),
        ('ckg','Chongqing'),
        ('dlc','Dalian'),
        ('dam','Damman'),
        ('dem','DEMHQ'),
        ('dub','Dubai'),
        ('dkk','Dunkerque'),
        ('gau','Guangzhou'),
        ('hkg','Hong Kong'),
        ('hkw','Hong Kong Warehouse'),
        ('hou','Houston'),
        ('ist','Istanbul'),
        ('jkt','Jakarta'),
        ('w22','JC Controls Warehouse'),
        ('w28','JC Spare Parts Warehouse'),
        ('jae','Jebel Ali'),
        ('jaw','Jebel Ali Warehouse'),
        ('jed','Jeddeh'),
        ('kuw','Kuwait'),
        ('leh','LE HAVRE'),
        ('lel','Le Locle'),
        ('lax','Los Angeles'),
        ('mrs','MARSEILLE'),
        ('mil','Milano'),
        ('mor','MORTEAU FRANCE'),
        ('mos','MORTEAU SUISSE'),
        ('mow','Moscow'),
        ('bom','Mumbai'),
        ('nkg','Nanjing'),
        ('icd','New Delhi'),
        ('nyc','New York'),
        ('ngb','Ningbo'),
        ('pkg','Port Klang'),
        ('tao','Qingdao'),
        ('raw','Rashidiya'),
        ('ryd','Riyadh'),
        ('roi','Roissy'),
        ('rom','Rome'),
        ('san','Santigo'),
        ('sao','Sao Paulo'),
        ('srg','Semarang'),
        ('sha','Shangai'),
        ('she','Shenyang'),
        ('szx','Shenzhen'),
        ('sub','surabaya'),
        ('szh','Suzhou'),
        ('tpe','Taipei'),
        ('tjd','Terminal AL-Khorma'),
        ('tsn','Tianjin'),
        ('tor','Toronto'),
        ('van','Vancouver'),
        ('vce','Venice'),
        ('sgn','Vietnam'),
        ('xmn','Xiamen'),
    ],string='Owner Office')
    contract = fields.Char('Contract#')
    named_acc = fields.Char('Named Account')
    named_acc_ref = fields.Char('Named Account Reference')
    comm_grp_or_bull_ggrp = fields.Char('Commodity Group or Bullet Group')
    cont_ser = fields.Char('Contract Service')
    cont_loc = fields.Char('Contract Location')
    ship_ref = fields.Char('Shipment Ref#')#use this in details
    cust_due_amount = fields.Float('Custom Due Amount')
    z_dest_ship_comm = fields.Char('Z Dest. Shipment Comment')
    # consolidation details
    consol_details_ids = fields.One2many('consol.details','shipment_id')

    #details
    shippers_ref = fields.Char('Shippers Ref')
    is_domestic = fields.Boolean(string='Is Domestic', compute="_compute_is_domestic")
    carrier_id = fields.Many2one('res.partner','Carrier')
    est_pickup_date = fields.Date('Est. Pickup')
    est_delivery_date = fields.Date('Est. Delivery')
    req_pickup_date = fields.Date('Required By')
    req_delivery_date = fields.Date('Required By')
    outers = fields.Float('Outers')
    outer_uom_id = fields.Many2one('uom.uom')
    volume = fields.Float('Volume')
    volume_uom_id = fields.Many2one('uom.uom')
    gross_weight = fields.Float('weight')
    gross_weight_uom_id = fields.Many2one('uom.uom')
    chargebale = fields.Float('Chargeable')
    charge_uom_id = fields.Many2one('uom.uom')
    pic_drop_id = fields.Selection([('any', 'Any'),
                                    ('hsl', 'Haulier Supplies Lift'),
                                    ('hul', 'Hand Upload /Load by Premise'),
                                    ('hwl', 'Hand Upload/ Load by Haulier'),
                                    ('psl', 'Premise Supplier Lift')], string='Goods Pickup')
    div_drop_id = fields.Selection([('any', 'Any'),
                                    ('hsl', 'Haulier Supplies Lift'),
                                    ('hul', 'Hand Upload /Load by Premise'),
                                    ('hwl', 'Hand Upload/ Load by Haulier'),
                                    ('psl', 'Premise Supplier Lift')], string='Goods Delivery')

    cargo_container_visible = fields.Selection([('both', 'Both'), ('cargo', 'Cargo'), ('none', 'None')],
                                               default='none', string='Cargo Container Visible')
    brokerage_type = fields.Selection([('pmt', 'PMT',),
                                       ('tsn', 'TSN',),
                                       ('ata', 'ATA',)], default='pmt', string='Type')
    brokerage_details = fields.Char(string="Details")
    goods_vals = fields.Float(string='Goods Val')
    goods_vals_currency_id = fields.Many2one('res.currency', string='Goods Vals Currency')
    ins_vals = fields.Float(string='Ins Val')
    ins_vals_currency_id = fields.Many2one('res.currency', string='Ins Vals Currency')
    is_insurance_required = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no", string="Insurance Required")
    inspection = fields.Selection([('unk', 'Unknown -No security Measures Taken'),
                                   ('lfc', 'Exempt /Life-saving materials (Save Human Life)'),
                                   ('trn', 'Transfer of Transshipment'),
                                   ('nuc', 'Exempt /Nuclear Material'),
                                   ('dip', 'Exempt /Diplomatic bags or diplomatic mails'),
                                   ('bio', 'Exempt /Biomedical samples'),
                                   ('mai', 'Exempt /Mail'),
                                   ('smu', 'Exempt /Small undersized shipments'),
                                   ('cmd', 'Cargo metal detection'),
                                   ('etd', 'Explosives trace detection equipment - particles or vapor'),
                                   ('edd', 'Explosives detection dogs'),
                                   ('xry', 'X-Ray Equipment'),
                                   ('vck', 'Visual Check'),
                                   ('app', 'Approved /Known Shipper'),
                                   ('phs', 'Physical Inspection and/or hand search'),
                                   ('eds', 'Explosives detection system'),
                                   ('aom', 'subjected to any other means')], string='Inspection')
    loose_cargo_ids = fields.Many2many('freight.loose.cargo', string='Loose Cargo', copy=False)
    container_ids = fields.Many2many('freight.container', string='Container', copy=False)
    vehicle_ids = fields.Many2many('vehicle.details', string="Vehicle Details", copy=False)
    job_management_order_ref = fields.Char(string="Order Refs", required=False)
    job_management_ids = fields.Many2many('job.management.link.line', string='Job Management Lines', copy=False)
    # Additional Details
    load_location_id = fields.Many2one('freight.port', 'Load', index=True)
    discharge_location_id = fields.Many2one('freight.port', 'Discharge', index=True)
    estimated_arrival_date = fields.Date(string="Estimated Arrival date")
    estimated_departure_date = fields.Date(string="Estimated Departure date")
    total_current_weight = fields.Float(string='Total current weight')
    weight_uom_id = fields.Many2one('uom.uom', string='Weight UOM')
    total_current_volume = fields.Float(string='Total current volume')
    volume_add_uom_id = fields.Many2one('uom.uom', string='Volume UOM')#
    cfs_cut_off = fields.Char(string="CFS CUt Off")
    cfs_ref = fields.Char(string="CFS Reference")
    cfs_id = fields.Many2one('res.partner', string='CFS')
    booking_party_id = fields.Many2one('res.partner', string='Booking Party')
    booked_date = fields.Date(string="Booked Date")
    client_req_eat_date = fields.Date(string="Client Req.EAT")
    warehouse_rec_date = fields.Date(string="Warehouse Rec")
    interim_receipt = fields.Char(string="Interim Receipt")
    pickup_agent_id = fields.Many2one('res.partner', string='Pickup Agent')
    delivery_agent_id = fields.Many2one('res.partner', string='Delivery Agent')
    export_broker_id = fields.Many2one('res.partner', string='Export Broker')
    import_broker_id = fields.Many2one('res.partner', string='Import Broker')
    port_transport_id = fields.Many2one('res.partner', string='Port Transport')
    controlling_customer_id = fields.Many2one('res.partner', string='Controlling Customer')
    reference_ids = fields.One2many('freight.reference.number', 'shipment_id', string='Reference Number', copy=False)
    service_details_ids = fields.One2many('freight.service.details', 'freight_booking_id', string='Commodity Details', copy=False)
    routing_ids = fields.One2many('freight.routing','shipment_id')

    # Pick Up Export
    pickup_export_broker_id = fields.Many2one('res.partner', string='Export Broker')
    pickup_shippers_ref = fields.Char('Shippers Ref')
    pickup_transport_id = fields.Many2one('res.partner', string="Pick Up Transport Company")
    transit_warehouse_id = fields.Many2one('res.partner', string="CFS / Transit Warehouse")
    pick_up_agent_id = fields.Many2one('res.partner', string='Pickup Agent')
    pickup_from_id = fields.Many2one('res.partner', string="Pickup From ")
    pickup_interim_receipt = fields.Char(string="Interim Receipt")
    receipt_requested = fields.Date('Receipt Requested')
    dispatch_requested = fields.Date('Dispatch Requested')
    pickup_interim_date_receipt = fields.Date(string="Interim Receipt")
    hbl_booking_status = fields.Selection([('sl', 'Confirmed')], string="HBL Booking status")
    drop_mode = fields.Selection([
        ('any', 'Any'),
        ('lof', 'Drop Container premise Supplies Lift '),
        ('sdl', 'Drop Container With Side Loader '),
        ('trl', 'Drop Trailer'),
        ('wup', 'Wait for Pack / Unpack '),
        ('ask', 'Ask Client')
    ], "Drop Mode")
    pickup_required_from = fields.Date('Pickup Required From ')
    pickup_required_by = fields.Date('Pickup Required By  ')
    estimated_pickup = fields.Date('Estimated Pickup ')
    actual_pickup = fields.Date('Actual Pickup ')
    trn_booking_requested = fields.Date('Trn. Booking Requested')
    pickup_labor_duration = fields.Float('Pickup Labor Duration')
    pickup_labor_charge = fields.Float('Pickup Labor Charge')
    truck_wait_time_duration = fields.Float('Truck Wait Time Duration ')
    truck_wait_time_charge = fields.Float('Truck Wait Time Charge ')
    detention_free = fields.Integer('Detention Free')
    detention_duration = fields.Integer('Detention Duration ')
    detention_charge = fields.Float('Detention Charge')

    # Pick From Shipper
    estimated_date = fields.Date('Estimated')
    requested_by = fields.Date('Requested By')
    picked_up_at = fields.Date('Picked Up At')
    transport_company = fields.Many2one('res.partner', 'Transport Company')
    good_sign_by = fields.Char('Good Sign By ')
    transport_company_name = fields.Char('Transport Company Name')
    driver_name = fields.Char('Driver Name')
    licence = fields.Char('Licence')
    vehicle_reg = fields.Char('Vehicle Registration')
    pc_distance = fields.Float('P/C Distance')
    driving_distance = fields.Float('Driving Distance')
    distance_type = fields.Selection([
        ('km', 'KM'),
        ('mi', 'MI'),
    ], string="Distance Type")
    pickup_from_shipper_addrs = fields.Many2one('res.partner', string="Shipper Address")
    note = fields.Text('Note')
    booking = fields.Many2one('res.partner', string="Booking")
    confirm_drop_mode = fields.Selection([
        ('any', 'Any'),
        ('lof', 'Drop Container premise Supplies Lift '),
        ('sdl', 'Drop Container With Side Loader '),
        ('trl', 'Drop Trailer'),
        ('wup', 'Wait for Pack / Unpack '),
        ('ask', 'Ask Client')
    ], "Drop Mode")
    # Delivery
    #details tab
    delivery_import_broker = fields.Many2one('res.partner','Import Broker')
    delivery_warehouse_id = fields.Many2one('res.partner','CFS/Transit Warehouse')
    delivery_transport_company_id = fields.Many2one('res.partner','Delivery Transport Company')
    delivery_delivery_agent_id = fields.Many2one('res.partner','Delivery Agent')
    deliver_to = fields.Many2one('res.partner','Delivered To')
    deliver_to_address = fields.Many2one('res.partner','Delivered To Address')#
    delivered_receipt_requested = fields.Date('receipt requested')
    delivery_dispatch_requested = fields.Date('dispatch requested')
    delivery_drop_mode = fields.Selection([
        ('any', 'Any'),
        ('lof', 'Drop Container premise Supplies Lift '),
        ('sdl', 'Drop Container With Side Loader '),
        ('trl', 'Drop Trailer'),
        ('wup', 'Wait for Pack / Unpack '),
        ('ask', 'Ask Client')
    ], "Drop Mode")
    delivery_fcl_date = fields.Date('FCL Available Date')
    delivery_required_from = fields.Date('Delivery Required From')
    delivery_required_by = fields.Date('Delivery Required By')
    delivery_booking_requested = fields.Date('Trn. Booing Requested')
    actual_delivery = fields.Date('Actual Delivery')
    delivery_labour_duration = fields.Float('Delivery Labor Duration')
    delivery_labour_charge = fields.Float('Delivery Labor Charge')
    delivery_truck_wait_time_charge = fields.Float('Truck Wait Time Charge')
    delivery_truck_wait_time_duration = fields.Float('Truck Wait Time Duration')
    storage_charge =fields.Float('Storage Charge')
    delivery_detention_charge = fields.Float('Detention Charge')
    delivery_detention_free = fields.Integer('Detention Free')
    delivery_detention_duration = fields.Integer('Detention Duration')
    fcl_storage_date = fields.Date('FCL Storage Date')
    estimated_delivery_date = fields.Date('Estimated Delivery')
    # transport_booking = fields.Many2one()
    # confirmation tab
    estimated_delivery_confirm_date = fields.Date('Estimated')
    delivery_requested_by = fields.Date('Requested By')
    delivery_actual_date = fields.Date('Actual')
    delivery_good_sign_by = fields.Char('Goods Signed By')
    delivery_confirm_dropm_mode = fields.Selection([
        ('any', 'Any'),
        ('lof', 'Drop Container premise Supplies Lift '),
        ('sdl', 'Drop Container With Side Loader '),
        ('trl', 'Drop Trailer'),
        ('wup', 'Wait for Pack / Unpack '),
        ('ask', 'Ask Client')
    ], "Drop Mode")
    delivery_booking_id = fields.Many2one('freight.booking','Booking')
    delivery_notes = fields.Text('Notes')
    delivery_transport_company = fields.Many2one('res.partner','Transport Company')
    delivery_transport_company_name = fields.Char('Transport company Name')
    delivery_driver_name = fields.Char('Drivers Name')
    delivery_license = fields.Char('License')
    delivery_vehicle_reg = fields.Char('Vehicle Registration')
    delivery_pc_distance = fields.Float('P/C Distance')
    delivery_pc_distance_type = fields.Selection([
        ('km','KM'),
        ('mi','MI')
    ], string='Distance Type')
    delivery_distance_driving = fields.Float('Driving Distance')
    delivery_address = fields.Many2one('res.partner','Address')
    delivery_storage_charge = fields.Float(string='Storage Charge')
    delivery_storage_charge_days = fields.Integer(string='Storage Charge Days')
    freight_order_id = fields.Many2one('freight.order', string="Order")
    source_location_id = fields.Many2one('freight.port', 'Source Location', index=True, required=False)
    destination_location_id = fields.Many2one('freight.port', 'Destination Location', index=True, required=False)
    branch_id = fields.Many2one('operating.unit', string="Branch")

    @api.model
    def create(self, values):
        """
        generate sequence
        :param values:
        :return:
        """
        if values.get('name', _('New')) == _('New') and values.get('operation') not in ['master', 'house', 'direct']:
            values['name'] = self.env['ir.sequence'].next_by_code('freight.operation') or _('New')
        res = super(FreightOperation, self).create(values)
        if res.booking_id and res.booking_id.freight_order_id:
            res.booking_id.freight_order_id.shipment_no = res.name
        return res

    def check_admin(self):
        """
        checks whether the user is admin or not
        """
        for rec in self:
            rec.is_admin = False
            if self.env.user.has_group('base.group_erp_manager') or self.env.user.has_group('base.group_system'):
                rec.is_admin = True

    @api.onchange('transport')
    def onchange_freight_booking_transport(self):
        """
        Set shipment type false when transport are change
        Loose Cargo available Air mode

        Set shipment type false when mode of transport are change
        Dimension Option available for LTL, LCL and Air
        :return:
        """

        self.write({'cargo_container_visible': 'none',})

    @api.onchange('rail_shipment_type', 'ocean_shipment_type', 'inland_shipment_type', 'sea_then_air_shipment',
                  'air_then_sea_shipment')
    def onchange_freight_booking_shipment_type(self):
        """
        => For FCL both (container and loose cargo) options available
        => For LCL/FTL/Air only Loose cargo
        => If out of the option select the Invisible both
        :return:
        """
        self.cargo_container_visible = 'none'
        if (not self.sea_then_air_shipment and not self.air_then_sea_shipment
                and not self.ocean_shipment_type
                and not self.rail_shipment_type):
            self.cargo_container_visible = 'none'
        elif (self.ocean_shipment_type and self.ocean_shipment_type == 'fcl') or (
                self.rail_shipment_type and self.rail_shipment_type == 'fcl') or (
                self.air_then_sea_shipment and self.air_then_sea_shipment == 'fcl') or (
                self.sea_then_air_shipment and self.sea_then_air_shipment == 'fcl'):
            self.cargo_container_visible = 'both'
        else:
            self.cargo_container_visible = 'none'


    @api.onchange('gross_weight', 'weight_uom_id')
    def onchange_gross_weight_and_weight_uom(self):
        """
        Set Chargeable Weight and Chargeable UOM according to the gross weight and gross uom
        :return:
        """
        self.write({'charge_uom_id': self.weight_uom_id and self.weight_uom_id.id or False,
                    'chargebale': self.gross_weight})


    def button_add_new_sailings(self):
        """
        Open View for add sailing
        :return:
        """
        return {
            'name': _('Add New Sailing'),
            'view_mode': 'form',
            'res_model': 'freight.sailing',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'active_model': 'freight.operation',
                'active_ids': self.ids,
            },
        }

    def button_clear_sailing(self):
        """
        Clear Sailing Details
        :return:
        """
        self.write({'carrier_id': False, 'voyage_no': False, 'vessel_id': False})
        return True

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

        direction = 'cross_state'
        if self.env.company.country_id:
            if (self.source_location_id and self.destination_location_id and self.source_location_id.country and
                    self.destination_location_id.country and self.source_location_id.country == self.env.company.country_id == self.destination_location_id.country):
                direction = 'domestic'
            elif (
                    self.source_location_id and not self.destination_location_id and self.source_location_id.country == self.env.company.country_id) or (
                    self.source_location_id and self.source_location_id.country and self.source_location_id.country == self.env.company.country_id and
                    (not self.destination_location_id or (
                            self.destination_location_id and self.destination_location_id.country != self.env.company.country_id))):
                direction = 'export'
            elif (
                    self.destination_location_id and not self.source_location_id.country and self.destination_location_id.country == self.env.company.country_id) or (
                    self.destination_location_id and self.destination_location_id.country and self.destination_location_id.country == self.env.company.country_id and
                    (not self.source_location_id or (
                            self.source_location_id and self.source_location_id.country != self.env.company.country_id))):
                direction = 'import'

        self.write({'load_location_id': load_location_id,
                    'discharge_location_id': discharge_location_id,
                    'direction': direction})

    @api.depends('source_location_id', 'destination_location_id')
    def _compute_is_domestic(self):
        """
        Is Domestic field readonly based on country and delivery country
        :return:
        """
        for req in self:
            if not req.source_location_id and not req.destination_location_id:
                is_domestic_readonly = True
            elif (req.source_location_id and req.destination_location_id and (
                    req.destination_location_id.country.id == req.source_location_id.country.id)):
                is_domestic_readonly = True
            else:
                is_domestic_readonly = False
            req.is_domestic = is_domestic_readonly


