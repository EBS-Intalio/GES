from odoo import api, models, _, fields
from odoo.tools import date_utils

from odoo.tools import formatLang
from odoo.addons.account_reports.models.formula import FormulaSolver, PROTECTED_KEYWORDS


class AccountReportExtended(models.AbstractModel):
    _inherit = 'account.report'

    filter_currency = None

    @api.model
    def _get_filter_currency(self):
        return self.env['res.currency'].sudo().search([
            ('active', '=', True), ('id', '!=', self.env.company.currency_id.id)])

    @api.model
    def _init_filter_date(self, options, previous_options=None):
        if self.filter_date is None:
            return

        # Default values.
        mode = self.filter_date.get('mode', 'range')
        options_filter = self.filter_date.get('filter') or ('today' if mode == 'single' else 'fiscalyear')
        date_from = self.filter_date.get('date_from') and fields.Date.from_string(self.filter_date['date_from'])
        date_to = self.filter_date.get('date_to') and fields.Date.from_string(self.filter_date['date_to'])
        strict_range = (previous_options and previous_options.get('date', {}).get('strict_range')) or False
        # Handle previous_options.
        if previous_options and previous_options.get('date') and previous_options['date'].get('filter') \
                and not (previous_options['date']['filter'] == 'today' and mode == 'range'):

            options_filter = previous_options['date']['filter']
            if options_filter == 'custom':
                if previous_options['date']['date_from'] and mode == 'range':
                    date_from = fields.Date.from_string(previous_options['date']['date_from'])
                if previous_options['date']['date_to']:
                    date_to = fields.Date.from_string(previous_options['date']['date_to'])
        if previous_options and previous_options.get('currency'):
            currency_map = dict((opt['id'], opt['selected']) for opt in previous_options['currency'] if
                                opt['id'] != 'divider' and 'selected' in opt)
        else:
            currency_map = {}
        options['currency'] = []

        # Create date option for each company.
        period_type = False
        if 'today' in options_filter:
            date_to = fields.Date.context_today(self)
            date_from = date_utils.get_month(date_to)[0]
        elif 'month' in options_filter:
            date_from, date_to = date_utils.get_month(fields.Date.context_today(self))
            period_type = 'month'
        elif 'quarter' in options_filter:
            date_from, date_to = date_utils.get_quarter(fields.Date.context_today(self))
            period_type = 'quarter'
        elif 'year' in options_filter:
            company_fiscalyear_dates = self.env.company.compute_fiscalyear_dates(fields.Date.context_today(self))
            date_from = company_fiscalyear_dates['date_from']
            date_to = company_fiscalyear_dates['date_to']
        elif not date_from:
            # options_filter == 'custom' && mode == 'single'
            date_from = date_utils.get_month(date_to)[0]

        options['date'] = self._get_dates_period(options, date_from, date_to, mode, period_type=period_type,
                                                 strict_range=strict_range)
        currencies = []
        currencies.append(self._get_filter_currency().ids)
        if 'last' in options_filter:
            options['date'] = self._get_dates_previous_period(options, options['date'])
        options['date']['filter'] = options_filter
        for c in self._get_filter_currency():
            options['currency'].append({
                'id': c.id,
                'name': c.name,
                'selected': currency_map.get(c.id, c.id in currencies),
            })


class ReportAccountFinancialReportExtended(models.Model):
    _inherit = "account.financial.html.report"

    def _build_headers_hierarchy(self, options_list, groupby_keys):

        groupby_list = self._get_options_groupby_fields(options_list[0])

        keys_grouped_by_ids = [set() for gb in groupby_list]
        for key in groupby_keys:
            # Skip the first element that is the period number.
            # All comparisons must have the same headers.
            for i, value in enumerate(key[1:]):
                if value is not None:
                    keys_grouped_by_ids[i].add(value)

        sorting_map = [{i: (i, self.format_date(options)) for i, options in enumerate(options_list)}]
        for groupby, ids_set in zip(groupby_list, keys_grouped_by_ids):
            groupby_field = self.env['account.move.line']._fields[groupby]
            values_map = {None: (len(ids_set) + 1, _('Undefined'))}
            if groupby_field.relational:
                # Preserve the table order by using search instead of browse.
                sorted_records = self.env[groupby_field.comodel_name].search([('id', 'in', tuple(ids_set))])
                index = 0
                for record, name_get_res in zip(sorted_records, sorted_records.name_get()):
                    values_map[record.id] = (index, name_get_res[1])
                    index += 1
            else:
                # Sort the keys in a lexicographic order.
                if groupby_field.name == 'date':
                    format_func = lambda v: fields.Date.to_string(v)
                elif groupby_field.name == 'datetime':
                    format_func = lambda v: fields.Datetime.to_string(v)
                else:
                    format_func = lambda v: v
                for i, v in enumerate(sorted(list(ids_set))):
                    values_map[v] = (i, format_func(v))
            sorting_map.append(values_map)

        def _create_headers_hierarchy(level_keys, level=0, options=options_list):
            current_node = {}
            for key in level_keys:
                current_node.setdefault(key[0], set())
                sub_key = key[1:]
                if sub_key:
                    current_node[key[0]].add(sub_key)
            headers = [{
                'name': sorting_map[level][key][1],
                'colspan': len(sub_keys) or 1,
                'children': _create_headers_hierarchy(sub_keys, level=level + 1) if sub_keys else None,
                'key': key,
                'class': 'number'
            } for key, sub_keys in current_node.items()]
            headers = sorted(headers, key=lambda header: sorting_map[level][header['key']][0])
            i = 1
            options[0]['unhide_currency'] = True
            if options[0].get('comparison').get('filter') != 'no_comparison':
                options[0]['unhide_currency'] = False
                for cur in options[0].get('currency'):
                    cur['selected'] = False

            for currency in options[0].get('currency'):
                if currency.get('selected'):
                    headers.append({'name': currency.get('name'),
                                    'colspan': 1,
                                    'key': i,
                                    'class': 'number',
                                    'children': None})
                    i += 1
            return headers

        level_keys = [(0,) + key[1:] for key in groupby_keys] or [(0,)]
        headers_hierarchy = _create_headers_hierarchy(set(level_keys))

        headers = [[] for i in range(len(groupby_list) + 1)]
        sorted_groupby_keys = []

        def _populate_headers(current_node, current_key=[], level=0):
            headers[level] += current_node
            for header in current_node:
                children = header.pop('children')
                if children:
                    _populate_headers(children, current_key + [header['key']], level=level + 1)
                else:
                    sorted_groupby_keys.append(tuple(current_key + [header['key']]))

        _populate_headers(headers_hierarchy)

        # Add empty header if there is no data.
        for j in range(1, len(headers)):
            if not headers[j]:
                headers[j].append({'name': '', 'class': 'number', 'colspan': 1})

        additional_sorted_groupby_keys = []
        additional_headers = [[] for i in range(len(groupby_list) + 1)]
        for i, options in enumerate(options_list):
            if i == 0:
                # Current period.
                headers[0][0]['name'] = sorting_map[0][0][1]
            else:
                for j in range(len(headers)):
                    if j == 0:
                        additional_headers[j].append(headers[j][-1].copy())
                    else:
                        additional_headers[j] += headers[j]
                additional_headers[0][-1]['name'] = sorting_map[0][i][1]
                for key in sorted_groupby_keys:
                    new_key = list(key)
                    new_key[0] = i
                    additional_sorted_groupby_keys.append(tuple(new_key))
        sorted_groupby_keys += additional_sorted_groupby_keys
        for i, headers_row in enumerate(additional_headers):
            headers[i] += headers_row

        # Add left unnamed header.
        for i in range(len(headers)):
            headers[i] = [{'name': '', 'class': 'number', 'colspan': 1}] + headers[i]

        # Manage the growth comparison feature.
        if self._display_growth_comparison(options_list[0]):
            headers[0].append({'name': '%', 'class': 'number', 'colspan': 1})

        # Manage the debug info columns.
        if self._display_debug_info(options_list[0]):
            for i in range(len(headers)):
                if i == 0:
                    headers[i].append({
                        'template': 'account_reports.cell_template_show_bug_financial_reports',
                        'style': 'width: 1%; text-align: right;',
                    })
                else:
                    headers[i].append({'name': '', 'style': 'width: 1%; text-align: right;'})

        return headers, sorted_groupby_keys

    @api.model
    def _get_financial_line_report_line(self, options, financial_line, solver, groupby_keys):

        results = solver.get_results(financial_line)['formula']

        is_leaf = solver.is_leaf(financial_line)
        has_lines = solver.has_move_lines(financial_line)
        has_something_to_unfold = is_leaf and has_lines and bool(financial_line.groupby)

        # Compute if the line is unfoldable or not.
        is_unfoldable = has_something_to_unfold and financial_line.show_domain == 'foldable'

        # Compute if the line is unfolded or not.
        # /!\ Take care about the case when the line is unfolded but not unfoldable with show_domain == 'always'.
        if not has_something_to_unfold or financial_line.show_domain == 'never':
            is_unfolded = False
        elif financial_line.show_domain == 'always':
            is_unfolded = True
        elif financial_line.show_domain == 'foldable' and financial_line.id in options['unfolded_lines']:
            is_unfolded = True
        else:
            is_unfolded = False

        # Standard columns.
        columns = []
        for key in groupby_keys:
            amount = results.get(key, 0.0)
            columns.append(
                {'name': self._format_cell_value(financial_line, amount), 'no_format': amount, 'class': 'number'})

        i = 1
        for curr in options.get('currency'):
            if curr.get('selected'):
                amount = self.get_multi_currency_balance(columns[0].get('no_format'), curr.get('id'))

                columns[i].update(amount)
                i += 1

        # Growth comparison column.
        if self._display_growth_comparison(options):
            columns.append(self._compute_growth_comparison_column(options,
                                                                  columns[0]['no_format'],
                                                                  columns[1]['no_format'],
                                                                  green_on_positive=financial_line.green_on_positive
                                                                  ))

        # Debug info columns.
        if self._display_debug_info(options):
            columns.append(self._compute_debug_info_column(options, solver, financial_line))

        financial_report_line = {
            'id': financial_line.id,
            'name': financial_line.name,
            'level': financial_line.level,
            'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
            'columns': columns,
            'unfoldable': is_unfoldable,
            'unfolded': is_unfolded,
            'page_break': financial_line.print_on_new_page,
            'action_id': financial_line.action_id.id,
        }

        # Custom caret_options for tax report.
        if self.tax_report and financial_line.domain and not financial_line.action_id:
            financial_report_line['caret_options'] = 'tax.report.line'

        return financial_report_line

    @api.model
    def _get_financial_aml_report_line(self, options, financial_line, groupby_id, display_name, results, groupby_keys):

        # Standard columns.
        columns = []
        for key in groupby_keys:
            amount = results.get(key, 0.0)
            columns.append(
                {'name': self._format_cell_value(financial_line, amount), 'no_format': amount, 'class': 'number'})

        i = 1
        for curr in options.get('currency'):
            if curr.get('selected'):
                amount = self.get_multi_currency_balance(columns[0].get('no_format'), curr.get('id'))
                columns[i].update(amount)
                i += 1

        # Growth comparison column.
        if self._display_growth_comparison(options):
            columns.append(self._compute_growth_comparison_column(options,
                                                                  columns[0]['no_format'],
                                                                  columns[1]['no_format'],
                                                                  green_on_positive=financial_line.green_on_positive
                                                                  ))

        if self._display_debug_info(options):
            columns.append({'name': '', 'style': 'width: 1%;'})

        return {
            'id': 'financial_report_group_%s_%s' % (financial_line.id, groupby_id),
            'name': display_name,
            'level': financial_line.level + 1,
            'parent_id': financial_line.id,
            'caret_options': financial_line.groupby == 'account_id' and 'account.account' or financial_line.groupby,
            'columns': columns,
        }

    def _get_table(self, options):

        self.ensure_one()

        options_list = self._get_options_periods_list(options)
        formula_solver = FormulaSolver(options_list, self)
        financial_lines = self.env['account.financial.html.report.line'].search([('id', 'child_of', self.line_ids.ids)])
        formula_solver.fetch_lines(financial_lines)
        groupby_keys = formula_solver.get_keys()
        headers, sorted_groupby_keys = self._build_headers_hierarchy(options_list, groupby_keys)
        lines = self._build_lines_hierarchy(options_list, self.line_ids, formula_solver, sorted_groupby_keys)

        options['sorted_groupby_keys'] = sorted_groupby_keys

        return headers, lines

    def get_multi_currency_balance(self, balance, currency, date=False):
        """
        Returns the computed balance for the selected currency.
        """
        date = date or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        company_currency = self.env.company.currency_id
        currency_id = self.env['res.currency'].browse(currency)
        multi_currency_amount = company_currency._convert(balance, currency_id, company, date)
        return {'name': formatLang(self.env, multi_currency_amount, currency_obj=currency_id),
                'no_format': multi_currency_amount}
