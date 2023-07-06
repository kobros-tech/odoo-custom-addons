# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_partner(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"
    _sql_constraints = [
        ("purchase_reg_no_uq", "UNIQUE (purchase_reg_no)", "Commercial Registration Number must be unique"),
        ("purchase_register_uq", "UNIQUE (purchase_register)", "Commercial Register must be unique"),
        ("vat_uq", "UNIQUE (vat)", "Tax ID must be unique"),
    ]

    # ---------------------------------------- Default Methods ------------------------------------

    @api.model
    def _commercial_fields(self):
        return super(res_partner, self)._commercial_fields()

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    purchase_partner_type = fields.Selection(
        selection=[
            ("vendor", "Vendor"),
            ("customer", "Customer"),
        ],
        required=True,
        default="vendor",
    )
    purchase_reg_no = fields.Char("Commercial Registration No")
    purchase_register = fields.Char("Commercial Register")

    # Special
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
        ],
        string="Status",
        default="draft",
    )
