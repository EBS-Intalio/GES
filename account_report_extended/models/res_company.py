# -*- coding: utf-8 -*-
from odoo import api, fields, models, _




class ResCompanyEXT(models.Model):
    _inherit = 'res.company'
    depreciation_ids = fields.Many2many('account.account', 'res_company_depreciation_ids_rel','company_id','depcreciate_id',string='Depreciation', readonly=False,
                                        domain="[('company_id', '=', company_id)]")
    allowance_doubtful_ids = fields.Many2many('account.account','res_company_allowance_doubtful_ids_rel','company_id','allowance_id', string='Allowance for doubtful debts - net',
                                              readonly=False,
                                              domain="[('company_id', '=', company_id)]")
    provision_employee_ids = fields.Many2many('account.account','res_company_provision_employee_ids_rel','company_id','provision_id',
                                              string='Provision for employees’ end of service benefits', readonly=False,
                                              domain="[('company_id', '=', company_id)]")
    interest_income_ids = fields.Many2many('account.account','res_company_interest_income_ids_rel','company_id','interest_id', string='Interest Income', readonly=False,
                                           domain="[('company_id', '=', company_id)]")
    finance_cost_ids = fields.Many2many('account.account','res_company_finance_cost_ids_rel','company_id','finance_id', string='Finance costs', readonly=False,
                                        domain="[('company_id', '=', company_id)]")
    depriciation_rou_ids = fields.Many2many('account.account','res_company_depriciation_rou_ids_rel','company_id','depcreciate_rou_id', string='Depreciation on ROU', readonly=False,
                                            domain="[('company_id', '=', company_id)]")

    gain_remeausement_ids = fields.Many2many('account.account','res_company_gain_remeausement_ids_rel','company_id','gain_remeausement_id',
                                             string='Gain on remeasurement of finance lease liability and finance lease liability',
                                             readonly=False,
                                             domain="[('company_id', '=', company_id)]")
