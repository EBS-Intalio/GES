# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountOperationMatrix(models.Model):
    _name = 'account.operation.matrix'
    _description = 'Account Operation Matrix'

    name = fields.Char("Line of service", required=True)
    shipment_department = fields.Char("Shipment Department")
    transport = fields.Selection([('air', 'Air'),
                                  ('ocean', 'Ocean'),
                                  ('land', 'Road'),
                                  ('sea_then_air', 'Sea then Air'),
                                  ('air_then_sea', 'Air then Sea'),
                                  ('rail', 'Rail'),
                                  ('courier', 'Courier'),
                                  ('documentation', 'Documentation')], default='air', string='Mode')
    direction = fields.Selection([('import', 'Import'), ('export', 'Export'), ('cross_state', 'Cross Border State'), ('domestic', 'Domestic')], default='import', string='Direction')
    service_type = fields.Selection([('door_to_door', 'Door to Door'), ('door_to_port', 'Door to Port'),
                                     ('port_to_port', 'Port to Port'), ('port_to_door', 'Port to Door'),
                                     ('custom_and_brokerage', 'Customs and Brokerage')],
                                    string="Service Level")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    income_account = fields.Many2one('account.account', 'Income Account',required=True, domain="[('company_id', '=', company_id)]")
    expense_account = fields.Many2one('account.account', 'Expense Account',required=True, domain="[('company_id', '=', company_id)]")
    matrix_line_ids = fields.One2many('account.operation.matrix.line', 'operation_matrix_id')
    ocean_shipment = fields.Selection([('fcl', 'FCL'), ('lcl', 'LCL'),
                                       ('breakbulk', 'Breakbulk'),
                                       ('liquid', 'Liquid'),
                                       ('bulk', 'Bulk'),
                                       ('roro', 'Roro')], string='Ocean Shipment Type')

    _sql_constraints = [
        ('_unique_mode_ocean_shipment_direction_service_type', 'unique (transport,ocean_shipment, direction, service_type)',
         "A record with the Same Mode,Ocean Shipment, Direction, Service type cannot be created"),
    ]

    @api.model
    def create(self, vals):
        res = super(AccountOperationMatrix, self).create(vals)
        if vals.get('transport') != 'ocean':
            account_matrix_id = self.env['account.operation.matrix'].search_count([('transport', '=', vals.get('transport')),
                                                                             ('direction', '=', vals.get('direction')),
                                                                             ('service_type', '=', vals.get('service_type'))])
            if account_matrix_id > 1:
                raise ValidationError(_("A record with the Same Mode, Direction, Service type cannot be created"))
        return res

    def write(self, vals):
        res = super(AccountOperationMatrix, self).write(vals)
        if vals.get('transport') != 'ocean':
            account_matrix_id = self.env['account.operation.matrix'].search_count([('transport', '=', self.transport),
                                                                            ('direction', '=', self.direction),
                                                                            ('service_type', '=', self.service_type)])
            if account_matrix_id > 1:
                raise ValidationError(_("A record with the Same Mode, Direction, Service type cannot be created"))

        return res

class AccountOperationMatrixLine(models.Model):
    _name = 'account.operation.matrix.line'

    operation_matrix_id = fields.Many2one('account.operation.matrix', "Operation Matrix")
    charge_code = fields.Many2one('product.product', 'Charge Code',required=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    income_account = fields.Many2one('account.account', 'Income Account', required=True,
                                     domain="[('company_id', '=', company_id)]")
    expense_account = fields.Many2one('account.account', 'Expense Account', required=True,
                                      domain="[('company_id', '=', company_id)]")