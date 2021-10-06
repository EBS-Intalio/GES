# -*- coding: utf-8 -*"-
from odoo import api, fields, models, _
class CrossoveredBudgetLinesInherited(models.Model):
    _inherit = "crossovered.budget.lines"

    sale_budget_line = fields.Many2one('sale.budget.line', string='sale budget line')