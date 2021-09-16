# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    freight_type = fields.Selection(([('shipper', 'Shipper'), ('consignee', 'Consignee')]), string='Freight Type')
    is_carrier = fields.Boolean(string='Is Carrier?')
#tabs
    is_national_account = fields.Boolean('National Account')
    is_global_supplier = fields.Boolean('Global Supplier')
    is_temporary_act = fields.Boolean('Temporary Act')
    is_payable = fields.Boolean('Payable')
    is_receivable = fields.Boolean('Receivable')
    is_shipper = fields.Boolean('Shipper')
    is_consignee = fields.Boolean('Consignee')
    is_transport_client = fields.Boolean('Transport Client')
    is_warehouse = fields.Boolean('Warehouse')
    is_this_a_carrier = fields.Boolean('Carrier')
    is_forwarder_Agent = fields.Boolean('Forwarder/Agent')
    is_broker = fields.Boolean('Broker')
    is_services = fields.Boolean('Services')
    is_competitor = fields.Boolean('Competitor')
    is_sales = fields.Boolean('Sales')
    is_controlling_agent = fields.Boolean('Controlling Agent')
    #Access Capability

    account_pay_mail_addr = fields.Boolean('Account Payable Mail Address')
    account_rec_mail_addr = fields.Boolean('Account Receivable Mail Address')
    awb_addr = fields.Boolean('AWB Address')
    cust_addr_rec = fields.Boolean('Custom Address of Records')
    cons_del_addr = fields.Boolean('Consignment Delivery Address')
    misc_addrr = fields.Boolean('Miscellaneous Address')
    office_addr = fields.Boolean('Office Address')
    cons_pick_del_addr = fields.Boolean('Consignment Pickup and Delivery Address')
    cust_pick_rec = fields.Boolean('Consignment Pickup Address')
    postal_addr = fields.Boolean('Postal Address')
    res_addr = fields.Boolean('Residential Address')
    mailing_addr_sales_update = fields.Boolean('Mailing Address for Sales Updates, Quotes and Special Offers')

    #loading/unloading contraints
    access_point = fields.Selection([
        ('dock','Dock'),
        ('rack','Rack'),
        ('interior','Interior'),
        ('interior_via_el','Interior Via Elivator'),
        ('interior_via_el','Interior Via Elivator'),
        ('interior_via_st','Interior Via Stairs'),
        ('other','Others'),
    ], string='Access point')
    communication = fields.Selection([
        ('app_req', 'Appointment Required'),
        ('cal_bef_del', 'Call Before Delivery'),
        ('not_bef_del', 'Notify Before Delivery'),
        ('other', 'Other - See Notes'),
    ], string='Communication')
    dock_height = fields.Selection([
        ('stand_dock_hei', 'Standard Dock Height'),
        ('non_stand_dock_hei', 'Non-Standard Dock Height'),
        ('other', 'Other - See Notes'),
    ], string='Dock Height')
    container_handling = fields.Selection([
        ('pack_unpack', 'Pack and Unpack'),
        ('pack_only', 'Pack Only'),
        ('unpack_only', 'Unpack Only'),
        ('drop_and_pull', 'Drop and Pull'),
        ('ask', 'Ask'),
        ('other', 'Other'),
    ], string='Container Handling')
    labour_required = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('ask', 'ASK'),
        ('fcl', 'For FCL Only'),
        ('out_on_gauge', 'For Out of Gauge'),
        ('heavy_pieces', 'For Heavy Pieces'),
        ('other', 'Other - See Notes'),
    ], string='Labour Required')
    reports_own_vgm = fields.Boolean('Reports Own VGM')
    service_duration = fields.Float('Service Duration')
    service_duration_default = fields.Boolean('Override Registry Default')
    further_constraints = fields.Text('Further Constraints')
    #WareHouse Equipment
    has_dock_leveler=fields.Boolean('Has Dock Leveler')
    has_pallect_jack=fields.Boolean('Has Pallet Jack')
    has_fork_lift=fields.Boolean('Has Fork Lift')
    other_warehouse_fac = fields.Text('Other Warehouse Facalities')
    #Drop Mode
    air_freight = fields.Selection([
        ('any','Any'),
        ('haul_supp_lift','Hauler Supplies Lift'),
        ('hand_premise','Hand Unload/Load by Premise'),
        ('hand_haul','Hand Unload/Load by Hauler'),
        ('prem_supp_lift', 'Premise Supplies Lift'),
        ('ask','Ask Client'),
    ],string='Air Freight')
    lcl_freight = fields.Selection([
        ('any', 'Any'),
        ('haul_supp_lift', 'Hauler Supplies Lift'),
        ('hand_premise', 'Hand Unload/Load by Premise'),
        ('hand_haul', 'Hand Unload/Load by Hauler'),
        ('prem_supp_lift', 'Premise Supplies Lift'),
        ('ask', 'Ask Client'),
    ],string='LCL Freight')
    fcl_freight = fields.Selection([
        ('any', 'Any'),
        ('haul_supp_lift', 'Hauler Supplies Lift'),
        ('hand_premise', 'Hand Unload/Load by Premise'),
        ('hand_haul', 'Hand Unload/Load by Hauler'),
        ('prem_supp_lift', 'Premise Supplies Lift'),
        ('ask', 'Ask Client'),
    ],string='FCL Freight')
    #pickup and delivery page
    auth_to_leave = fields.Selection([('def_from_reg','Default From Registry(Currently Authority to leave is denied).'),('no','Authority to leave is denied'),('yes','Authority to leave is Granted')], string='Authority to Leave')
    pickup_and_delivery_times = fields.Selection([
        ('def','Default'),
        ('weekday','Weekday'),
        ('everyday','EveryDay'),
        ('not_App','Not Applicable'),
    ], string='Pickup and delivery times')
    #gps page
    longitude = fields.Float('Longitude')
    latitude = fields.Float('Latitude')
    #delivery route
    delivery_route = fields.Selection([('not_Data','No data')])
    route_seq = fields.Integer('Route Sequence')
    #free waiting page
    use_cumulative = fields.Boolean('Use cumulative')
    free_waiting_ids = fields.One2many('free.waiting','partner_id',)





