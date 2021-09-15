# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    freight_type = fields.Selection(([('shipper', 'Shipper'), ('consignee', 'Consignee')]), string='Freight Type')
    is_carrier = fields.Boolean(string='Is Carrier?')

    # is_active_client = fields.Boolean('Active Client')
    # is_national_account = fields.Boolean('National Account')
    # is_global_supplier = fields.Boolean('Global Supplier')
    # is_temporary_act = fields.Boolean('Temporary Act')
    # is_payable = fields.Boolean('Payable')
    # is_receivable = fields.Boolean('Receivable')
    # is_shipper = fields.Boolean('Shipper')
    # is_consignee = fields.Boolean('Consignee')
    # is_transport_client = fields.Boolean('Transport Client')
    # is_warehouse = fields.Boolean('Warehouse')
    # is_this_a_carrier = fields.Boolean('Carrier')
    # is_forwarder_Agent = fields.Boolean('Forwarder/Agent')
    # is_broker = fields.Boolean('Broker')
    # is_services = fields.Boolean('Services')
    # is_competitor = fields.Boolean('Competitor')
    # is_sales = fields.Boolean('Sales')
    # is_controlling_agent = fields.Boolean('Controlling Agent')