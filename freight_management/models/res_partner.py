# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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

    #contact/address
    related_city = fields.Char('Related city/port')
    fax = fields.Char('Fax')
    language = fields.Many2one('res.lang',string='Language')
    building = fields.Char('Building')
    po_box = fields.Char('Po Box')
    driver_id = fields.Char('Driver ID')


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
        ('no_pack_unpack', 'No Pack or Unpack'),
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
    pickup_delivery_ids = fields.One2many('pickup.delivery','partner_id')

    #gps page
    longitude = fields.Float('Longitude')
    latitude = fields.Float('Latitude')
    #delivery route
    delivery_route = fields.Selection([('not_Data','No data')])
    route_seq = fields.Integer('Route Sequence')
    #free waiting page
    use_cumulative = fields.Boolean('Use cumulative')
    free_waiting_ids = fields.One2many('free.waiting','partner_id',)

    #main partner view changes
    organization_code = fields.Char('Organization Code')
    screening = fields.Selection([('screened','Screened'),('not_screened','Not Screened')],srtring='Screened')
    security = fields.Selection([('restricted','Restricted'),('not_restricted','Not Restricted')],srtring='Security')
    org_category = fields.Many2one('res.partner.org.cat',string='Organization Category')
    unloco = fields.Many2one('unloco.data','Unloco')
    controlling_branch = fields.Many2one('res.company',string='Controlling Branch')
    lang_main = fields.Many2one('res.lang','Language')
    vat_ges = fields.Many2one('res.partner.org.num',string='Organization Number')

    #Recivable Tabs
    account_group = fields.Selection([('no_data','No Data')], string='Account group')
    account_relationship = fields.Selection([('std','Standard Account Relation Ship'),('key','Key Client'),('sig','Significant Client')], string='Account RelationShip')
    conc_categ = fields.Selection([('unr','Unrelated Company'),
                                   ('who','Wholly owned Subsidiary'),
                                   ('mir','Minority Interest with reporting'),
                                   ('min','Minority Interest with no reporting'),
                                   ('rmi','Related Minority Shareholder'),
                                   ('rmj','Related Majority Shareholder'),
                                   ('rwh','Related Wholly Owning Shareholder'),
                                   ('gmi','Group Company Related Minority(no direct Ownership)'),
                                   ('gmj','Group Company Related Majority(no direct Ownership)'),
                                   ], string='Consolidation Category')
    def_inv_curr_id = fields.Many2one('res.currency','Default Invoice Currency')
    not_acc_reg_details = fields.Boolean('Do not use Account or Registry Details')
    bank_to_account = fields.Selection([('no_data','No Data')], string='Bank to This Account')
    bank_detail_ids = fields.One2many('account.bank.details','partner_id')
    currency_uplift_ids = fields.One2many('currency.uplift','partner_id')
    #tax Details
    vat_recog = fields.Selection(
        [('non', 'Not Applicable'), ('def', 'Tax is Applicable-Default Recognition Rules Apply'),
         ('acr', 'Accural Basis-All tax for this Organization reported on Accural Basis'),
         ('csh','Cash Basis-All tax for this Organization reported on Cash Basis')], string='VAT Recognition and reporting Basis Override')
    with_hol_tax = fields.Boolean('Withholding Tax is Applicable')
    dont_hol_tax = fields.Boolean('Dont Show tax on Documents')
    # Quality Assurance
    quality_assured= fields.Boolean('Quality Assured')
    last_check = fields.Datetime('Last Checked')
    # External SYstem
    external_debt_code = fields.Char('External Debtor Code')
    #Authority to leave
    auth_to_leave_rec = fields.Selection([('def_from_reg','Default From Registry(Currently Authority to leave is denied).'),('no','Authority to leave is denied'),('yes','Authority to leave is Granted')], string='Authority to Leave')
    # client number
    client_num = fields.Char('Client Number')
    # company data
    all_mul_curr = fields.Boolean('Allow Multiuple CUrrency payments')
    trans_cre_res = fields.Selection([('non','No Restriction'),('inv','Restricted from creating New Invoice, Credit note and Adjustment note'),
                                      ('all','Restricted from creating new Transactions(All Transaction Types)'),
                                      ('bal','Restricted from creating Transactions that would cause the outstanding balance in local Currency to increase in value')], string='Transaction creation Restriction')
    # credit control
    cred_rete = fields.Selection([
        ('cr1','Very Low Credit Risk'),
        ('cr2','Low Credit Risk'),
        ('cr3','Normal Credit Risk'),
        ('cr4','High Credit Risk'),
        ('cr5','Very High Credit Risk'),
    ], string='Credit Rating')
    credit_limit = fields.Float('credit Limit')
    temp_cred_limit_inc = fields.Float('Temporary Credit Limit Increase')
    temp_cred_limit = fields.Float('Temporary Credit Limit')
    expire_at = fields.Char('Expires At')
    acc_rev_due=fields.Date('Acc. & Credit Review due')
    agreed_pay_meth=fields.Selection([
        ('chk','Business Check'),
        ('ccd','Credit Card'),
        ('trf','Bank transfer'),
        ('cbc','Cash and/or  Bank check'),
        ('dbc','Debit Card'),
        ('crq','Collection Request'),
    ], string='Agreed Payment Method')
    use_sett = fields.Boolean('Use Settlement group Credit Limit')
    cred_appr = fields.Boolean('Credit Approved')
    ar_cred_hold = fields.Boolean('AR on credit Hold')
    ar_not_check = fields.Boolean('AR Do not check Overdue invoices Status')
    # settle
    settle_grp = fields.Many2one('res.partner',string='Settlement Group')
    # terms and term days
    terms_days_ids = fields.One2many('term.days','partner_id',)
    treat_dist = fields.Float('Treat Disbursements as Standard Under Value')
    # credit card details
    card_num = fields.Char('Card Number')
    card_type = fields.Selection([
        ('amx','American Express'),
        ('din','Dinners Club Carte Blanche'),
        ('dir','Dinners Club Enroute'),
        ('dii','Dinners Club us and Canada'),
        ('visa','Visa'),
        ('vie','Visa Electron'),
        ('msc','Master Card'),
        ('dis','Discover Card'),
        ('bnk','Bankcard'),
    ], string='Card Type')
    card_hold = fields.Char('Card Holder')
    expr_date_month = fields.Selection([
        ('01','01'),
        ('02','02'),
        ('03','03'),
        ('04','04'),
        ('05','05'),
        ('06','06'),
        ('07','07'),
        ('08','08'),
        ('09','09'),
        ('10','10'),
        ('11','11'),
        ('12','12'),
    ], string='Expiry Month')
    expr_year = fields.Selection([
        ('2015','2015'),
        ('2016','2016'),
        ('2017','2017'),
        ('2018','2018'),
        ('2019','2019'),
        ('2020','2020'),
        ('2021','2021'),
        ('2022','2022'),
        ('2023','2023'),
        ('2024','2024'),
        ('2025','2025'),
        ('2026','2026'),
        ('2027','2027'),
        ('2028','2028'),
        ('2029','2029'),
        ('2030','2030'),
        ('2031','2031'),
        ('2032','2032'),
        ('2033','2033'),
        ('2034','2034'),
        ('2035','2035'),
        ('2036','2036'),
        ('2037','2037'),
        ('2038','2038'),
        ('2039','2039'),
        ('2040','2040'),
    ], sring='Expiry Year')
    add_info = fields.Char('Additional Info')
    set_att = fields.Boolean('Set Account Fee')
    acc_fee_rule = fields.Selection([
        ('non','Do Not Charge Account Fee'),
        ('tcr','Bill When Transaction has been Posted'),
        ('osb','Bill when outsanding bill exist'),
        ('tcb','Bill When Transaction Posted OR when outsanding bill exist'),
    ], string='Account fee Rule')
    gl_acc = fields.Char('GL Account')
    flat_ffe_am = fields.Float('Flat fee Amount')
    flat_fee_curr = fields.Many2one('res.currency')
    # global rec
    gb_ced_partner_id = fields.Many2one('res.partner', string='Global Credit Group')
    gb_cred_limit = fields.Float(string='Global Credit Limit')
    gb_cred_curr_is = fields.Many2one('res.currency')
    gb_cred_apprr = fields.Boolean('Global Credit Approved')
    gb_arr_cred_hold = fields.Boolean('Global AR on Credit Hold')
    gb_not_chkoverdue_inv = fields.Boolean('Global Do Not Check Overdue Invoices Status')
    # Invoicing page
    enter_receipt_po = fields.Boolean('Enter Receipt Posting In..')
    cust_se_bill = fields.Boolean('Customer Self Bills')
    iss_stat_pack = fields.Boolean('Issue Statement Pack')
    charge_group_ids = fields.One2many('charge.grouping','partner_id')
    job_chrg = fields.Selection([
        ('all', 'All Job Types'),
        ('abk', 'Standalone Transport Booking Booked via CBA'),
        ('acd', 'Linear and Agency Detention Invoice'),
        ('acr', 'Air Cargo'),
        ('agb', 'Linear and Agency Booking'),
        ('ags', 'Linear and Agency Bill of Landing'),
        ('ahe', 'Air Cargo CTO Export HAWB'),
        ('ahw', 'Air Cargo CTO Import HAWB'),
        ('asc', 'Linear and Agency Sundry Charges'),
        ('ava', 'Linear and Agency Voyage Accounting'),
        ('awa', 'Master Air Waybill'),
        ('brk', 'Declaration Job'),
        ('cae', 'E manifest Forwarder'),
        ('cll', 'CFS Load List'),
        ('csh', 'CFS Shipment'),
        ('cst', 'FCL Container Storage'),
        ('cto', 'Air Cargo CTO'),
        ('cyi', 'Container Yard Gate In Job'),
        ('cyo', 'Container Yard Gate Out Job'),
        ('cys', 'Container Yard Storage  Job'),
        ('fcn', 'Consol'),
        ('gcn', 'Gateway Consol'),
        ('isf', 'Imported Security Filing'),
        ('ltc', 'Land Transport Consignment'),
        ('man', 'e-Manifest'),
        ('msc', 'Non Job related'),
        ('nct', 'Custom Transit(NCTS)'),
        ('pcb', 'Post Clearancer Declaration Job'),
        ('qsh', 'Quick Booking'),
        ('sab', 'Shipment and Brokerage'),
        ('shp', 'Shipment'),
        ('tbm', 'Standalone Transport Booking'),
        ('tcw', 'Transport Booking Consignment'),
        ('tdc', 'Transit Dispatch'),
        ('trc', 'Transit receive'),
        ('trn', 'Port Transport'),
        ('ubr', 'Air Cargo Outturn'),
        ('win', 'Warehouse Receive'),
        ('wki', 'Work Item'),
        ('wkp', 'Project'),
        ('wkr', 'Customer Service Ticket'),
        ('wou', 'Warehouse Release'),
        ('wsc', 'Warehouse Stockable'),
        ('wsj', 'Warehouse Ad Hoc Service Job'),
        ('wst', 'Warehouse Periodic'),
    ], string='Job type')
    direction_inv = fields.Selection([('no_data', 'No Data')], string='Direction')
    mode_inv = fields.Selection([('no_data', 'No Data')], string='Mode')
    display_chrg = fields.Selection([
        ('def', 'Use Default From Registry - refer to registry settings for details'),
        ('alp', 'Alphabetical'),
        ('rol', 'Roll Up charges'),
        ('rsq', 'Roll Up charges and Sequence'),
        ('seq', 'Sequence'),
        ('ssq', 'Subtotal Charges and Sequence'),
        ('sub', 'Subtotal Charges'),
        ('usr', 'User Entered'),
    ], string='Display')
    style_chrg = fields.Selection([
        ('def', 'Use Default From Registry - refer to registry settings for details'),
        ('nog', 'No Grouping Of Invoice Charges'),
        ('all', 'All Charges Except Custom Duty Tax as One Line'),
        ('aec', 'Origin, Loading, Freight, Insurance, Unload and Destination as one Line'),
        ('oaf', 'Origin, Loading, Freight and Insurance as one Line'),
        ('orf', 'Origin and Freight as one Line'),
        ('frt', 'Freight Charges as one Line'),
        ('fad', 'Freight, Insurance, Unload and Destination as one Line'),
        ('ofd', 'Origin and Landing as one Line, Freight and Insurance as one Line, Unload and Dest. as one Line'),
        ('ofo', 'Origin and Landing as one Line, Freight and Insurance as one Line'),
    ], string='Style')
    invoice_chrg = fields.Selection([
        ('def', 'Use Default From Registry - refer to registry settings for details'),
        ('all', 'Calc. Desc. for All Charges'),
        ('alx', 'Calc. Desc. for All Charges (With EX Rate and Foreign Amount)'),
        ('frt', 'Calc. Desc. for Freight Charges'),
        ('frx', 'Calc. Desc. for Freight Charges (With EX Rate and Foreign Amount)'),
        ('faf', 'Calc. Desc. for Freight and FOB Charges'),
        ('ffx', 'Calc. Desc. for Freight and FOB Charges (With EX Rate and Foreign Amount)'),
        ('non', 'Charge Code Description Only'),
        ('nex', 'Charge Code Desc., EX Rate and Foreign Amount'),

    ], string='Invoice')
    posting_chrg = fields.Selection([
        ('def', 'Use Default From Registry - refer to registry settings for details'),
        ('dfi', 'Disbursement and Final Invoice'),
        ('dfc', 'Disbursement in Foreign Currency and Final Invoice'),
        ('dfx', 'Disbursement in Foreign Currency (No Final Invoice, Only Disbursement Invoice)'),
        ('dff', 'Disbursement, Freight in Foreign Currency and Final Invoice'),
        ('dft', 'Disbursement and FRT Group on Disbursement Invoice and Final Invoice'),
        ('dfr',
         'Disbursement and FRT Group on Disbursement Invoice Per Foreign Currency, Standard Invoice Per Foreign Currency and Final Invoice'),
        ('ddf', 'Disbursement in Foreign Currency and freight in Foreign Currenct and Final Invoice'),
        ('dfo', 'Disbursement, Invoice per Foreign Currency and Final Invoice'),
        ('dsb', 'Disbursement Invoice Only'),
        ('dsf', 'Disbursement Per Foreign Currency and Standard Invoice Per Foreign Currency Final Invoice'),
        ('fio', 'Final Invoice Only'),
        ('fiu', 'Invoice Per Foreign Currency and Final Invoice'),
        ('ffi', 'Freight in Foreign Currency and Final Invoice'),
        ('itc', 'Invoiuce Per Tax Rate'),

    ], string='Posting')
    currency_chrg_id = fields.Many2one('res.currency', string='Currency')
    # peridic invoice conf
    periodic_invoice_ids = fields.One2many('periodic.invoice','partner_id')
    job_type_per = fields.Selection([],string='Job Type')
    bill_int = fields.Selection([],string='Billing Interval')
    trans = fields.Selection([],string='Transport Mode')
    serv_lev = fields.Selection([],string='Service Level')
    comm = fields.Selection([],string='Commence')
    layout = fields.Selection([],string='Layout')
    direct_per = fields.Selection([],string='Direction')
    sec_lay = fields.Selection([],string='Sec. layout')
    # charge code
    charge_code_ids =fields.One2many('charge.code','partner_id')
    # buyer
    buy_con_inv_sty = fields.Selection([
        ('def', 'Use Default From Registry - refer to registry settings for details'),
    ], string='Buyers Consol Invoicing Style')
    # Payable
    # creditor details
    account_group_pay = fields.Selection([('no_data', 'No Data')], string='Account group')
    account_relationship_pay = fields.Selection(
        [('std', 'Standard Account Relation Ship'), ('key', 'Key Client'), ('sig', 'Significant Client')],
        string='Account RelationShip')
    conc_categ_pay = fields.Selection([('unr', 'Unrelated Company'),
                                   ('who', 'Wholly owned Subsidiary'),
                                   ('mir', 'Minority Interest with reporting'),
                                   ('min', 'Minority Interest with no reporting'),
                                   ('rmi', 'Related Minority Shareholder'),
                                   ('rmj', 'Related Majority Shareholder'),
                                   ('rwh', 'Related Wholly Owning Shareholder'),
                                   ('gmi', 'Group Company Related Minority(no direct Ownership)'),
                                   ('gmj', 'Group Company Related Majority(no direct Ownership)'),
                                   ], string='Consolidation Category')
    # defaults
    currency_pay_id = fields.Many2one('res.currency', string='Currency')
    bank_pay_id = fields.Many2one('res.bank',string='Bank')
    charge_code = fields.Char('Charge Code')
    settle_grp_pay = fields.Many2one('res.partner','Settlement Group')
    # cedit details
    credit_limit_pay = fields.Float('Credit Limit')
    agreed_pay_meth_payable = fields.Selection([
        ('chk', 'Business Check'),
        ('ccd', 'Credit Card'),
        ('trf', 'Bank transfer'),
        ('cbc', 'Cash and/or  Bank check'),
        ('dbc', 'Debit Card'),
    ], string='Agreed Payment Method')
    # payment terms
    payment_terms = fields.Selection([
        ('def','Default From AP Settlement Group'),
        ('cod','Cash On delivery'),
        ('cus','From Custom clearance date'),
        ('inv','From Date of Invoice'),
        ('mth','From End of Invoice'),
        ('shp','From date of Shipment'),
        ('pia','Payment in Advance'),
    ], string='Payment Terms')
    days = fields.Float('Days')
    # tax details
    vat_recog_pay = fields.Selection(
        [('non', 'Not Applicable'), ('def', 'Tax is Applicable-Default Recognition Rules Apply'),
         ('acr', 'Accural Basis-All tax for this Organization reported on Accural Basis'),
         ('csh', 'Cash Basis-All tax for this Organization reported on Cash Basis')],
        string='VAT Recognition and reporting Basis Override')
    with_hol_tax_pay = fields.Boolean('Withholding Tax is Applicable')
    # other details
    pay_inv_post_pay = fields.Boolean('Pay Invoice After posting')
    iss_set_bil_inv = fields.Boolean('Issue Self Billing Invoice')
    # Quality Assurance
    quality_assured_pay = fields.Boolean('Quality Assured')
    last_check_pay = fields.Datetime('Last Checked')
    # External SYstem
    external_credit_code_pay = fields.Char('External Credit Code')
    # company data
    trans_cre_res_pay = fields.Selection(
        [('non', 'No Restriction'), ('inv', 'Restricted from creating New Invoice, Credit note and Adjustment note'),
         ('all', 'Restricted from creating new Transactions(All Transaction Types)'),
         ('bal',
          'Restricted from creating Transactions that would cause the outstanding balance in local Currency to increase in value')],
        string='Transaction creation Restriction')
    # acc det
    account_bank_details_pay_ids = fields.One2many('account.bank.details','partner_id')
#shipper
    related_parties_ids = fields.One2many('partner.related.parties', 'related_partner_id', string='Related Parties', copy=False)
    approve_to_print_original_bill = fields.Boolean(string='Approve to Print Original Bill of Loading')
    auto_create_parts_as_import_export = fields.Boolean(string='Auto-create Parts as Both Import and Export')
    house_bill_pre_allocation = fields.Char(string='House Bill Pre-Allocation')
    container_detention_ids = fields.One2many('container.detention','partner_id')
    cto_storage_ids = fields.One2many('cto.storage','partner_id')
    exporter_category = fields.Selection([('std', 'Standards Account Relationship')], string='Account fee Rule')
    shipper_country_id = fields.Many2one('res.country', string='Country Of Origin')
    shipper_currency_id = fields.Many2one('res.currency', string='Default Currency')
    shipper_incoterm_id = fields.Many2one('account.incoterms', string='Default Incoterm')
    awb_address_defaults_to = fields.Selection([('doc', 'Documentary Address'),
                                                ('ofc', 'Office Address'),
                                                ('pic', 'Pickup Address')], string='AWB Address Defaults To')
    invoice_price_from_ls_cost = fields.Selection([('yes', 'The Unit Price of The Commercial Invoice Line defaults to a Products Last Cost'),
                                                   ('no', 'Unit Price of The Commercial Invoice Line is Calculated Normally')],
                                                  string='Invoice Price From Last Cost')
    authority_to_leave = fields.Selection([('yes', 'Authority to leave is granted'),
                                           ('no', 'Authority to leave is denied'),
                                           ('def', 'Default From Registry (Currently Authority to leave is denied)')],
                                          default='def', string='Authority To Leave')
    unaudited_export_product = fields.Selection([('non', 'No Action'),
                                           ('wrn', 'Add Warning Validation'),
                                           ('def', 'Registry Default'),
                                           ('err', 'Add Message Error Validation')],
                                          default='non', string='Unaudited Export Product')
    required_order_no_on_doc = fields.Boolean(string='Requires Order Numbers on Documents')
    required_link_order_tacking = fields.Boolean(string='Required Linked Order Tracking')
    bill_agent_charges_direct = fields.Boolean(string='Bill Agents Changes Direct')
    always_own_product = fields.Boolean(string='Always Owns Product')
    shipment_goods_description = fields.Char(sting='Goods Description')
    handling_instructions = fields.Char(sting='Handling Instructions')
    service_level_id = fields.Many2one('service.level', string='Service Level')

    override_system_default = fields.Boolean(string='Override System Default')
    service_level_ids = fields.Many2many('service.level', string='Service Level', copy=False)

    exporter_bank_name = fields.Char(sting='Exporters Bank Name')
    exporter_bank_account = fields.Char(sting='Exporters Bank Account')
    exporter_swift_code = fields.Char(sting='Exporters SWIFT Code')
    method_of_payment = fields.Char(sting='Method Of Payment')
    additional_information = fields.Char(sting='Additional Information')

    #shipper/consignee
    shipper_consignee_ids = fields.One2many('shipper.consignee','partner_id')
    code_ship = fields.Many2one('res.partner', string='Code')
    imp_ctry = fields.Many2one('res.country','Imp Ctry.')
    curr_ship_id = fields.Many2one('res.currency','Currency')
    contr_cust_id = fields.Many2one('res.partner','Controlling Customer')
    import_brk = fields.Many2one('res.partner','Import Broker')
    prdct_rlshp = fields.Selection([
        ('imp','Importer'),
        ('sup','Supplier'),
    ], string='Product Relationship')
    doc_to = fields.Selection([
        ('imp','Send Import Documents To Importer'),
        ('brk','Send Import Documents To Broker'),
        ('bth','Send To Both Importer and Broker'),
    ], string='Docs To')
    auth_to_leave_ship = fields.Selection(
        [('def_from_reg', 'Default From Registry(Currently Authority to leave is denied).'),
         ('no', 'Authority to leave is denied'), ('yes', 'Authority to leave is Granted')], string='Authority to Leave')
    e_freight_status = fields.Selection([
        ('no_data','No Data')
    ], string='e-Freight Status')
    #custom valuation defaults
    trans_rel_ship = fields.Selection([
        ('no_data','No Data')
    ], string='Trans. Related')
    valu_basis = fields.Selection([
        ('no_data','No Data')
    ], string='Valuation Basis')
    ins_upl = fields.Float('Insurance Uplift')
    royalty = fields.Float('Royalty %')

    #filters
    #filters
    shipper_mode_ids = fields.One2many('shipper.mode','partner_id')
    trans = fields.Selection([
        ('air', 'Air'),
        ('ocean', 'Sea'),
        ('land', 'Road'),
        ('sea_then_air', 'Sea then Air'),
        ('air_then_sea', 'Air then Sea'),
        ('rail', 'Rail'),
        ('courier', 'Courier'),
        ('documentation', 'Documentation')
    ], string='Transport Mode')
    Cont_mode = fields.Selection([
        ('no_data','no Data')
    ], string='Container Mode')
    # def
    incoterm = fields.Many2one('freight.incoterms','Incoterm')
    serv_lev_ship = fields.Selection([
        ('no_data','No Data')
    ], string='service Level')
    orig_port_id = fields.Many2one('freight.port','Origin Port')
    dest_port_id = fields.Many2one('freight.port','Destination Port')
    incoterm_mode = fields.Selection([
        ('no_data','No Data')
    ], string='Incoterm Mode')
    carrier = fields.Many2one('res.partner','Carrier')
    send_ag = fields.Many2one('res.partner','Sending Agent')
    rec_ag = fields.Many2one('res.partner','Receiving Agent')
    contr_cust_def_id = fields.Many2one('res.partner','Controlling Customer')
    imp_cust_brk = fields.Many2one('res.partner','Import Customs Broker')
    org_bill = fields.Float('Original Bills')
    cop_bill = fields.Float('Copy Bills')
    inc_place = fields.Char('Incoterm Place')
    pkp_trm = fields.Selection([
        ('no_data','No Data')
    ], string='Pickup P.Tm')
    div_add = fields.Many2one('res.partner','Div. Address')
    div_cont = fields.Many2one('res.partner','Div. Contacts')
    pckp_add = fields.Many2one('res.partner','Pickup Address')
    pckp_cont = fields.Many2one('res.partner','Pickup Contact')
    ovd_del = fields.Boolean('Override delivery Days')
    del_day_est = fields.Float('Delivery Days Est.')
    not_part_contact = fields.Many2one('res.partner','Notify partner contact')
    del_po_tran_con = fields.Char('Delivery Pirt Transport Contractor')
    arr_loc = fields.Selection([('no_data','No Data')],string='Arr. Location')
    cust_ex_size = fields.Selection([('no_data','No Data')],string='Custom exam Site')

    country_image_url = fields.Char(related='country_id.image_url')

    # Shipping Line
    scac_code = fields.Char(string='SCAC Code')
    cw_code = fields.Char(string='CW1 Code')
    is_system = fields.Boolean(string='Is System')
    is_nvo = fields.Boolean(string='Is NVO')
    is_ocean_carrier_messaging = fields.Boolean(string='Ocean Carrier Messaging')
    is_global_sailing_schedule = fields.Boolean(string='Global Sailing Schedule')
    is_container_automation = fields.Boolean(string='CargoSphere Rates')
    is_invoice = fields.Boolean(string='Invoice')

    @api.constrains('email')
    def _check_partner_email_address(self):
        """
        To check partner Email is valid or not
        """
        for partner in self:
            if partner.email:
                if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', partner.email) == None:
                    raise ValidationError(_("%s is an invalid email") % partner.email.strip())

    @api.onchange('country_id')
    def onchange_partner_country(self):
        """
        Set country code before the phone and mobile
        :return:
        """
        for partner in self:
            partner.write({'phone': '', 'mobile': ''})
            if partner.country_id and partner.country_id.phone_code:
                partner.write({'phone': '+%s'%partner.country_id.phone_code, 'mobile': '+%s'%partner.country_id.phone_code})
