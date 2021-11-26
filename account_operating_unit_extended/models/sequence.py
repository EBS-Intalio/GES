from odoo import api, models, _, fields
from datetime import date

class FreightAccountMoveInherited(models.Model):
    _inherit = 'account.move'

    def action_create(self):
        for rec in self:
            if rec.name in [_('New'), '/'] or rec._context.get('reversal_journal_entry'):
                if rec.move_type == 'out_invoice':
                    rec.name = str(rec.operating_unit_id.code if rec.operating_unit_id else '') + '/'+date.today().strftime('%y')+'/'+ self.env[
                                         'ir.sequence'].next_by_code('account.move.sequence.updated') or _('New')
                if rec.move_type == 'in_invoice':
                    rec.name = 'vb' +'/' + date.today().strftime('%y') + '/' + self.env['ir.sequence'].next_by_code('account.move.sequence.bill') or _('New')
                if rec.move_type == 'entry':
                    rec.name = rec.journal_id.code + '/' + date.today().strftime('%y') + '/' + self.env.ref('account_operating_unit_extended.sequence_account_move_entry').next_by_code(
                        'account.move.sequence.entry') or _('New')
            rec.state = 'create'