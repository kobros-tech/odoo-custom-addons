# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    is_engineering_manager = fields.Boolean()
   