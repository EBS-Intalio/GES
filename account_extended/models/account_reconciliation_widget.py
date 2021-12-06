from odoo import api, fields, models, _

class AccountReconciliationExtended(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    @api.model
    def _prepare_js_reconciliation_widget_move_line(self, statement_line, line,recs_count=0):
        js_vals = super(AccountReconciliationExtended, self)._prepare_js_reconciliation_widget_move_line(statement_line=statement_line,line=line,recs_count=recs_count)
        js_vals.update({
            'payment_ref': line.payment_ref or '',
            'check_ref': line.check_ref or '',
        })
        return js_vals
