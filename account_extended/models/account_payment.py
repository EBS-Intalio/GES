from odoo import api, models, _, fields



class AccountPayemntEXT(models.Model):
    _inherit = 'account.payment'

    is_statement_create = fields.Boolean('Statement Created', compute='compute_reconciled_statement_create', store=True)

    @api.depends('reconciled_statement_ids')
    def compute_reconciled_statement_create(self):
        for rec in self:
            is_statement_create = False
            if rec.reconciled_statements_count != 0:
                is_statement_create = True
            rec.is_statement_create = is_statement_create


    def create_statements(self):
        company_id = self.env.company.id
        journals = self.env['account.journal'].search([('type', '=', 'bank'), ('company_id', '=', company_id)])
        if journals:
            journal =  journals[0]
        data_list = []
        for rec in self:
            data_list.append(
                (0,0,
                 {
                     'date':fields.Date.today(),
                     'payment_ref':'Payment',
                     'partner_id':rec.partner_id and rec.partner_id.id,
                     'amount':rec.amount if rec.payment_type == 'inbound' and rec.partner_type == 'customer' else -(rec.amount),
                 }
                 )
            )
        last_ending_balance = self.env['account.bank.statement'].search([('state', '=', 'confirm')], limit=1, order='id desc') and self.env['account.bank.statement'].search([('state', '=', 'confirm')], limit=1, order='id desc').balance_end_real or 0.0
        vals = {
            'journal_id': journal.id,
            'date': fields.Date.today(),
            'company_id': self.env.company.id,
            'line_ids':data_list,
            'balance_start':last_ending_balance,
            'balance_end_real':last_ending_balance + sum(self.filtered(lambda x: x.payment_type == 'inbound' and  x.partner_type == 'customer').mapped('amount')) - sum(self.filtered(lambda x: x.payment_type == 'outbound' and  x.partner_type == 'supplier').mapped('amount')),
        }
        bank_statement = self.env['account.bank.statement'].create(vals)
        print(bank_statement)
        return {
            'name': _('Bank Statement'),
            'view_mode': 'form',
            'res_model': 'account.bank.statement',
            'type': 'ir.actions.act_window',
            'res_id': bank_statement.id,
        }



