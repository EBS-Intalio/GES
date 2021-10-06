# -*- coding: utf-8 -*-
{
    'name': 'Account Sale Budget',
    'version': '1.0.0.0',
    'category': 'Accounting & Finance',
    'description': """
                Account Sale Budget
               """,
    'sequence': 51,
    'depends': ['account','sale' ,'operating_unit', 'account_operation_matrix', 'freight_management'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "views/account_budget_views.xml",
        "views/sale_budget_views.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
