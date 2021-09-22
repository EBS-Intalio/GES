# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class ShipperServiceLevel(models.Model):
    _name = 'service.level'
    _description = 'Service Level'

    service_level_code = fields.Char(string='Service Level Code', required=True)
    description = fields.Char(string='Description')
    active = fields.Boolean(string='Is Active')
    is_door_to_door = fields.Boolean(string='Is Door To Door')
    is_system = fields.Boolean(string='Is System')
    difot = fields.Float(string='DIFOT %')
    service_agreement = fields.Selection([('dft', 'Delivery in Full on Time Percentage (DIFOT)'),
                                          ('grn', 'Guaranteed')], string='Service Agreement')
    lang = fields.Selection(_lang_get, string='Language')
