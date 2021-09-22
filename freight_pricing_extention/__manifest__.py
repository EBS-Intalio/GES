# -*- coding: utf-8 -*-
{
    'name': 'Freight Pricing Extention',
    'version': '14.0.1.4',
    'category': 'Freight',
    'description': """
                Freight Pricing Extention
               """,
    'sequence': 51,
    'depends': ['ebs_freight_pricing','freight_management'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "views/freight_pricing.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
