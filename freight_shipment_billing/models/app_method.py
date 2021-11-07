# -*- coding: utf-8 -*"-
from odoo import models, fields, api, _


class AppMethod(models.Model):
    _name = 'app.method'
    _rec_name = 'code'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code", required=True)