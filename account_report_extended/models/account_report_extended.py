from odoo import api, models, _, fields
# from odoo.tools import date_utils
# from odoo.osv import expression
#
# from odoo.tools import formatLang, format_date
# from odoo.addons.account_reports.models.formula import FormulaSolver, PROTECTED_KEYWORDS
# from odoo.http import request
# from collections import defaultdict

class AccountCashFlowReportInherit(models.AbstractModel):
    _inherit = 'account.cash.flow.report'

    filter_operating_unit = True

    @api.model
    def _get_columns_name(self, options):
        options['unhide_operating_unit'] = True
        columns = [{'name': ''}, {'name': _('Balance'), 'class': 'number'}]
        for operating_unit in options.get('selected_operating_unit'):
            columns.append({'name': _(operating_unit), 'class': 'number'})
        return columns

    def _get_columns_value(self, options=False):
        columns = [{'name': 0.0, 'class': 'number'}]
        if options and  options.get('operating_unit'):
            for operating in options.get('operating_unit'):
                columns.append({'name': 0.0, 'class': 'number'})
        return columns

    def _get_columns_value_with_data(self, options=False,value=[]):
        columns = []
        if options and  options.get('operating_unit') and value:
            for val in value:
                columns.append({'name': val, 'class': 'number'})
        return columns



    @api.model
    def _get_lines_to_compute(self, options):
        options['unhide_operating_unit'] = True
        return [
            {
                'id': 'cash_flow_line_%s' % index,
                'name': name,
                'level': level,
                'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
                'columns': self._get_columns_value(options),
            } for index, level, name in [

                #
                (0, 1, _('Operating Activities')),
                (1, 3, _('Net profit / (loss) for the year')),
                (2, 1, _('Adjustments')),
                (3, 3, _('Depreciation')),
                (4, 3, _('Allowance for doubtful debts - net')),
                (5, 3, _('Provision for employees end of service benefits')),
                (6, 3, _('Interest Income')),
                (7, 3, _('Finance costs')),
                (8, 3, _('Depreciation on ROU')),
                (9, 3, _('Gain on remeasurement of finance lease liability and finance lease liability')),
                (10, 0, _('Operating cash flows before working capital changes')),
                (11, 0, _('Net increase in cash and cash equivalents')),
                (12, 2, _('Cash flows from operating activities')),#11,
                (13, 3, _('Advance Payments received from customers')),
                (14, 3, _('Cash received from operating activities')),
                (15, 3, _('Advance payments made to suppliers')),
                (16, 3, _('Cash paid for operating activities')),
                (17, 2, _('Cash flows from investing & extraordinary activities')),
                (18, 3, _('Cash in')),
                (19, 3, _('Cash out')),
                (20, 2, _('Cash flows from financing activities')),
                (21, 3, _('Cash in')),
                (22, 3, _('Cash out')),
                (23, 2, _('Cash flows from unclassified activities')),
                (24, 3, _('Cash in')),
                (25, 3, _('Cash out')),
                (26, 0, _('Cash and cash equivalents, beginning of period')),
                (27, 0, _('Cash and cash equivalents, closing balance')),

            ]
        ]

    # @api.model
    # def _compute_liquidity_balance(self, options, currency_table_query, payment_account_ids):
    #     ''' Compute the balance of all liquidity accounts to populate the following sections:
    #         'Cash and cash equivalents, beginning of period' and 'Cash and cash equivalents, closing balance'.
    #
    #     :param options:                 The report options.
    #     :param currency_table_query:    The custom query containing the multi-companies rates.
    #     :param payment_account_ids:     A tuple containing all account.account's ids being used in a liquidity journal.
    #     :return:                        A list of tuple (account_id, account_code, account_name, balance).
    #     '''
    #     data_list = super(AccountCashFlowReportInherit, self)._compute_liquidity_balance(options=options,currency_table_query=currency_table_query,payment_account_ids=payment_account_ids)
    #     new_options = self._get_options_current_period(options)
    #     if new_options.get('operating_unit') and data_list:
    #         for operating_unit in new_options.get('operating_unit'):
    #             operating_unit_options = new_options.copy()
    #             operating_unit_options['operating_unit'] = [operating_unit]
    #             tables, where_clause, where_params = self._query_get(operating_unit_options,
    #                                                                  domain=[('account_id', 'in', payment_account_ids)])
    #             query = '''
    #                         SELECT
    #                             account_move_line.account_id,
    #                             account.code AS account_code,
    #                             account.name AS account_name,
    #                             SUM(ROUND(account_move_line.balance * currency_table.rate, currency_table.precision))
    #                         FROM ''' + tables + '''
    #                         JOIN account_account account ON account.id = account_move_line.account_id
    #                         LEFT JOIN ''' + currency_table_query + ''' ON currency_table.company_id = account_move_line.company_id
    #                         WHERE ''' + where_clause + '''
    #                         GROUP BY account_move_line.account_id, account.code, account.name
    #                     '''
    #             self._cr.execute(query, where_params)
    #             data = self._cr.fetchall()
    #             if data:
    #                 data_list.append(data[0])
    #             else:
    #                 data_list.append()
    #     return data_list


    @api.model
    def _get_lines(self, options, line_id=None):


        def _insert_at_index(index, account_id, account_code, account_name, amount,options,list_index = 0):
            ''' Insert the amount in the right section depending the line's index and the account_id. '''
            # Helper used to add some values to the report line having the index passed as parameter
            # (see _get_lines_to_compute).
            line = lines_to_compute[index]

            if self.env.company.currency_id.is_zero(amount):
                return
            # if not line.get('unfolded_lines'):
            line.setdefault('unfolded_lines', {})
            line['unfolded_lines'].setdefault(account_id, {
                'id': account_id,
                'name': '%s %s' % (account_code, account_name),
                'level': line['level'] + 1,
                'parent_id': line['id'],
                'columns': self._get_columns_value(options),
                'caret_options': 'account.account',
            })
            line['columns'][list_index]['name'] += amount
            line['unfolded_lines'][account_id]['columns'][list_index]['name'] += amount

        def _dispatch_result(account_id, account_code, account_name, account_internal_type, amount,list_index = 0):
            ''' Dispatch the newly fetched line inside the right section. '''

            if account_id in self.env.company.depreciation_ids.ids:
                _insert_at_index(3, account_id, account_code, account_name, amount,options,list_index)
            if account_id in self.env.company.allowance_doubtful_ids.ids:
                _insert_at_index(4, account_id, account_code, account_name, amount,options,list_index)
            if account_id in self.env.company.provision_employee_ids.ids:
                _insert_at_index(5, account_id, account_code, account_name, amount,options,list_index)
            if account_id in self.env.company.interest_income_ids.ids:
                _insert_at_index(6, account_id, account_code, account_name, -amount,options,list_index)
            if account_id in self.env.company.finance_cost_ids.ids:
                _insert_at_index(7, account_id, account_code, account_name, amount,options,list_index)
            if account_id in self.env.company.depriciation_rou_ids.ids:
                _insert_at_index(8, account_id, account_code, account_name, amount,options,list_index)
            if account_id in self.env.company.gain_remeausement_ids.ids:
                _insert_at_index(9, account_id, account_code, account_name, -amount,options,list_index)
            if account_internal_type == 'receivable':
                # 'Advance Payments received from customers'                (index=3)
                _insert_at_index(13, account_id, account_code, account_name, -amount,options,list_index)
            elif account_internal_type == 'payable':
                # 'Advance Payments made to suppliers'                      (index=5)
                _insert_at_index(15, account_id, account_code, account_name, -amount,options,list_index)
            elif amount < 0:
                if tag_operating_id in tags_per_account.get(account_id, []):
                    # 'Cash received from operating activities'             (index=4)
                    _insert_at_index(14, account_id, account_code, account_name, -amount,options,list_index)
                elif tag_investing_id in tags_per_account.get(account_id, []):
                    # 'Cash in for investing activities'                    (index=8)
                    _insert_at_index(18, account_id, account_code, account_name, -amount,options,list_index)
                elif tag_financing_id in tags_per_account.get(account_id, []):
                    # 'Cash in for financing activities'                    (index=11)
                    _insert_at_index(21, account_id, account_code, account_name, -amount,options,list_index)
                else:
                    # 'Cash in for unclassified activities'                 (index=14)
                    _insert_at_index(24, account_id, account_code, account_name, -amount,options,list_index)
            elif amount > 0:
                if tag_operating_id in tags_per_account.get(account_id, []):
                    # 'Cash paid for operating activities'                  (index=6)
                    _insert_at_index(16, account_id, account_code, account_name, -amount,options,list_index)
                elif tag_investing_id in tags_per_account.get(account_id, []):
                    # 'Cash out for investing activities'                   (index=9)
                    _insert_at_index(19, account_id, account_code, account_name, -amount,options,list_index)
                elif tag_financing_id in tags_per_account.get(account_id, []):
                    # 'Cash out for financing activities'                   (index=12)
                    _insert_at_index(22, account_id, account_code, account_name, -amount,options,list_index)
                else:
                    # 'Cash out for unclassified activities'                (index=15)
                    _insert_at_index(25, account_id, account_code, account_name, -amount,options,list_index)

        self.flush()

        unfold_all = self._context.get('print_mode') or options.get('unfold_all')
        currency_table_query = self.env['res.currency']._get_query_currency_table(options)
        lines_to_compute = self._get_lines_to_compute(options)

        tag_operating_id = self.env.ref('account.account_tag_operating').id
        tag_investing_id = self.env.ref('account.account_tag_investing').id
        tag_financing_id = self.env.ref('account.account_tag_financing').id
        tag_ids = (tag_operating_id, tag_investing_id, tag_financing_id)
        tags_per_account = self._get_tags_per_account(options, tag_ids)

        payment_move_ids, payment_account_ids = self._get_liquidity_move_ids(options)

        # Compute 'Cash and cash equivalents, beginning of period'      (index=0)
        beginning_period_options = self._get_options_beginning_period(options)
        for account_id, account_code, account_name, balance in self._compute_liquidity_balance(beginning_period_options,
                                                                                               currency_table_query,
                                                                                               payment_account_ids):
            _insert_at_index(26, account_id, account_code, account_name, balance,options)
            _insert_at_index(27, account_id, account_code, account_name, balance,options)

        # Compute 'Cash and cash equivalents, closing balance'          (index=16)
        for account_id, account_code, account_name, balance in self._compute_liquidity_balance(options,
                                                                                               currency_table_query,
                                                                                               payment_account_ids):
            _insert_at_index(27, account_id, account_code, account_name, balance,options)

        # ==== Process liquidity moves ====
        res = self._get_liquidity_move_report_lines(options, currency_table_query, payment_move_ids,
                                                    payment_account_ids)
        for account_id, account_code, account_name, account_internal_type, amount in res:
            _dispatch_result(account_id, account_code, account_name, account_internal_type, amount)

        # ==== Process reconciled moves ====
        res = self._get_reconciled_move_report_lines(options, currency_table_query, payment_move_ids,
                                                     payment_account_ids)
        for account_id, account_code, account_name, account_internal_type, balance in res:
            _dispatch_result(account_id, account_code, account_name, account_internal_type, balance)

        #new
        i=1
        operating_unit_options = options.copy()
        if options.get('operating_unit'):
            for operating_unit in  options.get('operating_unit'):
                operating_unit_options['operating_unit']=[operating_unit]
                payment_move_ids, payment_account_ids = self._get_liquidity_move_ids(operating_unit_options)

                # Compute 'Cash and cash equivalents, beginning of period'      (index=0)
                beginning_period_options = self._get_options_beginning_period(operating_unit_options)
                for account_id, account_code, account_name, balance in self._compute_liquidity_balance(beginning_period_options,
                                                                                                       currency_table_query,
                                                                                                       payment_account_ids):
                    _insert_at_index(26, account_id, account_code, account_name, balance, options,i)
                    _insert_at_index(27, account_id, account_code, account_name, balance, options,i)

                # Compute 'Cash and cash equivalents, closing balance'          (index=16)
                for account_id, account_code, account_name, balance in self._compute_liquidity_balance(operating_unit_options,
                                                                                                       currency_table_query,
                                                                                                       payment_account_ids):
                    _insert_at_index(27, account_id, account_code, account_name, balance, options,i)

                # ==== Process liquidity moves ====
                res = self._get_liquidity_move_report_lines(operating_unit_options, currency_table_query, payment_move_ids,
                                                            payment_account_ids)
                for account_id, account_code, account_name, account_internal_type, amount in res:
                    _dispatch_result(account_id, account_code, account_name, account_internal_type, amount,i)

                # ==== Process reconciled moves ====
                res = self._get_reconciled_move_report_lines(operating_unit_options, currency_table_query, payment_move_ids,
                                                             payment_account_ids)
                for account_id, account_code, account_name, account_internal_type, balance in res:
                    _dispatch_result(account_id, account_code, account_name, account_internal_type, balance,i)
                i+=1


        profit_and_loss_report_obj = self.env.ref('account_reports.account_financial_report_profitandloss0')
        profit_loss_options = profit_and_loss_report_obj._get_options()
        profit_loss_options['multi_company'] = options.get('multi_company')
        profit_loss_options['date'] = options['date']
        profit_loss_options['all_entries'] = options['all_entries']
        profit_loss_options['filter_operating_unit'] = options['filter_operating_unit']
        profit_loss_options['operating_unit'] = options.get('operating_unit')
        profit_loss_options['selected_operating_unit'] = options['selected_operating_unit']
        profit_loss_options['filter_operating_unit'] = options['filter_operating_unit']
        profit_loss_options['unfold_all'] = options['unfold_all']
        profit_header, profit_lines = profit_and_loss_report_obj.with_context(from_cash_flow=True)._get_table(profit_loss_options)
        net_profit_amount = next(item for item in profit_lines if item["id"] == 1).get('columns')[0].get('no_format') or 0.0
        # Operating Activities
        lines_to_compute[0]['columns'][0]['name'] = lines_to_compute[1]['columns'][0]['name'] = net_profit_amount

        i=1
        profit_loss_options_new = profit_loss_options.copy()
        if options.get('operating_unit'):
            for operating_unit in  options.get('operating_unit'):
                profit_loss_options_new['operating_unit'] = [operating_unit]
                profit_header, profit_lines = profit_and_loss_report_obj.with_context(from_cash_flow=True)._get_table(
                    profit_loss_options_new)
                net_profit_amount = next(item for item in profit_lines if item["id"] == 1).get('columns')[0].get(
                    'no_format') or 0.0
                # Operating Activities
                lines_to_compute[0]['columns'][i]['name'] = lines_to_compute[1]['columns'][i][
                    'name'] = net_profit_amount
                i+=1
        lenght_operating_unit = len(options.get('operating_unit'))+1 if options.get('operating_unit') else 1
        for i in range(lenght_operating_unit):
            # Adjustments
            lines_to_compute[2]['columns'][i]['name'] = \
                lines_to_compute[3]['columns'][i]['name'] + \
                lines_to_compute[4]['columns'][i]['name'] + \
                lines_to_compute[5]['columns'][i]['name'] + \
                lines_to_compute[6]['columns'][i]['name'] + \
                lines_to_compute[7]['columns'][i]['name'] + \
                lines_to_compute[8]['columns'][i]['name'] + \
                lines_to_compute[9]['columns'][i]['name']
            # 'Operating cash flows before working capital changes'                            (index=2)
            lines_to_compute[10]['columns'][i]['name'] = \
                lines_to_compute[0]['columns'][i]['name'] + \
                lines_to_compute[2]['columns'][i]['name']
            # 'Cash flows from operating activities'                            (index=2)
            lines_to_compute[12]['columns'][i]['name'] = \
                lines_to_compute[13]['columns'][i]['name'] + \
                lines_to_compute[14]['columns'][i]['name'] + \
                lines_to_compute[15]['columns'][i]['name'] + \
                lines_to_compute[16]['columns'][i]['name']
            # 'Cash flows from investing & extraordinary activities'            (index=7)
            lines_to_compute[17]['columns'][i]['name'] = \
                lines_to_compute[18]['columns'][i]['name'] + \
                lines_to_compute[19]['columns'][i]['name']
            # 'Cash flows from financing activities'                            (index=10)
            lines_to_compute[20]['columns'][i]['name'] = \
                lines_to_compute[21]['columns'][i]['name'] + \
                lines_to_compute[22]['columns'][i]['name']
            # 'Cash flows from unclassified activities'                         (index=13)
            lines_to_compute[23]['columns'][i]['name'] = \
                lines_to_compute[24]['columns'][i]['name'] + \
                lines_to_compute[25]['columns'][i]['name']
            # 'Net increase in cash and cash equivalents'                       (index=1)
            lines_to_compute[11]['columns'][i]['name'] = \
                lines_to_compute[12]['columns'][i]['name'] + \
                lines_to_compute[17]['columns'][i]['name'] + \
                lines_to_compute[20]['columns'][i]['name'] + \
                lines_to_compute[23]['columns'][i]['name']



        # ==== Compute the unexplained difference ====

        closing_ending_gap = [lines_to_compute[27]['columns'][i]['name'] - lines_to_compute[26]['columns'][i]['name'] + lines_to_compute[10]['columns'][i]['name'] for i in range(lenght_operating_unit)]
        computed_gap = [sum(lines_to_compute[index]['columns'][i]['name'] for index in [10,12, 17, 20, 23]) for i in range(lenght_operating_unit)]
        delta = [closing_ending_gap[i] - computed_gap[i] for i in range(lenght_operating_unit)]
        for i in range(lenght_operating_unit):
            lines_to_compute[27]['columns'][i]['name']+=lines_to_compute[10]['columns'][i]['name']
        if not self.env.company.currency_id.is_zero(delta and delta[0]):
            lines_to_compute.insert(27, {
                'id': 'cash_flow_line_unexplained_difference',
                'name': _('Unexplained Difference'),
                'level': 0,
                'columns': self._get_columns_value_with_data(options,delta),
            })

        # ==== Build final lines ====

        lines = []
        for line in lines_to_compute:
            unfolded_lines = line.pop('unfolded_lines', {})
            sub_lines = [unfolded_lines[k] for k in sorted(unfolded_lines)]

            line['unfoldable'] = len(sub_lines) > 0
            line['unfolded'] = line['unfoldable'] and (unfold_all or line['id'] in options['unfolded_lines'])

            # Header line.
            for columns in line['columns']:
                columns['name'] = self.format_value(columns['name'])

            lines.append(line)

            # Sub lines.
            for sub_line in sub_lines:
                for columns in sub_line['columns']:
                    columns['name'] = self.format_value(columns['name'])
                sub_line['style'] = '' if line['unfolded'] else 'display: none;'
                lines.append(sub_line)

            # Total line.
            if line['unfoldable']:
                lines.append({
                    'id': '%s_total' % line['id'],
                    'name': _('Total') + ' ' + line['name'],
                    'level': line['level'] + 1,
                    'parent_id': line['id'],
                    'columns': line['columns'],
                    'class': 'o_account_reports_domain_total',
                    'style': '' if line['unfolded'] else 'display: none;',
                })
        return lines