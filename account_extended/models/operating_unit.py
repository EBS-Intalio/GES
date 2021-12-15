
from odoo import api, fields, models


class OperatingUnitInherit(models.Model):

    _inherit = "operating.unit"
    _description = "Operating Unit"

    internal_id = fields.Integer('Internal ID')
    phone = fields.Char('Phone')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state','State')
    country_id = fields.Many2one('res.country','Country')
    location_group = fields.Char('Location Group')


