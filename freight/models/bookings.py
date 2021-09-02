# -*- coding: utf-8 -*-
###################################################################################
#
#    inteslar software trading llc.
#    Copyright (C) 2018-TODAY inteslar (<https://www.inteslar.com>).
#    Author:   (<https://www.inteslar.com>)
#
###################################################################################
import logging
from odoo import api, fields, models, _
from random import choice
from string import digits
from json import dumps
import json
import datetime
from datetime import datetime as dt


class Bookings(models.Model):
    _name = 'freight.booking'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Freight Bookings'

    def _get_default_stage_id(self):
        return self.env['shipment.stage'].search([], order='sequence', limit=1)

    def _default_random_barcode(self):
        return "".join(choice(digits) for i in range(8))

    barcode = fields.Char(string="Barcode", help="ID used for shipment identification.",
                          default=_default_random_barcode, copy=False)
    color = fields.Integer('Color')
    stage_id = fields.Many2one('shipment.stage', 'Stage', default=_get_default_stage_id,
                               group_expand='_read_group_stage_ids')
    name = fields.Char(string='Name', copy=False)
    direction = fields.Selection(([('import', 'Import'), ('export', 'Export')]), string='Direction')
    state = fields.Selection(([('draft', 'Draft'), ('converted', 'Converted')]), string='Status', default='draft')
    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport', required=False)
    operation = fields.Selection([('direct', 'Direct'), ('house', 'House'), ('master', 'Master')], string='Operation')
    ocean_shipment_type = fields.Selection(([('fcl', 'FCL'), ('lcl', 'LCL')]), string='Ocean Shipment Type')
    inland_shipment_type = fields.Selection(([('ftl', 'FTL'), ('ltl', 'LTL')]), string='Inland Shipment Type')
    air_shipment_type = fields.Selection(([('breakbulk', 'Breakbulk'), ('roro', 'Roro')]), string='Air Shipment Type')
    shipper_id = fields.Many2one('res.partner', 'Shipper')
    consignee_id = fields.Many2one('res.partner', 'Consignee')
    source_location_id = fields.Many2one('freight.port', 'Origin Airport', index=True)
    destination_location_id = fields.Many2one('freight.port', 'Destination Airport', index=True)
    origin_close = fields.Boolean("Consider close by Airport")
    destination_close = fields.Boolean("Consider close by Airport")
    obl = fields.Char('OBL', help='Original Bill Of Landing')
    shipping_line_id = fields.Many2one('res.partner', 'Shipping Line')
    voyage_no = fields.Char('Voyage No')
    vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    mawb_no = fields.Char('MAWB No')
    airline_id = fields.Many2one('freight.airline', 'Airline')
    flight_no = fields.Char('Flight No')
    datetime = fields.Datetime('Date')
    truck_ref = fields.Char('CMR/RWB#/PRO#:')
    trucker = fields.Many2one('freight.trucker', 'Trucker')
    trucker_number = fields.Char('Trucker No')
    agent_id = fields.Many2one('res.partner', 'Customer', required=True)
    operator_id = fields.Many2one('res.users', 'User')
    freight_pc = fields.Selection(([('collect', 'Collect'), ('prepaid', 'Prepaid')]), string="Freight PC")
    other_pc = fields.Selection(([('collect', 'Collect'), ('prepaid', 'Prepaid')]), string="Other PC")
    notes = fields.Text('Notes')
    dangerous_goods = fields.Boolean('Dangerous Goods')
    dangerous_goods_notes = fields.Text('Dangerous Goods Info')
    move_type = fields.Many2one('freight.move.type', 'Move Type')
    tracking_number = fields.Char('Tracking Number')
    declaration_number = fields.Char('Declaration Number')
    declaration_date = fields.Date('Declaration Date')
    custom_clearnce_date = fields.Datetime('Customs Clearance Date')
    incoterm = fields.Many2one('freight.incoterms', 'Incoterm')
    parent_id = fields.Many2one('freight.operation', 'Parent')
    book_vals = fields.Char('Booking Vals')
    freight_id = fields.Many2one('freight.operation', 'Freight Operation')
    attachment = fields.Many2many('ir.attachment', 'attach_booking_rel', 'doc_id', 'booking_id',
                                  string="Attachment",
                                  help='You can attach the copy of your document', copy=False)
    track_ids = fields.One2many('booking.tracker', 'booking_id', 'Tracker Lines')

    job_type = fields.Char("Job Type")
    por_origin = fields.Selection(([('value_a', 'value_a'),('Value_b', 'Value_b')]), string="POR /Origin")
    pol = fields.Selection(([('value_a', 'value_a'),('Value_b', 'Value_b')]), string="POL")
    pod = fields.Selection(([('value_a', 'value_a'),('Value_b', 'Value_b')]), string="POD")
    pofd_destination = fields.Selection(([('value_a', 'value_a'),('Value_b', 'Value_b')]), string="POFD /Destination")
    equipment_type = fields.Selection(([('20', '20'), ('20_open_top', '20 Open Top'), ('40', '40'),
                                                ('40_hc', '40 HC'), ('40_open_top', '40 OPEN TOP'), ('45', '45'),
                                                ('53', '53'), ('goh_single', 'GOH (Single)'), ('goh_double', 'GOH (Double)'), ('open_top_gauge', 'Open Top in-gauge'),
                                                ('open_top_out_gauge', 'Open Top out-of-gauge'), ('isotank', 'Isotank'), ('shipper_own', 'Shipper Owned Container'),
                                                ('mafi_trailer', 'Mafi Trailer'), ('tank', 'Tank'), ('flexibag', 'Flexibag')]), string="Equipment Type")
    vehicle_size = fields.Selection(([('3_ton', '3 Ton Truck'), ('7_ton', '7 Ton Truck'), ('10_ton', '10 Ton Truck'),
                                      ('12_ton', '12 Meter Trailer'), ('15_ton', '15 Meter Trailer')]), string="Vehicle Size")
    vehicle_type = fields.Selection(([('flat_bed', 'Flat Bed'), ('full_box', 'Full Box'), ('curtain_slider', 'Curtain Slider'),
                                      ('53', '53'), ('hot_shot', 'Hot Shot'),('low_bed', 'Low Bed'), ('box_truck', 'Box Truck w/Liftgate')]), string="Vehicle Type")

    reefer_status = fields.Selection(([('yes', 'YES'), ('no', 'NO'), ('non_operate', 'Non Operating Reefer')]), string="Reefer Status",required=True)
    temperature = fields.Selection(([('celsius', 'Celsius'), ('fahrenheit', 'Fahrenheit')]), string="Temperature")
    set_temperature = fields.Float("Temp Set")
    commodity_category = fields.Selection(([('food_perishable', 'Food Perishable'), ('nonfood_perishable', 'Non food perishable'), ('non_perishable', 'Non perishable F&B'),
                                            ('furniture', 'Furniture'), ('building_material', 'Building Material'), ('automotive', 'Automotive'),
                                            ('pharmaceuticals', 'Pharmaceuticals'), ('petroleum_products', 'Petroleum Products'), ('other_chemicals', 'Other Chemicals')]), string="Commodity Category",required=True)
    commodity_description = fields.Text("Commodity Description", required=True)
    danger_class = fields.Selection(([('class_1', 'Class 1'), ('class_2 ', 'Class 2'), ('class_3', 'Class 3'),
                                            ('class_4', 'Class 4'), ('class_5', 'Class 5'), ('class_6', 'Class 6'),
                                            ('class_7', 'Class 7'), ('class_8', 'Class 8'), ('class_9', 'Class 9')]), string="Danger Class")
    hs_code = fields.Selection(([('value_1', 'value_1'),('value_2', 'value_2')]), string="HS Code")
    gross_weight= fields.Float("Gross weight (KG)", required=True)
    weight_type = fields.Selection(([('estimated', 'Estimated'), ('actual', 'Actual')]), string="Weight Type", required=True)
    number_packages = fields.Integer("Number of packages / Pallets", required=True)
    # dimensions_of_package =
    stackability = fields.Selection(([('stackable', 'Stackable'), ('no_stackable', 'No Stackable')]), string="Stackability")
    additional_requirements = fields.Text("Additional requirements")
    package_type_id = fields.Many2one('freight.package', 'Package Type')
    # loading_address
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=?', country_id)]")
    city = fields.Char("City")
    area = fields.Char("Area")
    street = fields.Char("Street")
    building = fields.Char("Building")
    po_box = fields.Char("PO Box")
    zip_code = fields.Integer("Zip Code")
    # delivery_address
    delivery_country_id = fields.Many2one('res.country', string='Country')
    delivery_state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=?', country_id)]")
    delivery_city = fields.Char("City")
    delivery_area = fields.Char("Area")
    delivery_street = fields.Char("Street")
    delivery_building = fields.Char("Building")
    delivery_po_box = fields.Char("PO Box")
    delivery_zip_code = fields.Integer("Zip Code")
    clearance_required = fields.Selection(([('yes', 'YES'), ('no', 'NO')]), string="Clearance Required", required=True)
    warehousing = fields.Selection(([('yes', 'YES'), ('no', 'NO')]), string="Warehousing / Storage", required=True)
    target_rate = fields.Float("Target Rate in USD")
    # shipment_ready_date = fields.Date("Shipment Ready Date")
    # shipment_ready_asap = fields.Boolean("Shipment Ready ASAP")
    # target_eta = fields.Date("Target ETA")
    # target_eta_asap = fields.Boolean("Target ETA SAP")
    # target_etd = fields.Date("Target ETD")
    # target_etd_asap = fields.Boolean("Target ETD SAP")
    target_transit_time = fields.Integer("Target Transit Time")
    expected_free_time_at_origin = fields.Integer("Expected Free Time at Origin")
    expected_free_time_at_destination = fields.Integer("Expected Free Time at Destination")
    additional_comments = fields.Text("Additional Comments")
    preferred_shipping_line = fields.Selection(([]), string="Preferred Shipping Line")
    preferred_airline_id = fields.Many2one('freight.airline', 'Preferred Airline')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['shipment.stage'].search([])
        return stage_ids

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('freight.booking') or _('New')
        booking = super(Bookings, self).create(values)
        return booking

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
        if self.shipper_id:
            final_dict['shipper_id'] = self.shipper_id.id or False
        if self.consignee_id:
            final_dict['consignee_id'] = self.consignee_id.id or False

        if self.source_location_id:
            final_dict['source_location_id'] = self.source_location_id.id or False
        if self.destination_location_id:
            final_dict['destination_location_id'] = self.destination_location_id.id or False
        if self.mawb_no:
            final_dict['mawb_no'] = self.mawb_no
        if self.flight_no:
            final_dict['flight_no'] = self.flight_no
        if self.airline_id:
            final_dict['airline_id'] = self.airline_id.id or False
        # Ocean Fields
        if self.shipping_line_id:
            final_dict['shipping_line_id'] =self.shipping_line_id.id or False
        if self.vessel_id:
            final_dict['vessel_id'] = self.vessel_id.id or False
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
            final_dict['trucker'] = self.trucker.id or False
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
            final_dict['pol'] = self.pol
        if self.pod:
            final_dict['pod'] = self.pod
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
            final_dict['hs_code'] = self.hs_code
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
            final_dict['agent_id'] = self.agent_id.id or False
        if self.operator_id:
            final_dict['operator_id'] = self.operator_id.id or False
        if self.move_type:
            final_dict['move_type'] = self.move_type.id or False
        if self.incoterm:
            final_dict['incoterm'] = self.incoterm.id or False
        if self.package_type_id:
            final_dict['package_type_id'] = self.package_type_id.id or False
        if self.datetime:
            final_dict['datetime'] = self.datetime
        res = {}
        for key, val in final_dict.items():
            if key != 'name':
                res.update({
                    'default_' + key: val
                })
        return res

    def convert_to_operation(self):
        name_act = ''
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
            res.update({'default_booking_id': book.id})
            book.write({'state':'converted'})
            return {
                'name': name_act,
                'res_model': 'freight.operation',
                'type': 'ir.actions.act_window',
                'views': [(form_view and form_view.id, 'form')],
                'context':res,
            }

    def reset_book(self):
        for rec in self:
            rec.state = 'draft'
            if rec.freight_id:
                freight = rec.freight_id
                freight.booking_id = False
                rec.freight_id = False


    def button_shipping(self):
        action = {
            'name': _('Shipment'),
            'type': 'ir.actions.act_window',
            'res_model': 'freight.operation',
            'target': 'current',
        }
        ope = self.env['freight.operation'].search([('booking_id', '=', self.id)], limit=1)
        action['domain'] =[('id', '=', ope.id)]
        action['res_id'] = ope.id
        action['view_mode'] = 'form'
        return action


class BookingTracker(models.Model):
    _name = 'booking.tracker'

    name = fields.Char('Note')
    user_id = fields.Many2one('res.users','User ID')
    date = fields.Datetime('Date')
    actual_date = fields.Datetime('Actual')
    vendor_attachment = fields.Binary(attachment=True, string="Attachment")
    booking_id = fields.Many2one('freight.booking', 'Tender')


    @api.depends('date')
    def compute_actual(self):
        for line in self:
            line.actual_date = datetime.strptime(str(line.create_date), "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=4)