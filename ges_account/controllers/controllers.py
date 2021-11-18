# -*- coding: utf-8 -*-
# from odoo import http


# class GesAccount(http.Controller):
#     @http.route('/ges_account/ges_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ges_account/ges_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ges_account.listing', {
#             'root': '/ges_account/ges_account',
#             'objects': http.request.env['ges_account.ges_account'].search([]),
#         })

#     @http.route('/ges_account/ges_account/objects/<model("ges_account.ges_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ges_account.object', {
#             'object': obj
#         })
