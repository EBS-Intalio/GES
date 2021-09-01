# -*- coding: utf-8 -*-
# from odoo import http


# class EbsMasHr(http.Controller):
#     @http.route('/ebs_mas_hr/ebs_mas_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ebs_mas_hr/ebs_mas_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ebs_mas_hr.listing', {
#             'root': '/ebs_mas_hr/ebs_mas_hr',
#             'objects': http.request.env['ebs_mas_hr.ebs_mas_hr'].search([]),
#         })

#     @http.route('/ebs_mas_hr/ebs_mas_hr/objects/<model("ebs_mas_hr.ebs_mas_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ebs_mas_hr.object', {
#             'object': obj
#         })
