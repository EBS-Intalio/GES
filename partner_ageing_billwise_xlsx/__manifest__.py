# -*- coding: utf-8 -*-
{
    'name': 'Aged Partner Balance In Excel',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Bill-Wise Aged Partner Balance in Excel Format',
    'description': """
    This module provides features to take an excel report of bill-wise aged partner balance.
    """,
    'author': 'EBS',
    'website': "http://www.ever-bs.com/",
    'depends': ['report_xlsx', 'account'],
    'data': [
        "security/ir.model.access.csv",
        'views/report_aged_partner_billwise.xml',
        'report/aged_partner_report.xml'
            ],
    'demo': [],
    # 'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
