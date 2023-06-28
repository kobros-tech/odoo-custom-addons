# -*- coding: utf-8 -*-                                                                                                                               
# Defining the Real Estate Property Users Model                                                                                                        

from odoo import fields, models


class Users(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.users"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    """ This domain gives the opportunity to mention the evaluated and non-evaluated domains """
    property_ids = fields.One2many(
        "estate.property", "user_id",
        string="Properties",
        domain=[("state", "in", ["new", "offer_received"])]
    )
