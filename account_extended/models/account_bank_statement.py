from odoo import api, models, _, fields

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'


    def reconcile_entries(self):
        for statement in self:
            for statement_line in statement.line_ids:
                datas = self.env['account.reconciliation.widget'].get_move_lines_for_bank_statement_line( statement_line.id, partner_id=statement_line.partner_id.id, excluded_ids=[], search_str=False, offset=0, limit=None, mode='rp')
                data_lines = []
                is_reconcile = False
                for data in datas:
                    if data.get('is_liquidity_line') and not is_reconcile:
                        is_reconcile = True
                        data_lines.append({
                            'partner_id':data.get('partner_id'),
                            'to_check':False,
                            'lines_vals_list':[{
                                'name':data.get('name'),
                                'balance':data.get('credit') if data.get('credit') > 0.0 else -(data.get('debit')),
                                'analytic_tag_ids':[[6,None,[]]],
                                'id':data.get('id'),
                                'currency_id':data.get('currency_id')
                            }],
                        })
                self.env['account.reconciliation.widget'].with_context({'active_model':'account.bank.statement','active_id':statement.id,'active_ids':statement.ids,'statement_line_ids':[statement_line.id],'force_price_include':True}).process_bank_statement_line([statement_line.id],data_lines)
