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
        return round(amount_conferted,3)

    def get_shipment(self):
        shipment_ids = []
        number_of_container = []
        if self.created_from_shipment == True:
            for rec in self.invoice_line_ids:
                shipment_ids += self.env['freight.operation'].search([('id','=',rec.shipment_line.id)])

        if len(shipment_ids) > 1 :
            shipment_ids = []
        else:
            shipment_ids
        if len(shipment_ids) == 1:
            for rec in shipment_ids[0].consol_details_ids:
                for line in rec.container_ids:
                    number_of_container.append(line.id)

        return{
            'transport':shipment_ids[0].transport if shipment_ids else 'air',
            'shipment_name':shipment_ids[0].name if shipment_ids else '',
            'shipper_name':shipment_ids[0].shipper_id.name if shipment_ids else '',
            'gross_weight':shipment_ids[0].gross_weight if shipment_ids else '',
            'volume':shipment_ids[0].volume if shipment_ids else '',
            'atd':shipment_ids[0].atd if shipment_ids else '',
            'consignee':shipment_ids[0].consignee_id.name if shipment_ids else '',
            'ata':shipment_ids[0].ata if shipment_ids else '',
            'house_bill':shipment_ids[0].house_bill if shipment_ids else '',
            'number_of_container': len(number_of_container) if number_of_container else 0,
        }