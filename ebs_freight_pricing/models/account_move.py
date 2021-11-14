from odoo import api, fields, models, _
import logging
from odoo.tools.misc import formatLang, format_date, get_lang
from collections import defaultdict

_logger = logging.getLogger(__name__)


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id',
                 'currency_id')
    def _compute_invoice_taxes_by_group(self):
        for move in self:

            # Not working on something else than invoices.
            if not move.is_invoice(include_receipts=True):
                move.amount_by_group = []
                continue

            lang_env = move.with_context(lang=move.partner_id.lang).env
            balance_multiplicator = -1 if move.is_inbound() else 1

            tax_lines = move.line_ids.filtered('tax_line_id')
            base_lines = move.line_ids.filtered('tax_ids')

            print(self._recompute_tax_lines()._compute_base_line_taxes(base_lines))

            # print(move.line_ids.filtered('tax_line_id'))
            # print(move.line_ids.filtered('tax_ids'))

            tax_group_mapping = defaultdict(lambda: {
                'base_lines': set(),
                'base_amount': 0.0,
                'tax_amount': 0.0,
            })

            # Compute base amounts.
            for base_line in base_lines:
                print('BASE')
                print(base_line.tax_line_id)
                print(base_line.tax_ids)
                base_amount = balance_multiplicator * (
                    base_line.amount_currency if base_line.currency_id else base_line.balance)

                for tax in base_line.tax_ids.flatten_taxes_hierarchy():

                    if base_line.tax_line_id.tax_group_id == tax.tax_group_id:
                        continue

                    tax_group_vals = tax_group_mapping[tax.tax_group_id]
                    if base_line not in tax_group_vals['base_lines']:
                        tax_group_vals['base_amount'] += base_amount
                        tax_group_vals['base_lines'].add(base_line)

            # print(tax_group_mapping)
            # Compute tax amounts.
            for tax_line in tax_lines:
                # print('TAX')
                # print(tax_line.tax_line_id)
                # print(tax_line.tax_ids)
                tax_amount = balance_multiplicator * (
                    tax_line.amount_currency if tax_line.currency_id else tax_line.balance)
                tax_group_vals = tax_group_mapping[tax_line.tax_line_id.tax_group_id]

                # print(tax_group_vals)
                tax_group_vals['tax_amount'] += tax_amount
                # print(tax_group_vals)
                # print(tax_lines)
                # print(tax_line.amount_currency)
                # print(tax_line.balance)

            tax_groups = sorted(tax_group_mapping.keys(), key=lambda x: x.sequence)
            amount_by_group = []
            for tax_group in tax_groups:
                tax_group_vals = tax_group_mapping[tax_group]
                amount_by_group.append((
                    tax_group.name,
                    tax_group_vals['tax_amount'],
                    tax_group_vals['base_amount'],
                    formatLang(lang_env, tax_group_vals['tax_amount'], currency_obj=move.currency_id),
                    formatLang(lang_env, tax_group_vals['base_amount'], currency_obj=move.currency_id),
                    len(tax_group_mapping),
                    tax_group.id
                ))
            move.amount_by_group = amount_by_group
