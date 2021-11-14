# -*- coding: utf-8 -*-
{
    'name': 'Freight Accounting Shipment pdf Report',
    'version': '14.0.1.50',
    'category': 'Accounting & Finance',
    'description': """
                Freight Accounting Shipment 
               """,
    'sequence': 51,
    'depends': ['account','ebs_freight_pricing'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        # "security/ir.model.access.csv",
        "report/report.xml",
        "report/templates.xml",
        "report/form_header.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
