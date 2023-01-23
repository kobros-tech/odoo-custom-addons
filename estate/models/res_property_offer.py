from odoo import fields, models, api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
import datetime

class EstatePropertyOffer(models.Model):
    _name  = "estate.property.offer"
    _description = "The offers related to each property"
    _order = "price desc"
    
    price = fields.Float(default=0.01, string="price")
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity", string="Deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    _sql_constraints = [('check_price', 'CHECK (price > 0)', 'The offer price must be strictly positive'), ]

    
    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.validity:
                create_date = fields.Date.today()
                record.date_deadline = create_date + relativedelta(days=+record.validity)
    
    def _inverse_validity(self):
        for record in self:
            create_date = fields.Date.today()
            date1 = fields.Datetime.to_datetime(create_date)
            date2 = fields.Datetime.to_datetime(record.date_deadline)
            record.validity = (date2 - date1).days


    # It is ultimately important that if a partner accepts an offer no any other partner can accept it again!
    # Also no need to accept sold or canceld offers
    @api.depends("property_id.offer_ids.status", "property_id")        
    def action_offer_accept(self):
        for record in self:
            for rec in record.mapped("property_id.offer_ids.status"):
                if rec == "accepted":
                    return False

            if record.property_id.state == "sold" or record.property_id.state == "canceled":
                return False

            record.status = "accepted"
            record.property_id.apply_offer_details(record.price, record.partner_id)
        return True


    # Watch out that selling price is not less than 50% off expected price
    # No new offers should be less than previous ones
    @api.constrains("price")
    def	_check_selling_price(self):
        for record in self:
            if float_compare(record.property_id.expected_price, 2 * record.price, precision_rounding=0.00001) == 1:
                raise ValidationError("The selling price should not be less than half of the expected price #offer")

            if record.property_id.min_offer:
                if float_compare( record.property_id.min_offer, record.price, precision_rounding=0.00001) == 1:
                    raise UserError("Offers that are less than other ones are not allowed!")
    

    # Check if the partner has previously accepted the offer otherwise refuse, no need to check records in other views!
    def action_offer_refuse(self):
        if self.status == "accepted":
            return False
        self.status = "refused"
        return True



    
    # Once an offer is accepted apply these updates to estate property model       
    @api.model
    def create(self, vals_list):

        
        self.env['estate.property'].browse([vals_list['property_id']]).write({'state': "offer received"})
        return super(EstatePropertyOffer, self).create(vals_list)


    
