from odoo import _, models


class TrialBalanceXslxInherited(models.AbstractModel):
    _inherit = "report.a_f_r.report_trial_balance_xlsx"
    _description = "Trial Balance XLSX Report"

    def _get_report_columns(self, report):
        wizard = self._context.get('active_id') and self.env['trial.balance.report.wizard'].browse(self._context.get('active_id'))
        if not report.show_partner_details:
            if not wizard.show_total:
                res = {
                    0: {"header": _("Code"), "field": "code", "width": 10},
                    1: {"header": _("Account"), "field": "name", "width": 60},
                    2: {
                        "header": _("Initial balance"),
                        "field": "initial_balance",
                        "type": "amount",
                        "width": 14,
                    },
                    3: {
                        "header": _("Debit"),
                        "field": "debit",
                        "type": "amount",
                        "width": 14,
                    },
                    4: {
                        "header": _("Credit"),
                        "field": "credit",
                        "type": "amount",
                        "width": 14,
                    },
                    5: {
                        "header": _("Period balance"),
                        "field": "balance",
                        "type": "amount",
                        "width": 14,
                    },
                    6: {
                        "header": _("Ending balance"),
                        "field": "ending_balance",
                        "type": "amount",
                        "width": 14,
                    },
                }
                if report.foreign_currency:
                    foreign_currency = {
                        7: {
                            "header": _("Cur."),
                            "field": "currency_id",
                            "field_currency_balance": "currency_id",
                            "type": "many2one",
                            "width": 7,
                        },
                        8: {
                            "header": _("Initial balance"),
                            "field": "initial_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                        9: {
                            "header": _("Ending balance"),
                            "field": "ending_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                    }
                    res = {**res, **foreign_currency}
                return res
            else:
                res = {
                    0: {"header": _("Code"), "field": "code", "width": 10},
                    1: {"header": _("Account"), "field": "name", "width": 60},
                    2: {
                        "header": _("Initial balance"),
                        "field": "initial_balance",
                        "type": "amount",
                        "width": 14,
                    },
                    3: {
                        "header": _("Period balance"),
                        "field": "balance",
                        "type": "amount",
                        "width": 14,
                    },
                    4: {
                        "header": _("Ending balance"),
                        "field": "ending_balance",
                        "type": "amount",
                        "width": 14,
                    },
                }
                if report.foreign_currency:
                    foreign_currency = {
                        5: {
                            "header": _("Cur."),
                            "field": "currency_id",
                            "field_currency_balance": "currency_id",
                            "type": "many2one",
                            "width": 7,
                        },
                        6: {
                            "header": _("Initial balance"),
                            "field": "initial_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                        7: {
                            "header": _("Ending balance"),
                            "field": "ending_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                    }
                    res = {**res, **foreign_currency}
                return res
        else:
            if not wizard.show_total:
                res = {
                    0: {"header": _("Partner"), "field": "name", "width": 70},
                    1: {
                        "header": _("Initial balance"),
                        "field": "initial_balance",
                        "type": "amount",
                        "width": 14,
                    },
                    2: {
                        "header": _("Debit"),
                        "field": "debit",
                        "type": "amount",
                        "width": 14,
                    },
                    3: {
                        "header": _("Credit"),
                        "field": "credit",
                        "type": "amount",
                        "width": 14,
                    },
                    4: {
                        "header": _("Period balance"),
                        "field": "balance",
                        "type": "amount",
                        "width": 14,
                    },
                    5: {
                        "header": _("Ending balance"),
                        "field": "ending_balance",
                        "type": "amount",
                        "width": 14,
                    },
                }
                if report.foreign_currency:
                    foreign_currency = {
                        6: {
                            "header": _("Cur."),
                            "field": "currency_id",
                            "field_currency_balance": "currency_id",
                            "type": "many2one",
                            "width": 7,
                        },
                        7: {
                            "header": _("Initial balance"),
                            "field": "initial_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                        8: {
                            "header": _("Ending balance"),
                            "field": "ending_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                    }
                    res = {**res, **foreign_currency}
                return res
            else:
                res = {
                    0: {"header": _("Partner"), "field": "name", "width": 70},
                    1: {
                        "header": _("Initial balance"),
                        "field": "initial_balance",
                        "type": "amount",
                        "width": 14,
                    },
                    2: {
                        "header": _("Period balance"),
                        "field": "balance",
                        "type": "amount",
                        "width": 14,
                    },
                    3: {
                        "header": _("Ending balance"),
                        "field": "ending_balance",
                        "type": "amount",
                        "width": 14,
                    },
                }
                if report.foreign_currency:
                    foreign_currency = {
                        4: {
                            "header": _("Cur."),
                            "field": "currency_id",
                            "field_currency_balance": "currency_id",
                            "type": "many2one",
                            "width": 7,
                        },
                        5: {
                            "header": _("Initial balance"),
                            "field": "initial_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                        6: {
                            "header": _("Ending balance"),
                            "field": "ending_currency_balance",
                            "type": "amount_currency",
                            "width": 14,
                        },
                    }
                    res = {**res, **foreign_currency}
                return res


    def _generate_report_content(self, workbook, report, data, report_data):
        wizard = self._context.get('active_id') and self.env['trial.balance.report.wizard'].browse(
            self._context.get('active_id'))
        res_data = self.env[
            "report.account_financial_report.trial_balance"
        ]._get_report_values(report, data)
        trial_balance = res_data["trial_balance"]
        total_amount = res_data["total_amount"]
        partners_data = res_data["partners_data"]
        accounts_data = res_data["accounts_data"]
        hierarchy_on = res_data["hierarchy_on"]
        show_partner_details = res_data["show_partner_details"]
        show_hierarchy_level = res_data["show_hierarchy_level"]
        foreign_currency = res_data["foreign_currency"]
        limit_hierarchy_level = res_data["limit_hierarchy_level"]
        if not show_partner_details:
            # Display array header for account lines
            self.write_array_header(report_data)

        # For each account
        if not show_partner_details:
            for balance in trial_balance:
                if hierarchy_on == "relation":
                    if limit_hierarchy_level:
                        if show_hierarchy_level > balance["level"]:
                            # Display account lines
                            self.write_line_from_dict(balance, report_data)
                    else:
                        self.write_line_from_dict(balance, report_data)
                elif hierarchy_on == "computed":
                    if balance["type"] == "account_type":
                        if limit_hierarchy_level:
                            if show_hierarchy_level > balance["level"]:
                                # Display account lines
                                self.write_line_from_dict(balance, report_data)
                        else:
                            self.write_line_from_dict(balance, report_data)
                else:
                    self.write_line_from_dict(balance, report_data)
        else:
            for account_id in total_amount:
                # Write account title
                self.write_array_title(
                    accounts_data[account_id]["code"]
                    + "- "
                    + accounts_data[account_id]["name"],
                    report_data,
                )
                # Display array header for partner lines
                self.write_array_header(report_data)

                # For each partner
                for partner_id in total_amount[account_id]:
                    if isinstance(partner_id, int):
                        # Display partner lines
                        self.write_line_from_dict_order(
                            total_amount[account_id][partner_id],
                            partners_data[partner_id],
                            report_data,
                        )

                # Display account footer line
                accounts_data[account_id].update(
                    {
                        "initial_balance": total_amount[account_id]["initial_balance"],
                        "balance": total_amount[account_id]["balance"],
                        "ending_balance": total_amount[account_id]["ending_balance"],
                    }
                )
                if not wizard.show_total:
                    accounts_data[account_id].update(
                        {
                        "credit": total_amount[account_id]["credit"],
                        "debit": total_amount[account_id]["debit"],
                        }
                    )
                if foreign_currency:
                    accounts_data[account_id].update(
                        {
                            "initial_currency_balance": total_amount[account_id][
                                "initial_currency_balance"
                            ],
                            "ending_currency_balance": total_amount[account_id][
                                "ending_currency_balance"
                            ],
                        }
                    )
                self.write_account_footer(
                    accounts_data[account_id],
                    accounts_data[account_id]["code"]
                    + "- "
                    + accounts_data[account_id]["name"],
                    report_data,
                )

                # Line break
                report_data["row_pos"] += 2

