# -*- coding: utf-8 -*-
{
    'name': "EBS Currency Revaluation",

    'summary': """
        alter the revaluation behavior in odoo """,

    'description': """
        alter the revaluation behavior in odoo
    """,

    'author': "Mohamed Rabiea",
    'website': "",


    'category': 'Accounting',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_reports'],

    # always loaded
    'data': [
        'views/account_account.xml',
    ],

}
