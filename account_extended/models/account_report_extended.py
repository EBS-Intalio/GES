from odoo import api, models, _, fields
from odoo.tools import date_utils
from odoo.osv import expression
import ast
from odoo.addons.web.controllers.main import clean_action
from odoo.tools import formatLang, format_date
from odoo.addons.account_reports.models.formula import FormulaSolver, PROTECTED_KEYWORDS
from odoo.http import request
from collections import defaultdict

MAX_NAME_LENGTH = 50


class AccountReportExtended(models.AbstractModel):
    _inherit = 'account.report'

    filter_currency = None
    filter_operating_unit = None

    @api.model
    def _init_filter_operating_unit(self, options, previous_options=None):
        if not self.filter_operating_unit:
            return
        options['filter_operating_unit'] = True
        previous_accounts = (previous_options or {}).get('operating_unit', [])
        operating_unit_ids = [int(x) for x in previous_accounts]
        selected_operating_unit = self.env['operating.unit'].search([('id', 'in', operating_unit_ids)])
        options['operating_unit'] = selected_operating_unit.ids
        options['selected_operating_unit'] = selected_operating_unit.mapped('name')


    def get_report_informations(self, options):
        if options and options.get('operating_unit') is not None:
            options['selected_operating_unit'] = [self.env['operating.unit'].browse(int(operating_unit_id)).name for
                                                  operating_unit_id in options['operating_unit']]

        return super(AccountReportExtended, self).get_report_informations(options=options)




    @api.model
    def _get_options_operating_unit_domain(self, options):
        domain = []
        if options.get('operating_unit'):
            operating_unit_ids = [int(acc) for acc in options['operating_unit']]
            domain.append(('operating_unit_id', 'in', operating_unit_ids))
        return domain

    @api.model
    def _get_options_domain(self, options):
        domain = super(AccountReportExtended, self)._get_options_domain(options=options)
        domain += self._get_options_operating_unit_domain(options)
        return domain



    def open_journal_items(self, options, params):
        action = super(AccountReportExtended, self).open_journal_items(options=options,params=params)
        if action and options.get('operating_unit'):
            domain = action['domain']
            operating_unit_ids = [int(r) for r in options['operating_unit']]
            domain = expression.AND([domain, [('operating_unit_id', 'in', operating_unit_ids)]])
            action['domain'] = domain
        return action


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

    @api.model
    def _create_hierarchy(self, lines, options):
        """Compute the hierarchy based on account groups when the option is activated.

        The option is available only when there are account.group for the company.
        It should be called when before returning the lines to the client/templater.
        The lines are the result of _get_lines(). If there is a hierarchy, it is left
        untouched, only the lines related to an account.account are put in a hierarchy
        according to the account.group's and their prefixes.
        """
        options['curr_model'] = self._context.get('model')
        unfold_all = self.env.context.get('print_mode') and len(options.get('unfolded_lines')) == 0 or options.get(
            'unfold_all')

        def add_to_hierarchy(lines, key, level, parent_id, hierarchy_parent, hierarchy):
            val_dict = hierarchy[key]
            # add the group totals
            lines.append({
                'id': val_dict['id'],
                'name': val_dict['name'],
                'title_hover': val_dict['name'],
                'unfoldable': True,
                'unfolded': hierarchy_parent in options.get('unfolded_lines') or unfold_all,
                'level': level,
                'parent_id': parent_id,
                'columns': [{'name': self.format_value(c) if isinstance(c, (int, float)) else c, 'no_format_name': c}
                            for c in val_dict['totals']],
                'name_class': 'o_account_report_name_ellipsis top-vertical-align'
            })
            # add every direct child group recursively
            for child in val_dict['children_codes']:
                add_to_hierarchy(lines, child, level + 1, val_dict['id'], hierarchy_parent, hierarchy)
            # add all the lines that are in this group but not in one of this group's children groups
            for l in val_dict['lines']:
                l['level'] = level + 1
                l['parent_id'] = val_dict['id']
            lines.extend(val_dict['lines'])

        def compute_hierarchy(lines, level, parent_id, hierarchy_parent, options=False):
            # put every line in each of its parents (from less global to more global) and compute the totals
            hierarchy = defaultdict(
                lambda: {'totals': [None] * len(lines[0]['columns']), 'lines': [], 'children_codes': set(), 'name': '',
                         'parent_id': None, 'id': ''})
            for line in lines:
                account = self.env['account.account'].browse(
                    line.get('account_id', self._get_caret_option_target_id(line.get('id'))))
                codes = self.get_account_codes(account)  # id, name
                for code in codes:
                    hierarchy[code[0]]['id'] = 'hierarchy_' + str(code[0])
                    hierarchy[code[0]]['name'] = code[1]
                    for i, column in enumerate(line['columns']):
                        if 'no_format_name' in column:
                            no_format = column['no_format_name']
                        elif 'no_format' in column:
                            no_format = column['no_format']
                        else:
                            no_format = None
                        if isinstance(no_format, (int, float)):
                            if hierarchy[code[0]]['totals'][i] is None:
                                hierarchy[code[0]]['totals'][i] = no_format
                            else:
                                hierarchy[code[0]]['totals'][i] += no_format
                for code, child in zip(codes[:-1], codes[1:]):
                    hierarchy[code[0]]['children_codes'].add(child[0])
                    hierarchy[child[0]]['parent_id'] = hierarchy[code[0]]['id']
                hierarchy[codes[-1][0]]['lines'] += [line]
            # compute the tree-like structure by starting at the roots (being groups without parents)
            hierarchy_lines = []
            for root in [k for k, v in hierarchy.items() if not v['parent_id']]:
                add_to_hierarchy(hierarchy_lines, root, level, parent_id, hierarchy_parent, hierarchy)
            if self._context.get(
                    'model') == 'account.financial.html.report' and hierarchy_lines and 'currency' in options:
                for heararchy in hierarchy_lines:
                    i = 1
                    for curr in options.get('currency'):
                        if curr.get('selected'):
                            currency_id = request.env['res.currency'].browse(curr.get('id'))
                            heararchy['columns'][i]['name'] = formatLang(request.env, heararchy['columns'][i].get(
                                'no_format_name') or heararchy['columns'][i].get('no_format') or 0.0,
                                                                         currency_obj=currency_id)
                            i += 1

            if self._context.get('model') == 'account.assets.report' and hierarchy_lines and 'currency' in options:
                for heararchy in hierarchy_lines:
                    currency_list_index = -(
                        len([curr.get('id') for curr in options.get('currency') if curr.get('selected')]))
                    for curr in options.get('currency'):
                        if curr.get('selected'):
                            currency_id = request.env['res.currency'].browse(curr.get('id'))
                            heararchy['columns'][currency_list_index]['name'] = formatLang(request.env,
                                                                                           heararchy['columns'][
                                                                                               currency_list_index].get(
                                                                                               'no_format_name') or
                                                                                           heararchy['columns'][
                                                                                               currency_list_index].get(
                                                                                               'no_format') or 0.0,
                                                                                           currency_obj=currency_id)
                            currency_list_index += 1

            return hierarchy_lines

        new_lines = []
        account_lines = []
        current_level = 0
        parent_id = 'root'
        for line in lines:
            if not (line.get('caret_options') == 'account.account' or line.get('account_id')):
                # make the hierarchy with the lines we gathered, append it to the new lines and restart the gathering
                if account_lines:
                    new_lines.extend(compute_hierarchy(account_lines, current_level + 1, parent_id, parent_id, options))
                account_lines = []
                new_lines.append(line)
                current_level = line['level']
                parent_id = line['id']
            else:
                # gather all the lines we can create a hierarchy on
                account_lines.append(line)
        # do it one last time for the gathered lines remaining
        if account_lines:
            new_lines.extend(compute_hierarchy(account_lines, current_level + 1, parent_id, parent_id, options))
        return new_lines

    ####################################################
    # OPTIONS: CORE
    ####################################################


class ReportAccountFinancialReportExtended(models.Model):
    _inherit = "account.financial.html.report"

    filter_operating_unit = True

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

            options[0]['unhide_currency'] = True
            if options[0].get('comparison').get('filter') != 'no_comparison':
                options[0]['unhide_currency'] = False
                for cur in options[0].get('currency'):
                    cur['selected'] = False
            i = 1
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
                amount = self.get_multi_currency_balance(columns[0].get('no_format'), curr.get('id'),
                                                         options.get('date').get('date_to'))

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
                amount = self.get_multi_currency_balance(columns[0].get('no_format'), curr.get('id'),
                                                         options.get('date').get('date_to'))
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





class assets_report_extended(models.AbstractModel):
    _inherit = 'account.assets.report'

    def get_header(self, options):
        options['unhide_currency'] = True
        start_date = format_date(self.env, options['date']['date_from'])
        end_date = format_date(self.env, options['date']['date_to'])
        header = [
            [
                {'name': ''},
                {'name': _('Characteristics'), 'colspan': 4},
                {'name': _('Assets'), 'colspan': 4},
                {'name': _('Depreciation'), 'colspan': 4},
                {'name': _('Book Value')},
            ],
            [
                {'name': ''},  # Description
                {'name': _('Acquisition Date'), 'class': 'text-center'},  # Characteristics
                {'name': _('First Depreciation'), 'class': 'text-center'},
                {'name': _('Method'), 'class': 'text-center'},
                {'name': _('Rate'), 'class': 'number', 'title': _(
                    'In percent.<br>For a linear method, the depreciation rate is computed per year.<br>For a declining method, it is the declining factor'),
                 'data-toggle': 'tooltip'},
                {'name': start_date, 'class': 'number'},  # Assets
                {'name': _('+'), 'class': 'number'},
                {'name': _('-'), 'class': 'number'},
                {'name': end_date, 'class': 'number'},
                {'name': start_date, 'class': 'number'},  # Depreciation
                {'name': _('+'), 'class': 'number'},
                {'name': _('-'), 'class': 'number'},
                {'name': end_date, 'class': 'number'},
                {'name': '', 'class': 'number'},  # Gross
            ],
        ]
        for currency in options.get('currency'):
            if currency.get('selected'):
                header[0].append({'name': _('Book Value ' + currency.get('name'))})
                header[1].append({'name': '', 'class': 'number'})

        return header
#
    def _get_lines(self, options, line_id=None):
        options['self'] = self
        lines = []
        total = [0] * 9
        asset_lines = self._get_assets_lines(options)
        parent_lines = []
        children_lines = defaultdict(list)
        for al in asset_lines:
            if al['parent_id']:
                children_lines[al['parent_id']] += [al]
            else:
                parent_lines += [al]
        for al in parent_lines:
            if al['asset_method'] == 'linear' and al[
                'asset_method_number']:  # some assets might have 0 depreciations because they dont lose value
                asset_depreciation_rate = ('{:.2f} %').format(
                    (100.0 / al['asset_method_number']) * (12 / int(al['asset_method_period'])))
            elif al['asset_method'] == 'linear':
                asset_depreciation_rate = ('{:.2f} %').format(0.0)
            else:
                asset_depreciation_rate = ('{:.2f} %').format(float(al['asset_method_progress_factor']) * 100)

            depreciation_opening = al['depreciated_start'] - al['depreciation']
            depreciation_closing = al['depreciated_end']
            depreciation_minus = 0.0

            opening = (al['asset_acquisition_date'] or al['asset_date']) < fields.Date.to_date(
                options['date']['date_from'])
            asset_opening = al['asset_original_value'] if opening else 0.0
            asset_add = 0.0 if opening else al['asset_original_value']
            asset_minus = 0.0

            if al['import_depreciated']:
                asset_opening += asset_add
                asset_add = 0
                depreciation_opening += al['import_depreciated']
                depreciation_closing += al['import_depreciated']

            for child in children_lines[al['asset_id']]:
                depreciation_opening += child['depreciated_start'] - child['depreciation']
                depreciation_closing += child['depreciated_end']

                opening = (child['asset_acquisition_date'] or child['asset_date']) < fields.Date.to_date(
                    options['date']['date_from'])
                asset_opening += child['asset_original_value'] if opening else 0.0
                asset_add += 0.0 if opening else child['asset_original_value']

            depreciation_add = depreciation_closing - depreciation_opening
            asset_closing = asset_opening + asset_add

            if al['asset_state'] == 'close' and al['asset_disposal_date'] and al[
                'asset_disposal_date'] < fields.Date.to_date(options['date']['date_to']):
                depreciation_minus = depreciation_closing
                depreciation_closing = 0.0
                depreciation_opening += depreciation_add
                depreciation_add = 0
                asset_minus = asset_closing
                asset_closing = 0.0

            asset_gross = asset_closing - depreciation_closing

            total = [x + y for x, y in zip(total,
                                           [asset_opening, asset_add, asset_minus, asset_closing, depreciation_opening,
                                            depreciation_add, depreciation_minus, depreciation_closing, asset_gross])]

            id = "_".join([self._get_account_group(al['account_code'])[0], str(al['asset_id'])])
            name = str(al['asset_name'])
            line = {
                'id': id,
                'level': 1,
                'name': name if len(name) < MAX_NAME_LENGTH else name[:MAX_NAME_LENGTH - 2] + '...',
                'columns': [
                    {'name': al['asset_acquisition_date'] and format_date(self.env, al['asset_acquisition_date']) or '',
                     'no_format_name': ''},  # Characteristics
                    {'name': al['asset_date'] and format_date(self.env, al['asset_date']) or '', 'no_format_name': ''},
                    {'name': (al['asset_method'] == 'linear' and _('Linear')) or (
                                al['asset_method'] == 'degressive' and _('Declining')) or _('Dec. then Straight'),
                     'no_format_name': ''},
                    {'name': asset_depreciation_rate, 'no_format_name': ''},
                    {'name': self.format_value(asset_opening), 'no_format_name': asset_opening},  # Assets
                    {'name': self.format_value(asset_add), 'no_format_name': asset_add},
                    {'name': self.format_value(asset_minus), 'no_format_name': asset_minus},
                    {'name': self.format_value(asset_closing), 'no_format_name': asset_closing},
                    {'name': self.format_value(depreciation_opening), 'no_format_name': depreciation_opening},
                    # Depreciation
                    {'name': self.format_value(depreciation_add), 'no_format_name': depreciation_add},
                    {'name': self.format_value(depreciation_minus), 'no_format_name': depreciation_minus},
                    {'name': self.format_value(depreciation_closing), 'no_format_name': depreciation_closing},
                    {'name': self.format_value(asset_gross), 'no_format_name': asset_gross},  # Gross
                ],
                'unfoldable': False,
                'unfolded': False,
                'caret_options': 'account.asset.line',
                'account_id': al['account_id']
            }
            if len(name) >= MAX_NAME_LENGTH:
                line.update({'title_hover': name})
            lines.append(line)
        lines.append({
            'id': 'total',
            'level': 0,
            'name': _('Total'),
            'columns': [
                {'name': ''},  # Characteristics
                {'name': ''},
                {'name': ''},
                {'name': ''},
                {'name': self.format_value(total[0]), 'no_format_name': total[0]},  # Assets
                {'name': self.format_value(total[1]), 'no_format_name': total[1]},
                {'name': self.format_value(total[2]), 'no_format_name': total[2]},
                {'name': self.format_value(total[3]), 'no_format_name': total[3]},
                {'name': self.format_value(total[4]), 'no_format_name': total[4]},  # Depreciation
                {'name': self.format_value(total[5]), 'no_format_name': total[5]},
                {'name': self.format_value(total[6]), 'no_format_name': total[6]},
                {'name': self.format_value(total[7]), 'no_format_name': total[7]},
                {'name': self.format_value(total[8]), 'no_format_name': total[8]},  # Gross
            ],
            'unfoldable': False,
            'unfolded': False,
        })
        for line in lines:
            amount = line['columns'][-1].get('no_format_name')
            for currency in options.get('currency'):
                if currency.get('selected'):
                    line['columns'].append(self.get_multi_currency_balance(amount, currency.get('id')))
        return lines

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
                'no_format_name': multi_currency_amount}

    class AccountCashFlowReportInherit(models.AbstractModel):
        _inherit = 'account.cash.flow.report'

        filter_operating_unit = True