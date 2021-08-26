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
            line[2]['account_int_id'] =line[2]['account_id']
            line[2]['debit_int'] =line[2]['debit']
            line[2]['credit_int'] =line[2]['credit']
        return super(AccountMoveEXT, self)._move_dict_to_preview_vals(move_vals, currency_id)

    @api.model
    def cron_unrealized_gain_loss(self):
        company_tz_dict = {company: company.tz for company in self.env['res.company'].search([])}
        for company in company_tz_dict.keys():
            now_utc = datetime.utcnow()
            tz = pytz.timezone(company_tz_dict.get(company))
            now_kl = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)
            max_day = calendar.monthrange(now_utc.year, now_utc.month)[1]
            # previous_options = {}
            # rates = {}
            # if now_kl.day == max_day and now_kl.hour == 23 and now_kl.minute == 59:
            # if now_kl.day == 25 and now_kl.hour == 19:
            # journal_entries = self.env['account.move'].search([('move_type', '=', 'entry'), ('company_id', '=', company.id)])
            # stop = 0
            # for journal_entries in journal_entries:
            #     if journal_entries.date.month == now_kl.month and journal_entries.date.year == now_kl.year:
            #         print("journal_entries", journal_entries.move_type,journal_entries)
            #         stop=1
            #         break
            # if stop:
            #     continue

            previous_options = {}
            rates = self.env['res.currency'].search([('active', '=', True)])._get_rates(self.env.company,
                                                                                        (now_kl.replace(day=max_day)+timedelta(days=1)).strftime("%Y-%m-%d"))
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

            options={
                'unfolded_lines': [],

                'currency_rates':currency_rates,
            }


            # rec = self.env['account.multicurrency.revaluation'].with_context(unfolded_lines=[], currency_rates=currency_rates)._get_lines(options=options,)
            try:
                wiz_rec = self.env['account.multicurrency.revaluation.wizard'].with_context(allowed_company_ids=[company.id],company_id=company.id,unfolded_lines=[],
                                                                                  currency_rates=currency_rates).create({
                        'journal_id':company.account_revaluation_journal_id.id,
                        'expense_provision_account_id':company.account_revaluation_expense_provision_account_id.id,
                        'income_provision_account_id':company.account_revaluation_income_provision_account_id.id,
                        'date':now_kl.replace(day=max_day).strftime("%Y-%m-%d"),
                        'reversal_date':(now_kl.replace(day=max_day)+timedelta(days=1)).strftime("%Y-%m-%d"),
                        'company_id':company.id
                    })
                if wiz_rec and company.expense_account_id and company.income_account_id:
                    account_move_id = self.env['account.move'].create({
                        'date': date.today(),
                        'ref': 'Adjustment Entry',
                        'company_id':company.id,
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
                                    'name':data.get('name'),
                                    'move_id':account_move_id.id,
                                    'account_id':data.get('account_int_id'),
                                    'debit':data.get('debit_int'),
                                    'credit':data.get('credit_int'),
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
                                    })
                                else:
                                    self.env['account.move.line'].with_context(check_move_validity=False).create({
                                        'date': date.today(),
                                        'name': data.get('name'),
                                        'move_id': account_move_id.id,
                                        'account_id': company.income_account_id.id,
                                        'debit': data.get('debit_int'),
                                        'credit': data.get('credit_int'),
                                    })
                    account_move_id.post()
            except:
                continue


            # self.env['account.aged.receivable'].with_context(date_to=fields.Date.today(),
            #                                                  account_type='receivable')._get_lines(options=options,
            #                                                                                        line_id='partner_' + str(
            #                                                                                            self.partner_id.id))
            # unpaid_invoices = self.env['account.move'].search(
            #     [('move_type', '=', 'out_invoice'), ('company_id', '=', company.id),
            #      ('payment_state', '=', 'not_paid')])
            # unpaid_bills = self.env['account.move'].search(
            #     [('move_type', '=', 'in_invoice'), ('company_id', '=', company.id),
            #      ('payment_state', '=', 'not_paid')])
            # for rec in unpaid_invoices:
            #     if rec.currency_id != company.currency_id:
            #         old_amount = rec.currency_id._convert(rec.amount_total, company.currency_id, company,
            #                                               rec.invoice_date or rec.create_date)
            #         new_amount = rec.currency_id._convert(rec.amount_total, company.currency_id, company,
            #                                               date.today())
            #         # journal_id = int(self.env['ir.config_parameter'].sudo().get_param('account_extended.account_journal_id'))
            #         # income_account_id = int(self.env['ir.config_parameter'].sudo().get_param('account_extended.income_account_id'))
            #         # expense_account_id = int(self.env['ir.config_parameter'].sudo().get_param('account_extended.expense_account_id'))
            #         if new_amount != old_amount:
            #             if new_amount >= old_amount:
            #                 jv = self.env['account.move'].create({
            #                     'date': date.today(),
            #                     'ref': rec.name,
            #                     'journal_id': company.account_journal_id.id or False,
            #                     'reversal_date': (date.today() + timedelta(days=1)),
            #                     'line_ids': [
            #                         (0, 0, {
            #                             'account_id': company.receivable_id.id or False,
            #                             'debit': new_amount - old_amount,
            #                             'name': _(
            #                                 'Provision for {for_cur} (1 {comp_cur} = {rate} {for_cur})').format(
            #                                 for_cur=company.currency_id.display_name,
            #                                 comp_cur=rec.currency_id.display_name,
            #                                 rate=1 / rec.currency_id.rate
            #                             )
            #                             }),
            #                         (0, 0, {
            #                             'account_id': company.income_account_id.id or  False,
            #                             'credit': new_amount - old_amount,
            #                             'name': (_('Profit Provision for {for_cur}')).format(
            #                                 for_cur=company.currency_id.display_name,
            #                             )
            #                             })]
            #                 })
            #                 jv.post()
            #
            #             else:
            #                 jv = self.env['account.move'].create({
            #                     'date': date.today(),
            #                     'ref': rec.name,
            #                     'journal_id': company.account_journal_id.id or False,
            #                     'reversal_date': (date.today() + timedelta(days=1)),
            #                     'line_ids': [
            #                         (0, 0, {
            #                             'account_id': company.receivable_id.id or  False,
            #                             'credit': abs(new_amount - old_amount),
            #                             'name': _(
            #                                 'Provision for {for_cur} (1 {comp_cur} = {rate} {for_cur})').format(
            #                                 for_cur=company.currency_id.display_name,
            #                                 comp_cur=rec.currency_id.display_name,
            #                                 rate=1 / rec.currency_id.rate
            #                             )
            #                         }),
            #                         (0, 0, {
            #                             'account_id': company.expense_account_id.id or False,
            #                             'debit': abs(new_amount - old_amount),
            #                             'name': (_('Expense Provision for {for_cur}')).format(
            #                                 for_cur=company.currency_id.display_name,
            #                             )
            #                         })]
            #                 })
            #                 jv.post()
            #
            # for rec in unpaid_bills:
            #     if rec.currency_id != company.currency_id:
            #         old_amount = rec.currency_id._convert(rec.amount_total, company.currency_id, company,
            #                                               rec.invoice_date or date.today())
            #         new_amount = rec.currency_id._convert(rec.amount_total, company.currency_id, company,
            #                                               date.today())
            #         if new_amount != old_amount:
            #             if new_amount <= old_amount:
            #                 jv = self.env['account.move'].create({
            #                     'date': date.today(),
            #                     'ref': rec.name,
            #                     'journal_id': company.account_journal_id.id or False,
            #                     'reversal_date': (date.today() + timedelta(days=1)),
            #                     'line_ids': [
            #                         (0, 0, {
            #                             'account_id': company.payable_id.id or  False,
            #                             'debit': new_amount - old_amount,
            #                             'name': _(
            #                                 'Provision for {for_cur} (1 {comp_cur} = {rate} {for_cur})').format(
            #                                 for_cur=company.currency_id.display_name,
            #                                 comp_cur=rec.currency_id.display_name,
            #                                 rate=1 / rec.currency_id.rate
            #                             )
            #                         }),
            #                         (0, 0, {
            #                             'account_id': company.income_account_id.id or  False,
            #                             'credit': new_amount - old_amount,
            #                             'name': (_('Profit Provision for {for_cur}')).format(
            #                                 for_cur=company.currency_id.display_name,
            #                             )
            #                         })]
            #                 })
            #                 jv.post()
            #             else:
            #                 jv = self.env['account.move'].create({
            #                     'date': date.today(),
            #                     'ref': rec.name,
            #                     'journal_id': company.account_journal_id.id or False,
            #                     'reversal_date': (date.today() + timedelta(days=1)),
            #                     'line_ids': [
            #                         (0, 0, {
            #                             'account_id': company.payable_id.id or  False,
            #                             'credit': abs(new_amount - old_amount),
            #                             'name': _(
            #                                 'Provision for {for_cur} (1 {comp_cur} = {rate} {for_cur})').format(
            #                                 for_cur=company.currency_id.display_name,
            #                                 comp_cur=rec.currency_id.display_name,
            #                                 rate=1 / rec.currency_id.rate
            #                             )
            #                         }),
            #                         (0, 0, {
            #                             'account_id': company.expense_account_id.id or  False,
            #                             'debit': abs(new_amount - old_amount),
            #                             'name': (_('Expense Provision for {for_cur}')).format(
            #                                 for_cur=company.currency_id.display_name,
            #                             )
            #                         })]
            #                 })
            #                 jv.post()

                # rates = self.env['res.currency'].search([('active', '=', True)])._get_rates(self.env.company,
                #                                                                         (now_kl.replace(day=max_day)+timedelta(days=1)).strftime("%Y-%m-%d"))
                # for key in rates.keys():  # normalize the rates to the company's currency
                #     rates[key] /= rates[self.env.company.currency_id.id]
                # currency_rates = {
                #     str(currency_id.id): {
                #         'currency_id': currency_id.id,
                #         'currency_name': currency_id.name,
                #         'currency_main': self.env.company.currency_id.name,
                #         'rate': (rates[currency_id.id]
                #                  if not (previous_options or {}).get('currency_rates', {}).get(str(currency_id.id),
                #                                                                                {}).get('rate') else
                #                  float(previous_options['currency_rates'][str(currency_id.id)]['rate'])),
                #     } for currency_id in self.env['res.currency'].search([('active', '=', True)])
                # }
                # self.env['account.multicurrency.revaluation.wizard'].with_context(unfolded_lines=[], currency_rates=currency_rates).create({
                #     'journal_id':company.account_revaluation_journal_id,
                #     'expense_provision_account_id':company.account_revaluation_expense_provision_account_id,
                #     'income_provision_account_id':company.account_revaluation_income_provision_account_id,
                #     'date':now_kl.replace(day=max_day).strftime("%Y-%m-%d"),
                #     'reversal_date':(now_kl.replace(day=max_day)+timedelta(days=1)).strftime("%Y-%m-%d"),
                #     'company_id':company.id
                # }).create_entries()

    def reverse_account_entry(self):
        moves = self.env['account.move'].search([('reversal_date', '=', date.today()),('state','=','posted')])
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
