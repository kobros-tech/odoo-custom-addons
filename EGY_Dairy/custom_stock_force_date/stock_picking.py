# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockPicking(models.Model):
    _inherit = ['stock.picking',]

    journal_id = fields.Many2one('account.move', string="Journal Entery")
    move_id = fields.Many2one('account.move.line', string="Journal Item")
    
    @api.onchange("force_date")
    def _onchange_force_date(self):
        for rec in self:
            stock_move = self.env["stock.move"].search([('picking_id', '=', rec.id)])
            
            if stock_move.mapped('id') > []:
                account_moves = self.env["account.move"].search([('stock_move_id', '=', stock_move.id)])
            
                if account_moves.mapped('id') > []:
                    for account_move in account_moves:
                        if rec.force_date and rec.force_date != account_move.date:
                            new_date = rec.force_date.date().strftime("%Y-%m-%d")
                            account_move.write({"date": datetime.strptime(new_date, "%Y-%m-%d")})
            
                    move_lines = self.env["account.move.line"].search([('move_id', '=', account_move.id)])
                    
                    if move_lines.mapped('id') > []:
                        for move_line in move_lines:
                            if rec.force_date and rec.force_date != move_line.date:
                                new_date = rec.force_date.date().strftime("%Y-%m-%d")
                                move_line.write({"date": datetime.strptime(new_date, "%Y-%m-%d")})
                                