# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    transport = fields.Selection(([('air', 'Air'), ('sea', 'Sea'), ('road', 'Road'), ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'), ('rail', 'Rail'), ('courier', 'Courier')]),
                                 default='air', string='Mode')
    direction = fields.Selection([('import', 'Import'), ('export', 'Export'), ('cross', 'Cross')], default='import',
                                 string='Direction')
    service_type = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                     ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door')],
                                    default='door_to_door', string='Service type')

    @api.onchange('product_id', 'transport', 'direction', 'service_type')
    def _onchange_product_transport_direction_service(self):
        for rec in self:
            if rec.transport and rec.direction and rec.service_type:
                if rec.product_id:
                    account_matrix_id = self.env['account.operation.matrix'].search([('transport', '=', rec.transport),('direction', '=', rec.direction),
                                                                                     ('service_type', '=', rec.service_type)], limit=1)
                    if account_matrix_id:
                        account_matrix_line_id = account_matrix_id.matrix_line_ids.search([('charge_code', '=', rec.product_id.id)], limit=1)
                        if account_matrix_line_id:
                            if rec.move_id.move_type == 'out_invoice':
                                rec.account_id = account_matrix_line_id.income_account.id
                            elif rec.move_id.move_type == 'in_invoice':
                                rec.account_id = account_matrix_line_id.expense_account.id
                else:
                    account_matrix_id = self.env['account.operation.matrix'].search([('transport', '=', rec.transport), ('direction', '=', rec.direction),
                                                                                     ('service_type', '=', rec.service_type)], limit=1)
                    if account_matrix_id:
                        if rec.move_id.move_type == 'out_invoice':
                            rec.account_id = account_matrix_id.income_account.id
                        elif rec.move_id.move_type == 'in_invoice':
                            rec.account_id = account_matrix_id.expense_account.id