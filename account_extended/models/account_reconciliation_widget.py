from odoo import api, fields, models, _
from odoo.tools.misc import  parse_date

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

    def _str_domain_for_mv_line(self, search_str):
        return [
            '|', ('payment_ref', 'ilike', search_str),
            '|',('check_ref','ilike',search_str),
            '|', ('account_id.code', 'ilike', search_str),
            '|', ('move_id.name', 'ilike', search_str),
            '|', ('move_id.ref', 'ilike', search_str),
            '|', ('date_maturity', 'like', parse_date(self.env, search_str)),
            '&', ('name', '!=', '/'), ('name', 'ilike', search_str),
        ]

    @api.model
    def get_move_lines_for_bank_statement_line(self, st_line_id, partner_id=None, excluded_ids=None, search_str=False,
                                               offset=0, limit=None, mode=None):
        """ Returns move lines for the bank statement reconciliation widget,
            formatted as a list of dicts

            :param st_line_id: ids of the statement lines
            :param partner_id: optional partner id to select only the moves
                line corresponding to the partner
            :param excluded_ids: optional move lines ids excluded from the
                result
            :param search_str: optional search (can be the amout, display_name,
                partner name, move line name)
            :param offset: offset of the search result (to display pager)
            :param limit: number of the result to search
            :param mode: 'rp' for receivable/payable or 'other'
        """

        statement_line = self.env['account.bank.statement.line'].browse(st_line_id)

        if search_str:
            domain = self._get_search_domain(search_str=search_str)
        else:
            domain = []

        if partner_id:
            domain.append(('partner_id', '=', partner_id))

        if excluded_ids:
            domain.append(('id', 'not in', tuple(excluded_ids)))

        if mode == 'rp':
            query, params = self._get_query_reconciliation_widget_customer_vendor_matching_lines(statement_line,
                                                                                                 domain=domain)
        else:
            query, params = self._get_query_reconciliation_widget_miscellaneous_matching_lines(statement_line,
                                                                                               domain=domain)

        trailing_query, trailing_params = self._get_trailing_query(statement_line, limit=limit, offset=offset)

        self._cr.execute(query + trailing_query, params + trailing_params)
        results = self._cr.dictfetchall()
        if results:
            recs_count = results[0].get('full_count', 0)
        else:
            recs_count = 0


        move_lines = self.env['account.move.line'].browse(res['id'] for res in results)
        if self._context and self._context.get('filter_head'):
            reverse = False
            if self._context.get('filter_head_asc_desc') and self._context.get('filter_head_asc_desc') == 'desc':
                reverse = True
            if self._context.get('filter_head') == 'date':
                move_lines = move_lines.sorted(lambda x: x.date_maturity or x.date, reverse=reverse)
            if self._context.get('filter_head') == 'code':
                move_lines = move_lines.sorted(lambda x: x.account_id.code or x.date, reverse=reverse)
            # if self._context.get('filter_head') == 'label':
            #     move_lines = move_lines.sorted(lambda x: (x.partner_id and x.partner_id.name) or x.name or x.ref or x.payment_ref or x.check_ref, reverse=reverse)

        js_vals_list = []
        for line in move_lines:
            js_vals_list.append(
                self._prepare_js_reconciliation_widget_move_line(statement_line, line, recs_count=recs_count))
        return js_vals_list
