# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritAccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_date = fields.Date(string='Payment Date')
    mode_of_payment = fields.Many2one('payment.mode', string='Mode Of Payment')
    payment_ref = fields.Char(string='Payment Ref')
    check_number = fields.Char(string='Check Number')
