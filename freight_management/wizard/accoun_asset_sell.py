from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from calendar import monthrange
from odoo.tools import float_compare, float_round




class AssetSellInherit(models.TransientModel):
    _inherit= 'account.asset.sell'

    action = fields.Selection([('sell', 'Sell'), ('dispose', 'Write Off')], required=True, default='sell')
    disposal_date = fields.Date('Disposal Date', default=fields.date.today())


    @api.constrains('disposal_date')
    def chech_disposal_date(self):
        for rec in self:
            if rec.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted'):
                max_date = max(rec.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted').mapped('date'))
                if max_date and max_date > rec.disposal_date:
                    raise ValidationError('Disposal Date should be greater than last posted entries date')


    def do_action(self):
        self.ensure_one()
        if self.action == 'dispose':
            if self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'draft') and self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted'):
                amount = 0
                month_days = monthrange(self.disposal_date.year, self.disposal_date.month)[1]
                asset_remaining_value=0
                asset_depreciated_value = 0
                if self.asset_id.method=='linear':

                    # asset_remaining_value = 0
                    # asset_depreciated_value = 0
                    # last_dep_sate = False
                    # last_depr_move = False
                    avg_amount_to_depr = self.asset_id.original_value / self.asset_id.method_number
                    # if not self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted'):
                    #     last_dep_sate = self.asset_id.first_depreciation_date

                    # else:
                    last_depr_move = self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted')[0]
                    last_dep_sate = last_depr_move.date

                    days_diffr = (self.disposal_date - last_dep_sate).days
                    if self.asset_id.method_period == '1':
                        amount = avg_amount_to_depr*days_diffr/month_days
                    if self.asset_id.method_period == '12':
                        month_diff = days_diffr/30
                        amount = avg_amount_to_depr * month_diff / 12
                    # if not self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted'):
                    #     asset_remaining_value = self.asset_id.original_value - amount
                    #     asset_depreciated_value = amount
                    # else:
                    if amount >last_depr_move.asset_remaining_value:
                        amount = last_depr_move.asset_remaining_value
                    asset_remaining_value = last_depr_move.asset_remaining_value-amount
                    asset_depreciated_value = last_depr_move.asset_depreciated_value+amount
                elif self.asset_id.method=='degressive':
                    last_depr_move = self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted')[0]
                    last_dep_sate = last_depr_move.date
                    avg_amount_dep = last_depr_move.asset_remaining_value*self.asset_id.method_progress_factor
                    days_diffr = (self.disposal_date - last_dep_sate).days
                    if self.asset_id.method_period == '1':
                        amount = avg_amount_dep*days_diffr/month_days
                    if self.asset_id.method_period == '12':
                        month_diff = days_diffr/30
                        amount = avg_amount_dep * month_diff / 12
                    if amount >last_depr_move.asset_remaining_value:
                        amount = last_depr_move.asset_remaining_value
                    asset_remaining_value = last_depr_move.asset_remaining_value - amount
                    asset_depreciated_value = last_depr_move.asset_depreciated_value + amount

                elif self.asset_id.method == 'degressive_then_linear':
                    last_depr_move = self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted')[0]
                    last_dep_sate = last_depr_move.date
                    avg_amount_dep_deg = last_depr_move.asset_remaining_value * self.asset_id.method_progress_factor
                    avg_amount_dep_linear = self.asset_id.original_value / self.asset_id.method_number
                    days_diffr = (self.disposal_date - last_dep_sate).days
                    if avg_amount_dep_deg>avg_amount_dep_linear:
                        if self.asset_id.method_period == '1':
                            amount = avg_amount_dep_deg * days_diffr / month_days
                        if self.asset_id.method_period == '12':
                            month_diff = days_diffr / 30
                            amount = avg_amount_dep_deg * month_diff / 12
                    else:
                        if self.asset_id.method_period == '1':
                            amount = avg_amount_dep_linear * days_diffr / month_days
                        if self.asset_id.method_period == '12':
                            month_diff = days_diffr / 30
                            amount = avg_amount_dep_linear * month_diff / 12
                    if amount >last_depr_move.asset_remaining_value:
                        amount = last_depr_move.asset_remaining_value
                    asset_remaining_value = last_depr_move.asset_remaining_value - amount
                    asset_depreciated_value = last_depr_move.asset_depreciated_value + amount
            # elif self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'draft'):
            #     amount = 0
            #     month_days = monthrange(self.disposal_date.year, self.disposal_date.month)[1]
            #     asset_remaining_value = 0
            #     asset_depreciated_value = 0
            #     if self.asset_id.method == 'linear':
            #         avg_amount_to_depr = self.asset_id.original_value / self.asset_id.method_number
            #         last_dep_sate = self.asset_id.first_depreciation_date
            #         days_diffr = (self.disposal_date - last_dep_sate).days
            #         if self.asset_id.method_period == '1':
            #             amount = avg_amount_to_depr * days_diffr / month_days
            #         if self.asset_id.method_period == '12':
            #             month_diff = days_diffr / 30
            #             amount = avg_amount_to_depr * month_diff / 12
            #         # if not self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted'):
            #         #     asset_remaining_value = self.asset_id.original_value - amount
            #         #     asset_depreciated_value = amount
            #         # else:
            #         if amount > last_depr_move.asset_remaining_value:
            #             amount = last_depr_move.asset_remaining_value
            #         asset_remaining_value = last_depr_move.asset_remaining_value - amount
            #         asset_depreciated_value = last_depr_move.asset_depreciated_value + amount
            #     elif self.asset_id.method == 'degressive':
            #         last_depr_move = self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted')[0]
            #         last_dep_sate = last_depr_move.date
            #         avg_amount_dep = last_depr_move.asset_remaining_value * self.asset_id.method_progress_factor
            #         days_diffr = (self.disposal_date - last_dep_sate).days
            #         if self.asset_id.method_period == '1':
            #             amount = avg_amount_dep * days_diffr / month_days
            #         if self.asset_id.method_period == '12':
            #             month_diff = days_diffr / 30
            #             amount = avg_amount_dep * month_diff / 12
            #         if amount > last_depr_move.asset_remaining_value:
            #             amount = last_depr_move.asset_remaining_value
            #         asset_remaining_value = last_depr_move.asset_remaining_value - amount
            #         asset_depreciated_value = last_depr_move.asset_depreciated_value + amount
            #
            #     elif self.asset_id.method == 'degressive_then_linear':
            #         last_depr_move = self.asset_id.depreciation_move_ids.filtered(lambda x: x.state == 'posted')[0]
            #         last_dep_sate = last_depr_move.date
            #         avg_amount_dep_deg = last_depr_move.asset_remaining_value * self.asset_id.method_progress_factor
            #         avg_amount_dep_linear = self.asset_id.original_value / self.asset_id.method_number
            #         days_diffr = (self.disposal_date - last_dep_sate).days
            #         if avg_amount_dep_deg > avg_amount_dep_linear:
            #             if self.asset_id.method_period == '1':
            #                 amount = avg_amount_dep_deg * days_diffr / month_days
            #             if self.asset_id.method_period == '12':
            #                 month_diff = days_diffr / 30
            #                 amount = avg_amount_dep_deg * month_diff / 12
            #         else:
            #             if self.asset_id.method_period == '1':
            #                 amount = avg_amount_dep_linear * days_diffr / month_days
            #             if self.asset_id.method_period == '12':
            #                 month_diff = days_diffr / 30
            #                 amount = avg_amount_dep_linear * month_diff / 12
            #         if amount > last_depr_move.asset_remaining_value:
            #             amount = last_depr_move.asset_remaining_value
            #         asset_remaining_value = last_depr_move.asset_remaining_value - amount
            #         asset_depreciated_value = last_depr_move.asset_depreciated_value + amount
            company_currency = self.asset_id.company_id.currency_id
            current_currency = self.asset_id.currency_id
            analytic_tag_ids = self.asset_id.analytic_tag_ids
            account_analytic_id = self.asset_id.account_analytic_id
            prec = company_currency.decimal_places

            move_line_1 = {
                'name': self.asset_id.name,
                # 'partner_id': self.asset_id.partner.id,
                'account_id': self.asset_id.account_depreciation_id.id,
                'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'analytic_account_id': account_analytic_id.id if self.asset_id.asset_type == 'sale' else False,
                'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if self.asset_id.asset_type == 'sale' else False,
                'currency_id': current_currency.id,
            }
            move_line_2 = {
                'name': self.asset_id.name,
                # 'partner_id': partner.id,
                'account_id': self.asset_id.account_depreciation_expense_id.id,
                'credit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'debit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'analytic_account_id': account_analytic_id.id if self.asset_id.asset_type in ('purchase', 'expense') else False,
                'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if self.asset_id.asset_type in (
                'purchase', 'expense') else False,
                'currency_id': current_currency.id,
            }
            move_vals = {
                'ref': 'Extra Difference',
                # 'partner_id': partner.id,
                'date': self.disposal_date,
                'journal_id': self.asset_id.journal_id.id,
                'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
                'asset_id': self.asset_id.id,
                'asset_remaining_value': asset_remaining_value,
                'asset_depreciated_value': asset_depreciated_value,
                'amount_total': amount,
                'name': '/',
                'move_type': 'entry',
                'currency_id': current_currency.id,
            }
            self.env['account.move'].create(move_vals).post()

        invoice_line = self.env['account.move.line'] if self.action == 'dispose' else self.invoice_line_id or self.invoice_id.invoice_line_ids

        return self.asset_id.set_to_close(invoice_line_id=invoice_line, date=invoice_line.move_id.invoice_date)
