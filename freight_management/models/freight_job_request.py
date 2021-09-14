# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FreightJobRequest(models.Model):
    _name = 'freight.job.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Freight Job Request'
    _order = 'name desc, id desc'

    lead_id = fields.Many2one('crm.lead', string="lead")
    name = fields.Char(string='Name', translate=True, copy=False)
    partner_id = fields.Many2one('res.partner', string="Customer")
    mode_of_transport = fields.Selection([('air', 'Air'),
                                           ('ocean', 'Sea'),
                                           ('land', 'Road'),
                                           ('sea_then_air', 'Sea then Air'),
                                           ('air_then_sea', 'Air then Sea'),
                                           ('rail', 'Rail'),
                                           ('courier', 'Courier')], default="air", string="Mode of Transport")
    rail_shipment_type = fields.Selection([('fcl', 'FCL'), ('lcl', 'LCL'),
                                      ('breakbulk', 'Breakbulk'),
                                      ('liquid', 'Liquid'),
                                      ('bulk','Bulk'),
                                      ('roro', 'Roro')], string='Rail Shipment Type')
    ocean_shipment = fields.Selection([('fcl', 'FCL'), ('lcl', 'LCL'),
                                      ('breakbulk', 'Breakbulk'),
                                      ('liquid', 'Liquid'),
                                      ('bulk', 'Bulk'),
                                      ('roro', 'Roro')], string='Ocean Shipment Type')
    inland_shipment = fields.Selection([('ftl', 'FTL'), ('ltl', 'LTL')], string='Road Shipment Type')
    #air_shipment = fields.Selection([('breakbulk', 'Breakbulk'),
                                      # ('roro', 'Roro')], string='Air Shipment Type')
    job_type = fields.Char(string="Job Type")
    #
    # por_origin = fields.Selection(([]), string="POR /Origin")
    # pol = fields.Selection(([]), string="POL")
    # pod = fields.Selection(([]), string="POD")
    # pofd_destination = fields.Selection(([]), string="POFD /Destination")

    freight_incoterm_id = fields.Many2one('freight.incoterms', string="Incoterm")
    origin_airport_id = fields.Many2one('freight.port', string="Origin")
    destination_airport_id = fields.Many2one('freight.port', string="Destination")
    # consider_origin_close = fields.Boolean("Consider close by Origin")
    consider_origin_close = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no",
                                             string="Consider close by Origin", required=True)
    # consider_destination_close = fields.Boolean("Consider close by Destination")
    consider_destination_close = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no",
                                             string="Consider close by Destination", required=True)
    equipment_type = fields.Selection([('20', '20'), ('20_open_top', '20 Open Top '), ('40', '40'),
                                        ('40_hc', '40 HC'), ('40_open_top', '40 OPEN TOP'), ('45', '45'),
                                        ('53', '53'), ('goh_single', 'GOH (Single)'), ('goh_double', 'GOH (Double)'),
                                        ('open_top_gauge', 'Open Top in-gauge'),
                                        ('open_top_out_gauge', 'Open Top out-of-gauge'), ('isotank', 'Isotank'),
                                        ('shipper_own', 'Shipper Owned Container'),
                                        ('mafi_trailer', 'Mafi Trailer'), ('tank', 'Tank'), ('flexibag', 'Flexibag')], string="Equipment Type")
    vehicle_size = fields.Selection([('3_ton', '3 Ton Truck'),
                                      ('7_ton', '7 Ton Truck'),
                                      ('10_ton', '10 Ton Truck'),
                                      ('12_ton', '12 Meter Trailer'),
                                      ('15_ton', '15 Meter Trailer')], string="Vehicle Size")
    vehicle_type = fields.Selection([('flat_bed', 'Flat Bed'),
                                      ('full_box', 'Full Box'),
                                      ('curtain_slider', 'Curtain Slider'),
                                      ('53', '53'),
                                      ('hot_shot', 'Hot Shot'),
                                      ('low_bed', 'Low Bed'), ('box_truck', 'Box Truck w/Liftgate')],
                                    string="Vehicle Type")
    reefer_status = fields.Selection([('yes', 'YES'), ('no', 'NO'), ('non_operate', 'Non Operating Reefer')],
                                     string="Reefer Status", default="yes", required=True)
    temperature = fields.Selection([('celsius', 'Celsius'), ('fahrenheit', 'Fahrenheit')], string="Temperature")
    temperature_value = fields.Float("Temp Set")
    commodity_category = fields.Selection([('food_perishable', 'Food Perishable'),
                                            ('nonfood_perishable', 'Non food perishable'),
                                            ('non_perishable', 'Non perishable F&B'),
                                            ('furniture', 'Furniture'),
                                            ('building_material', 'Building Material'),
                                            ('automotive', 'Automotive'),
                                            ('pharmaceuticals', 'Pharmaceuticals'),
                                            ('petroleum_products', 'Petroleum Products'),
                                            ('other_chemicals', 'Other Chemicals')],
                                          string="Commodity Category", default="food_perishable", required=True)
    commodity_description = fields.Text(string="Commodity Description", required=True)
    # is_dangerous_goods = fields.Boolean(string="Is Dangerous Goods?")
    is_dangerous_goods = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no",
                                                  string="Is Dangerous Goods?", required=True)
    dangerous_goods_notes = fields.Text(string="Dangerous Goods Info")
    dangerous_goods_class = fields.Selection([('class_1', 'Class 1'), ('class_2', 'Class 2'), ('class_3', 'Class 3'),
                                               ('class_4', 'Class 4'), ('class_5', 'Class 5'), ('class_6', 'Class 6'),
                                               ('class_7', 'Class 7'), ('class_8', 'Class 8'), ('class_9', 'Class 9')],
                                             string="Dangerous Goods Class")
    # Many2many ned new model
    freight_hs_code_ids = fields.Many2many('freight.hs.code', string="HS-Codes", required=True)
    gross_weight = fields.Float(string="Gross weight (KG)", required=True)
    number_of_pallets_packages = fields.Integer(string="Number of packages / Pallets", required=True)
    # dimensions_of_package = Dimensions of each package / Pallets   dimensions
    stackability = fields.Selection(([('stackable', 'Stackable'),
                                      ('no_stackable', 'No Stackable')]),
                                    string="Stackability")
    additional_requirements = fields.Text(string="Additional requirements")
    # package_type_id = fields.Many2one('freight.package', string="Packaging Type", required=True)
    package_type_id = fields.Selection([('palatized', 'Palatized'),
                                         ('cartons', 'Cartons'),
                                         ('bulk', 'Bulk'),
                                         ('drums', 'Drums'),
                                         ('other', 'Others  (Please specify)')], string="Packaging Type", required=True)


    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State',
                               domain="[('country_id', '=?', country_id)]")
    city = fields.Char(string="City")
    area = fields.Char(string="Area")
    street = fields.Char(string="Street")
    building = fields.Char(string="Building")
    po_box = fields.Char(string="PO Box")
    zip_code = fields.Integer(string="Zip Code")

    delivery_country_id = fields.Many2one('res.country', string='Country')
    delivery_state_id = fields.Many2one('res.country.state', string='State',
                               domain="[('country_id', '=?', delivery_country_id)]")

    # delivery_state_id = fields.Many2one('res.country.state', string='State',
    #                                     domain="[('country_id', '=', delivery_country_id)]")
    delivery_city = fields.Char(string="City")
    delivery_area = fields.Char(string="Area")
    delivery_street = fields.Char(string="Street")
    delivery_building = fields.Char(string="Building")
    delivery_po_box = fields.Char(string="PO Box")
    delivery_zip_code = fields.Integer(string="Zip Code")
    shipper_id = fields.Many2one('res.partner', string="Shipper", required=True)
    consignee_id = fields.Many2one('res.partner', string="Consignee", required=True)
    clearance_required = fields.Selection([('yes', 'YES'),
                                            ('no', 'NO')], default="yes", string="Clearance Required", required=True)
    warehousing = fields.Selection([('yes', 'YES'),
                                     ('no', 'NO')], default="yes", string="Warehousing / Storage", required=True)
    target_rate = fields.Float(string="Target Rate in USD")

    # Added
    shipment_ready_date = fields.Date(string="Shipment Ready Date")
    # shipment_ready_asap = fields.Boolean(string="Shipment Ready ASAP")
    shipment_ready_asap = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no",
                                           string="Shipment Ready ASAP", required=True)
    target_eta = fields.Date(string="Target ETA")
    # target_eta_asap = fields.Boolean(string="Target ETA ASAP")
    target_eta_asap = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no",
                                       string="Target ETA ASAP", required=True)
    target_etd = fields.Date(string="Target ETD")
    # target_etd_asap = fields.Boolean(string="Target ETD ASAP")
    target_etd_asap = fields.Selection([('yes', 'YES'), ('no', 'NO')], default="no",
                                       string="Target ETD ASAP", required=True)

    # por_origin_id = fields.Many2one('freight.por.origin', string="POR /Origin")
    pol_id = fields.Many2one('freight.pol', string="POL")
    pod_id = fields.Many2one('freight.pod', string="POD")
    # pofd_destination_id = fields.Many2one('freight.pofd.destination', string="POFD /Destination")
    service_level = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                       ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door')],
                                     string="Service Level")
    # End

    target_transit_time = fields.Integer(string="Target Transit Time")
    expected_free_time_at_origin = fields.Integer(string="Expected Free Time at Origin")
    expected_free_time_at_destination = fields.Integer(string="Expected Free Time at Destination")
    additional_comments = fields.Text(string="Additional Comments")
    # preferred_shipping_line = fields.Selection(([]), string="Preferred Shipping Line")
    preferred_airline_id = fields.Many2one('freight.airline', string="Preferred Airline")
    shipping_line_id = fields.Many2one('res.partner', 'Shipping Line')
    vessel_id = fields.Many2one('freight.vessel', string="Vessel")
    voyage_no = fields.Char(string="Voyage No")
    mawb_no = fields.Char(string="MAWB No")
    truck_ref = fields.Char(string="CMR/RWB#/PRO#")
    trucker = fields.Many2one('freight.trucker', string="Trucker")
    trucker_number = fields.Char(string="Trucker No")
    pricing_id = fields.Many2one('freight.pricing', string='Shipment Pricing')
    flight_no = fields.Char(string="Flight No")
    state = fields.Selection([('draft', 'Draft'),
                               ('pricing', 'Pricing Progress'),
                               ('converted', 'Converted')],
                             string='Status', default='draft')

    sales_count = fields.Integer(string='Total Orders', compute='_compute_freight_sales_orders')
    order_ids = fields.One2many('sale.order', 'freight_request_id', string='Orders', copy=False)
    booking_id = fields.Many2one('freight.booking','BookingId')
    is_booking_done = fields.Boolean('Booking Done')
    is_web_request = fields.Boolean(string="Is Created From Website?", default=False)
    weight_type = fields.Selection([('estimated', 'Estimated'), ('actual', 'Actual')], string="Weight Type")

    def action_view_sales_order(self):
        """
        Prepare a action for the display sales order
        :return:
        """
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        orders = self.order_ids
        if len(orders) > 1:
            action['domain'] = [('id', 'in', orders.ids)]
        elif orders:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = orders.id

        return action

    @api.depends('order_ids')
    def _compute_freight_sales_orders(self):
        """
        Count total freight request sales order
        :return:
        """
        for pricing in self:
            pricing.sales_count = len(pricing.order_ids)

    @api.model
    def create(self, values):
        """
        Generate Sequence for the freight request
        :param vals:{}
        :return:
        """
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('freight.job.request') or _('New')
        return super(FreightJobRequest, self).create(values)

    def create_request_pricing(self):
        """
        Create request pricing
        :return:
        """
        sale_order_template_id = self.env['sale.order.template'].search([('transport', '=', self.mode_of_transport)], limit=1)

        pricing = self.env['freight.pricing'].create({
            'state': 'draft',
            'sale_order_template_id': sale_order_template_id.id,
            'freight_request_id': self.id})
        order_lines = []
        for line in sale_order_template_id.sale_order_template_line_ids:
            if line.product_id:
                order_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'pricing_id': pricing.id,
                }))
        pricing.update({'charges_ids': order_lines})
        self.state = 'pricing'
        self.pricing_id = pricing.id
        return {
            'name': _('Freight pricing'),
            'view_mode': 'form',
            'view_id': self.env.ref('freight_management.freight_management_freight_pricing_form_view').id,
            'res_model': 'freight.pricing',
            'type': 'ir.actions.act_window',
            'res_id': pricing.id,
        }

    def button_pricing(self):
        """
        View freight request pricing
        :return:
        """
        ope = self.env['freight.pricing'].search([('freight_request_id', '=', self.id)])
        action = self.env.ref('freight_management.freight_management_view_freight_pricing_action').read()[0]
        if len(ope) > 1:
            action['domain'] = [('id', 'in', ope.ids)]
        elif ope:
            form_view = [(self.env.ref('freight_management.freight_management_freight_pricing_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = ope.id

        return action

    def create_booking(self):
        if not(self.mode_of_transport and self.shipper_id and self.consignee_id and self.partner_id and self.reefer_status and self.commodity_category and
               self.commodity_description and self.weight_type and self.clearance_required and self.warehousing):
            raise ValidationError('Either of the Transport, Shipper, Consignee, Customer, Reefer status, Commodity Category, Commodity Description, Weight Type, Clearance Required, Warehousing, Gross Weight, Number of packages are not filled please fill all the mandatory details before creating a booking.')
        vals = {
            'transport':self.mode_of_transport, #mandatory
            'shipper_id':self.shipper_id.id, #mandatory
            'consignee_id':self.consignee_id.id, #mandatory
            'agent_id':self.partner_id.id, #mandatory
            'reefer_status':self.reefer_status, #mandatory
            'commodity_category':self.commodity_category, #mandatory
            'commodity_description':self.commodity_description, #mandatory
            'weight_type':self.weight_type, #mandatory
            'clearance_required':self.clearance_required, #mandatory
            'warehousing':self.warehousing, #mandatory
            'gross_weight':self.gross_weight, #mandatory
            'number_packages': self.number_of_pallets_packages,#mandatory
        }
        if self.mode_of_transport == 'ocean':
            if not self.equipment_type:
                raise ValidationError(
                    'For ocean, Equipment Type must be selected')
            vals.update({'equipment_type':self.equipment_type})
        elif self.mode_of_transport == 'land':
            if not (self.vehicle_size and self.vehicle_type):
                raise ValidationError(
                    'For Land, Vehicle Type and Size must be selected')
            vals.update({
                'vehicle_size':self.vehicle_size, #mandatory
                'vehicle_type':self.vehicle_type, #mandatory
            })
        origin_close = False
        if self.consider_origin_close == 'yes':
            origin_close = True
        destination_close = False
        if self.consider_destination_close == 'yes':
            destination_close = True
        dangerous_goods = False
        if self.is_dangerous_goods == 'yes':
            dangerous_goods = True
        vals.update(
            {
                'incoterm':self.freight_incoterm_id and self.freight_incoterm_id.id,
                # 'air_shipment_type':self.air_shipment,
                'job_type':self.job_type,
                'source_location_id':self.origin_airport_id and self.origin_airport_id.id,
                # 'origin_close':self.consider_origin_close,
                'origin_close': origin_close,
                'destination_location_id':self.destination_airport_id and self.destination_airport_id.id,
                # 'destination_close':self.consider_destination_close,
                'destination_close': destination_close,
                'voyage_no':self.voyage_no,
                'vessel_id':self.vessel_id and self.vessel_id.id,
                'shipping_line_id':self.shipping_line_id and self.shipping_line_id.id,
                'mawb_no':self.mawb_no,
                'flight_no':self.flight_no,
                'dangerous_goods': dangerous_goods,
                # 'dangerous_goods':self.is_dangerous_goods,
                'danger_class':self.dangerous_goods_class,
                'temperature':self.temperature,
                'hs_code':self.freight_hs_code_ids and self.freight_hs_code_ids.ids,
                'stackability':self.stackability,
                'additional_requirements':self.additional_requirements,
                'target_rate':self.target_rate,
                # 'package_type_id':self.package_type_id and self.package_type_id.id,
                # 'shipment_ready_date':self.shipment_ready_date,
                # 'target_eta':self.target_eta,
                # 'target_etd':self.target_etd,
                'target_transit_time':self.target_transit_time,
                'expected_free_time_at_origin':self.expected_free_time_at_origin,
                'expected_free_time_at_destination':self.expected_free_time_at_destination,
                'additional_comments':self.additional_comments,
                'preferred_airline_id':self.preferred_airline_id and self.preferred_airline_id.id,
                #Loading
                'country_id':self.country_id and self.country_id.id,
                'state_id':self.state_id and self.state_id.id,
                'city':self.city,
                'area':self.area,
                'street':self.street,
                'building':self.building,
                'po_box': self.po_box,
                'zip_code': self.zip_code,
                #delivery
                'delivery_country_id':self.delivery_country_id and  self.delivery_country_id.id,
                'delivery_state_id':self.delivery_state_id and  self.delivery_state_id.id,
                'delivery_city': self.delivery_city,
                'delivery_area': self.delivery_area,
                'delivery_street': self.delivery_street,
                'delivery_building': self.delivery_building,
                'delivery_po_box': self.delivery_po_box,
                'delivery_zip_code': self.delivery_zip_code,
                'ocean_shipment_type': self.ocean_shipment,
                'truck_ref': self.truck_ref,
                'trucker': self.trucker.id and self.trucker.id,
                'trucker_number': self.trucker_number,
                'ocean_shipment_type': self.ocean_shipment,
                'freight_request_id':self.id,
            }
        )

        booking = self.env['freight.booking'].create(vals)
        self.booking_id = booking.id
        self.is_booking_done = True

        return {
            'name': _('Freight Booking'),
            'view_mode': 'form',
            'res_model': 'freight.booking',
            'type': 'ir.actions.act_window',
            'res_id': booking.id,
        }

    def button_booking(self):
        return {
            'name': _('Freight Booking'),
            'view_mode': 'form',
            'res_model': 'freight.booking',
            'type': 'ir.actions.act_window',
            'res_id': self.booking_id.id,
        }
