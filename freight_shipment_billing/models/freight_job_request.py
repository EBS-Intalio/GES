# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _

class FreightRequestInherit(models.Model):
    _inherit = "freight.job.request"

    transport = fields.Selection(related='mode_of_transport')
    operating_unit_id = fields.Many2one('operating.unit', string='Branch')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Department')
    account_operation_lines = fields.One2many(comodel_name='freight.operation.billing', inverse_name='freight_request_id')

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


    def create_booking(self, amount_total=0):
        res = super(FreightRequestInherit, self).create_booking()
        book_id = self.env['freight.booking'].browse(res['res_id'])
        book_id.write({
            'operating_unit_id': self.operating_unit_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'account_operation_lines': [(6, 0, self.account_operation_lines.ids)],
        })
        return res
