# -*- coding: utf-8 -*-
from docutils.nodes import field

from odoo import api, fields, models, _
from datetime import date


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
    # branch_id = fields.Many2one('operating.unit', string="Branch")

    # NEW FIELDS ACCORDING TO FILE
    freight_doc_line_ids = fields.One2many('freight.doc.line', 'shipment_id', string='Doc Line', copy=False)
    allocation_pack_line = fields.One2many('freight.allocated.packlines', 'shipment_id', string="Allocation Packlines")
    hs_country_code = fields.Many2one('res.country', string="Hs Country Code")
    origin = fields.Many2one('res.country', string="Origin")
    goods_description = fields.Text(string="Goods Description")
    ref_number = fields.Char(string="Ref Number")
    address_ids = fields.Many2many('res.partner', string="Addresses")
    freight_amount = fields.Float(string="Freight Amount")
    sending_forwarder = fields.Char(string="Sending Forwarder")
    access_value_declaration = fields.Char(string="Access Value Declaration")
    consider_shipper_phone = fields.Char(string="Consignor – Shipper Phone")
    shipper_load_and_count = fields.Selection([('count', 'Shipper Load And Count'),
                                               ('sealed', 'Shipper Load And Count and Sealed')],
                                              string="Shipper Load And Count")
    date_of_issue = fields.Date(string="Date Of Issue")
    place_of_issue = fields.Char(string="Place Of Issue")
    as_agent_details = fields.Char(string="As Agent Details")
    as_agent_option = fields.Selection([('carrier', 'As Carrier'), ('agent', 'As Agent'),
                                        ('agent_carrier', 'As Agent For Carrier'), ('agent_for', 'As Agent For')],
                                       string="As Agent Option")
    destination = fields.Char(string="Destination")
    freight_payable_at = fields.Char(string="Freight Payable At")
    port_of_discharge = fields.Char(string="Port Of Discharge")
    port_of_loading = fields.Char(string="Port Of Loading")
    port_of_destination_delivery = fields.Char(string="Destination Port – Place Of Delivery")
    port_place_receipt = fields.Char(string="Origin Port – Place Of Receipt")
    delivery_agent_fax = fields.Char(string="Delivery Agent Fax")
    delivery_agent_address = fields.Char(string="Delivery Agent Address")
    notify_party = fields.Char(strin="Notify Party")
    consignee_importer = fields.Char(string="Consignee – Importer")
    consignee_shipper = fields.Char(string="Consignor – Shipper")
    always_show_common_fields = fields.Boolean(string="Always Show Common Fields")
    document_type = fields.Selection([('all', 'All'), ('export_letter', 'Export Letter'),
                                      ('commercial_inv', 'Commercial Invoice'),
                                      ('shipper_letter', 'Shippers Letter Of Instruction'),
                                      ('eur_1', 'EUR. 1'), ('bank_draft', 'Bank Draft'),
                                      ('documentary', 'Documentary Collection Form'),
                                      ('beneficiary', 'Beneficiary Certificate')], string="Document Type")
    master_lead = fields.Many2one('freight.operation', string="Master/ Lead")
    custom_tax_1 = fields.Char(string="Custom Text 1")
    custom_tax_2 = fields.Char(string="Custom Text 2")
    custom_tax_3 = fields.Char(string="Custom Text 3")
    custom_tax_4 = fields.Char(string="Custom Text 4")
    custom_date_1 = fields.Date(string="Custom Date 1")
    custom_date_2 = fields.Date(string="Custom Date 2")
    custom_decimal_1 = fields.Float(string="Custom Decimal 1")
    custom_decimal_2 = fields.Float(string="Custom Decimal 2")
    custom_flag_1 = fields.Boolean(string="Custom Flag 1")
    custom_flag_2 = fields.Boolean(string="Custom Flag 2")
    commodity_id = fields.Many2one('freight.commodity', string='Commodity Code')
    dg_class = fields.Selection([('class_1', 'Class 1'), ('class_1_1a', 'Class 1.1A'), ('class_1_1b', 'Class 1.1B'),
                                 ('class_1_1c', 'Class 1.1C'), ('class_1_1d', 'Class 1.1D'),
                                 ('class_1_1e', 'Class 1.1E'), ('class_1_1f', 'Class 1.1F'),
                                 ('class_1_1g', 'Class 1.1G'), ('class_1_1j', 'Class 1.1J'),
                                 ('class_1_1l', 'Class 1.1L'), ('class_1_2b', 'Class 1.2B'),
                                 ('class_1_2c', 'Class 1.2C'), ('class_1_2d', 'Class 1.2D'),
                                 ('class_1_2e', 'Class 1.2E'), ('class_1_2f', 'Class 1.2F'),
                                 ('class_1_2g', 'Class 1.2G'), ('class_1_2h', 'Class 1.2H'),
                                 ('class_1_2j', 'Class 1.2J'), ('class_1_2k', 'Class 1.2K'),
                                 ('class_1_2l', 'Class 1.2L'), ('class_1_3c', 'Class 1.3C'),
                                 ('class_1_3g', 'Class 1.3G'), ('class_1_3h', 'Class 1.3H'),
                                 ('class_1_3j', 'Class 1.3J'), ('class_1_3k', 'Class 1.3K'),
                                 ('class_1_3l', 'Class 1.3L'), ('class_1_4b', 'Class 1.4B'),
                                 ('class_1_4c', 'Class 1.4C'), ('class_1_4d', 'Class 1.4D'),
                                 ('class_1_4e', 'Class 1.4E'), ('class_1_4f', 'Class 1.4F'),
                                 ('class_1_4g', 'Class 1.4G'), ('class_1_4s', 'Class 1.4S'),
                                 ('class_1_5d', 'Class 1.5D'), ('class_1_6n', 'Class 1.6N'),
                                 ('class_2', 'Class 2'), ('class_2_1', 'Class 2.1'), ('class_2_2', 'Class 2.2'),
                                 ('class_2_3', 'Class 2.3'), ('class_3', 'Class 3'), ('class_4', 'Class 4'),
                                 ('class_4_1', 'Class 4.1'), ('class_4_2', 'Class 4.2'), ('class_4_3', 'Class 4.3'),
                                 ('class_5_1', 'Class 5.1'), ('class_5_2', 'Class 5.2'), ('class_6', 'Class 6'),
                                 ('class_6_1', 'Class 6.1'), ('class_6_2', 'Class 6.2'), ('class_7', 'Class 7'),
                                 ('class_8', 'Class 8'), ('class_9', 'Class 9'),
                                 ('combustible_liquid', 'Combustible Liquid')], string="DG Class")
    flash_point = fields.Float(string="Flash Point")
    undg_contact = fields.Many2one('res.partner', string="UNDG Contact")
    is_temp_controlled = fields.Boolean(string="Is Temperature Controlled")
    min_temp = fields.Float(string="Min. Temp.")
    min_temp_type = fields.Selection([('cel', 'Celsius'), ('fahrenheit', 'Fahrenheit')], string="Min. Temp. Type")
    max_temp = fields.Float(string="Max. Temp.")
    max_temp_type = fields.Selection([('cel', 'Celsius'), ('fahrenheit', 'Fahrenheit')], string="Max. Temp. Type")
    outer_package_total = fields.Float(string="Outer Packages")
    outer_package_weight = fields.Float(string="Weight")
    outer_package_weight_uom = fields.Many2one('uom.uom', string="Outer Package Weight UOM")
    outer_package_volume = fields.Float(string="Volume")
    outer_package_volume_uom = fields.Many2one('uom.uom', string="Outer Package Volume UOM")
    shipment_total_package = fields.Float(string="Outer Packages")
    shipment_weight = fields.Float(string="Weight")
    shipment_weight_uom = fields.Many2one('uom.uom', string="Shipment Weight UOM")
    shipment_volume_uom = fields.Many2one('uom.uom', string="Shipment Volume UOM")
    shipment_volume = fields.Float(string="Volume")
    packs = fields.Integer(string="Packs")
    packs_type = fields.Selection([('bag', 'bag'), ('bulk_bag', 'Bulk Bag'), ('break_bulk', 'Break Bulk'),
                                   ('bale', 'Bale'), ('compressed', 'compressed'), ('bale', 'Bale'),
                                   ('uncompressed', 'Uncompressed'), ('bundle', 'Bundle'), ('bottle', 'Bottle'),
                                   ('box', 'Box'), ('basket', 'Basket'), ('case', 'Case'), ('col', 'Col'),
                                   ('creade', 'Creade'), ('crate', 'Crate'), ('carton', 'Carton'),
                                   ('cylnder', 'Cylnder'), ('dozen', 'Dozen'), ('drum', 'Drum'),
                                   ('envelope', 'Envelope'), ('gross', 'Gross'), ('keg', 'KEG'), ('mix', 'Mix'),
                                   ('pal', 'Pal'), ('piece', 'Piece'), ('package', 'Package'), ('pallet', 'Pallet'),
                                   ('panel', 'Panel'), ('rails', 'Rails'), ('reel', 'Reel'), ('rol', 'Rol'),
                                   ('sheet', 'Sheet'), ('skid', 'Skid'), ('spool', 'Spool'), ('tote', 'Tote'),
                                   ('tube', 'Tube'), ('unit', 'Unit')], string="Packs Type")
    weight = fields.Float(string="Weight")
    weight_uom = fields.Many2one('uom.uom', string="Weight UOM")
    packing_volume_uom = fields.Many2one('uom.uom', string="Volume UOM")
    packing_volume = fields.Float(string="Volume")
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    height = fields.Float(string="Height")
    height_uom = fields.Many2one('uom.uom', string="Height UOM")
    packing_transit_warehouse_id = fields.Many2one('res.partner', string="Transit Warehouse")
    status = fields.Selection([('received', 'Received'),
                               ('dispatched', 'Dispatched')], string="Status")
    date = fields.Date(string="Date")
    outturn = fields.Integer(string="Outturn")
    damaged = fields.Integer(string="Damaged")
    pillaged = fields.Integer(string="Pillaged")

    outturned_weight = fields.Float(string="Weight")
    outturned_uom = fields.Many2one('uom.uom', string="Weight UOM")
    outturned_volume_uom = fields.Many2one('uom.uom', string="Volume UOM")
    outturned_volume = fields.Float(string="Outturned Volume")
    outturned_length = fields.Float(string="Length")
    outturned_width = fields.Float(string="Outturn Width")
    outturned_height = fields.Float(string="Height")
    outturned_height_uom = fields.Many2one('uom.uom', string="Volume UOM")
    outturned_comments = fields.Text(string="Outturn Comments")
    marks_and_number = fields.Text(string="Marks & Nums.")

    shipmen_defined_lines = fields.One2many('freight.doc.line', 'shipment_id', string="System Defined Lines")
    entry_details = fields.Selection([('pmt', 'Customs Permit/Clearance Number'),
                                      ('tsn', 'Transhipment Number'),
                                      ('ata', 'ATA Carnet Number')],
                                      string="Entry Details")
    screening_status = fields.Selection([('yes', 'YES'), ('no', 'NO')], string="Screening Status")
    description = fields.Text(string="Description")


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
        if self._context and self._context.get('from_booking'):
            branch = ''
            if res.operating_unit_id:
                branch = res.operating_unit_id.code
            mode = ''
            if res.transport:
                if res.transport == 'land':
                    mode = 'R'
                else:
                    mode = res.transport[0].upper()
            direction = res.direction[0].upper() if res.direction else ''
            res.name = branch + '-' + date.today().strftime('%y') + mode + direction + self.env[
                'ir.sequence'].next_by_code('freight.operation.quotation') or _('New')
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
        # load_location_id = False
        # discharge_location_id = False
        if self.source_location_id:
            self.load_location_id = self.source_location_id and self.source_location_id.id
        if self.destination_location_id:
            self.discharge_location_id = self.destination_location_id and self.destination_location_id.id

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

        self.direction = direction


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


