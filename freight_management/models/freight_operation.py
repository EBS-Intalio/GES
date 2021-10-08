# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightOperation(models.Model):
    _inherit = 'freight.operation'

    container_ids = fields.Many2many('freight.container', string='Container', copy=False)
    loose_cargo_ids = fields.Many2many('freight.loose.cargo', string='Loose Cargo', copy=False)
    vehicle_ids = fields.Many2many('vehicle.details', string="Vehicle Details", copy=False)
    transport = fields.Selection([('air', 'Air'),
                                  ('ocean', 'Ocean'),
                                  ('land', 'Road'),
                                  ('sea_then_air', 'Sea then Air'),
                                  ('air_then_sea', 'Air then Sea'),
                                  ('rail', 'Rail'),
                                  ('courier', 'Courier')], default='air', string='Transport')

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
    move_type = fields.Many2one('freight.move.type', 'Service Type')
    job_management_order_ref = fields.Char(string="Order Refs", required=False)
    job_management_ids = fields.Many2many('job.management.link.line', string='Job Management Lines', copy=False)
    is_admin = fields.Boolean('Is Admin',compute='check_admin')
    direction = fields.Selection(selection_add=[('cross_state', 'Cross Border State')], default='cross_state')
    incotearm_name = fields.Char(related='incoterm.code')
    add_terms = fields.Char(string="Add. Terms")
    ata = fields.Date('ATA')
    atd = fields.Date('ATD')
    iss_date = fields.Date('Issue Date')
    exp_date = fields.Date('Expiry Date')
    release_type = fields.Selection([('no_data', 'No data')], string='Release Type')
    house_bill_type = fields.Selection([('no_data', 'No data')], string='House Bill Type')
    on_board = fields.Selection([('no_data', 'No data')], string='Onboard')
    on_board_date = fields.Date()
    hbl_div_mode = fields.Selection([('no_data', 'No data')], string='HBL Div.Mode')
    iss_date_1 = fields.Date('Issue Date')
    org_bill = fields.Integer('Original Bills')
    copy_bill = fields.Integer('Copy Bills')
    charges_apply = fields.Selection([('no_data', 'No Data')], string='Charges Apply')
    phase = fields.Selection([('no_data', 'No Data')], string='Phase')
    e_freight_status = fields.Selection([('no_data', 'No Data')], string='e-Freight Status')
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

    @api.onchange('source_location_id', 'destination_location_id')
    def onchange_shipment_source_destination_location(self):
        """
        Set Given Value according to the origin and destination
        1) Import, Export, Cross Border State
        2) Is Domestic
        :return:
        """
        for shipment in self:
            direction = 'cross_state'
            if (
                    shipment.source_location_id and not shipment.destination_location_id and shipment.source_location_id.country.id == self.env.company.country_id.id) or (
                    shipment.source_location_id and shipment.source_location_id.country and shipment.source_location_id.country.id == self.env.company.country_id.id and
                    (not shipment.destination_location_id or (
                            shipment.destination_location_id and shipment.destination_location_id.country.id != self.env.company.country_id.id))):
                direction = 'export'
            elif (
                    shipment.destination_location_id and not shipment.source_location_id.country and shipment.destination_location_id.country.id == self.env.company.country_id.id) or (
                    shipment.destination_location_id and shipment.destination_location_id.country and shipment.destination_location_id.country.id == self.env.company.country_id.id and
                    (not shipment.source_location_id or (
                            shipment.source_location_id and shipment.source_location_id.country.id != self.env.company.country_id.id))):
                direction = 'import'
            shipment.direction = direction

    def check_admin(self):
        """
        checks whether the user is admin or not
        """
        for rec in self:
            rec.is_admin = False
            if self.env.user.has_group('base.group_erp_manager') or self.env.user.has_group('base.group_system'):
                rec.is_admin = True
