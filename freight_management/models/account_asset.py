from odoo import api, fields, models, _



class AccountAssetInherit(models.Model):
    _inherit = 'account.asset'

    asset_mode_ow_le = fields.Selection([('own','Own'),('lease','Lease')], string='Mode')

    def action_set_to_close(self):
        """ Returns an action opening the asset pause wizard."""
        self.ensure_one()
        new_wizard = self.env['account.asset.sell'].create({
            'asset_id': self.id,
        })
        return {
            'name': _('Dispose Asset'),
            'view_mode': 'form',
            'res_model': 'account.asset.sell',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': new_wizard.id,
        }