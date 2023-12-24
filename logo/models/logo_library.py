# -*- coding: utf-8 -*-

from odoo import fields, models

class LogoLibrary(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "library"
    _description = "Library of submitted logos for all webiste sales quotations"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char("Name")

    image = fields.Image()

    order_ids = fields.Many2many("sale.order.line", string="Sales Quotation")

    product_ids = fields.Many2many("product.product", string="Related Products")

    product_description = fields.Html()

