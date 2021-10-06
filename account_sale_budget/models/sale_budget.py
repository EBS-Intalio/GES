# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _

class SaleBudget(models.Model):
    _name = 'sale.budget'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Account Sale Budget'

    name = fields.Char("Name")
    date_from = fields.Date("Date From", required=True, track_visibility='always')
    date_to = fields.Date("Date From", required=True, track_visibility='always')
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        readonly=True,
        string="Company",
    )
    location_id = fields.Many2one(comodel_name="operating.unit", domain="[('company_id', '=', company_id)]", required=True)

    budget_id = fields.Many2one('crossovered.budget', 'Budget', readonly=False) # will be recalculated based on crossovered.budget that will be created and will be in other info page
    state = fields.Selection(selection=[('draft', 'Draft'),('confirmed', 'Confirmed')], string='Status', readonly=True, copy=False, tracking=True, default='draft')

    sale_budget_line_ids = fields.One2many(comodel_name='sale.budget.line', inverse_name='sale_budget_id')

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            # log the date in chatter
            message = _("Date is from %s to %s") % (record.date_from, record.date_to)
            record.message_post(body=message)

            # Creating a crossovered.budget record
            budget = self.env['crossovered.budget'].sudo().create({
                'date_from': record.date_from,
                'date_to': record.date_to,
                'name': record.name,
                'user_id': self.env.uid,
                # 'date_check_theoretcial_amount': record.date_to,
                'company_id': record.company_id.id,
                'state': 'draft',
            })
            record.budget_id = budget.id

            #Get or create budgetary position
            for line in record.sale_budget_line_ids:
                income_account_id = line.line_of_service_id.income_account
                expense_account_id = line.line_of_service_id.expense_account

                income_budgetary_position_id = self.env['account.budget.post'].search([('account_ids', 'in', income_account_id.id)], limit=1)
                if not income_budgetary_position_id:
                    income_budgetary_position_id = self.env['account.budget.post'].create({
                        'name': income_account_id.code,
                        'account_ids': [(4, income_account_id.id)],
                    })
                expense_budgetary_position_id = self.env['account.budget.post'].search([('account_ids', 'in', expense_account_id.id)], limit=1)
                if not expense_budgetary_position_id:
                    expense_budgetary_position_id = self.env['account.budget.post'].create({
                        'name': expense_account_id.code,
                        'account_ids': [(4, expense_account_id.id)],
                    })
                # create two different budget lines
                if line.revenue > 0:
                    self.env['crossovered.budget.lines'].create({
                        'crossovered_budget_id': budget.id,
                        'date_from': record.date_from,
                        'date_to': record.date_to,
                        'general_budget_id': income_budgetary_position_id.id,
                        'planned_amount': line.revenue,
                        'partner_id': line.customer_id.id,
                        'operating_unit_id': record.location_id.id,
                        'sale_budget_line': line.id,
                    })
                if line.cos > 0:
                    self.env['crossovered.budget.lines'].create({
                        'crossovered_budget_id': budget.id,
                        'date_from': record.date_from,
                        'date_to': record.date_to,
                        'general_budget_id': expense_budgetary_position_id.id,
                        'planned_amount': -line.cos,
                        'partner_id': line.customer_id.id,
                        'operating_unit_id': record.location_id.id,
                        'sale_budget_line': line.id,
                    })

class SaleBudgetLine(models.Model):
    _name = 'sale.budget.line'
    _rec_name = 'sale_budget_id'

    customer_id = fields.Many2one('res.partner', 'Customer', required=True)
    line_of_service_id = fields.Many2one('account.operation.matrix', 'Line of Service')
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)
    revenue = fields.Monetary(string="Revenue", currency_field='currency_id')
    gp = fields.Monetary(string="GP", currency_field='currency_id')
    cos = fields.Monetary(string="COS", currency_field='currency_id', compute='compute_cos_gm')
    gm = fields.Float(string="GM%", compute='compute_cos_gm', default=0)
    sale_budget_id = fields.Many2one('sale.budget', readonly=True)

    budget_line_id = fields.One2many(comodel_name='crossovered.budget.lines', inverse_name='sale_budget_line')

    @api.depends('revenue','gp')
    def compute_cos_gm(self):
        for rec in self:
            rec.cos = rec.revenue - rec.gp
            if rec.revenue:
                rec.gm = (rec.gp / rec.revenue) * 100