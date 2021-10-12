# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        payments = self._create_payments()

        for payment in payments:
            move_id = self.env['account.move'].browse(self._context.get('active_ids', []))
            payment_name = ""
            if move_id.custom_payment_reference:
                payment_name = move_id.custom_payment_reference + " - " +payment.name
            if not move_id.custom_payment_reference:
                payment_name = payment.name

            move_id.sudo().write({'custom_payment_reference': payment_name})

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action