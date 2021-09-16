from odoo import api, fields, models, _

class FreeWaiting(models.Model):
    _name = 'free.waiting'

    partner_id = fields.Many2one('res.partner',string='Partner')
    container_type_id = fields.Many2one('container.type',string='Container Type')
    drop_mode = fields.Selection([
        ('any','Any'),
        ('ask','Ask Client'),
        ('haul_supp_lift', 'Hauler Supplies Lift'),
        ('hand_premise', 'Hand Unload/Load by Premise'),
        ('hand_haul', 'Hand Unload/Load by Hauler'),
        ('drop_cont_sup_lift','Drop Container - Premise supplies Lift'),
        ('prem_supp_lift', 'Premise Supplies Lift'),
        ('drop_cont_side', 'Drop Container with Sideloader'),
        ('drop_trail','Drop Trailer'),
        ('wait_unpack_pack','Wait for Unpack/Pack'),

    ],string='Drop Mode')
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
    Description = fields.Char('Description')
    has_tynes = fields.Boolean('Has Tynes')
    high_cube = fields.Boolean('High Cube')
    has_vents = fields.Boolean('Has Vents')
    container_transport_mode = fields.Selection([
        ('sea','Sea FCL Container'),
        ('air','Air ULD Container'),
        ('road','Road/Truck Container'),
    ],string='Container Transport Mode')
    container_type = fields.Selection([
        ('refrige','Refrigerated'),
        ('dry','Dry Storage'),
        ('top','Open Top'),
        ('flat','Flat Rack'),
        ('bloster','Bloster'),
        ('tank','Tank'),
        ('other','Other'),
        ('mafi','Mafi'),
    ], string='Container Type')
    uld_rate_class = fields.Selection([('no_data','No data')])
    # Custom Container Codes
    country_data_ids = fields.One2many('country.data','container_type_id')
    #ISO Container Details
    iso_type = fields.Selection([
        ('no_data','No data')
    ], string='ISO Type')
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
        ('20f','Twenty Foot Equivalent Unit'),
        ('20r','Twenty Foot Reefer'),
        ('20h','Twenty Foot Hight Cube'),
        ('40f','Forty Foot Equivalent Unit'),
        ('40r','Forty Foot Reefer'),
        ('40h','Forty Foot Hight Cube'),
        ('45f','Forty Five Foot'),
        ('gen','Genset')
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

    container_type_id = fields.Many2one('container.type',string='Container')
    country_id = fields.Many2one('res.country',string='Country')
    country_code = fields.Char(related='country_id.code')
    code = fields.Char('Code')
    usage = fields.Char(string='Usage')
    description = fields.Char('Description')
