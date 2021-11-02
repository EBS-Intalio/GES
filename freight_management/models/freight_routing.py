# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _

class FreightRouting(models.Model):
    _name = 'freight.routing'
    _description = 'Freight Routing'

    console_id = fields.Many2one('consol.details','Consol ID')
    # Leg Details
    defined_by = fields.Char('Defined By', related='console_id.name')
    mode = fields.Selection([('af', 'Air Freight'),
                             ('sf', 'Sea Freight'),
                             ('rof', 'Road Freight'),
                             ('raf', 'Rail Freight'),
                             ('st', 'Storage'),
                             ], string='Mode')
    Type = fields.Selection([
        ('mv','Main Vessel'),
        ('pcv','Pre-Carriage Vessel'),
        ('ofv','On-forwarding Vessel'),
        ('ot','Other'),
    ], string="Type")
    status = fields.Selection([
        ('planned','Planned'),
        ('confirmed','Confirmed'),
        ('hsn','Held – See Note'),
    ], string="Status")
    leg_order = fields.Float('Leg order')
    charter_route = fields.Boolean('Charter Route')
    is_linked = fields.Boolean('Is Linked')
    notes = fields.Text('Notes')
    # Voyage / Flight Details
    voyage = fields.Char('Voyage')
    Vessel = fields.Many2one('freight.vessel','Vessel')
    carrier = fields.Many2one('res.partner','Carrier')
    creditor = fields.Many2one('res.partner','Creditor')
    carrier_ref = fields.Char('Carrier Reference')
    published = fields.Boolean('Published')
    carrier_service_level = fields.Selection([
        ('no_data','No Data')
    ], string='Carrier Service Level')
    # Origin Details
    load_port = fields.Many2one('unloco.data','Load Port')
    dept_from = fields.Many2one('res.country','Dept From')
    etd = fields.Date('ETD')
    atd = fields.Date('ATD')
    cto_received_date = fields.Date('CTO Received')
    cfs_received_date = fields.Date('CFS Received')
    cto_cutt_off_date = fields.Date('CTO Cutt Off')
    cfs_cutt_off_date = fields.Date('CFS Cutt Off')
    docs_due_date = fields.Date('Docs Due')
    vgm_cutt_off_date = fields.Date('VGM Cutt Off')
    # Destinatiuon Details
    disc_port = fields.Many2one('unloco.data', 'Discharge port')
    arrival_at = fields.Many2one('res.country', 'Arrival At')
    eta = fields.Date('ETA')
    ata = fields.Date('ATA')
    cto_available_date = fields.Date('CTO Available')
    cfs_available_date = fields.Date('CFS Available')
    cto_storage_date = fields.Date('CTO Storage')
    cfs_storage_date = fields.Date('CFS Storage')
    shipment_id = fields.Many2one('freight.operation', 'Shipment ID')

    air_type = fields.Selection([
        ('f1', 'Flight 1'),
        ('f2', 'Flight 2'),
        ('f3', 'Flight 3'),
        ('other', 'Other')
    ], string="Type")
    aircraft_type = fields.Char('AirCraft Type')
    flight = fields.Char('Flight')
    aircraft_reg = fields.Char('Aircraft Reg.')

    truck_ref = fields.Char('Truck Ref')
    other_info = fields.Char('Other Info')
    journey_num = fields.Char('Journey Num.')
    journey_ref = fields.Char('Journey Ref.')

    carrier_service_level = fields.Selection([('std', 'Standard')],string="Carrier Service Level")
