# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class FreightBooking(models.Model):
    _inherit = 'freight.booking'

    @api.depends('invoice_ids')
    def _compute_freight_customer_invoice(self):
        """
        Count total booking Customer Invoice
        :return:
        """
        for booking in self:
            booking.invoice_count = len(booking.invoice_ids)


    freight_request_id = fields.Many2one('freight.job.request','RequestID')
    hs_code = fields.Many2many('freight.hs.code', string="Hs-Codes")

    transport = fields.Selection([('air', 'Air'),
                                   ('ocean', 'Ocean'),
                                   ('land', 'Road'),
                                   ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'),
                                   ('rail', 'Rail'),
                                   ('courier', 'Courier'),
                                   ('documentation', 'Documentation')], string='Transport', default='air', required=False)

    ocean_shipment_type = fields.Selection(selection_add=[('breakbulk', 'Breakbulk'),
                                              ('liquid', 'Liquid'),
                                              ('bulk', 'Bulk'),
                                              ('roro', 'Roro')])

    # ADDED Field for booking cargo
    marks_and_num = fields.Char(string='Marks & Nums')
    add_terms = fields.Char(string="Add. Terms")
    service_level = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                      ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door'),
                                      ('custom_and_brokerage', 'Customs and Brokerage')],
                                     string="Service Level")
    shippers_ref = fields.Char(string="Shipper's Ref")
    carrier_id = fields.Many2one('res.partner', string='Carrier')
    goods_vals = fields.Float(string='Goods Val')
    booking_gross_weight = fields.Float(string='Weight')
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
                                    ('psl', 'Premise Supplier Lift')], string='Goods Pickup')
    div_drop_id = fields.Selection([('any', 'Any'),
                                    ('hsl', 'Haulier Supplies Lift'),
                                    ('hul', 'Hand Upload /Load by Premise'),
                                    ('hwl', 'Hand Upload/ Load by Haulier'),
                                    ('psl', 'Premise Supplier Lift')], string='Goods Delivery')

    brokerage_type = fields.Selection([('pmt', 'PMT',),
                                       ('tsn', 'TSN',),
                                       ('ata', 'ATA',)], default='pmt', string='Type')
    brokerage_details = fields.Char(string="Details")

    is_domestic = fields.Boolean(string='Is Domestic', compute="_compute_is_domestic")
    is_insurance_required = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no", string="Insurance Required")
    # is_insurance_required = fields.Boolean(string='Insurance Required')
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
    weight_uom_id = fields.Many2one('uom.uom', string='Weight UOM')
    total_current_volume = fields.Float(string='Total current volume')
    volume_uom_id = fields.Many2one('uom.uom', string='Volume UOM')
    container_ids = fields.Many2many('freight.container', string='Container', copy=False)
    loose_cargo_ids = fields.Many2many('freight.loose.cargo', string='Loose Cargo', copy=False)
    job_management_order_ref = fields.Char(string="Order Refs", required=False)
    job_management_ids = fields.Many2many('job.management.link.line', string='Job Management Lines', copy=False)
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
                                               string="Dimensions of each package /Pallets")

    bl_copy = fields.Boolean("BL Copy Available ?")
    shipping_documents = fields.Boolean("Shipping Documents")
    original_copy = fields.Selection([('original', 'Original'), ('copy', 'Copy')], string='Original/Copy')

    load_location_id = fields.Many2one('freight.port', 'Load', index=True)
    discharge_location_id = fields.Many2one('freight.port', 'Discharge', index=True)
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

    hs_code = fields.Many2many('freight.hs.code', string="Hs-Codes")
    cargo_container_visible = fields.Selection([('both', 'Both'), ('cargo', 'Cargo'), ('none', 'None')],
                                               default='none', string='Cargo Container Visible')
    package_type_id = fields.Selection([('palatized', 'Palatized'),
                                     ('cartons', 'Cartons'),
                                     ('bulk', 'Bulk'),
                                     ('drums', 'Drums'),
                                     ('other', 'Others')], string="Packaging Type")
    pol = fields.Many2one('freight.pol', string="POL")
    pod = fields.Many2one('freight.pod', string="POD")
    preferred_shipping_line = fields.Many2one('res.partner', 'Preferred Shipping Line')
    invoice_count = fields.Integer(string='Total Customer Invoice', compute='_compute_freight_customer_invoice')
    invoice_ids = fields.One2many('account.move', 'freight_booking_id', string='Customer Invoice', copy=False)
    vehicle_ids = fields.Many2many('vehicle.details', string="Vehicle Details", copy=False)

    is_dimensions_visible = fields.Boolean(string="Is Dimensions Available?", default=False)

    shipment_ready_date = fields.Date(string="Shipment Ready Date")

    shipment_ready_asap = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="yes",
                                           string="Shipment Ready ASAP", required=True)
    target_eta_asap = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="yes",
                                       string="Target ETA ASAP", required=True)
    target_etd_asap = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="yes",
                                       string="Target ETD ASAP", required=True)

    direction = fields.Selection(selection_add=[('cross_state', 'Cross Border State'), ('domestic', 'Domestic')], default='cross_state')
    incotearm_name = fields.Char(related='incoterm.code')
    equipment_count = fields.Integer(string='Equipment Count')
    is_review_booking = fields.Boolean('Review Booking')

    freight_order_id = fields.Many2one('freight.order', string='Order')

    # Override fields for require false
    agent_id = fields.Many2one('res.partner', 'Customer', required=False)
    commodity_description = fields.Text("Commodity Description", required=False)
    reefer_status = fields.Selection(([('yes', 'YES'), ('no', 'NO'), ('non_operate', 'Non Operating Reefer')]),
                                     string="Reefer Status", required=False)
    commodity_category = fields.Selection(([('food_perishable', 'Food Perishable'), ('nonfood_perishable', 'Non food perishable'), ('non_perishable', 'Non perishable F&B'),
                                            ('furniture', 'Furniture'), ('building_material', 'Building Material'), ('automotive', 'Automotive'),
                                            ('pharmaceuticals', 'Pharmaceuticals'), ('petroleum_products', 'Petroleum Products'), ('other_chemicals', 'Other Chemicals')]), string="Commodity Category",required=False)
    weight_type = fields.Selection(([('estimated', 'Estimated'), ('actual', 'Actual')]), string="Weight Type", required=False,default='estimated')
    clearance_required = fields.Selection(([('yes', 'YES'), ('no', 'NO')]), string="Clearance Required", required=False, default='no')
    warehousing = fields.Selection(([('yes', 'YES'), ('no', 'NO')]), string="Warehousing / Storage", required=False,default='no')

    def action_create_new_invoice(self):
        """
        Create a new Customer Invoice
        :return:
        """
        ctx = self._context.copy()
        ctx['default_freight_booking_id'] = self.id
        ctx['default_partner_id'] = self.agent_id and self.agent_id.id or False
        ctx['default_move_type'] = 'out_invoice'
        return {
            'name': _('Create invoice'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'context': ctx,
        }

    def action_view_customer_invoice(self):
        """
        Prepare a action for the display the Customer Invoice
        :return:
        """
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        invoice = self.invoice_ids
        if len(invoice) > 1:
            action['domain'] = [('id', 'in', invoice.ids)]
        elif invoice:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoice.id

        return action

    def convert_to_operation(self):
        name_act = ''
        warn_list = []
        if self.transport in ['ocean','land','sea_then_air','air_then_sea','rail']:
            if not self.ocean_shipment_type and not self.inland_shipment_type and not self.sea_then_air_shipment and not self.air_then_sea_shipment and not self.rail_shipment_type :
                warn_list.append("Shipment Type")
        if not self.agent_id:
            warn_list.append("Customer")
        if not self.commodity_description and self.transport != 'documentation':
            warn_list.append("Commodity description")
        if not self.hs_code and self.transport != 'documentation':
            warn_list.append("hs code")
        if not self.source_location_id and self.transport != 'documentation':
            warn_list.append("Origin")
        if not self.destination_location_id and self.transport != 'documentation':
            warn_list.append("Destination")
        if not self.gross_weight and self.transport != 'documentation':
            warn_list.append("Gross Weight")
        if not self.incoterm and self.transport not in ['documentation','land']:
            warn_list.append("incoterm")
        if not self.clearance_required:
            warn_list.append("Clearance required")
        if not self.number_packages and self.transport != 'documentation':
            warn_list.append("Number of packages / Pallets")
        if not self.reefer_status and self.transport != 'documentation':
            warn_list.append("Reefer status")
        if not self.warehousing:
            warn_list.append("Warehousing")
        if not self.weight_type:
            warn_list.append("Weight Type")
        if not self.commodity_category and self.transport != 'documentation' :
            warn_list.append("Commodity category")
        if self.dangerous_goods and not self.danger_class:
            warn_list.append("Danger class")
        if self.transport == 'land' and not self.vehicle_size:
            warn_list.append("Vehicle Size")
        if self.transport == 'land' and not self.vehicle_type:
            warn_list.append("Vehicle Type")
        if self.transport == 'ocean' and not self.equipment_type:
            warn_list.append("Equipment type")



        if warn_list:
            raise ValidationError("Please Fill up this require fields %s"%warn_list)
        for book in self:
            res = self.convert_fields_to_dict()
            if res.get('operation') == 'master':
                name_act = 'Master'
                res['name'] = self.env['ir.sequence'].next_by_code('operation.master') or _('New')
            elif res.get('operation') == 'house':
                name_act = 'House'
                res['name'] = self.env['ir.sequence'].next_by_code('operation.house') or _('New')
            elif res.get('operation') == 'direct':
                name_act = 'Direct'
                res['name'] = self.env['ir.sequence'].next_by_code('operation.direct') or _('New')
            form_view = self.env.ref('freight.view_freight_operation_form')
            res.update({'default_booking_id': book.id, 'default_job_management_order_ref': self.job_management_order_ref,
                        'default_loose_cargo_ids': [(6, 0, self.loose_cargo_ids.ids)],
                        'default_job_management_ids': [(6, 0, self.job_management_ids.ids)],
                        'default_vehicle_ids': [(6, 0, self.vehicle_ids.ids)],
                        'default_target_rate': self.target_rate,
                        'default_container_ids': [(6, 0, self.container_ids.ids)]}),

            book.write({'state':'ship_order'})
            return {
                'name': name_act,
                'res_model': 'freight.operation',
                'type': 'ir.actions.act_window',
                'views': [(form_view and form_view.id, 'form')],
                'context':res,
            }

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

    @api.onchange('source_location_id', 'destination_location_id')
    def onchange_source_destination_location(self):
        """
        Set Given Value according to the origin and destination
        1) Import, Export, Cross Border State
        2) Is Domestic
        :return:
        """
        for req in self:
            direction = 'cross_state'
            if self.env.company.country_id:
                if (req.source_location_id and req.destination_location_id and req.source_location_id.country and
                        req.destination_location_id.country and req.source_location_id.country == self.env.company.country_id == req.destination_location_id.country):
                    direction = 'domestic'
                elif (req.source_location_id and not req.destination_location_id and req.source_location_id.country == self.env.company.country_id) or (
                        req.source_location_id and req.source_location_id.country and req.source_location_id.country == self.env.company.country_id and
                        (not req.destination_location_id or (req.destination_location_id and req.destination_location_id.country != self.env.company.country_id))):
                    direction = 'export'
                elif (req.destination_location_id and not req.source_location_id.country and req.destination_location_id.country == self.env.company.country_id) or (
                        req.destination_location_id and req.destination_location_id.country and req.destination_location_id.country == self.env.company.country_id and
                        (not req.source_location_id or (req.source_location_id and req.source_location_id.country != self.env.company.country_id))):
                    direction = 'import'
            req.direction = direction

    @api.onchange('booking_gross_weight', 'weight_uom_id')
    def onchange_booking_gross_weight_and_weight_uom(self):
        """
        Set Chargeable Weight and Chargeable UOM according to the gross weight and gross uom
        :return:
        """
        self.write({'chargeable_uom_id': self.weight_uom_id and self.weight_uom_id.id or False,
                    'chargeable': self.booking_gross_weight})

    @api.onchange('transport')
    def onchange_freight_booking_transport(self):
        """
        Set shipment type false when transport are change
        Loose Cargo available Air mode

        Set shipment type false when mode of transport are change
        Dimension Option available for LTL, LCL and Air
        :return:
        """
        cargo_container_visible = 'none'
        is_dimensions_visible = False
        if self.transport == 'air':
            is_dimensions_visible = True
        self.write({'rail_shipment_type': False,
                    'ocean_shipment_type': False,
                    'inland_shipment_type': False,
                    'sea_then_air_shipment': False,
                    'air_then_sea_shipment': False,
                    'cargo_container_visible': cargo_container_visible,
                    'dimensions_of_package_id': False,
                    'is_dimensions_visible': is_dimensions_visible})

    @api.onchange('rail_shipment_type', 'ocean_shipment_type', 'inland_shipment_type', 'sea_then_air_shipment', 'air_then_sea_shipment')
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

        self.dimensions_of_package_id = False
        if (not self.sea_then_air_shipment and not self.air_then_sea_shipment
            and not self.inland_shipment_type and not self.ocean_shipment_type
            and not self.rail_shipment_type and self.transport != 'air') or (
                self.transport in ['courier', 'documentation']):
            self.is_dimensions_visible = False
        elif (self.rail_shipment_type and self.rail_shipment_type == 'lcl') or (
                self.ocean_shipment_type and self.ocean_shipment_type == 'lcl') or (
                self.inland_shipment_type and self.inland_shipment_type == 'ltl') or (
                self.air_then_sea_shipment and self.air_then_sea_shipment == 'lcl') or (
                self.sea_then_air_shipment and self.sea_then_air_shipment == 'lcl') or (
                self.transport == 'air'):
            self.is_dimensions_visible = True
        else:
            self.is_dimensions_visible = False

    def convert_fields_to_dict(self):
        final_dict  = {}
        if self.operation:
            final_dict['operation'] = self.operation
        if self.direction:
            final_dict['direction'] = self.direction
        if self.transport:
            final_dict['transport'] = self.transport
        if self.ocean_shipment_type:
            final_dict['ocean_shipment_type'] = self.ocean_shipment_type
        if self.inland_shipment_type:
            final_dict['inland_shipment_type'] = self.inland_shipment_type
        if self.air_shipment_type:
            final_dict['air_shipment_type'] = self.air_shipment_type
        if self.rail_shipment_type:
            final_dict['rail_shipment_type'] = self.rail_shipment_type
        if self.sea_then_air_shipment:
            final_dict['sea_then_air_shipment'] = self.sea_then_air_shipment
        if self.air_then_sea_shipment:
            final_dict['air_then_sea_shipment'] = self.air_then_sea_shipment
        if self.shipper_id:
            final_dict['shipper_id'] = self.shipper_id and self.shipper_id.id or False
        if self.consignee_id:
            final_dict['consignee_id'] = self.consignee_id and self.consignee_id.id or False
        if self.source_location_id:
            final_dict['source_location_id'] = self.source_location_id and self.source_location_id.id or False
        if self.destination_location_id:
            final_dict['destination_location_id'] = self.destination_location_id and self.destination_location_id.id or False
        if self.mawb_no:
            final_dict['mawb_no'] = self.mawb_no
        if self.flight_no:
            final_dict['flight_no'] = self.flight_no
        if self.airline_id:
            final_dict['airline_id'] = self.airline_id and self.airline_id.id or False
        # Ocean Fields
        if self.add_terms:
            final_dict['add_terms'] = self.add_terms
        if self.shipping_line_id:
            final_dict['shipping_line_id'] =self.shipping_line_id and self.shipping_line_id.id or False
        if self.vessel_id:
            final_dict['vessel_id'] = self.vessel_id and self.vessel_id.id or False
        if self.voyage_no:
            final_dict['voyage_no'] = self.voyage_no
        if self.obl:
            final_dict['obl'] = self.obl
        # Inland Fields
        if self.truck_ref:
            final_dict['truck_ref'] = self.truck_ref
        if self.trucker_number:
            final_dict['trucker_number'] = self.trucker_number
        if self.vehicle_size:
            final_dict['vehicle_size'] = self.vehicle_size
        if self.vehicle_type:
            final_dict['vehicle_type'] = self.vehicle_type
        if self.trucker:
            final_dict['trucker'] = self.trucker and self.trucker.id or False
        # Air Fields
        if self.origin_close:
            final_dict['origin_close'] = True
        if self.destination_close:
            final_dict['destination_close'] = True
        # General Data
        if self.job_type:
            final_dict['job_type'] = self.job_type
        if self.por_origin:
            final_dict['por_origin'] = self.por_origin
        if self.pol:
            final_dict['pol'] = self.pol and self.pol.id or False
        if self.pod:
            final_dict['pod'] = self.pod and self.pod.id or False
        if self.pofd_destination:
            final_dict['pofd_destination'] = self.pofd_destination
        if self.equipment_type:
            final_dict['equipment_type'] = self.equipment_type
        if self.barcode:
            final_dict['barcode'] = self.barcode
        if self.notes:
            final_dict['notes'] = self.notes
        if self.freight_pc:
            final_dict['freight_pc'] = self.freight_pc
        if self.other_pc:
            final_dict['other_pc'] = self.other_pc
        if self.reefer_status:
            final_dict['reefer_status'] = self.reefer_status
        if self.hs_code:
            final_dict['hs_code'] = [(6, 0, self.hs_code.ids)]
        if self.gross_weight:
            final_dict['gross_weight'] = self.gross_weight
        if self.weight_type:
            final_dict['weight_type'] = self.weight_type
        if self.number_packages:
            final_dict['number_packages'] = self.number_packages
        if self.stackability:
            final_dict['stackability'] = self.stackability
        if self.clearance_required:
            final_dict['clearance_required'] = self.clearance_required
        if self.warehousing:
            final_dict['warehousing'] = self.warehousing
        if self.target_rate:
            final_dict['target_rate'] = self.target_rate
        if self.expected_free_time_at_origin:
            final_dict['expected_free_time_at_origin'] = self.expected_free_time_at_origin
        if self.expected_free_time_at_destination:
            final_dict['expected_free_time_at_destination'] = self.expected_free_time_at_destination
        if self.target_transit_time:
            final_dict['target_transit_time'] = self.target_transit_time
        if self.additional_requirements:
            final_dict['additional_requirements'] = self.additional_requirements
        if self.temperature:
            final_dict['temperature'] = self.temperature
        if self.set_temperature:
            final_dict['set_temperature'] = self.set_temperature
        if self.commodity_category:
            final_dict['commodity_category'] = self.commodity_category
        if self.commodity_description:
            final_dict['commodity_description'] = self.commodity_description
        if self.tracking_number:
            final_dict['tracking_number'] = self.tracking_number
        if self.dangerous_goods:
            final_dict['dangerous_goods'] = True
            if self.dangerous_goods_notes:
                final_dict['dangerous_goods_notes'] = self.dangerous_goods_notes
            if self.danger_class:
                final_dict['danger_class'] = self.danger_class
        if self.agent_id:
            final_dict['agent_id'] = self.agent_id and self.agent_id.id or False
        if self.operator_id:
            final_dict['operator_id'] = self.operator_id and self.operator_id.id or False
        if self.move_type:
            final_dict['move_type'] = self.move_type and self.move_type.id or False
        if self.incoterm:
            final_dict['incoterm'] = self.incoterm and self.incoterm.id or False
        if self.package_type_id:
            final_dict['package_type_id'] = self.package_type_id or False
        if self.datetime:
            final_dict['datetime'] = self.datetime
        res = {}
        for key, val in final_dict.items():
            if key != 'name':
                res.update({
                    'default_' + key: val
                })
        return res

    @api.onchange('consignee_id')
    def onchange_consignee_id(self):
        """
        when change the consignee reset the consignee address
        :return:
        """
        for rec in self:
            rec.write({'consignee_address_id': False})

    @api.onchange('shipper_id')
    def onchange_shipper_id(self):
        """
        when change the shipper reset the shipper address
        :return:
        """
        for rec in self:
            rec.write({'shipper_address_id': False})

    @api.onchange('shipper_address_id', 'consignee_address_id')
    def set_loading_delivery_address(self):
        """
        Set loading and delivery address according to the consignee and shipper
        :return:
        """
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
                'active_model': 'freight.booking',
                'active_ids': self.ids,
            },
        }

    def button_view_sailings(self):
        return True

    def button_clear_sailing(self):
        """
        Clear Sailing Details
        :return:
        """
        self.write({'carrier_id': False, 'voyage_no': False, 'vessel_id': False})
        return True

    def button_lode_list(self):
        return True

    def review_booking(self):
        for rec in self:
            rec.is_review_booking = True
