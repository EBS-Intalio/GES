# -*- coding: utf-8 -*-
{
    'name': 'Freight Accounting Extension',
    'version': '1.0.0.0',
    'category': 'Accounting & Finance',
    'description': """
                Freight Accounting Extension
               """,
    'sequence': 51,
    'depends': ['account', 'sales_team','operating_unit', 'account_operating_unit','freight_management'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
        "views/account_journal_view.xml",
        "views/operation_unit_views.xml",
        "views/account_payment_view.xml",
        "views/china_account_views.xml",
        "views/account_account_views.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
