# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockMove(models.Model):
    _inherit = 'stock.move'

    force_date = fields.Datetime(string="Force Date", required=True)

    def _action_done(self, cancel_backorder=False):
        force_date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
            account_move_obj = self.env['account.move']
            for move in self:
                if move.picking_id:
                    if move.picking_id.force_date:
                        force_date = move.picking_id.force_date
                    else:
                        force_date = move.picking_id.scheduled_date
                else:
                    force_date = move.force_date

        res = super(StockMove, self)._action_done()
        if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
            if force_date:
                for move in res:
                    move.write({'date': force_date})
                    if move.move_line_ids:
                        for move_line in move.move_line_ids:
                            move_line.write({'date': force_date})
                    if move.stock_valuation_layer_ids:
                        for val_layer in move.stock_valuation_layer_ids:
                            # val_layer.write({'create_date': force_date})
                            update_sql = """
                                        UPDATE stock_valuation_layer 
                                        SET create_date = %s
                                        WHERE id = %s
                                        """
                            self.env.cr.execute(update_sql, (force_date, val_layer.id))

                    if move.account_move_ids:
                        for account_move in move.account_move_ids:
                            account_move.force_date(force_date)
                            # if move.inventory_id:
                            #     account_move.write({'ref': move.inventory_id.name})
                    else:
                        entries = account_move_obj.search([('stock_move_id', '=', move.id)])
                        for entry in entries:
                            entry.date = force_date
        return res
