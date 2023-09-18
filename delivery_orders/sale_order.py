# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPicking(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    
    _inherit = 'stock.picking'

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    reference = fields.Char("Invoice Reference", required=True)


class AccountAccount(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'account.move'

    # --------------------------------------- Fields Declaration ----------------------------------

    # Computed

    reference = fields.Char(compute="_compute_reference", 
        string="Delivery Reference", store=True)    

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("stock_move_id")
    def _compute_reference(self):
        for rec in self:
            stock_move = self.env["stock.move"].browse(rec.stock_move_id)
            print("****************************************************")
            print(stock_move)
            if stock_move.mapped('id') > []:
                transfer = self.env["stock.picking"].browse(stock_move.picking_id)
                rec.reference = transfer.reference
                print("****************************************************")
                print(transfer)
