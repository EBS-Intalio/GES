# -*- coding: utf-8 -*-
{
    'name': 'Account Extended',
    'version': '14.0.0.9',
    'category': 'Accounting/Accounting',
    'description': """
                Multi currency according to the company timezone
               """,
    'sequence': 51,
    'depends': ['account', 'base','account_reports','web'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        'views/ir_cron.xml',
        'views/res_company.xml',
        'views/assets.xml',
        'views/account_payment.xml',
        'wizard/res_config_settings_view.xml',
        'views/search_template_inherit.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
