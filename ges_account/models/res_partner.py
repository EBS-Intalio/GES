from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    legal_name = fields.Char(string="Legal Name")
