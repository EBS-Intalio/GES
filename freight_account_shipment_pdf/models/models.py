# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def convert_Currency_to_usd(self, amount, currency_id):
        USD = self.env['res.currency'].search([('name', '=', 'USD')])
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        line_currency = self.env['res.currency'].search([('name', '=', currency_id.name)])

        date = self._context.get('date') or fields.Date.today()
        amount_conferted = line_currency._convert(amount, USD, company, date)
        return amount_conferted

    # def get_shipment(self):
    #     if self.created_from_shipment == True:
    #         if len(self.invoice_line_ids) == 1:
    #             shipment_id = self.invoice_line_ids.shipment_line
    #     print('#############',shipment_id)
    #
    #     return{
    #         'shipment_name':shipment_id.name or '',
    #         'shipper_name':shipment_id.shipper_id.name or '',
    #         'gross_weight':shipment_id.gross_weight or '',
    #         'volume':shipment_id.volume or '',
    #         'atd':shipment_id.atd or '',
    #         'consignee':shipment_id.consignee_id.name or '',
    #         'ata':shipment_id.ata or '',
    #     }