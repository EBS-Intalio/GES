from odoo import api, models, _, fields


class FreightAccountMove(models.Model):
    _inherit = 'account.move'

    freight_booking_id = fields.Many2one('freight.booking', string='Freight Booking')


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    employee_id = fields.Many2one('hr.employee','Employee')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Department',
                                          index=True, compute="_compute_analytic_account_id", store=True,
                                          readonly=False, check_company=True, copy=True)


    def _prepare_analytic_line(self):
        """ Prepare the values used to create() an account.analytic.line upon validation of an account.move.line having
            an analytic account. This method is intended to be extended in other modules.
            :return list of values to create analytic.line
            :rtype list
        """
        result = []
        for move_line in self:
            amount = (move_line.credit or 0.0) - (move_line.debit or 0.0)
            default_name = move_line.name or (move_line.ref or '/' + ' -- ' + (move_line.partner_id and move_line.partner_id.name or '/'))
            result.append({
                'name': default_name,
                'date': move_line.date,
                'account_id': move_line.analytic_account_id.id,
                'group_id': move_line.analytic_account_id.group_id.id,
                'tag_ids': [(6, 0, move_line._get_analytic_tag_ids())],
                'unit_amount': move_line.quantity,
                'employee_id': move_line.employee_id and move_line.employee_id.id or False,
                'operating_unit_id': move_line.operating_unit_id and move_line.operating_unit_id.id or False,
                'product_id': move_line.product_id and move_line.product_id.id or False,
                'product_uom_id': move_line.product_uom_id and move_line.product_uom_id.id or False,
                'amount': amount,
                'general_account_id': move_line.account_id.id,
                'ref': move_line.ref,
                'move_id': move_line.id,
                'user_id': move_line.move_id.invoice_user_id.id or self._uid,
                'partner_id': move_line.partner_id.id,
                'company_id': move_line.analytic_account_id.company_id.id or move_line.move_id.company_id.id,
            })
        return result

class AccountAnalyticLineInherit(models.Model):
    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one('hr.employee','Employee')
    operating_unit_id = fields.Many2one('operating.unit','Operating Unit')