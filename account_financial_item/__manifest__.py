# -*- coding: utf-8 -*-
{
    'name': 'Account Financial Item',
    'version': '1.0.0.1',
    'category': 'Accounting & Finance',
    'description': """
                Account Financial Line Item
               """,
    'sequence': 51,
    'depends': ['account'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "views/account_financial_item_views.xml",
        "views/account_account_views.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
