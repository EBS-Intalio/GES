# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import logging
from odoo import fields
from odoo.http import request, route
from odoo import http, tools, _

SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)
_logger = logging.getLogger(__name__)


class RequestCustom(http.Controller):

    @http.route(['/createrequest'], type='http', auth='user', website=True, cache=300, csrf=False)
    def portal_my_request_create(self, redirect=None, **post):
        """
        Open Request Create Form and pass required data
        :param redirect:
        :param post:
        :return:
        """
        partners = request.env['res.partner'].sudo().search([])
        consignees = request.env['res.partner'].sudo().search([('consignee', '=', True)])
        shippers = request.env['res.partner'].sudo().search([('shipper', '=', True)])
        users = request.env['res.users'].sudo().search([])
        incoterms = request.env['freight.incoterms'].sudo().search([])
        # move_type = request.env['freight.move.type'].search([])
        gateways = request.env['freight.port'].sudo().search([])
        airlines = request.env['freight.airline'].sudo().search([])
        vessels = request.env['freight.vessel'].sudo().search([])
        truckers = request.env['freight.trucker'].sudo().search([])
        hs_codes = request.env['freight.hs.code'].sudo().search([])
        packages = request.env['freight.package'].sudo().search([])
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        # origins = request.env['freight.por.origin'].sudo().search([])
        pols = request.env['freight.pol'].sudo().search([])
        pods = request.env['freight.pod'].sudo().search([])

        values = {
            'countries':countries,
            'pods':pods,
            'pols':pols,
            'states': states,
            'partners':partners,
            'shipper': shippers,
            'consignees': consignees,
            'users':users,
            'incoterms':incoterms,
            'codes':hs_codes,
            'packages': packages,
            'gateways':gateways,
            'airlines':airlines,
            'vessels':vessels,
            'truckers':truckers,
            'dimensions': 'aaa'
        }
        return request.render("freight_management.portal_request_create", values)

    @http.route(['/submit_request'], type='http', auth='public', website=True, cache=300,  csrf=False)
    def portal_my_request_submit(self, **post):
        """
        Submit Request Detail and based on details create CRM Lead and Freight Request
        :param post:
        :return:
        """
        final_dict = {'is_web_request': True}
        dir = ''
        final_dict['gross_weight'] = 0
        if post:
            dir = post.get('mode_of_transport')
            final_dict['consider_origin_close'] = 'no'
            if post.get('consider_origin_close'):
                final_dict['consider_origin_close'] = post.get('consider_origin_close')
            final_dict['consider_destination_close'] = 'no'
            if post.get('consider_destination_close'):
                final_dict['consider_destination_close'] = post.get('consider_destination_close')
            final_dict['is_dangerous_goods'] = 'no'
            if post.get('is_dangerous_goods'):
                final_dict['is_dangerous_goods'] = post.get('is_dangerous_goods')
            if post.get('mode_of_transport'):
                final_dict['mode_of_transport'] = post.get('mode_of_transport')

            if post.get('shipper_id'):
                final_dict['shipper_id'] = int(post.get('shipper_id'))
            if post.get('shipper_address'):
                final_dict['shipper_addr'] = int(post.get('shipper_address'))

            if post.get('consignee_id'):
                final_dict['consignee_id'] = int(post.get('consignee_id'))
            if post.get('consignee_address'):
                final_dict['consignee_addr'] = int(post.get('consignee_address'))

            if post.get('air_source_location_id'):
                final_dict['origin_airport_id'] = int(post.get('air_source_location_id'))
            if post.get('mawb_no'):
                final_dict['mawb_no'] = post.get('mawb_no')
            if post.get('shipping_line_id'):
                final_dict['shipping_line_id'] = int(post.get('shipping_line_id'))
            if post.get('vessel_id'):
                final_dict['vessel_id'] = int(post.get('vessel_id'))
            if post.get('equipment_type'):
                final_dict['equipment_type'] = post.get('equipment_type')
            if post.get('preferred_airline_id'):
                final_dict['preferred_airline_id'] = int(post.get('preferred_airline_id'))
            if post.get('flight_no'):
                final_dict['flight_no'] = post.get('flight_no')
            if post.get('truck_ref'):
                final_dict['truck_ref'] = post.get('truck_ref')
            if post.get('trucker_number'):
                final_dict['trucker_number'] = post.get('trucker_number')
            if post.get('trucker'):
                final_dict['trucker'] = post.get('trucker')
            if post.get('job_type'):
                final_dict['job_type'] = post.get('job_type')
            if request.env.user:
                final_dict['partner_id'] = request.env.user.partner_id.id
            if post.get('package_type_id'):
                final_dict['package_type_id'] = post.get('package_type_id')
            if post.get('reefer_status'):
                final_dict['reefer_status'] = post.get('reefer_status')
            if post.get('temperature'):
                final_dict['temperature'] = post.get('temperature')
            if post.get('set_temperature_value'):
                final_dict['temperature_value'] = float(post.get('set_temperature_value'))
            if post.get('target_transit_time'):
                final_dict['target_transit_time'] = int(post.get('target_transit_time'))
            if post.get('expected_free_time_at_origin'):
                final_dict['expected_free_time_at_origin'] = int(post.get('expected_free_time_at_origin'))
            if post.get('expected_free_time_at_destination'):
                final_dict['expected_free_time_at_destination'] = int(post.get('expected_free_time_at_destination'))

            if post.get('original_copy'):
                final_dict['original_copy'] = post.get('original_copy')

            bl_copy = False
            if post.get('bl_copy') == 'on':
                bl_copy = True
            final_dict['bl_copy'] = bl_copy
            shipping_documents = False
            if post.get('shipping_documents') == 'on':
                shipping_documents = True
            final_dict['shipping_documents'] = shipping_documents
            if post.get('dimensions_of_package_id'):
                final_dict['dimensions_of_package_id'] = int(post.get('dimensions_of_package_id'))

            if post.get('commodity_category'):
                final_dict['commodity_category'] = post.get('commodity_category')
            if post.get('commodity_description'):
                final_dict['commodity_description'] = post.get('commodity_description')
            if post.get('freight_incoterm_id'):
                final_dict['freight_incoterm_id'] = int(post.get('freight_incoterm_id'))
            if post.get('dangerous_goods_class'):
                final_dict['dangerous_goods_class'] = post.get('dangerous_goods_class')
            if post.get('clearance_required'):
                final_dict['clearance_required'] = post.get('clearance_required')
            if post.get('warehousing'):
                final_dict['warehousing'] = post.get('warehousing')
            if post.get('target_rate'):
                final_dict['target_rate'] = float(post.get('target_rate'))
            final_dict['gross_weight'] = 0
            if post.get('gross_weight'):
                final_dict['gross_weight'] = float(post.get('gross_weight'))
            final_dict['number_of_pallets_packages'] = 0
            if post.get('number_of_pallets_packages'):
                final_dict['number_of_pallets_packages'] = int(post.get('number_of_pallets_packages'))
            if post.get('stackability'):
                final_dict['stackability'] = post.get('stackability')
            if post.get('service_level'):
                final_dict['service_level'] = post.get('service_level')
            if post.get('shipment_ready_date'):
                final_dict['shipment_ready_date'] = post.get('shipment_ready_date')
            if post.get('target_eta'):
                final_dict['target_eta'] = post.get('target_eta')
            if post.get('target_etd'):
                final_dict['target_etd'] = post.get('target_etd')
            final_dict['shipment_ready_asap'] = 'no'
            if post.get('shipment_ready_asap'):
                final_dict['shipment_ready_asap'] = post.get('shipment_ready_asap')
            final_dict['target_eta_asap'] = 'no'
            if post.get('target_eta_asap'):
                final_dict['target_eta_asap'] = post.get('target_eta_asap')
            final_dict['target_etd_asap'] = 'no'
            if post.get('target_etd_asap'):
                final_dict['target_etd_asap'] = post.get('target_etd_asap')
            if post.get('pol_id'):
                final_dict['pol_id'] = int(post.get('pol_id'))
            if post.get('pod_id'):
                final_dict['pod_id'] = int(post.get('pod_id'))
            if post.get('mode_of_transport') == 'ocean':
                final_dict['ocean_shipment'] = post.get('ocean')
            if post.get('mode_of_transport') == 'land':
                final_dict['inland_shipment'] = post.get('land')
            if post.get('mode_of_transport') == 'rail':
                final_dict['rail_shipment_type'] = post.get('rail')
            if post.get('mode_of_transport') == 'sea_then_air':
                final_dict['sea_then_air_shipment'] = post.get('sea_then_air')
            if post.get('mode_of_transport') == 'air_then_sea':
                final_dict['air_then_sea_shipment'] = post.get('air_then_sea')
            final_dict['vehicle_size'] = post.get('vehicle_size')
            final_dict['vehicle_type'] = post.get('vehicle_type')
            if post.get('freight_hs_code_ids'):
                code_vals = []
                for f_val in request.httprequest.form.getlist('freight_hs_code_ids'):
                    code_vals.append(int(f_val))
                final_dict['freight_hs_code_ids'] = [[6, False, code_vals]]
            if post.get('additional_comments'):
                final_dict['additional_comments'] = post.get('additional_comments')
            if post.get('additional_requirement'):
                final_dict['additional_requirements'] = post.get('additional_requirement')
            if post.get('dangerous_goods_notes'):
                final_dict['dangerous_goods_notes'] = post.get('dangerous_goods_notes')
            if dir == 'air' or not dir:
                if post.get('air_source_location_id'):
                    final_dict['origin_airport_id'] = int(post.get('air_source_location_id'))
                if post.get('air_destination_location_id'):
                    final_dict['destination_airport_id'] = int(post.get('air_destination_location_id'))
            if dir == 'ocean':
                if post.get('ocean_source_location_id'):
                    final_dict['origin_airport_id'] = int(post.get('ocean_source_location_id'))
                if post.get('ocean_destination_location_id'):
                    final_dict['destination_airport_id'] = int(post.get('ocean_destination_location_id'))
        request_obj = request.env['freight.job.request']
        freight_request = request_obj.sudo().create(final_dict)

        lead_obj = request.env['crm.lead']
        lead_vals = {
            'name': freight_request.name,
            'type': 'lead'}
        if freight_request.partner_id:
            lead_vals.update({'partner_id': freight_request.partner_id.id})
        lead_id = lead_obj.sudo().create(lead_vals)
        freight_request.lead_id = lead_id.id
        return request.render("freight_management.portal_my_request_thank_you")

    @http.route(['/freight_request'], type='http', auth="user", website=True, cache=300)
    def portal_my_request(self, **post):
        request_obj = request.env['freight.job.request']
        # make pager
        values = {}
        domain = ['|', ('create_uid', '=', False), ('create_uid', '=', request.env.user.id)]
        freight_request = request_obj.sudo().search(domain)
        values.update({
            'freight_requests': freight_request.sudo(),
        })
        return request.render("freight_management.portal_my_request", values)

    @http.route(['/freight_request/details/<model("freight.job.request"):f_request>'], type='http', auth="user", website=True, cache=300)
    def portal_my_request_detail(self, f_request):
        track_ids = request.env['booking.tracker'].sudo().search([('freight_request_id', '=', f_request.id)], order='id DESC')
        values = {
            'f_request': f_request.sudo(),
            'track_ids': track_ids,
        }

        return request.render("freight_management.portal_my_request_detail", values)

    @http.route(['/post/request/comment'], type='http', auth="user", website=True)
    def post_comment(self, **kw):
        """
        Post comments on request
        :param kw:
        :return:
        """
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
