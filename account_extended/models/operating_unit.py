
from odoo import api, fields, models


class OperatingUnitInherit(models.Model):

    _inherit = "operating.unit"
    _description = "Operating Unit"

    company_id = fields.Many2one(
        "res.company",string="Company",
        required=False,
        readonly=False,
        default=lambda self: self.env.company,
    )

    internal_id = fields.Integer('Internal ID')
    phone = fields.Char('Phone')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state','State')
    country_id = fields.Many2one('res.country','Country')
    location_group = fields.Char('Location Group')


