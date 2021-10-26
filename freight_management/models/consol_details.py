# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class ConsolDerails(models.Model):
    _name = 'consol.details'

    shipment_id = fields.Many2one('freight.operation')
    # consol details
    type = fields.Selection([
        ('drt','Direct'),
        ('cld','Co-Load'),
        ('agt','Agent'),
        ('cht','Charter'),
        ('cou','Courier'),
        ('oth','Other'),
    ], string='Type')
    transport = fields.Selection([
        ('air', 'Air'),
        ('ocean', 'Ocean'),
        ('land', 'Road'),
        ('sea_then_air', 'Sea then Air'),
        ('air_then_sea', 'Air then Sea'),
        ('rail', 'Rail'),
        ('courier', 'Courier'),
        ('documentation', 'Documentation')], string='Transport')
    cont_mode = fields.Selection([
        ('fcl','Full Container Load'),
        ('lcl','Less Container Load'),
        ('blk','Bulk'),
        ('lqd','Liquid'),
        ('bbk','Break Bulb'),
        ('bcn','Buyers Consolidation'),
        ('ror','Roll On / Roll Off'),
        ('oth','Other'),
    ],string='Container Mode')
    phase = fields.Selection([
        ('all','Open Security'),
        ('dst','Destination'),
        ('vld','Validated')
    ], string='Phase')
    is_domestic = fields.Boolean('Domestic')
    fst_load = fields.Many2one('unloco.data',string='1st Load')
    last_disc = fields.Many2one('unloco.data',string='Last Disc')
    # voyage
    voyage = fields.Char('Voyage')
    vessel = fields.Many2one('freight.vessel','Vessel')
    load_port = fields.Many2one('unloco.data','Load Port')
    disc_port = fields.Many2one('unloco.data','Discharge')
    etd = fields.Datetime('ETD')
    eta = fields.Datetime('ETA')
    ata = fields.Datetime('ATA')
    atd = fields.Datetime('ATD')
    is_domestic_voyage = fields.Boolean('Is Domestic')
    is_linked = fields.Boolean('Is Linked')
    is_charter = fields.Boolean('Is Charter')
    # bol
    bol = fields.Char('Bol')
    payment = fields.Selection([
        ('ppd','Prepaid'),
        ('ccx','Collect')
    ], string='Payment')
    serv_level = fields.Selection([
        ('std','Standard')
    ], string='Service Level')
    crn = fields.Char('CRN:')
    # new
    freight_order_id = fields.Many2one('freight.order', string="Order")
    shipment_ids = fields.Many2many('freight.operation', string="Shipment ids")
    show = fields.Boolean('Show')
    ship_count = fields.Integer('Ship count')
    packs = fields.Integer('Packs')
    weight = fields.Float('Weight')
    weight_uom = fields.Many2one('uom.uom', string="Weight uom")
    volume = fields.Float('Volume')
    volume_uom_id = fields.Many2one('uom.uom', string='Volume uom')
    chargeable = fields.Float('Chargeable')
    chargeable_uom = fields.Many2one('uom.uom', string="Chargeable uom")
    prepaid = fields.Float('Prepaid')
    prepaid_curr = fields.Many2one('res.currency', string="Prepaid uom")
    collect = fields.Float('Collect')
    collect_curr = fields.Many2one('res.currency', string="Collect uom")

    sending_agent_id = fields.Many2one('res.partner', string="Sending agent")
    sending_agent_address_id = fields.Many2one('res.partner', string="Sending agent address")
    receiving_agent_id = fields.Many2one('res.partner', string="Receiving agent")
    receiving_agent_address_id = fields.Many2one('res.partner', string="Receiving agent address")
    carrier = fields.Many2one('res.partner', string="Carrier")
    creditor = fields.Many2one('res.partner', string="Creditor")
    carrier_bkg_ref = fields.Char('Carrier bkg ref')
    agent_reference = fields.Char('Agent reference')

    cto_address = fields.Many2one('res.partner', string="CTO Address")
    cfs_address = fields.Many2one('res.partner', string="CFS Address")
    receipt_requested = fields.Date(string="Receipt Requested")
    dispatch_requested = fields.Date(string="Dispatch Requested")
    container_yard_id = fields.Many2one('res.partner', string="Container yard ")
    port_transport_id = fields.Many2one('freight.port', string="Port Transport")
    first_foreign_port_id = fields.Many2one('freight.port', string="First Foreign Port")
    last_foreign_port_id = fields.Many2one('freight.port', string="Last Foreign Port")
    first_arrival_port_arrival_date = fields.Date('First Arrival Port Arrival Date')
    departure_date = fields.Date('Departure Date')

    cto_address_arrival = fields.Many2one('res.partner', string="CTO Address")
    cfs_address_arrival = fields.Many2one('res.partner', string="CFS Address")
    receipt_requested_arrival = fields.Date(string="Receipt Requested")
    dispatch_requested_arrival = fields.Date(string="Dispatch Requested")
    container_yard_arrival_id = fields.Many2one('res.partner', string="Container yard")
    port_transport_arrival_id = fields.Many2one('freight.port', string="Port Transport")
    first_foreign_port_arrival_id = fields.Many2one('freight.port', string="First Arrival Port")
    last_foreign_port_arrival_id = fields.Many2one('freight.port', string="Last Foreign Port")
    first_arrival_port_arrival_date_arrival = fields.Date('First Arrival Port Arrival Date')
    departure_date_arrival = fields.Date('Departure Date')

    manifest_Print = fields.Selection([
        ('sub_house_bill', 'Sub house bill'),
        ('print_masters_only', 'Print Masters Only'),
        ('print_sub_house_bill_only', 'Print sub house bill only')])
    awb_dimensions = fields.Selection([
        ('DEF','Default '),
        ('M3','Volume Only'),
        ('ALL','Both Dimension and volume if available'),
        ('PKS','Dimension of outer packs only'),
        ('NDA','No Dimension available')],string="AWB Dimensions")
    release_type = fields.Selection([
        ('BRR','Latter of credit '),
        ('BSD','Sight Draft'),
        ('BTD','Time Draft'),
        ('CSH','Company / Cashier Check'),
        ('CAD','Cash Against Document'),
        ('EBL','Express Bill of Lading'),
        ('LOI','Latter of Indemnity'),
        ('NON','Not Negotiable unless consigned to order '),
        ('OBO','Original Bill - Surrendered at Origin'),
        ('OBR','Original Bill Required at destination'),
        ('SWB','Sea way Bill'),
        ('TLX','Telex Release'),
        ('OB','Original Bill of Landing'),
        ('OBD','Original Bill Surrendered at destination'),
    ],string="Release Type")
    place_of_issue = fields.Many2one('unloco.data',string="Place Of Issue")
    original_bills = fields.Integer('Original bills')
    copy_bills = fields.Integer('Copy bills')
    print_option_for_other_doc = fields.Selection([
        ('sub_house_bill', 'Sub house bill'),
        ('print_masters_only', 'Print Masters Only'),
        ('print_sub_house_bill_only', 'Print sub house bill only')])
    master_bill_issue_date = fields.Date('master bill issue date')
    shipment = fields.Integer('Shipment')
    weight_pre = fields.Float('Weight pre')
    weight_uom_pre_id = fields.Many2one('uom.uom', string="Weight uom pre")
    volume_pre = fields.Float('Volume pre')
    volume_uom_pre_id = fields.Many2one('uom.uom', string='Volume uom pre ')
    max_dims = fields.Float('Max dimension')
    max_dims1 = fields.Float('Max dimension 1')
    max_dims2 = fields.Float('Max dimension 2')
    max_dims_uom = fields.Many2one('uom.uom', 'Max dimension uom')
    chargeable_pre = fields.Float('Chargeable Pre')
    cut_off_date = fields.Date('Cut Off Date')
    is_hazardous = fields.Boolean('Is Hazardous')
    is_temperature_controlled = fields.Boolean('Is Temperature Controlled')
    min_temp = fields.Float('Min Temp')
    max_temp = fields.Float('Max Temp')
    min_temp_in = fields.Selection([
        ('celsius', 'Celsius'),
        ('fahrenheit', 'Fahrenheit')], string="Min temperature")
    max_temp_in = fields.Selection([
        ('celsius', 'Celsius'),
        ('fahrenheit', 'Fahrenheit')], string="Max temperature")
    quantities_override = fields.Boolean('Quantities Override')
    weight_vol = fields.Float('Weight Volume')
    weight_vol_uom_id = fields.Many2one('uom.uom', 'Weight Volume')
    consolidated_weight = fields.Float('Consolidated Weight')
    consolidated_volume = fields.Float('Consolidated Volume')
    cons_charge_qty = fields.Float('Cons Charge Qty')
    cons_charge_qty_uom_id = fields.Many2one('uom.uom', 'Cons Charge Qty Uom')
    consolidated_volume_uom_id = fields.Many2one('uom.uom', 'Consolidated volume Uom')
    consolidated_weight_uom_id = fields.Many2one('uom.uom', 'Consolidated weight Uom')
    excess_wgt_vol = fields.Float('Excess weight volume')
    excess_wgt_vol_uom_id = fields.Many2one('uom.uom', 'Excess weight volume')
    frt_cost_mb_charge = fields.Float('FRT Cost MB Charge')
    frt_cost_mb_charge_currency_id = fields.Many2one('res.currency', 'FRT Cost MB Charge')
    frt_cost_hb_charge = fields.Float('FRT Cost HB Charge')
    frt_cost_hb_charge_currency_id = fields.Many2one('res.currency', 'FRT Cost HB Charge')

    weight_utilization = fields.Float('Weight Utilization')
    volume_utilization = fields.Float('Volume Utilization')
    cost_free = fields.Float('Cost Free')
    cost_free_unit = fields.Float('Cost Free unit')
    cost_free_units_uom_id = fields.Many2one('uom.uom', 'Cost Free Units uom')
    density_factor = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12')], string="Density Factor")
    reference_number_ids = fields.One2many('freight.reference.number', 'freight_console_id', string="Reference number")
    Dest_cntr_comments = fields.Char('Density CNTR Comments')
    chassis_provider = fields.Char('Chassis Provider')
    atd_update = fields.Char('ATD Update')
    #routing tab
    defined_by = fields.Char('Defined By')
    # status = fields.Selection([()], string="Status")
    notes_rout = fields.Text('Notes')
    leg_order = fields.Float('Leg order')
    depart = fields.Many2one('res.country','Dep. From')
    arrival = fields.Many2one('res.country','Arrival At')
    cto_received_date = fields.Date('CTO received')
    cfs_received_date = fields.Date('CFS received')
    cto_available_date = fields.Date('CTO Available')
    cfs_available_date = fields.Date('CFS Available')
    cto_cutt_off_date = fields.Date('CTO Cutt Off')
    cfs_cutt_off_date = fields.Date('CFS Cutt Off')
    cto_storage_date = fields.Date('CTO Storage')
    cfs_storage_date = fields.Date('CFS Storage')
    docs_due_date = fields.Date('Docs Due')
    vgm_cutt_off_date = fields.Date('VGM Cutt Off')
    container_ids = fields.Many2many('freight.container', string='Container', copy=False)

    @api.onchange('bol')
    def get_old_data(self):
        for rec in self:
            if rec.bol:
                old_rec = self.search([('bol','=',rec.bol)],order='id asc',limit=1)
                if old_rec:
                    rec.serv_level = old_rec.serv_level
                    rec.payment = old_rec.payment
                    rec.crn = old_rec.crn
                    rec.serv_level = old_rec.serv_level
                    rec.is_domestic = old_rec.is_domestic
                    rec.transport = old_rec.transport
                    rec.cont_mode = old_rec.cont_mode
                    rec.fst_load = old_rec.fst_load and old_rec.fst_load.id
                    rec.last_disc = old_rec.last_disc and old_rec.last_disc.id
                    rec.last_disc = old_rec.last_disc and old_rec.last_disc.id
                    rec.phase = old_rec.phase
                    rec.voyage = old_rec.voyage
                    rec.vessel = old_rec.vessel and old_rec.vessel.id
                    rec.load_port = old_rec.load_port and old_rec.load_port.id
                    rec.disc_port = old_rec.disc_port and old_rec.disc_port.id
                    rec.etd = old_rec.etd
                    rec.atd = old_rec.atd
                    rec.eta = old_rec.eta
                    rec.ata = old_rec.ata
                    rec.is_domestic_voyage = old_rec.is_domestic_voyage
                    rec.is_linked = old_rec.is_linked
                    rec.is_charter = old_rec.is_charter


