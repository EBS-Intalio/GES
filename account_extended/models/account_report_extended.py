from odoo import api, models, _, fields
from odoo.odoo.tools import date_utils


class AccountReportExtended(models.AbstractModel):
    _inherit = 'account.report'

    filter_currency = None
    @api.model
    def _get_filter_currency(self):
        return self.env['res.currency'].sudo().search([
            ('active', '=', True)])

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
            if self._context.get('model') == 'account.coa.report':
                currency_map = {}
                for curr in previous_options['currency']:
                    if curr['selected'] is True:
                        currency_map.update({
                            curr['id']: curr['selected'],
                            'currency_flag': True
                        })
                        break
            elif self._context.get('model') == 'account.assets.report':
                currency_map = {}
                for curr in previous_options['currency']:
                    if curr['selected'] is True:
                        currency_map.update({
                            curr['id']: curr['selected'],
                            'currency_flag': True
                        })
                        break
            else:
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


# class ReportAccountFinancialReportExtended(models.Model):
#     _inherit = "account.financial.html.report"




