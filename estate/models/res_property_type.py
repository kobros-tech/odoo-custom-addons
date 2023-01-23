# -*- coding: utf-8 -*-                                                   
# Defining the Real Estate Property Type Model                                 

from odoo import fields, models, api


class RealEstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type Details"
    _sql_constraints = [('check_property_type', 'UNIQUE (name)', 'The property type name must be unique'), ]
    _order = "name"
    
    name = fields.Char(required=True, string="Property Type", default="Unknown")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    total_offers = fields.Integer(compute="_compute_total_offers")


    @api.depends("offer_ids")
    def _compute_total_offers(self):
        # self.total_offers = len(self.mapped("offer_ids.price"))

        for record in self:
            record.total_offers = len(record.offer_ids)
