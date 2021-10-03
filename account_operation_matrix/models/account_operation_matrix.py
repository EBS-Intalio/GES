# -*- coding: utf-8 -*"-
from odoo import models, fields

class AccountOperationMatrix(models.Model):
    _name = 'account.operation.matrix'
    _description = 'Account Operation Matrix'

    name = fields.Char("Line of service", required=True)
    shipment_department = fields.Char("Shipment Department", required=True)
    transport = fields.Selection(([('air', 'Air'), ('sea', 'Sea'), ('road', 'Road'), ('sea_then_air', 'Sea then Air'),
                                   ('air_then_sea', 'Air then Sea'), ('rail', 'Rail'), ('courier', 'Courier')]), default='air', string='Mode')
    direction = fields.Selection([('import','Import'),('export','Export'),('cross','Cross')], default='import', string='Direction')
    service_type = fields.Selection([('door_to_door','Door to Door'),('door_to_port','Door to Port'),
                                     ('port_to_port','Port to Port'),('port_to_door','Port to Door')], default='door_to_door', string='Service type')
    income_account = fields.Many2one('account.account', 'Income Account',required=True)
    expense_account = fields.Many2one('account.account', 'Expense Account',required=True)
    matrix_line_ids = fields.One2many('account.operation.matrix.line', 'operation_matrix_id')

    _sql_constraints = [
        ('_unique_mode_direction_service_type', 'unique (transport, direction, service_type)',
         "A record with the Same Mode,Direction,Service type cannot be created"),
    ]

class AccountOperationMatrixLine(models.Model):
    _name = 'account.operation.matrix.line'

    operation_matrix_id = fields.Many2one('account.operation.matrix', "Operation Matrix")
    charge_code = fields.Many2one('product.template', 'Charge Code',required=True)
    income_account = fields.Many2one('account.account', 'Income Account', required=True)
    expense_account = fields.Many2one('account.account', 'Expense Account', required=True)