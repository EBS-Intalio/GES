# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightBooking(models.Model):
    _inherit = 'freight.booking'

    freight_request_id = fields.Many2one('freight.job.request','RequestID')
    hs_code = fields.Many2many('freight.hs.code', string="Freight Hs-Codes")

    transport = fields.Selection([('air', 'Air'),
                                   ('ocean', 'Ocean'),
                                   ('land', 'Land'),
                                   ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'),
                                   ('rail', 'Rail'),
                                   ('courier', 'Courier')], string='Transport', required=False)

    def button_request(self):
        return {
            'name': _('Freight Request'),
            'view_mode': 'form',
            'res_model': 'freight.job.request',
            'type': 'ir.actions.act_window',
            'res_id': self.freight_request_id.id,
        }
