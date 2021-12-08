from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class AccountPayemntEXT(models.Model):
    _inherit = 'account.payment'



    is_statement_create = fields.Boolean('Statement Created', compute='compute_reconciled_statement_create', store=True)

    def action_post(self):
        res = super(AccountPayemntEXT, self).action_post()
        for rec in self:
            if rec.payment_type == 'inbound':
                rec.name = rec.journal_id.code + '/r/' + date.today().strftime('%y') + '/' + self.env[
                               'ir.sequence'].next_by_code('account.payment.sequence.receive') or _('New')
            else:
                rec.name = rec.journal_id.code + '/s/' + date.today().strftime('%y') + '/' + self.env[
                               'ir.sequence'].next_by_code('account.payment.sequence.send') or _('New')
            if rec.move_id and rec.move_id.line_ids:
                for line in rec.move_id.line_ids:
                    line.payment_ref = rec.payment_ref
                    line.check_ref = rec.check_num
        return res

    @api.depends('reconciled_statement_ids')
    def compute_reconciled_statement_create(self):
        for rec in self:
            is_statement_create = False
            if rec.reconciled_statements_count != 0:
                is_statement_create = True
            rec.is_statement_create = is_statement_create

    def create_statements(self):
        if 'draft' in self.mapped('state') or 'create' in self.mapped('state') or 'cancel' in self.mapped('state'):
            raise ValidationError(_('All payment should be in posted state!'))
        if self.mapped('reconciled_statement_ids'):
            raise ValidationError(_('Already reconciled!'))
        company_id = self.env.company.id
        journal = self.env['account.journal'].search([('type', '=', 'bank'), ('company_id', '=', company_id)], limit=1)
        last_ending_balance = self.env['account.bank.statement'].search([('state', '=', 'confirm'),('company_id', '=', company_id)], limit=1, order='id desc') and self.env['account.bank.statement'].search([('state', '=', 'confirm'),('company_id', '=', company_id)], limit=1, order='id desc').balance_end_real or 0.0
        vals = {
            'journal_id': journal.id,
            'date': fields.Date.today(),
            'company_id': self.env.company.id,
            'balance_start':last_ending_balance,
            'balance_end_real':last_ending_balance + sum(self.filtered(lambda x: x.payment_type == 'inbound' and  x.partner_type == 'customer').mapped('amount')) - sum(self.filtered(lambda x: x.payment_type == 'outbound' and  x.partner_type == 'supplier').mapped('amount')),
        }
        bank_statement = self.env['account.bank.statement'].create(vals)
        for rec in self:
            statement_line_id = self.env['account.bank.statement.line'].create({
                 'date':fields.Date.today(),
                 'payment_ref':self.name,
                 'statement_id': bank_statement.id,
                 'amount':rec.amount if rec.payment_type == 'inbound' and rec.partner_type == 'customer' else -(rec.amount),
             })
            statement_line_id.write({'partner_id':rec.partner_id and rec.partner_id.id or False})
        bank_statement.button_post()
        bank_statement.reconcile_entries()
        if bank_statement.state == 'posted':
            bank_statement.button_validate_or_action()
        return {
            'name': _('Bank Statement'),
            'view_mode': 'form',
            'res_model': 'account.bank.statement',
            'type': 'ir.actions.act_window',
            'res_id': bank_statement.id,
        }



