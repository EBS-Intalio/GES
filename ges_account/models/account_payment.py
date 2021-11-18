# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritAccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_date = fields.Date(string='Payment Date')
    mode_of_payment = fields.Many2one('payment.mode', string='Mode Of Payment')
    payment_ref = fields.Char(string='Payment Ref')
    check_num = fields.Char(string='Check Number', readonly=False)
    check_name = fields.Char(related='payment_method_id.name')
    legal_name = fields.Char(string='Legal Name', readonly=False)

    @api.onchange('partner_id')
    def _get_legal_name_partner(self):
        for record in self:
            if record.partner_id:
                if record.partner_id.legal_name:
                    record.legal_name = record.partner_id.legal_name
