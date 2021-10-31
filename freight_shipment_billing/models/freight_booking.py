# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class FreightBookingInherit(models.Model):
    _inherit = "freight.booking"

    operating_unit_id = fields.Many2one('operating.unit', string='Branch')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Department')
    account_operation_lines = fields.One2many(comodel_name='freight.operation.billing', inverse_name='booking_id')

    total_revenue = fields.Monetary(string="Total Revenue", currency_field='company_currency_id',
                                    compute="compute_data")
    total_cost = fields.Monetary(string="Total Cost", currency_field='company_currency_id', compute="compute_data")
    profit = fields.Monetary(string="Profit", currency_field='company_currency_id', compute="compute_data")
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          default=lambda self: self.env.company.currency_id.id)

    @api.depends('account_operation_lines')
    def compute_data(self):
        for rec in self:
            rec.total_revenue = sum(rec.account_operation_lines.mapped('local_sell_amount'))
            rec.total_cost = sum(rec.account_operation_lines.mapped('local_cost_amount'))
            rec.profit = rec.total_revenue - rec.total_cost

    def convert_to_operation(self):
        res = super(FreightBookingInherit, self).convert_to_operation()
        res['context'].update({
            'default_operating_unit_id': self.operating_unit_id.id,
            'default_analytic_account_id': self.analytic_account_id.id,
            'default_account_operation_lines': [(6, 0, self.account_operation_lines.ids)],
        })
        return res