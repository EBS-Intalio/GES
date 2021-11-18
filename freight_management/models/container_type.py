from odoo import api, fields, models, _
import pytz

# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


def _tz_get(self):
    return _tzs


class FreeWaiting(models.Model):
    _name = 'free.waiting'

    partner_id = fields.Many2one('res.partner', string='Partner')
    container_type_id = fields.Many2one('container.type', string='Container Type')
    drop_mode = fields.Selection([
        ('any', 'Any'),
        ('ask', 'Ask Client'),
        ('haul_supp_lift', 'Hauler Supplies Lift'),
        ('hand_premise', 'Hand Unload/Load by Premise'),
        ('hand_haul', 'Hand Unload/Load by Hauler'),
        ('drop_cont_sup_lift', 'Drop Container - Premise supplies Lift'),
        ('prem_supp_lift', 'Premise Supplies Lift'),
        ('drop_cont_side', 'Drop Container with Sideloader'),
        ('drop_trail', 'Drop Trailer'),
        ('wait_unpack_pack', 'Wait for Unpack/Pack'),

    ], string='Drop Mode')
    cfs = fields.Integer('CFS')
    cne = fields.Integer('CNE')
    cnr = fields.Integer('CNR')
    cto = fields.Integer('CTO')
    cyd = fields.Integer('CYD')
    other = fields.Integer('Other')


class ContainerType(models.Model):
    _name = 'container.type'

    # Container Type Details
    name = fields.Char('Type')
    description = fields.Char('Description')
    has_tynes = fields.Boolean('Has Tynes')
    high_cube = fields.Boolean('High Cube')
    has_vents = fields.Boolean('Has Vents')
    lang_cont = fields.Many2one('res.lang', string="Lang")
    container_transport_mode = fields.Selection([
        ('sea', 'Sea FCL Container'),
        ('air', 'Air ULD Container'),
        ('road', 'Road/Truck Container'),
    ], string='Container Transport Mode')
    container_type = fields.Selection([
        ('refrige', 'Refrigerated'),
        ('dry', 'Dry Storage'),
        ('top', 'Open Top'),
        ('flat', 'Flat Rack'),
        ('bloster', 'Bloster'),
        ('tank', 'Tank'),
        ('other', 'Other'),
        ('mafi', 'Mafi'),
    ], string='Container Type')
    uld_rate_class = fields.Selection([('no_data', 'No data')])
    # Custom Container Codes
    country_data_ids = fields.One2many('country.data', 'container_type_id')
    # ISO Container Details
    iso_type = fields.Many2one('iso.types.container', string='ISO Type')
    iso_off_cont_size = fields.Boolean('ISO Official Container Size')
    is_comm_Oversize = fields.Boolean('Is Commonly Oversize')
    Size = fields.Char('Size')
    description = fields.Text('Description')
    # Container Dimesions
    lenght_in_foot = fields.Float('Length')
    lenght_in_meter = fields.Float()
    lenght_in_foot1 = fields.Float()
    lenght_in_inch = fields.Float()
    container_width_in_foot = fields.Float()
    container_width_in_meter = fields.Float()
    container_width_in_inch = fields.Float()
    container_width_in_foot2 = fields.Float()
    height_width_in_foot = fields.Float()
    height_width_in_meter = fields.Float()
    height_width_in_inch = fields.Float()
    height_width_in_foot2 = fields.Float()
    teu_count = fields.Float('TEU Count')
    max_gross_wt_lb = fields.Float()
    max_gross_wt_kg = fields.Float()
    tare_wt_lb = fields.Float()
    tare_wt_kg = fields.Float()
    max_net_wt_lb = fields.Float()
    max_net_wt_kg = fields.Float()
    capacity_cf = fields.Float()
    capacity_m3 = fields.Float()
    cont_sto_class = fields.Selection([
        ('20f', 'Twenty Foot Equivalent Unit'),
        ('20r', 'Twenty Foot Reefer'),
        ('20h', 'Twenty Foot Hight Cube'),
        ('40f', 'Forty Foot Equivalent Unit'),
        ('40r', 'Forty Foot Reefer'),
        ('40h', 'Forty Foot Hight Cube'),
        ('45f', 'Forty Five Foot'),
        ('gen', 'Genset')
    ], string='Container storage Class')

    frei_charg_rate_class = fields.Selection([
        ('20gn', '20 Generic'),
        ('40gn', '40 Generic'),
    ], string='Freight Charges Rate Class')
    hand_charg_rate_class = fields.Selection([
        ('20gn', '20 Generic'),
        ('40gn', '40 Generic'),
    ], string='Handling Charges Rate Class')
    eq_sz_ty_code = fields.Selection([
        ('dct', 'Dime Coated Tank'),
        ('ect', 'Epoxy Coated Tank'),
        ('pt', 'Pressurized Tank'),
        ('rt', 'Refrigerated Tank'),
        ('sst', 'Stainless Steel Tank'),
        ('nr40', 'Nonworking Reefer 40ft'),
        ('ept', 'Europalet'),
        ('sp', 'Scandinavian Pallet'),
        ('trailer', 'Trailer'),
        ('nr20', 'Nonworking Reefer 20ft'),
    ], string='Equipment Size Type Code')


class CountryDetails(models.Model):
    _name = 'country.data'

    container_type_id = fields.Many2one('container.type', string='Container')
    unlco_id = fields.Many2one('unloco.data', string='Unlco')
    country_id = fields.Many2one('res.country', string='Country')
    country_code = fields.Char(related='country_id.code')
    code = fields.Char('Code')
    usage = fields.Char(string='Usage')
    description = fields.Char('Description')


class UNLOCOData(models.Model):
    _name = 'unloco.data'

    name = fields.Char('UNLOCO Code')
    iata_code = fields.Char('IATA Code')
    iata_reg_code = fields.Char('IATA Region Code')
    port_name = fields.Char('Port Name')
    proper_name = fields.Char('Proper Name')
    country_id = fields.Many2one('res.country', STring='Country')
    state_id = fields.Many2one('res.state', STring='State')
    tz = fields.Selection(_tz_get, string='Timezone', default=lambda self: self._context.get('tz'),
                          help="The partner's timezone, used to output proper date and time values "
                               "inside printed reports. It is important to set a value for this field. "
                               "You should use the same timezone that is otherwise used to pick and "
                               "render date and time values: your computer's timezone.")
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    # identifiers
    has_post = fields.Boolean('Has Post')
    has_customs = fields.Boolean('Has Customs ')
    has_post = fields.Boolean('Has Post')
    has_unload = fields.Boolean('Has Unloads')
    has_airport = fields.Boolean('Has Airport')
    has_rail = fields.Boolean('Has Rail')
    has_road = fields.Boolean('Has Road')
    has_store = fields.Boolean('Has Store')
    has_terminal = fields.Boolean('Has Terminal')
    has_disc = fields.Boolean('Has Discharge')
    has_seaport = fields.Boolean('Has Seaport')
    has_outport = fields.Boolean('Has Outport')
    date_current = fields.Datetime('Date/time in AEDXB')
    date_covert = fields.Datetime('Date/time in')
    country_data_ids = fields.One2many('country.data', 'unlco_id', string='Local Codes')
    is_system_updateble = fields.Boolean('Is System Updatable')
    is_system = fields.Boolean('Is System')


class OrganizationalCategory(models.Model):
    _name = 'res.partner.org.cat'

    name = fields.Char('Name')
    code = fields.Char('Code')


class OrganizationNumber(models.Model):
    _name = 'res.partner.org.num'

    name = fields.Char('Name')
    code = fields.Char('Code')


class AccountBankName(models.Model):
    _name = 'account.bank.details'

    partner_id = fields.Many2one('res.partner', string='Partner')
    default_method = fields.Char('Default Method')
    currency_id = fields.Many2one('res.currency', 'Currency')
    name = fields.Char('Account Name')
    bank = fields.Many2one('res.bank', 'Bank')


class CurrencyUplift(models.Model):
    _name = 'currency.uplift'

    partner_id = fields.Many2one('res.partner', string='Partner')
    source = fields.Char('source')
    job_type = fields.Selection([('no_data', 'No data')], string='Job Type')
    direction = fields.Char('Direction')
    transport = fields.Char('Transport')
    currency_id = fields.Many2one('res.currency', 'Currency')
    cfx = fields.Float('CFX%')


class TermsDays(models.Model):
    _name = 'term.days'

    partner_id = fields.Many2one('res.partner')
    job_type = fields.Selection([('no_data', 'No data')], string='Job Type')
    Branch = fields.Char(string='Branch')
    depart = fields.Char(string='Department')
    direct = fields.Selection([('no_data', 'No data')], string='Direction')
    trans_mod = fields.Selection([('no_data', 'No data')], string='Transport Mode')
    inv_term = fields.Selection([('no_data', 'No data')], string='Invoice Team')
    agree_paym = fields.Char(string='Agreed Payment')


class ChargeGrouping(models.Model):
    _name = 'charge.grouping'

    partner_id = fields.Many2one('res.partner')
    job = fields.Selection([
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
    ], string='Job')
    direction_inv = fields.Selection([('no_data', 'No Data')], string='Direction')
    mode_inv = fields.Selection([('no_data', 'No Data')], string='Mode')
    display = fields.Selection([
        ('def', 'Use Default From Registry - refer to registry settings for details'),
        ('alp', 'Alphabetical'),
        ('rol', 'Roll Up charges'),
        ('rsq', 'Roll Up charges and Sequence'),
        ('seq', 'Sequence'),
        ('ssq', 'Subtotal Charges and Sequence'),
        ('sub', 'Subtotal Charges'),
        ('usr', 'User Entered'),
    ], string='Display')
    style = fields.Selection([
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
    invoice = fields.Selection([
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
    posting = fields.Selection([
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
    currency_id = fields.Many2one('res.currency', string='Currency')


class periodicInvoice(models.Model):
    _name = 'periodic.invoice'

    partner_id = fields.Many2one('res.partner')
    # job_type = fields.Char(string='job type')
    serv_dir = fields.Char(string='Service Directory')
    transport = fields.Char(string='Transport')
    serv_lev = fields.Char(string='Service Level')
    bill = fields.Char(string='Billing')
    # comm = fields.Char(string='Comm')
    # layout = fields.Char(string='Layout')
    lay_des = fields.Char(string='Layout Des.')
    # sec_l = fields.Char(string='Sec. Layout')
    sec_d = fields.Char(string='Sec. Layout description')
    job_type = fields.Selection([('air', 'Air'),
                                 ('ocean', 'Ocean'),
                                 ('land', 'Road'),
                                 ('sea_then_air', 'Sea then Air'),
                                 ('air_then_sea', 'Air then Sea'),
                                 ('rail', 'Rail'),
                                 ('courier', 'Courier'),
                                 ('documentation', 'Documentation'),
                                 ('all', 'ALL')], default='all', string='Job Title')
    comm = fields.Selection([
        ('last_day_of_month', 'Last Day Of Month'),
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    ], default='01', string='Commence')
    layout = fields.Selection([
        ('summary_by_charge_code', 'Summary By Charge Code'),
        ('summary_by_job', 'Summary By Job'),
        ('no_summary', 'No Summary'),
    ], default='summary_by_charge_code', string='Layout')
    sec_l = fields.Selection([
        ('summary_by_charge_code', 'Summary By Charge Code'),
        ('summary_by_job', 'Summary By Job'),
    ], string='Secondary Layout')

    _sql_constraints = [
        ('partner_uniq', 'UNIQUE (partner_id)', 'The Partner is Unique, Please Choice Another Partner!'),
        ('job_type_unique', 'UNIQUE (job_type)', 'The Job Type is Unique, Please Choice Another Job Type!'),
        ('comm_unique', 'UNIQUE (comm)', 'The Commence is Unique, Please Choice Another Commence!'),
        ('layout_unique', 'UNIQUE (layout)', 'The Layout is Unique, Please Choice Another Layout!'),
        ('sec_l_unique', 'UNIQUE (sec_l)', 'The Secondary Layout is Unique, Please Choice Another Secondary Layout!'),
    ]


class ChargeCode(models.Model):
    _name = 'charge.code'

    partner_id = fields.Many2one('res.partner')
    chrg_grp = fields.Char('Charge Group')
    chrg_code = fields.Char('Charge Code')


class ShipperConsignee(models.Model):
    _name = 'shipper.consignee'

    partner_id = fields.Many2one('res.partner')
    code = fields.Many2one('res.partner')
    unlco_id = fields.Many2one('unloco.data', string='Unlco')
    imp_ctry = fields.Many2one('res.country', string='Imp Ctry.')
    currency_id = fields.Many2one('res.currency', string='Curr')
    notify = fields.Char('Notify Party')
    fst_shp = fields.Date('1st ship')
    val_basis = fields.Float('Valuation Basis')
    trans_rel = fields.Selection([
        ('y', 'Yes(Related)'),
        ('n', 'No(Unrelated)'),
    ], string='Trans. Related')
    val_basis_2 = fields.Float('Val. Basis')
    ins_upl = fields.Float('Ins. Uplift')
    royalty = fields.Float('Royalty %')
    vend_id = fields.Char('Vendor ID')
    e_fre_status = fields.Char('e-Freight Status')
    atl = fields.Selection([
        ('def', 'No data')
    ], string='ATL')


class ShipperModes(models.Model):
    _name = 'shipper.mode'

    partner_id = fields.Many2one('res.partner')
    mode = fields.Char(string="Mode")
    cont = fields.Char(string='Cont')
    inco1 = fields.Char('INCO')
    inco2 = fields.Char('INCO')
    inco3 = fields.Char('INCO')
    service_lev = fields.Char('Service Level')
    over_deliv = fields.Boolean('Override Delivery')
    div_days = fields.Float('Div. days')
    org_bills = fields.Float('Original Bills')
    cop_bills = fields.Float('Copy Bills')
    load_port = fields.Char('Load Port')
    org_port = fields.Char('Origin Port')
    pckp_addr = fields.Char('Pickup Addr.')
    pckp_ctct = fields.Char('Pickup Ctct')
    pckp_ptrn = fields.Char('Pickup P.Tm.')
    disc = fields.Char('Discharge')
    dest = fields.Char('destination')
    div_add = fields.Char('Div. Address')
    div_cont = fields.Char('Div. Contact')
    div_p_tm = fields.Char('Div. P.Tm')
    not_part = fields.Char('Notify party')
    arr_loc = fields.Char('Arr. Location')
    ex_site = fields.Char('Ex. Site')


class PickupDelivery(models.Model):
    _name = 'pickup.delivery'

    partner_id = fields.Many2one('res.partner')
    type = fields.Char('Type')
    desc = fields.Char('Type description')
    from_date = fields.Date('from')
    to_date = fields.Date('To')
    day = fields.Char('Day')


class ISOType(models.Model):
    _name = 'iso.types.container'

    name = fields.Char('Description')
    code = fields.Char('Code')


class ContainerDetention(models.Model):
    _name = 'container.detention'

    partner_id = fields.Many2one('res.partner')
    carrier = fields.Many2one('res.partner', 'Carrier')
    detention = fields.Many2one('unloco.data', 'Detention')
    container = fields.Selection([
        ('20f', 'Twenty Foot Equivalent Unit'),
        ('20r', 'Twenty Foot Reefer'),
        ('20h', 'Twenty Foot Hight Cube'),
        ('40f', 'Forty Foot Equivalent Unit'),
        ('40r', 'Forty Foot Reefer'),
        ('40h', 'Forty Foot Hight Cube'),
        ('45f', 'Forty Five Foot'),
        ('gen', 'Genset')
    ], string='Container')
    days = fields.Char('days')


class CtoStorage(models.Model):
    _name = 'cto.storage'

    partner_id = fields.Many2one('res.partner')
    carrier = fields.Many2one('res.partner', 'Carrier')
    cto = fields.Many2one('res.partner', 'CTO')
    port_cont = fields.Many2one('unloco.data', 'Port/Country')
    class_cont = fields.Selection([
        ('20f', 'Twenty Foot Equivalent Unit'),
        ('20r', 'Twenty Foot Reefer'),
        ('20h', 'Twenty Foot Hight Cube'),
        ('40f', 'Forty Foot Equivalent Unit'),
        ('40r', 'Forty Foot Reefer'),
        ('40h', 'Forty Foot Hight Cube'),
        ('45f', 'Forty Five Foot'),
        ('gen', 'Genset')
    ], string='Class')
    credit_st = fields.Char('Creditor/Storage Data')
    days = fields.Char('Free days')
