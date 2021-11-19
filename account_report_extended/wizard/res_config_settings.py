# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettingsExt(models.TransientModel):
    _inherit = 'res.config.settings'

    depreciation_ids = fields.Many2many(related='company_id.depreciation_ids', string='Depreciation', readonly=False,
                                        domain="[('company_id', '=', company_id)]")
    allowance_doubtful_ids = fields.Many2many(related='company_id.allowance_doubtful_ids', string='Allowance for doubtful debts - net',
                                              readonly=False,
                                              domain="[('company_id', '=', company_id)]")
    provision_employee_ids = fields.Many2many(related='company_id.provision_employee_ids',
                                              string='Provision for employees’ end of service benefits', readonly=False,
                                              domain="[('company_id', '=', company_id)]")
    interest_income_ids = fields.Many2many(related='company_id.interest_income_ids', string='Interest Income', readonly=False,
                                           domain="[('company_id', '=', company_id)]")
    finance_cost_ids = fields.Many2many(related='company_id.finance_cost_ids', string='Finance costs', readonly=False,
                                           domain="[('company_id', '=', company_id)]")
    depriciation_rou_ids = fields.Many2many(related='company_id.depriciation_rou_ids', string='Depreciation on ROU', readonly=False,
                                            domain="[('company_id', '=', company_id)]")

    gain_remeausement_ids = fields.Many2many(related='company_id.gain_remeausement_ids',
                                             string='Gain on remeasurement of finance lease liability and finance lease liability',
                                             readonly=False,
                                             domain="[('company_id', '=', company_id)]")