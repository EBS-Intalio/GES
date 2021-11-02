# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class FreightContainer(models.Model):
    _name = 'freight.container'
    _rec_name = "number"

    number = fields.Char(string='Container#', required=True)
    count = fields.Integer(string='Count')
    active = fields.Boolean(default=True, string="Active")
    humidity_percentage = fields.Float(string='Humidity Percentage')
    is_shipper_owned = fields.Boolean(string='Is Shipper Owned?')
    cont_type = fields.Many2one('container.type', string='Container Type')
    commodity = fields.Many2one('freight.commodity', string='Commodity')
    release = fields.Char(string='Release')
    delivery_mode = fields.Selection([('cfs_cfs', 'CFS/CFS'),
                                      ('cy_cy', 'CY/CY'),
                                      ('cy_cfs', 'CY/CFS'),
                                      ('cfs_cy', 'CFS/CY'),
                                      ('dr_cy', 'DR/CY'),
                                      ('cy_dr', 'CY/DR'),
                                      ('fcl_fcl', 'FCL/FCL')], string='Delivery Mode')
    dep_container_id = fields.Many2one('res.partner', string='Dep. Container Yard')
    arr_container_yard_id = fields.Many2one('res.partner', string='Arr. Container Yard')
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')
    seal = fields.Char('Seal')
    sealed_by_1 = fields.Selection([
        ('csl','Carrier shipping Line'),
        ('cs','Cosigner/Shipper'),
        ('ct','Customs'),
        ('qt','Quarantine'),
        ('tm','Terminal'),
    ], string="Sealed By")
    seal_2 = fields.Char('2nd Seal')
    sealed_by_2 = fields.Selection([
        ('csl','Carrier shipping Line'),
        ('cs','Cosigner/Shipper'),
        ('ct','Customs'),
        ('qt','Quarantine'),
        ('tm','Terminal'),
    ], string="Sealed By")
    seal_3 = fields.Char('3rd Seal Num')
    sealed_by_3 = fields.Selection([
        ('csl','Carrier shipping Line'),
        ('cs','Cosigner/Shipper'),
        ('ct','Customs'),
        ('qt','Quarantine'),
        ('tm','Terminal'),
    ], string="Sealed By")
    # weight
    tare_weight = fields.Float('Tare Weight')
    tare = fields.Float('Tare')
    goods_weight = fields.Float('Goods weight')
    dunnage = fields.Float('Dunnage')
    gross_weight = fields.Float('Gross Weight')
    weight_uom = fields.Many2one('uom.uom','Weight UQ')
    max = fields.Float('Max')
    is_seal_ok = fields.Boolean('Is Seal Ok')
    empty_container = fields.Boolean('Empty Contanier')
    is_damage = fields.Boolean('Is Damage')


    quality = fields.Selection([
        ('gen','General'),
        ('ric','Rice'),
        ('hid','Hides'),
        ('ven','Vent General'),
        ('rep','Reposition'),
        ('lbg','Liner Bag'),
        ('sfr','Super Freezer'),
        ('fod','Food'),
    ],string="Quality")
    status = fields.Selection([
        ('avl','Available'),
        ('ins','To Be Inspected'),
        ('wap','Wash'),
        ('app','Approved'),
        ('awa','Awaiting Approved'),
        ('rej','Rejected'),
        ('dam','Damaged'),
        ('dm1','Damaged Minor'),
        ('Ddm2','Damaged Medium'),
        ('dm3','Damaged Major'),
    ],string="Status")

    mode = fields.Selection([
        ('lcl','Less Container Load'),
        ('fcl','Full Container Load'),
        ('frp','Groupage /Freight All Kinds'),
        ('bcn','Buyers Consolidation '),
        ('bbk','Break Bulk'),
        ('ror','Roll on / Roll off'),
    ],string="Mode")
    reference_number_ids = fields.One2many('freight.reference.number', 'freight_container_id', string='Number')

    # Refrigeration
    control_atmosphere= fields.Boolean('Controlled Atmosphere')
    chiller = fields.Boolean('Chiller')
    frozen= fields.Boolean('Frozen')
    temp_set_point = fields.Float('Temp Set Point')
    temp_unit = fields.Selection([
        ('centigrade','Centigrade'),
        ('fahrenheit','Fahrenheit'),
    ],string="Temp unit")
    humidity_percent = fields.Integer('Humidity Percent')
    temp_rec_number = fields.Char('Temp Rec. Number')
    air_vent_setting = fields.Integer('Air Vent Setting')
    air_vent_unit = fields.Selection([
        ('2L','Cubic feet per minute'),
        ('mqh','Cubic Meter per hours'),
        ('p1','percent'),

    ],string="Air Vent Unit")
    clip_on_unit_number = fields.Char('Clip On Unit Number')

    # Measures
    height_on_file = fields.Float('Height On File')
    height_actual = fields.Float('Height  Actual')
    height_overhang = fields.Float('Height Overhang')
    length_on_file = fields.Float('Length On File')
    length_actual = fields.Float('Length  Actual')
    length_overhang = fields.Float('Length Overhang')
    front = fields.Float('Front')
    back = fields.Float('Back')
    width_on_file = fields.Float('Width On File')
    width_actual = fields.Float('Width  Actual')
    width_overhang = fields.Float('Width Overhang')
    left = fields.Float('Left')
    right = fields.Float('Right')
    volume_on_file = fields.Float('Volume On File')
    volume_actual = fields.Float('Volume Actual')
    volume_overhang = fields.Float('Volume Overhang')


    # Import
    import_container_ids = fields.One2many('import.process.line', 'import_container_id')
    cto_available = fields.Char('CTO Available')
    cto_storage_start = fields.Char('CTO Storage Start')
    cfs_available = fields.Char('CFS Available')
    cfs_storage_start = fields.Char('CFS Storage Start')
    fcl_upload = fields.Date('FCL Upload')
    port_transport_booked = fields.Date('Port Transport Booked')
    slot_date = fields.Date('Slot Date')
    wharf_gate_out = fields.Date('Wharf Gate Out')
    estimated_full_delivery = fields.Date('Estimated Full Delivery')
    actual_full_delivery = fields.Date('Actual Full Delivery')
    empty_return_to = fields.Many2one('res.partner')
    empty_return_req_By = fields.Date('Empty Return Req. By')
    empty_ready = fields.Date('Empty Ready')
    port_transport_ref = fields.Char('Port Transport Ref')
    port_or_custom_ref = fields.Char('Port/Custom Ref')
    import_release_no = fields.Char('Import Release Number')
    slot_booking_ref = fields.Char('Slot Booking Ref')
    pickup_by_rail = fields.Boolean('Pickup By Rail')
    held_for_fcl_transit_staging = fields.Boolean('Held For FCL Transit Staging')
    empty_returned_on = fields.Date('Empty Returned On')
    empty_return_reference = fields.Char('Empty Return Reference')

    # Export
    empty_required_by = fields.Date('Empty Required By')
    empty_pickup_from = fields.Many2one('res.partner', string="Empty Pickup From")
    empty_release_number = fields.Char('Empty Release Number')
    export_port_or_cus_ref = fields.Char('Export Port/ Cus. Ref')
    port_transport_reference = fields.Char('Port Transport Ref')
    slot_booking_ref_export = fields.Char('Slot Booking Ref')
    empty_release_from_cy = fields.Date('Empty Release From CY')
    port_transport_advised_booked = fields.Date('Port Transport Advised/ Booked ')
    estimated_full_pickup = fields.Date('Estimated Full Pickup ')
    actual_full_pickup = fields.Date('Actual Full Pickup ')
    departure_slot_date = fields.Date('Departure Slot Date ')
    fcl_wharf_gate_in = fields.Date('FCL Wharf Gate In')
    fcl_loaded = fields.Date('FCL Loaded')
    is_arriving_at_cto_by_rail= fields.Boolean('Is Arriving At CTO By Rail')
    export_process_line_ids = fields.One2many('export.process.line','export_container_id')

    # OUTTURN
    outturn_line_ids = fields.One2many('container.outturn.line','outturn_container_id',string="Outturn Lines")
    volume = fields.Float('Volume')
    weight = fields.Float('Weight')
    mark_and_numbers = fields.Text('Mark & Numbers')
    outturn_comments = fields.Text('Outturn Comments')

    outturn_location_ids = fields.One2many('freight.container.location','outturn_location_id',string="Outturn Location Lines")

    #VGM
    verified_method = fields.Selection([
        ('non','Not verified'),
        ('nrq','Not required'),
        ('cnt','Method 1 - container'),
        ('pkg','Method 2 - packages '),
        ('wta','weight at terminal'),
    ],string="Verified Method")
    verified_date = fields.Date('Verified Date')
    verified_status = fields.Selection([
        ('non', 'Not verified'),
        ('nrq', 'Not required'),
        ('cnt', 'Method 1 - container'),
        ('pkg', 'Method 2 - packages '),
        ('wta', 'weight at terminal'),
    ], string="Verified Status")
    vgm_verified_by = fields.Many2one('res.partner',string="VGM Verified By")
    vgm_verified_address = fields.Many2one('res.partner' ,string="VGM verified Address")


    # Service
    service_line_ids = fields.One2many('freight.container.service','container_service_id',string="Service Lines")

    # Freight Rates
    spot_rate = fields.Float('Spot Rate')
    negotiated_cost = fields.Float('Negotiated Cost')
    gateway_sell = fields.Float('Gateway Sell')
    spot_rate_currency = fields.Many2one('res.currency',string="Spot Rate Currency")
    negotiated_cost_currency = fields.Many2one('res.currency',string="Negotiated Cost Currency")
    gateway_sell_currency = fields.Many2one('res.currency',string="Gateway Sell Currency")
    spot_rate_type = fields.Selection([
        ('usr','use standard rates'),
        ('fpr','freight plush rates'),
        ('air','All in rate')
    ], default='usr', string="Sport Rate Type")
    negotiated_rate_type = fields.Selection([
        ('usr','use standard rates'),
        ('fpr','freight plush rates'),
        ('air','All in rate')
    ], default='usr', string="Negotiated Rate Type")
    gateway_rate_type = fields.Selection([
        ('usr','use standard rates'),
        ('fpr','freight plush rates'),
        ('air','All in rate')
    ], default='usr', string="Gateway Rate Type")

    number_lines_ids = fields.One2many('freight.reference.number','freight_container_id')


