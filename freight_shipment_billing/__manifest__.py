# -*- coding: utf-8 -*-
{
    'name': 'Freight Shipment Billing',
    'version': '1.0.0.6',
    'category': 'Freight',
    'description': """
                Freight Shipment Billing
               """,
    'sequence': 51,
    'depends': ['base', 'account', 'freight','freight_management'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "security/shipment_billing_security.xml",
        "views/product_views.xml",
        "views/account_move_view.xml",
        "views/freight_operation_billing_views.xml",
        "views/freight_operation_views.xml",
        "views/freight_booking_views.xml",
        "views/freight_job_request_views.xml",
        "views/consol_details_views.xml",
        "wizard/res_config_settings_view.xml",
        "data/ir_cron.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
