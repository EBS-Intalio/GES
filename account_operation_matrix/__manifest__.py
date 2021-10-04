# -*- coding: utf-8 -*-
{
    'name': 'Account Operation Matrix',
    'version': '1.0.0.1',
    'category': 'Accounting & Finance',
    'description': """
                Account Operation Matrix
               """,
    'sequence': 51,
    'depends': ['account','freight'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "views/account_operation_matrix_views.xml",
        "views/account_move_views.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
