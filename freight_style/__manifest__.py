# -*- coding: utf-8 -*-
{
    'name': "freight_style",

    'summary': """
        Styling of Mandatory fields in Odoo""",

    'description': """
        Styling of Mandatory fields in Odoo
    """,

    'author': "EBS",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Theme',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/assets.xml',
    ],
}
