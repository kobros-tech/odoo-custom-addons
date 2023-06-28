# -*- coding: utf-8 -*-                                                   
# Defining the Real Estate Property Type Model                                 

from odoo import fields, models, api


class RealEstatePropertyType(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property.type"
    _description = "Real Estate Property Type Details"
    _sql_constraints = [('check_property_type', 'UNIQUE (name)', 'The property type name must be unique'), ]
    _order = "sequence, name"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char(required=True, string="Property Type")
    sequence = fields.Integer("Sequence", default=10)

    # Relational
    property_ids = fields.One2many("estate.property", "property_type_id")

    # Computed
    total_offers = fields.Integer(string="Offers Count", compute="_compute_total_offers")
    offer_ids = fields.Many2many("estate.property.offer", string="Offers", compute="_compute_total_offers")  # Not needed

    # ---------------------------------------- Compute methods ------------------------------------

    def _compute_total_offers(self):
        # This solution is quite complex. It is likely that the trainee would have done a search in
        # a loop.
        data = self.env["estate.property.offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)],
            ["ids:array_agg(id)", "property_type_id"],
            ["property_type_id"],
        )
        mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.total_offers = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    # ---------------------------------------- Action Methods -------------------------------------

    def action_view_offers(self):
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res

