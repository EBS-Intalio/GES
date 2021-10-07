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
                                  ('courier', 'Courier')], string='Transport')

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
    # is_admin = fields.Boolean('Is Admin',compute='check_admin')
    direction = fields.Selection(selection_add=[('cross_state', 'Cross Border State')])

    # def check_admin(self):
    #     """
    #     checks whether the user is admin or not
    #     """
    #     for rec in self:
    #         rec.is_admin = False
    #         if self.env.user.has_group('base.group_erp_manager') or self.env.user.has_group('base.group_system'):
    #             rec.is_admin = True
    incotearm_name = fields.Char(related='incoterm.code')
    add_terms = fields.Char(string="Add. Terms")
