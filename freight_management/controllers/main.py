# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
from itertools import islice
import json
import xml.etree.ElementTree as ET
import logging
import re
import werkzeug.utils
import werkzeug.wrappers
import base64
import csv
import sys
import io
import tempfile

from odoo import fields
from odoo import http
from odoo.http import request, route
from odoo import http, tools, _
from odoo.exceptions import Warning
from odoo.addons.web.controllers.main import WebClient, Binary, Home

SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)
from datetime import datetime as dt
_logger = logging.getLogger(__name__)


class RequestCustom(http.Controller):

    @http.route(['/createrequest'], type='http', auth='user', website=True, cache=300, csrf=False)
    def portal_my_bookings_create(self, redirect=None, **post):
        partners = request.env['res.partner'].search([])
        consignees = request.env['res.partner'].search([('freight_type', '=', 'consignee')])
        shippers = request.env['res.partner'].search([('freight_type', '=', 'shipper')])
        users = request.env['res.users'].search([])
        incoterms = request.env['freight.incoterms'].search([])
        # move_type = request.env['freight.move.type'].search([])
        gateways = request.env['freight.port'].search([])
        airlines = request.env['freight.airline'].search([])
        vessels = request.env['freight.vessel'].search([])
        truckers = request.env['freight.trucker'].search([])
        packages = request.env['freight.package'].search([])

        values = {
            'partners':partners,
            'shipper': shippers,
            'consignees': consignees,
            'users':users,
            'incoterms':incoterms,
            # 'move_type':move_type,
            'packages': packages,
            'gateways':gateways,
            'airlines':airlines,
            'vessels':vessels,
            'truckers':truckers,
        }
        return request.render("freight_management.portal_request_create", values)

    @http.route(['/submit_request'], type='http', auth='public', website=True, cache=300,  csrf=False)
    def portal_my_request_submit(self, **post):
        partner_obj = request.env['res.partner']
        users = request.env['res.users']
        incoterms = request.env['freight.incoterms']
        # move_type = request.env['freight.move.type']
        gateways = request.env['freight.port']
        airlines = request.env['freight.airline']
        vessels = request.env['freight.vessel']
        truckers = request.env['freight.trucker']
        operation = request.env['freight.booking']
        final_dict = {}
        dir = ''
        if post:
            # Air Fields
            if 'origin_close' in post.keys() and post.get('origin_close') == 'on':
                final_dict['consider_origin_close'] = True
            if 'destination_close' in post.keys() and post.get('destination_close') == 'on':
                final_dict['consider_destination_close'] = True
            if 'danger' in post.keys() and post.get('danger') == 'on':
                final_dict['is_dangerous_goods'] = True

            # General Data
            # Mode of transport and shipment
            # final_dict['mode_of_transport'] = 'air'
            # if post.get('transport'):
            #     final_dict['mode_of_transport'] = post.get('transport')
            #     dir = post.get('transport')
            #
            # if final_dict.get('mode_of_transport') == 'air':
            #     final_dict['air_shipment'] = 'breakbulk'
            #     if post.get('air'):
            #         final_dict['air_shipment'] = post.get('air')
            # elif final_dict.get('mode_of_transport') == 'ocean':
            #     final_dict['air_shipment'] = 'fcl'
            #     if post.get('ocean'):
            #         final_dict['ocean_shipment'] = post.get('ocean')
            # else:
            #     final_dict['inland_shipment'] = 'ftl'
            #     if post.get('land'):
            #         final_dict['inland_shipment'] = post.get('land')
            #



            # if post.get('shipper_id'):
            #     post['shipper_id'] = int(post.get('shipper_id'))
            # if post.get('consignee_id'):
            #     post['consignee_id'] = int(post.get('consignee_id'))
            #
            # # if post.get('air_source_location_id'):
            # post['origin_airport_id'] = int(post.get('air_source_location_id'))
            # # if post.get('destination_location_id'):
            # post['destination_airport_id'] = int(post.get('air_destination_location_id'))
            # post['preferred_airline_id'] = int(post.get('preferred_airline_id'))
            # post['freight_incoterm_id'] = int(post.get('freight_incoterm_id'))




            # if post.get('mawb'):
            #     final_dict['mawb_no'] = post.get('mawb')
        #     if post.get('flight_no'):
        #         final_dict['flight_no'] = post.get('flight_no')
        #     if post.get('airline'):
        #         final_dict['airline_id'] = airlines.browse(int(post.get('airline'))).id
        #     #Ocean Fields
        #     if post.get('por_origin'):
        #         final_dict['por_origin'] = post.get('por_origin')
        #     if post.get('pol'):
        #         final_dict['pol'] = post.get('pol')
        #     if post.get('pod'):
        #         final_dict['pod'] = post.get('pod')
        #     if post.get('pofd_destination'):
        #         final_dict['pofd_destination'] = post.get('pofd_destination')
        #     if post.get('equipment_type'):
        #         final_dict['equipment_type'] = post.get('equipment_type')
        #     if post.get('shipping_line_id'):
        #         final_dict['shipping_line_id'] = partner_obj.browse(int(post.get('shipping_line_id'))).id
        #     if post.get('vessel_id'):
        #         final_dict['vessel_id'] = vessels.browse(int(post.get('vessel_id'))).id
        #     if post.get('voyage_no'):
        #         final_dict['voyage_no'] = post.get('voyage_no')
        #     if post.get('obl'):
        #         final_dict['obl'] = post.get('obl')
        #     # Inland Fields
        #     if post.get('cmr_no'):
        #         final_dict['truck_ref'] = post.get('cmr_no')
        #     if post.get('trucker_number'):
        #         final_dict['trucker_number'] = post.get('trucker_number')
        #     if post.get('vehicle_size'):
        #         final_dict['vehicle_size'] = post.get('vehicle_size')
        #     if post.get('vehicle_type'):
        #         final_dict['vehicle_type'] = post.get('vehicle_type')
        #     if post.get('trucker'):
        #         final_dict['trucker'] = truckers.browse(int(post.get('trucker'))).id
        #

        #     if post.get('freight_pc'):
        #         final_dict['freight_pc'] = post.get('freight_pc')
        #     if post.get('other_pc'):
        #         final_dict['other_pc'] = post.get('other_pc')
        #     if post.get('reefer_status'):
        #         final_dict['reefer_status'] = post.get('reefer_status')
        #     if post.get('temperature'):
        #         final_dict['temperature'] = post.get('temperature')
        #     if post.get('set_temperature'):
        #         final_dict['set_temperature'] = post.get('set_temperature')
        #     if post.get('commodity_category'):
        #         final_dict['commodity_category'] = post.get('commodity_category')
        #     if post.get('commodity_description'):
        #         final_dict['commodity_description'] = post.get('commodity_description')
        #     if post.get('trac_no'):
        #         final_dict['tracking_number'] = post.get('trac_no')
        #     if 'danger' in post.keys() and post.get('danger') == 'on':
        #         final_dict['dangerous_goods'] = True
        #         if 'danger_info' in post.keys():
        #             final_dict['dangerous_goods_notes'] = post.get('danger_info')
        #     if post.get('agent_id'):
        #         final_dict['agent_id'] = partners.browse(int(post.get('agent_id'))).id
        #     if post.get('operator_id'):
        #         final_dict['operator_id'] = users.browse(int(post.get('operator_id'))).id
        #     if post.get('incoterm'):
        #         final_dict['incoterm'] = incoterms.browse(int(post.get('incoterm'))).id
        #     if post.get('date'):
        #         final_dict['datetime'] = dt.strptime(post.get('date'), '%Y-%m-%dT%H:%M')
        #     if post.get('new_date'):
        #         final_dict['datetime'] = dt.strptime(post.get('new_date'), '%Y-%m-%dT%H:%M')
        #     if dir == 'air' or not dir:
        #         if post.get('air_source_location_id'):
        #             final_dict['origin_airport_id'] = gateways.browse(int(post.get('air_source_location_id'))).id
        #         if post.get('air_destination_location_id'):
        #             final_dict['destination_airport_id'] = gateways.browse(int(post.get('air_destination_location_id'))).id
            # if dir == 'ocean':
            #     if post.get('ocean_source_location_id'):
            #         final_dict['source_location_id']  = gateways.browse(int(post.get('ocean_source_location_id'))).id
            #     if post.get('ocean_destination_location_id'):
            #         final_dict['destination_location_id'] = gateways.browse(int(post.get('ocean_destination_location_id'))).id
            # if dir == 'land':
            #     if post.get('land_source_location_id'):
            #         final_dict['source_location_id']  = gateways.browse(int(post.get('land_source_location_id'))).id
            #     if post.get('land_destination_location_id'):
            #         final_dict['destination_location_id'] = gateways.browse(int(post.get('land_destination_location_id'))).id
        #
        # final_dict.update({'state':'draft'})
        # booking = operation.sudo().create(final_dict)
        # for file in request.httprequest.files.getlist('file_booking'):
        #     data = file.read()
        #     mimetype = file.content_type
        #     attachment_id = request.env['ir.attachment'].create({
        #         'name':  file.filename,
        #         'mimetype': mimetype,
        #         'type': 'binary',
        #         'datas':base64.b64encode(data),
        #         'res_model': booking._name,
        #         'res_id': booking.id
        #     })
        #     booking.update({
        #         'attachment': [(4, attachment_id.id)],
        #     })
        # del final_dict['state']
        request_obj = request.env['freight.job.request']

        # default_vals = request_obj.sudo().default_get(request_obj._fields.keys())

        default_vals = {'mode_of_transport': 'air',
                'shipper_id': 13,
                'consignee_id': 14,
                'freight_incoterm_id': 1,
                'is_dangerous_goods': True,
                'dangerous_goods_class': 'class_1',
                'package_type_id': 1,
                'commodity_category': 'food_perishable',
                'commodity_description': '2345asdf',
                'freight_hs_code_ids': [[6, False, [1, 2]]],
                'number_of_pallets_packages': 12,
                'gross_weight': 0}




        freight_request = request_obj.sudo().create(post)
        print("freight_requestfreight_requestfreight_request", freight_request)
        return request.render("freight_management.portal_my_request_thank_you")

    @http.route(['/freight_request'], type='http', auth="user", website=True, cache=300)
    def portal_my_bookings(self, **post):
        request_obj = request.env['freight.job.request']
        # make pager
        values = {}
        domain = ['|', ('create_uid', '=', False), ('create_uid', '=', request.env.user.id)]
        freight_request = request_obj.search(domain)
        values.update({
            'freight_requests': freight_request.sudo(),
        })
        return request.render("freight_management.portal_my_request", values)

    @http.route(['/freight_request/details/<model("freight.job.request"):f_request>'], type='http', auth="user", website=True, cache=300)
    def portal_my_booking_detail(self, f_request):
        track_ids = request.env['booking.tracker'].sudo().search([('freight_request_id', '=', f_request.id)], order='id DESC')
        values = {
            'f_request': f_request.sudo(),
            'track_ids': track_ids,
        }

        return request.render("freight_management.portal_my_request_detail", values)

    @http.route(['/post/request/comment'], type='http', auth="user", website=True)
    def post_comment(self, **kw):
        freight_request_id = request.env['freight.job.request'].sudo().browse(int(kw['freight_request_id']))
        vals = {'name': tools.ustr(kw['comment']),
                'user_id': request.env.user.id,
                'date': fields.datetime.now(),
                'freight_request_id': freight_request_id.id}
        request.env['booking.tracker'].sudo().create(vals)
        track_ids = request.env['booking.tracker'].sudo().search([('freight_request_id', '=', freight_request_id.id)], order='id DESC')
        body = 'Note:%s noted by %s' % (tools.ustr(kw['comment']), request.env.user.partner_id.name)
        freight_request_id.sudo().message_post(body=body)
        values = {}
        values.update({
            'booking': freight_request_id.sudo(),
            'track_ids': track_ids,
        })
        return request.render("freight_management.portal_my_request_thank_you", values)
