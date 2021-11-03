from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AgedTrialBalanceBillwise(models.TransientModel):
    _name = 'account.aged.trial.balance.xls'
    _inherit = 'account.aged.trial.balance'
    _description = 'Account Aged Trial balance Report Bill-wise'

    def _print_report(self, data):
        res = {}
        data = self.pre_print_report(data)

        data['form'].update(self.read(['period_length'])[0])
        data['form'].update(self.read(['period_count'])[0])
        period_length = data['form']['period_length']
        period_count = data['form']['period_count']
        if period_length <= 0:
            raise UserError(_('You must set a period length greater than 0.'))
        if period_count<=0:
            raise UserError(_('You must set periods greater than 0.'))
        if not data['form']['date_from']:
            raise UserError(_('You must set a start date.'))

        start = datetime.strptime(str(data['form']['date_from']), "%Y-%m-%d")

        for i in range(period_count)[::-1]:
            stop = start - relativedelta(days=period_length - 1)
            res[str(i)] = {
                'name': (i != 0 and (str((period_count - (i + 1)) * period_length) + '-' + str((period_count - i) * period_length)) or (
                '+' + str((period_count-1) * period_length))),
                'stop': start.strftime('%Y-%m-%d'),
                'start': (i != 0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop - relativedelta(days=1)
        data['form'].update(res)
        return self.env.ref('partner_ageing_billwise_xlsx.financial_report_xlsx').with_context(landscape=True).report_action(self, data=data)
