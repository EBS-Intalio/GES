# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class JobManagementLink(models.Model):
    _name = 'job.management.link'
    _rec_name = "order_ref"

    order_ref = fields.Many2one('sale.order', string="Order Refs", required=True)
    job_management_link_line_ids = fields.One2many('job.management.link.line', 'job_management_link_id',
                                                   string='Job Management link Lines', copy=False)
    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')


class JobManagementLinkLine(models.Model):
    _name = 'job.management.link.line'

    job_management_link_id = fields.Many2one('job.management.link', string="Job Management link")
    job_number = fields.Char(string="Job Number")
    # service_id = fields.Many2one('freight.service.details', string="Service")
    job_description = fields.Char(string="Job Description")
