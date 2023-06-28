from odoo import fields, models, api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property.offer"
    _description = "The offers related to each property"
    _order = "price desc"
    _sql_constraints = [('check_price', 'CHECK (price > 0)', 'The offer price must be strictly positive'), ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    price = fields.Float(string="price", required=True)      # Need to be required, default value not needed
    validity = fields.Integer(string="Validity (days)", default=7)  # String attribute is better at first

    # Special
    state = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'), ('refused', 'Refused'),
        ],
        copy=False,
        default=False
    )     # Need adjustment

    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id",
        string="Property Type", store=True
    )  # Need the firstly related attribute

    # Computed
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")

    # ---------------------------------------- Compute methods ------------------------------------
    
    @api.depends("validity", "create_date")     # Change create_date variable adjust days argument
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                date = record.create_date.date()
            else:
                date = fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)
    
    def _inverse_deadline(self):        # Datetime conversion is not needed
        for record in self:
            if record.create_date:
                date = record.create_date.date()
            else:
                date = fields.Date.today()
            record.validity = (record.date_deadline - date).days

    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer_received"
        return super().create(vals)

    # ---------------------------------------- Action Methods -------------------------------------

    """ It is ultimately important that if a partner accepts an offer no any other partner can accept it again! """
    def action_offer_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer has already been accepted.")
        self.write({"state": "accepted"})
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_offer_refuse(self):
        return self.write({"state": "refused", })
