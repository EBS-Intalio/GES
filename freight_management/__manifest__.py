# -*- coding: utf-8 -*-
{
    'name': 'Freight Request Management',
    'version': '14.0.0.3',
    'category': 'Freight',
    'description': """
                Freight Management
               """,
    'sequence': 51,
    'depends': ['mail', 'freight', 'crm', 'base', 'ebs_freight_pricing', 'sale_management'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "data/website_menu.xml",
        "data/ir_sequence.xml",
        "views/freight_job_request.xml",
        "views/freight_hs_code.xml",
        "views/res_partner.xml",
        "views/crm_lead.xml",
        "views/freight_pricing.xml",
        "views/freight_templates.xml"
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
