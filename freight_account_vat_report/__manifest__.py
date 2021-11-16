# -*- coding: utf-8 -*-
{
    'name': 'Freight Account VAT Report',
    'version': '14.0.0.5',
    'category': 'Freight',
    'description': """
                Freight VAT
               """,
    'sequence': 51,
    'depends': ['account','freight_shipment_billing'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        # "security/ir.model.access.csv",
        "views/sales_vat_view.xml",
        "views/purchase_vat_view.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
