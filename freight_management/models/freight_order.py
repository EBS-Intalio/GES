# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightOrder(models.Model):
    _inherit = 'freight.order'
    _rec_name = 'order_no'

    @api.depends('freight_booking_ids')
    def _compute_freight_booking(self):
        """
        Count total freight booking
        :return:
        """
        for order in self:
            order.booking_count = len(order.freight_booking_ids)

    booking_count = fields.Integer(string='Total Freight Booking', compute='_compute_freight_booking')
    freight_booking_ids = fields.One2many('freight.booking', 'freight_order_id', string='Freight Booking', copy=False)

    buyer = fields.Many2one('res.partner', string="Buyer")
    buyer_address = fields.Many2one('res.partner', string="Buyer Address")
    shipper = fields.Many2one('res.partner', string="Shipper")
    shipper_address = fields.Many2one('res.partner', string="Shipper Address")
    order_no = fields.Char(string="Order No")
    confirm_no = fields.Char(string="Confirm No")
    invoice_no = fields.Char(string="Invoice No")
    req_ex_work = fields.Date(string="Req ex works")
    oder_date = fields.Date(string="Order Date")
    confirm_date = fields.Date(string="Confirm Date")
    invoice_date = fields.Date(string="Invoice Date")
    followup_date = fields.Date(string="Follow-Up Date")
    req_in_store = fields.Date(string="Req In Store")
    goods_description = fields.Char(string="Goods description")
    currency = fields.Many2one('res.currency', string="Currency")
    currency_value = fields.Float(string="Currency value")
    service_level = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                      ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door'),
                                      ('custom_and_brokerage', 'Customs and Brokerage')],
                                     string="Service Level")
    incoterm_id = fields.Many2one('freight.incoterms', string="Incoterm")
    additional_terms = fields.Char(string="Additional Terms")
    mode_of_transport = fields.Selection([('air', 'Air'),
                                          ('ocean', 'Sea'),
                                          ('land', 'Road'),
                                          ('sea_then_air', 'Sea then Air'),
                                          ('air_then_sea', 'Air then Sea'),
                                          ('rail', 'Rail'),
                                          ('courier', 'Courier'),
                                          ('documentation', 'Documentation')], default="air",
                                         string="Mode of Transport")
    cont_mode = fields.Selection([
        ('fcl', 'Full Container Load'),
        ('lcl', 'Less Container Load'),
        ('blk', 'Bulk'),
        ('lqd', 'Liquid'),
        ('bbk', 'Break Bulb'),
        ('bcn', 'Buyers Consolidation'),
        ('ror', 'Roll On / Roll Off'),
        ('oth', 'Other'),
    ], string='Container Mode')
    pre_advice_id = fields.Many2one('freight.pre.advice', string="Pre-Advice")
    origin_country = fields.Many2one('res.country', 'Origin Country')
    line_count = fields.Integer(string="Line Count")
    inner_packs = fields.Integer(string="Inner packs")
    outer_packs = fields.Integer(string="Outers pack")
    quantity = fields.Float(string="Quantity")
    invoiced = fields.Float(string="Invoiced")
    quantity_received = fields.Float(string="Quantity received")
    remaining = fields.Float(string="Remaining")
    origin_cutoff = fields.Date(string="Origin Cutoff")
    carrier = fields.Many2one('res.partner', 'Carrier')
    house_bill = fields.Char(string="House Bill")
    master_bill = fields.Char(string="Master Bill")
    departure = fields.Many2one('freight.vessel', string="Departure")
    intermediate = fields.Many2one('freight.vessel', string="Intermediate")
    arrival = fields.Many2one('freight.vessel', string="Arrival")
    goods_origin = fields.Many2one('freight.port', string="Goods Origin")
    goods_destination = fields.Many2one('freight.port', string="Goods Destination")
    port_of_loading = fields.Many2one('freight.port', string="Port Of Loading")
    discharge_port = fields.Many2one('freight.port', string="Discharge Port")

    voyage_departure = fields.Many2one('freight.vessel', string="Departure")
    voyage_intermediate = fields.Many2one('freight.vessel', string="Intermediate")
    voyage_arrival = fields.Many2one('freight.vessel', string="Arrival")

    estimated_depart = fields.Date(string="Estimated Depart")
    estimated_arrive = fields.Date(string="Estimated Arrive")
    sending_agent = fields.Many2one('res.partner', string="Sending Agent")
    receiving_agent = fields.Many2one('res.partner', string="Receiving Agent")
    packs = fields.Integer(string="Packs")
    package_type_id = fields.Selection([('palatized', 'Palatized'),
                                        ('cartons', 'Cartons'),
                                        ('bulk', 'Bulk'),
                                        ('drums', 'Drums'),
                                        ('other', 'Others')], string="Packaging Type")
    actual_volume = fields.Float(string="Actual Volume")
    actual_weight = fields.Float(string="Actual Weight")
    actual_volume_uom = fields.Many2one('uom.uom', string="Actual Volume UOM")
    actual_weight_uom = fields.Many2one('uom.uom', string="Actual Weight UOM")

    shipment_no = fields.Char(string="Shipment No")
    booking_no = fields.Char(string="Booking No")
    declaration_ref = fields.Char(string="Declaration Ref")
    shipment_house_bil = fields.Char(string="House Bill")

    shipment_origin = fields.Many2one('freight.port', string="Origin")
    shipment_destination = fields.Many2one('freight.port', string="Destination")
    shipment_service_level = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                      ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door'),
                                      ('custom_and_brokerage', 'Customs and Brokerage')],
                                     string="Service Level")
    consol_details_ids = fields.One2many('consol.details', 'freight_order_id', string="Console")
    custom_valuation_charges_ids = fields.One2many('customer.valuation.charge', 'freight_order_id', string="Custom Valuation Changes")
    product_qty_summary_ids = fields.One2many('product.quantity.summary', 'freight_order_id', string='Product Quantity Summary', copy=False)
    product_summary_line_count = fields.Integer(string="Line Count",compute="compute_product_qty_summary")
    product_summary_inner_packs = fields.Integer(string="Inner packs")
    product_summary_outer_packs = fields.Integer(string="Outers pack")
    product_summary_quantity = fields.Float(string="Quantity",compute="compute_product_qty_summary")
    product_summary_invoiced = fields.Float(string="Invoiced",compute="compute_product_qty_summary")
    product_summary_quantity_received = fields.Float(string="Quantity received",compute="compute_product_qty_summary")
    product_summary_remaining = fields.Float(string="Remaining",compute="compute_product_qty_summary")
    order_line_line_count = fields.Integer(string="Line Count", compute="compute_data")
    order_line_inner_packs = fields.Integer(string="Inner packs",compute="compute_data")
    order_line_outer_packs = fields.Integer(string="Outers pack",compute="compute_data")
    order_line_quantity = fields.Float(string="Quantity", compute="compute_data")
    order_line_invoiced = fields.Float(string="Invoiced", compute="compute_data")
    order_line_quantity_received = fields.Float(string="Quantity received", compute="compute_data")
    order_line_remaining = fields.Float(string="Remaining", compute="compute_data")
    order_line_ids = fields.One2many('freight.order.line', 'freight_order', string='Order Line', copy=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('converted', 'Converted')],
                             string='Status', default='draft')
    name = fields.Char(string='Description', required=False)
    package = fields.Many2one('freight.package', 'Package', required=False)
    reefer_status = fields.Selection([('yes','YES'),('no','NO'),('non_operate','Non Operating Reefer')], default='yes', string='Reefer Status')
    commodity_category = fields.Selection(([('food_perishable', 'Food Perishable'),
                                            ('nonfood_perishable', 'Non food perishable'),
                                            ('non_perishable', 'Non perishable F&B'),
                                            ('furniture', 'Furniture'), ('building_material', 'Building Material'),
                                            ('automotive', 'Automotive'),
                                            ('pharmaceuticals', 'Pharmaceuticals'),
                                            ('petroleum_products', 'Petroleum Products'),
                                            ('other_chemicals', 'Other Chemicals')]), default='food_perishable', string="Commodity Category")
    commodity_description = fields.Text("Commodity Description")
    hs_code = fields.Many2many('freight.hs.code', string="Hs-Codes")
    gross_weight = fields.Float("Gross weight (KG)")
    weight_type = fields.Selection([('estimated', 'Estimated'), ('actual', 'Actual')], default='estimated', string="Weight Type",)
    equipment_type = fields.Selection(([('20', '20'), ('20_open_top', '20 Open Top'), ('40', '40'),
                                        ('40_hc', '40 HC'), ('40_open_top', '40 OPEN TOP'), ('45', '45'),
                                        ('53', '53'), ('goh_single', 'GOH (Single)'), ('goh_double', 'GOH (Double)'),
                                        ('open_top_gauge', 'Open Top in-gauge'),
                                        ('open_top_out_gauge', 'Open Top out-of-gauge'), ('isotank', 'Isotank'),
                                        ('shipper_own', 'Shipper Owned Container'),
                                        ('mafi_trailer', 'Mafi Trailer'), ('tank', 'Tank'), ('flexibag', 'Flexibag')]),
                                      default='20', string="Equipment Type")
    vehicle_size = fields.Selection(([('3_ton', '3 Ton Truck'), ('7_ton', '7 Ton Truck'), ('10_ton', '10 Ton Truck'),
                                      ('12_ton', '12 Meter Trailer'), ('15_ton', '15 Meter Trailer')]),
                                    default='3_ton', string="Vehicle Size")
    vehicle_type = fields.Selection(
        ([('flat_bed', 'Flat Bed'), ('full_box', 'Full Box'), ('curtain_slider', 'Curtain Slider'),
          ('53', '53'), ('hot_shot', 'Hot Shot'), ('low_bed', 'Low Bed'), ('box_truck', 'Box Truck w/Liftgate')]),
        default='flat_bed', string="Vehicle Type")
    agent_id = fields.Many2one('res.partner', 'Customer')
    clearance_required = fields.Selection(([('yes', 'YES'), ('no', 'NO')]), default='yes', string="Clearance Required")
    warehousing = fields.Selection(([('yes', 'YES'), ('no', 'NO')]), default='yes', string="Warehousing / Storage")
    order_status = fields.Selection([
        ('inc','Incomplete'),
        ('plc','Placed'),
        ('cnf','Confirmed'),
        ('shp','Shipped'),
        ('prt','Part Delivered'),
        ('dlv','Delivered'),
        ('can','Canceled'),
    ], string='Order Status')

    @api.depends('order_line_ids')
    def compute_data(self):
        for rec in self:
            rec.order_line_line_count = len(rec.order_line_ids.ids)
            rec.order_line_inner_packs = sum(rec.order_line_ids.mapped('inner_packs'))
            rec.order_line_outer_packs = sum(rec.order_line_ids.mapped('outer_packs'))
            rec.order_line_quantity = sum(rec.order_line_ids.mapped('quantity'))
            rec.order_line_invoiced = sum(rec.order_line_ids.mapped('invoiced'))
            rec.order_line_quantity_received = sum(rec.order_line_ids.mapped('quantity_received'))
            rec.order_line_remaining = sum(rec.order_line_ids.mapped('remaining'))

    def convert_to_booking(self):
        """
        Convert  order to booking
        :return:
        """
        vals = {
            'job_management_order_ref': self.order_no,
            'transport': self.mode_of_transport,
            'source_location_id': self.shipment_origin and self.shipment_origin.id or False,
            'destination_location_id': self.shipment_destination and self.shipment_destination.id or False,
            'agent_id': self.agent_id.id,
            'shipper_id': self.shipper and self.shipper.id or False,
            'consignee_id': self.buyer and self.buyer.id or False,
            'number_packages': self.packs,
            'incoterm': self.incoterm_id and self.incoterm_id.id or False,
            'reefer_status': self.reefer_status,
            'commodity_category': self.commodity_category,
            'commodity_description': self.commodity_description,
            'hs_code': [(6, 0, self.hs_code.ids)],
            'gross_weight': self.gross_weight,
            'warehousing': self.warehousing,
            'clearance_required': self.clearance_required,
            'weight_type': self.weight_type,
            'equipment_type': self.equipment_type,
            'vehicle_size': self.vehicle_size,
            'vehicle_type': self.vehicle_type,
            'freight_order_id': self.id
        }
        #TODO Add Warning of Require field
        freight_booking = self.env['freight.booking'].create(vals)
        self.write({'state': 'converted', 'booking_no': freight_booking.name})
        return True

    @api.model
    def create(self,vals):
        res = super(FreightOrder, self).create(vals)
        data = res.prepare_product_qaunt_summ()
        res.with_context({'product_qty_summary':True}).write({'product_qty_summary_ids': data})
        return res

    def write(self,vals):
        res = super(FreightOrder, self).write(vals)
        if not self._context.get('product_qty_summary'):
            data = self.prepare_product_qaunt_summ()
            self.with_context({'product_qty_summary':True}).write({'product_qty_summary_ids': data})
        return res

    def prepare_product_qaunt_summ(self,):
        data = []
        i = 1
        if self.product_qty_summary_ids:
            self.product_qty_summary_ids.unlink()
        for rec in self.order_line_ids:
            rec.line = i
            i += 1
            data.append((0,0,{
                'part_no':rec.product_id.id,
                'description':rec.description,
                'quantity_ordered':rec.quantity,
                'quantity_invoiced':rec.invoiced,
                'quantity_received':rec.quantity_received,
                'quantity_remaining':rec.remaining,
            }))

        return data

    def action_view_freight_booking(self):
        """
        Prepare a action for the display the Freight Booking
        :return:
        """
        action = self.env.ref('freight.view_freight_booking_action').read()[0]
        booking = self.freight_booking_ids
        if len(booking) > 1:
            action['domain'] = [('id', 'in', booking.ids)]
        elif booking:
            form_view = [(self.env.ref('freight.view_freight_booking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = booking.id

        return action

    @api.depends('product_qty_summary_ids')
    def compute_product_qty_summary(self):
        for rec in self:
            rec.product_summary_line_count = len(rec.product_qty_summary_ids)
            rec.product_summary_quantity= sum(rec.product_qty_summary_ids.mapped('quantity_ordered'))
            rec.product_summary_invoiced = sum(rec.product_qty_summary_ids.mapped('quantity_invoiced'))
            rec.product_summary_quantity_received = sum(rec.product_qty_summary_ids.mapped('quantity_received'))
            rec.product_summary_remaining = sum(rec.product_qty_summary_ids.mapped('quantity_remaining'))
        return True

    @api.onchange('port_of_loading','discharge_port')
    def get_origin_destination(self):
        for rec in self:
            rec.shipment_origin = rec.port_of_loading.id
            rec.shipment_destination = rec.discharge_port.id


    def create_declaration(self):
        return True


class FreightOrderLine(models.Model):
    _name = 'freight.order.line'

    line = fields.Integer(string="Line")
    product_id = fields.Many2one('product.product',string="Part No.")
    description = fields.Char(string="Description")
    inner_packs = fields.Integer(string="Inner Packs")
    outer_packs = fields.Integer(string="Outer Packs")
    type = fields.Char(string="Type")
    quantity = fields.Float(string="Quantity")
    invoiced = fields.Float(string="Invoiced")
    quantity_received = fields.Float(string="Quantity received")
    remaining = fields.Float(string="Remaining")
    unit_of_qty = fields.Many2one('uom.uom', string="Unit of quantity")
    line_price = fields.Float(string="Line price")
    item_price = fields.Float(string="Item price")
    invoice_no = fields.Char(string="Invoice No")
    origin = fields.Many2one('res.country', string="Origin")
    manufacturer = fields.Many2one('res.partner', string="Manufacturer")
    manufacturer_address = fields.Many2one('res.partner', string="Manufacturer Address")
    freight_order = fields.Many2one('freight.order', string="Order")




