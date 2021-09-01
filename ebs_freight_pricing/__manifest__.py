# -*- coding: utf-8 -*-
{
    'name': "ebs_freight_pricing",

    'summary': """Freight Pricing Management""",

    'description': """Freight Pricing Management""",

    'author': "Ragaa Maher",
    'website': "https://www.everbsgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'freight', 'sale_management'],

    # always loaded
    'data': [
        'data/charges_data.xml',
        'data/freight_pricing_data.xml',
        'security/ir.model.access.csv',
        'views/freight_pricing_views.xml',
        'views/booking_views.xml',
        'views/sales_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
