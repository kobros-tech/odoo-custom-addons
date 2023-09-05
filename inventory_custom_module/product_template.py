# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    
    # ---------------------------------------- Private Attributes ---------------------------------
    
    _inherit = "product.template"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    label = fields.Char("Label")
    