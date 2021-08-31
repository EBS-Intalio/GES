# -*- coding: utf-8 -*-
from odoo import api, models, _, fields
from datetime import datetime, timedelta, date
import pytz
import calendar
import json
from odoo.tools.misc import format_date


class AccountMoveEXT(models.Model):
    _inherit = 'account.move'

    reversal_date = fields.Date('Reversal Date')

    @api.model
    def _move_dict_to_preview_vals(self, move_vals, currency_id=None):
        preview_vals = {
            'group_name': "%s, %s" % (format_date(self.env, move_vals['date']) or _('[Not set]'), move_vals['ref']),
            'items_vals': move_vals['line_ids'],
        }
        for line in preview_vals['items_vals']:
            line[2]['account_int_id'] = line[2]['account_id']
            line[2]['debit_int'] = line[2]['debit']
            line[2]['credit_int'] = line[2]['credit']
        return super(AccountMoveEXT, self)._move_dict_to_preview_vals(move_vals, currency_id)

    @api.model
    def cron_unrealized_gain_loss(self):
        company_tz_dict = {company: company.tz for company in self.env['res.company'].search([])}
        for company in company_tz_dict.keys():
            now_utc = datetime.utcnow()
            tz = pytz.timezone(company_tz_dict.get(company))
            now_kl = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
            max_day = calendar.monthrange(now_utc.year, now_utc.month)[1]

            # if now_kl.day == max_day and now_kl.hour == 23 and now_kl.minute == 59:
            # if now_kl.day == 25 and now_kl.hour == 19:

            previous_options = {}
            rates = self.env['res.currency'].search([('active', '=', True)])._get_rates(self.env.company,
                                                                                        (now_kl.replace(
                                                                                            day=max_day) + timedelta(
                                                                                            days=1)).strftime(
                                                                                            "%Y-%m-%d"))
            for key in rates.keys():  # normalize the rates to the company's currency
                rates[key] /= rates[self.env.company.currency_id.id]
            currency_rates = {
                str(currency_id.id): {
                    'currency_id': currency_id.id,
                    'currency_name': currency_id.name,
                    'currency_main': self.env.company.currency_id.name,
                    'rate': (rates[currency_id.id]
                             if not (previous_options or {}).get('currency_rates', {}).get(str(currency_id.id),
                                                                                           {}).get('rate') else
                             float(previous_options['currency_rates'][str(currency_id.id)]['rate'])),
                } for currency_id in self.env['res.currency'].search([('active', '=', True)])
            }

            options = {
                'unfolded_lines': [],

                'currency_rates': currency_rates,
            }

            try:
                wiz_rec = self.env['account.multicurrency.revaluation.wizard'].with_context(
                    allowed_company_ids=[company.id], company_id=company.id, unfolded_lines=[],
                    currency_rates=currency_rates).create({
                    'journal_id': company.account_revaluation_journal_id.id,
                    'expense_provision_account_id': company.account_revaluation_expense_provision_account_id.id,
                    'income_provision_account_id': company.account_revaluation_income_provision_account_id.id,
                    'date': now_kl.replace(day=max_day).strftime("%Y-%m-%d"),
                    'reversal_date': (now_kl.replace(day=max_day) + timedelta(days=1)).strftime("%Y-%m-%d"),
                    'company_id': company.id
                })
                if wiz_rec and company.expense_account_id and company.income_account_id:
                    account_move_id = self.env['account.move'].create({
                        'date': date.today(),
                        'ref': _('Foreign currencies adjustment entry as of %s', format_date(self.env, date.today())),
                        'company_id': company.id,
                        'journal_id': company.account_journal_id.id or False,
                        'reversal_date': (date.today() + timedelta(days=1)),
                    })
                    preview_data = json.loads(wiz_rec.preview_data)
                    for group in preview_data.get('groups_vals'):
                        for items_vals in group.get('items_vals'):
                            data = items_vals[2]
                            if data.get('account_int_id') != False:
                                self.env['account.move.line'].with_context(check_move_validity=False).create({
                                    'date': date.today(),
                                    'name': data.get('name'),
                                    'move_id': account_move_id.id,
                                    'account_id': data.get('account_int_id'),
                                    'debit': data.get('debit_int'),
                                    'credit': data.get('credit_int'),
                                    'currency_id': data.get('currency_id'),
                                })
                            else:
                                if data.get('debit_int') != 0.0:
                                    # for loss
                                    # loss account

                                    self.env['account.move.line'].with_context(check_move_validity=False).create({
                                        'date': date.today(),
                                        'name': data.get('name'),
                                        'move_id': account_move_id.id,
                                        'account_id': company.expense_account_id.id,
                                        'debit': data.get('debit_int'),
                                        'credit': data.get('credit_int'),
                                        'currency_id': data.get('currency_id'),
                                    })
                                else:
                                    self.env['account.move.line'].with_context(check_move_validity=False).create({
                                        'date': date.today(),
                                        'name': data.get('name'),
                                        'move_id': account_move_id.id,
                                        'account_id': company.income_account_id.id,
                                        'debit': data.get('debit_int'),
                                        'credit': data.get('credit_int'),
                                        'currency_id': data.get('currency_id'),
                                    })
                    account_move_id.post()
            except:
                continue

    def reverse_account_entry(self):
        moves = self.env['account.move'].search([('reversal_date', '=', date.today()), ('state', '=', 'posted')])
        if moves:
            default_values_list = [{
                'date': date.today(),
                'ref': _('Reversal of: %s') % move.name,
            } for move in moves]
            moves_reverse = moves.with_context(reversal_date=False)._reverse_moves(default_values_list, cancel=True)
            for rec in moves_reverse:
                rec.reversal_date = False
            for rec in moves:
                rec.reversal_date = False
