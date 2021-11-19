# -*- coding: utf-8 -*-
{
    'name': 'Account Report Extended',
    'version': '14.0.0.0',
    'category': 'Accounting/Accounting',
    'description': """
                Multi currency according to the company timezone
               """,
    'sequence': 51,
    'depends': ['account', 'base','account_reports','web'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        # 'views/res_company.xml',
        'wizard/res_config_settings_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
