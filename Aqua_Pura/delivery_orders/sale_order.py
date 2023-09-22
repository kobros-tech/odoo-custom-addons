# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    
    _inherit = 'stock.picking'

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    reference = fields.Char("Invoice Reference", required=True)
    
    # ---------------------------------------- Additional methods ------------------------------------
    
    

class AccountAccount(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'account.move'

    # --------------------------------------- Fields Declaration ----------------------------------

    reference = fields.Char(string="Delivery Reference", 
        compute="_compute_reference",)
    
    # ---------------------------------------- Compute methods ------------------------------------
  
    @api.depends("transfer_ids.reference")
    def _compute_reference(self):
        for rec in self:
            sale_orders = rec.line_ids.sale_line_ids.order_id
            purchase_orders = rec.line_ids.purchase_line_id.order_id

            # According to sale orders
            if len(sale_orders) > 0:
                transfers = sale_orders.picking_ids
                rec.reference = f"{transfers.mapped('reference')}"
            # According to purchase orders
            elif len(purchase_orders) > 0:
                transfers = purchase_orders.picking_ids
                rec.reference = f"{transfers.mapped('reference')}"
            elif len(rec.transfer_ids) > 0:
                transfers = rec.transfer_ids
                rec.reference = f"{transfers.mapped('reference')}"
            else:
                rec.reference = "zero"
            
        