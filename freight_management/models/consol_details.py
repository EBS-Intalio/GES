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
        ('air','Air Freight'),
        ('sea','Sea Freight'),
        ('roa','Road Freight'),
        ('rail','Rail Freight'),
    ], string='Transport')
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
                    rec.load_port = old_rec.load_port and old_rec.load_port.id
                    rec.etd = old_rec.etd
                    rec.atd = old_rec.atd
                    rec.eta = old_rec.eta
                    rec.ata = old_rec.ata
                    rec.is_domestic_voyage = old_rec.is_domestic_voyage
                    rec.is_linked = old_rec.is_linked
                    rec.is_charter = old_rec.is_charter


