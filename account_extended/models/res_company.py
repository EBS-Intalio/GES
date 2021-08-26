# -*- coding: utf-8 -*-
import pytz
from odoo import api, fields, models, _

# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]
def _tz_get(self):
    return _tzs


class ResCompanyEXT(models.Model):
    _inherit = 'res.company'

    tz = fields.Selection(_tz_get, string='Timezone', default=lambda self: self._context.get('tz'),
                          help="The partner's timezone, used to output proper date and time values "
                               "inside printed reports. It is important to set a value for this field. "
                               "You should use the same timezone that is otherwise used to pick and "
                               "render date and time values: your computer's timezone.")

    account_journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', '=', 'general')])
    expense_account_id = fields.Many2one('account.account', string='Expense Account')
    income_account_id = fields.Many2one('account.account', string='Income Account')
