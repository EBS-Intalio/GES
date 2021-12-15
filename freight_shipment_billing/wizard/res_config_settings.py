# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_accrual_creditor_id = fields.Many2one('account.account', string='Accrual Account')
    accrual_journal_id = fields.Many2one('account.journal', string='Accrual Journal')
    deferral_journal_id = fields.Many2one('account.journal', string='Deferral Journal')
    account_deferral_creditor_id = fields.Many2one('account.account', string='Deferral Account')




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_accrual_creditor_id = fields.Many2one(related='company_id.account_accrual_creditor_id', readonly=False)
    accrual_journal_id = fields.Many2one(related='company_id.accrual_journal_id', readonly=False)
    deferral_journal_id = fields.Many2one(related='company_id.deferral_journal_id', readonly=False)
    account_deferral_creditor_id = fields.Many2one(related='company_id.account_deferral_creditor_id', readonly=False)

    @api.onchange('deferral_journal_id')
    def get_journaL_deferral(self):
        deferral_journal = self.env['account.journal'].search([('company_id','=',self.company_id.id),('is_deferral','=',True)])
        if deferral_journal:
            for deferral in deferral_journal:
                deferral.is_deferral = False
        self.deferral_journal_id.is_deferral = True