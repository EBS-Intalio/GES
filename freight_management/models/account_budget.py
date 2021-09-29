from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class CrossoveredBudgetInherit(models.Model):
    _inherit = "crossovered.budget"

    date_check_theoretcial_amount = fields.Date('Theoretical Amount At', default = fields.Date.today())
    partner_id = fields.Many2one('res.partner','Customer')

    @api.constrains('date_check_theoretcial_amount')
    def check_date_check_theoretcial_amount(self):
        for rec in self:
            if rec.date_check_theoretcial_amount:
                if not (rec.date_check_theoretcial_amount>=rec.date_from and rec.date_check_theoretcial_amount<=rec.date_to):
                    raise ValidationError('Theoretical Amount At should be between The selected Period!')


class CrossoveredBudgetLinesInherit(models.Model):
    _inherit = "crossovered.budget.lines"

    theoritical_amount_custom = fields.Monetary(
        compute='_compute_theoritical_amount_custom', string='Theoretical Amount Custom',
        help="Amount you are supposed to have earned/spent at this date.")

    employee_id = fields.Many2one('hr.employee','Employee')
    operating_unit_id = fields.Many2one('operating.unit','Operating Unit')
    partner_id = fields.Many2one(related='crossovered_budget_id.partner_id', store=True)

    @api.depends('date_from', 'date_to', 'crossovered_budget_id.date_check_theoretcial_amount')
    def _compute_theoritical_amount_custom(self):
        # beware: 'today' variable is mocked in the python tests and thus, its implementation matter
        today = fields.Date.today()
        for line in self:
            if line.paid_date:
                if today <= line.paid_date:
                    theo_amt = 0.00
                else:
                    theo_amt = line.planned_amount
            else:
                if not line.date_from or not line.date_to:
                    line.theoritical_amount_custom = 0
                    continue
                # One day is added since we need to include the start and end date in the computation.
                # For example, between April 1st and April 30th, the timedelta must be 30 days.
                line_timedelta = line.date_to - line.date_from + timedelta(days=1)
                if line.crossovered_budget_id.date_check_theoretcial_amount:
                    elapsed_timedelta = line.crossovered_budget_id.date_check_theoretcial_amount - line.date_from + timedelta(
                        days=1)

                    if elapsed_timedelta.days < 0:
                        # If the budget line has not started yet, theoretical amount should be zero
                        theo_amt = 0.00
                    elif line_timedelta.days > 0 and today < line.date_to:
                        # If today is between the budget line date_from and date_to
                        theo_amt = (
                                           elapsed_timedelta.total_seconds() / line_timedelta.total_seconds()) * line.planned_amount
                    else:
                        theo_amt = line.planned_amount
                else:
                    theo_amt = 0.00
            line.theoritical_amount_custom = theo_amt


    def _compute_practical_amount(self):
        for line in self:
            acc_ids = line.general_budget_id.account_ids.ids
            date_to = line.date_to
            date_from = line.date_from
            if line.analytic_account_id.id:
                analytic_line_obj = self.env['account.analytic.line']
                domain = [('account_id', '=', line.analytic_account_id.id),
                          ('date', '>=', date_from),
                          ('date', '<=', date_to),
                          ]
                if line.employee_id:
                    domain.append(('employee_id','=',line.employee_id.id))
                if line.operating_unit_id:
                    domain.append(('operating_unit_id','=',line.operating_unit_id.id))
                if line.partner_id:
                    domain.append(('partner_id','=',line.partner_id.id))
                if acc_ids:
                    domain += [('general_account_id', 'in', acc_ids)]

                where_query = analytic_line_obj._where_calc(domain)
                analytic_line_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(amount) from " + from_clause + " where " + where_clause

            else:
                aml_obj = self.env['account.move.line']
                domain = [('account_id', 'in',
                           line.general_budget_id.account_ids.ids),
                          ('date', '>=', date_from),
                          ('date', '<=', date_to),
                          ('move_id.state', '=', 'posted')
                          ]
                if line.employee_id:
                    domain.append(('employee_id','=',line.employee_id.id))
                if line.operating_unit_id:
                    domain.append(('operating_unit_id','=',line.operating_unit_id.id))
                if line.partner_id:
                    domain.append(('partner_id','=',line.partner_id.id))
                where_query = aml_obj._where_calc(domain)
                aml_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause

            self.env.cr.execute(select, where_clause_params)
            line.practical_amount = self.env.cr.fetchone()[0] or 0.0
