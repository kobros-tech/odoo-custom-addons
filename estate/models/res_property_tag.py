from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name  = "estate.property.tag"
    _description = "The tags that characterizes each property"
    _sql_constraints = [('check_property_tag', 'UNIQUE (name)', 'The property tag name must be unique'), ]
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer(default=4)
