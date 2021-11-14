# -*- coding: utf-8 -*"-
from odoo import models, fields, api

class AccountMoveinherit(models.Model):
    _inherit = "account.move"

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('create', 'Create'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    payment_hold = fields.Boolean(string='Payment Hold', default=False, tracking=True)
    custom_payment_reference = fields.Char(string="Payment Reference", readonly=True)
    code_journal_id = fields.Many2one('account.code.journal', string='Code Journal Type')

    # name = fields.Char(string='Number', copy=False, compute='_compute_name', readonly=False, store=True, index=True,
    #                    tracking=True)

    # @api.depends('posted_before', 'state', 'journal_id', 'date')
    # def _compute_name(self):
    #     for rec in self:
    #         if rec.state == 'draft':
    #             rec.name = ""
    #         else:
    #             super(AccountMoveinherit, self)._compute_name()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name"):
                vals["name"] = "/"
            if not vals.get("name"):
                vals["name"] = "/"
        return super().create(vals_list)

    @api.depends('restrict_mode_hash_table', 'state')
    def _compute_show_reset_to_draft_button(self):
        for move in self:
            move.show_reset_to_draft_button = not move.restrict_mode_hash_table and move.state in ('posted','create' ,'cancel')

    def action_create(self):
        for rec in self:
            rec._set_next_sequence()
            rec.state = 'create'