# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.depends('freight_request_ids')
    def _compute_freight_request_ids(self):
        for req in self:
            req.freight_request_count = len(req.freight_request_ids)

    freight_request_ids = fields.One2many('freight.job.request', 'lead_id', string='Request', copy=False)
    freight_request_count = fields.Integer('Request Count', compute='_compute_freight_request_ids')

    def action_show_request(self):
        action = self.env.ref('freight_management.freight_management_freight_job_request_action').read()[0]
        freight_request_ids = self.freight_request_ids
        if len(freight_request_ids) > 1:
            action['domain'] = [('id', 'in', freight_request_ids.ids)]
        elif freight_request_ids:
            form_view = [(self.env.ref('freight_management.freight_management_freight_booking_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = freight_request_ids.id
        return action

    def create_freight_request(self):
        if not self.partner_id:
            raise ValidationError(_('Customer Not Selected.'))
        return {
            'name': _('Request'),
            'res_model': 'freight.job.request',
            # 'res_id': self.partner_id.id if self.partner_id else False,
            'views': [[False, 'form']],
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_lead_id': self.id
            }
        }
