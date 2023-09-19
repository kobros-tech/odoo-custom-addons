# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPicking(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    
    _inherit = 'stock.picking'

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    reference = fields.Char("Invoice Reference", required=True)
    
    # ---------------------------------------- Additional methods ------------------------------------
    
    def write(self, vals):
        for rec in self:
            for invoice in rec.sale_id.invoice_ids:
                if "reference" in vals:
                    super().write(vals)
                    invoice.write({"reference": rec.reference})
                    
        return True


class AccountAccount(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'account.move'

    # --------------------------------------- Fields Declaration ----------------------------------

    reference = fields.Char(string="Delivery Reference", readonly=True)

    # ---------------------------------------- Additional methods ------------------------------------
  
    def write(self, vals):
        if "reference" in vals:
            source_orders = self.line_ids.sale_line_ids.order_id
            for picking in source_orders.picking_ids:
                if picking.reference != self.reference:
                    vals["reference"] = picking.reference
        
        super().write(vals)    
        return True
