from odoo import _, api, fields, models

class TrialBalanceReportWizardInherit(models.TransientModel):
    """Trial balance report wizard."""

    _inherit = "trial.balance.report.wizard"
    _description = "Trial Balance Report Wizard"

    show_total = fields.Boolean('Show Total')