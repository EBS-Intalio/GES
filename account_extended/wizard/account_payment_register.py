from odoo import api, fields, models, _

class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Register Payment'

    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
        compute='_compute_journal_id',
        domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]", string='Journal Bank')

    payment_date = fields.Date(string="Accounting Date", required=True,
        default=fields.Date.context_today)
    payment_date_new = fields.Date(string="Payment Date",
        default=fields.Date.context_today)
    operating_unit_id = fields.Many2one('operating.unit','Branch')
    payment_ref = fields.Char('Payment Ref')
    legal_name = fields.Char('Legal Name')
    mode_of_payment = fields.Many2one('payment.mode','Mode of Payment')
    check_num = fields.Char(string='Check Number', readonly=False)
    check_name = fields.Char(related='payment_method_id.name')


    @api.model
    def default_get(self, fields):
        vals = super(AccountPaymentRegisterInherit, self).default_get(fields)
        if self._context and self._context.get('active_id'):
            move = self.env['account.move'].browse(self._context.get('active_id'))
            vals['operating_unit_id'] = move.operating_unit_id and move.operating_unit_id.id
            vals['legal_name'] = move.partner_id and move.partner_id.legal_name

        return vals

    def get_defualt_branch(self):
        for rec in self:
            if self._context and self._context.get('active_id'):
                move = self.env['account.move'].browse(self._context.get('active_id'))
                rec.operating_unit_id = move.operating_unit_id and move.operating_unit_id.id

    def _create_payment_vals_from_wizard(self):
        # OVERRIDE
        payment_vals = super()._create_payment_vals_from_wizard()
        payment_vals['operating_unit_id'] = self.operating_unit_id and self.operating_unit_id.id
        payment_vals['payment_date'] = self.payment_date_new
        payment_vals['payment_ref'] = self.payment_ref
        payment_vals['legal_name'] = self.legal_name
        payment_vals['mode_of_payment'] = self.mode_of_payment and self.mode_of_payment.id
        payment_vals['check_num'] = self.check_num
        return payment_vals

    @api.depends('payment_type',
                 'journal_id.inbound_payment_method_ids',
                 'journal_id.outbound_payment_method_ids')
    def _compute_payment_method_fields(self):
        for wizard in self:
            if wizard.payment_type == 'inbound':
                wizard.available_payment_method_ids = wizard.journal_id.inbound_payment_method_ids
            else:
                wizard.available_payment_method_ids = wizard.journal_id.outbound_payment_method_ids

            wizard.hide_payment_method = len(wizard.available_payment_method_ids) == 1 and wizard.available_payment_method_ids.code == 'manual'
            wizard.hide_payment_method = False