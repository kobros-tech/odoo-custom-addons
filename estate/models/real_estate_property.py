# -*- coding: utf-8 -*-
# Defining the Real Estate Property Model

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from . import res_property_type

# from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is my first model!"
    _order = "id desc"

    sequence = fields.Integer("Sequence", default=1)
    name = fields.Char(required=True, string="Title", default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    
    expected_price = fields.Float(required=True, default=0.01)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
        )

    """ Watch up any change in garden value and it's related fields"""
    @api.onchange("garden", "garden_area", "garden_orientation")
    def _onchange_garden(self):
        if self.garden:
            if self.garden_area == 0 or self.garden_orientation == None:
                self.garden_area = 10
                self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
            
    
    """ Set a date variable with a value of today + 3 months """
    date_availability = fields.Date(string="Available From", default=lambda self: fields.Date.today() + relativedelta(months=+3) )

    selling_price = fields.Float(readonly=True, copy=False, default=0.01)
    
    living_area = fields.Integer(string="Living Area (sqm)")
    garage = fields.Boolean()
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    active = fields.Boolean(default=False)

    state = fields.Selection(string="Status",
                             selection=[('new', 'New'), ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default='new'
                             )

    def action_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold!")

            record.state = "sold"
            
        return True

    
    def action_property_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled!")
            
            record.state = "canceled"
            
        return True

    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Partner")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Available Offers")

    
    # Total Area field which is a computed field that will not be stored in the database

    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


            
    # Extract the best offer which is the highest one

    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")
    
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        # Listing all values for offer field and returning the maximum one
        for record in self:
            # Return zero if there is no any offer
            try:
                record.best_price = max(record.mapped("offer_ids.price"))
            except ValueError:
                record.best_price = 0

                
    min_offer = fields.Float(compute="_compute_min_offer")
    
    # Extract the minimum offer which is the lowest one  
    @api.depends("offer_ids.price")
    def _compute_min_offer(self):
        
        # Listing all values for offer field and returning the minimum one      
        for record in self:
            
            # Return None if there is no any offer
            try:
                record.min_offer = max(record.mapped("offer_ids.price"))
            except ValueError:
                record.min_offer = None


    _sql_constraints = [('check_expected_price', 'CHECK (expected_price > 0)', 'The expected price must be strictly positive'),
                        ('check_selling_price', 'CHECK (selling_price > 0)', 'The selling price must be strictly positive'), ]


    
    # Watch out that selling price is not less than 50% off expected price
    # Also we shall keep this condition even after offers be launched
    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            for offer in record.mapped("offer_ids.price"):
                if float_compare(record.expected_price, 2 * offer, precision_rounding=3) == 1:
                    raise ValidationError("The selling price should not be less than half of the expected price" )
                
            # Another further restriction afer offer is accepted
            for rec in record.mapped("offer_ids.status"):
                if rec == "accepted":
                    if float_compare(record.expected_price, 2 * record.selling_price, precision_rounding=3) == 1:
                        raise ValidationError("The selling price should not be less than half of the expected price")


    @api.ondelete(at_uninstall=True)
    def _unlink_if_property_new_canceled(self):
        for record in self:
            if record.state in ["new", "canceled"]:
                continue
            else:
                raise UserError("Only new and canceled properties can be deleted!")


    def apply_offer_details(self, price, partner):
        for record in self:
            record.selling_price = price
            record.partner_id = partner
            record.state = "offer accepted"

            
    
