# -*- coding: utf-8 -*-
{
    'name': 'Account Reports Extention',
    'version': '1.0.0.1',
    'category': 'Accounting & Finance',
    'description': """
                Account Aged Payable & Receivable
               """,
    'sequence': 51,
    'depends': ['account', 'account_reports', 'account_operating_unit'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        'views/general_ledger_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
