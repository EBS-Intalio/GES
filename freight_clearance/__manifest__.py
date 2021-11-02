# -*- coding: utf-8 -*-
{
    'name': 'Freight Clearance',
    'version': '14.0.0.5',
    'category': 'Freight',
    'description': """
                Freight Clearance
               """,
    'sequence': 51,
    'depends': ['mail','freight_management', 'freight', 'crm', 'base', 'ebs_freight_pricing', 'sale_management'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "data/clearance_data.xml",
        "views/freight_clearance_views.xml",
        "views/freight_job_request_views.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
