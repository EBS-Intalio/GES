# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettingsExt(models.TransientModel):
    _inherit = 'res.config.settings'

    account_journal_id = fields.Many2one(related='company_id.account_journal_id', string='Journal', readonly=False,
                                         domain="[('company_id', '=', company_id), ('type', '=', 'general')]")
    expense_account_id = fields.Many2one(string='Expense Account', related='company_id.expense_account_id', readonly=False,
        domain=lambda self: "[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id),\
                             ('user_type_id', '=', %s)]" % self.env.ref('account.data_account_type_expenses').id)
    income_account_id = fields.Many2one(string='Income Account', related='company_id.income_account_id', readonly=False,
                                        domain=lambda self: "[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id),\
                                                                     ('user_type_id', 'in', %s)]" % [
                                            self.env.ref('account.data_account_type_revenue').id,
                                            self.env.ref('account.data_account_type_other_income').id])
    # receivable_id = fields.Many2one('account.account', string='Receivable Account', related='company_id.receivable_id',readonly=False)
    # payable_id = fields.Many2one('account.account', string='Payable Account', related='company_id.payable_id', readonly=False)

