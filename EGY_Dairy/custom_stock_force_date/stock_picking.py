# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockPicking(models.Model):
    _inherit = ['stock.picking',]

    journal_id = fields.Many2one('account.move', string="Journal Entery")
    move_id = fields.Many2one('account.move.line', string="Journal Item")

    # ------------------------------------------ CRUD Methods -------------------------------------

    def write(self, vals):
        if "force_date" in vals:
            for rec in self:
                super().write(vals)

                journal_enteries = rec.sale_id.invoice_ids
                
                # Update Journal Entery and Journal Items per Transfer
                for journal_entery in journal_enteries:
                    if journal_entery.date != rec.force_date.date():
                        journal_entery.write({"date": rec.force_date.date()})
    
    # ---------------------------------------- Action Methods -------------------------------------

    def action_force(self):
        
        transfers = self.env["stock.picking"].search([("force_date", "!=", None)])
        
        # Updating all Journal Enteries and as a consequence Journal Items
        # for all Transfers that have force_dates
        for transfer in transfers:
            
            journal_enteries = transfer.sale_id.invoice_ids
            
            for journal_entery in journal_enteries:
                if journal_entery.date != transfer.force_date.date():
                    journal_entery.write({"date": rec.force_date.date()})
                    
        return True
    
    