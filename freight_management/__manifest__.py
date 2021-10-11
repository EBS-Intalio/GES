# -*- coding: utf-8 -*-
{
    'name': 'Freight Request Management',
    'version': '14.0.1.34',

    'category': 'Freight',
    'description': """
                Freight Management
               """,
    'sequence': 51,
    'depends': ['account', 'mail', 'freight', 'crm', 'base', 'uom', 'ebs_freight_pricing', 'sale_management', 'web','account_asset','account_budget','analytic','hr','operating_unit'],
    'author': 'Ever Business Solutions',
    'website': "http://www.ever-bs.com/",
    'data': [
        "security/ir.model.access.csv",
        "data/website_menu.xml",
        "data/ir_sequence.xml",
        "data/data.xml",
        "views/freight_job_request.xml",
        "views/freight_hs_code.xml",
        "views/res_partner.xml",
        "views/crm_lead.xml",
        "views/freight_pricing.xml",
        "views/freight_templates.xml",
        "views/freight_pod.xml",
        # "views/freight_pod_destination.xml",
        "views/freight_pol.xml",
        # "views/freight_por_origin.xml"
        "views/sale_order.xml",
        "report/sale_order_ges.xml",
        "report/sale_order_report.xml",
        "views/order_line_section.xml",
        "views/container_type.xml",
        "views/freight_package.xml",
        "views/unloco.xml",
        "views/partner_related_parties.xml",
        "views/service_level.xml",
        "views/freight_airline.xml",
        "views/freight_shipping_line.xml",
        "views/account_asset.xml",
        "views/account_move.xml",
        "views/account_budget.xml",
        "wizard/account_asset_sell.xml",
        "views/loose_cargo.xml",
        # "views/job_management_link.xml",
        "views/freight_container.xml",
        "views/reference_number.xml",
        "views/freight_commodity.xml",
        "views/freight_booking.xml",
        "wizard/freight_sailing.xml",
        "views/freight_vessel.xml",
        "views/vehicle_details.xml",
        "views/freight_operation.xml",
        "views/freight_incoterms.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
