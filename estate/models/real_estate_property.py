# -*- coding: utf-8 -*-
# Defining the Real Estate Property Model

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from . import res_property_type

# from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class RealEstateProperty(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property"
    _description = "This is my first model!"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK (selling_price > 0)', 'The selling price must be strictly positive'), ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char(string="Title", required=True)    # No need for default value
    description = fields.Text()
    postcode = fields.Char()
    expected_price = fields.Float(required=True)  # No need for default value
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    selling_price = fields.Float(readonly=True, copy=False)  # No need for default
    living_area = fields.Integer(string="Living Area (sqm)")
    garage = fields.Boolean()
    """ Set a date variable with a value of today + 3 months """
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False
    )  # months equal only 3

    # Special

    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West'), ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
        default='new'
    )

    # Relational
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)  # need more attributes
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Available Offers")

    # Computed
    """ Extract the best offer which is the highest one """
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")
    """ Total Area field which is a computed field that will not be stored in the database """
    total_area = fields.Float(
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )
    sequence = fields.Integer("Sequence", default=1)  # weired field
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())  # extra not needed field

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):  # A better if statement than an exception
        # Listing all values for offer field and returning the maximum one
        for record in self:
            # Return zero if there is no any offer
            if record.offer_ids:
                record.best_price = max(record.mapped("offer_ids.price"))
            else:
                record.best_price = 0.0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_rounding=0.01)
                and float_compare(record.selling_price, record.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    """ Watch up any change in garden value and it's related fields"""
    @api.onchange("garden", "garden_area", "garden_orientation")
    def _onchange_garden(self):
        if self.garden:
            if not self.garden_area > 0 or self.garden_orientation == None:
                self.garden_area = 10
                self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.ondelete(at_uninstall=False)  # Condition should be false, in rare cases it be true
    def _unlink_if_new_or_canceled(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")

    # ---------------------------------------- Action Methods -------------------------------------

    def action_property_sold(self):     # Need more adjustment, and no need to return a value
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold!")
        else:
            return self.write({"state": "sold"})

    def action_property_canceled(self):     # Need more adjustment, and no need to return a value
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled!")
        else:
            return self.write({"state": "canceled"})

