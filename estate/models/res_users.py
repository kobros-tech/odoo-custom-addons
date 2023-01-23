# -*- coding: utf-8 -*-                                                                                                                               
# Defining the Real Estate Property Users Model                                                                                                        

from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "user_id", domain=[("active", "=", True)])
