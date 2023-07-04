# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountJournal(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "account.journal"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    cash_in = fields.Boolean("Cash in")
    cash_out = fields.Boolean("Cash out")

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.onchange("cash_in", "type")
    def _onchange_cash_in(self):
        if "cash" in self.mapped("type"):
            if self.cash_in == True:
                self.cash_out = False
        else:
            self.cash_in = False

    @api.onchange("cash_out", "type")
    def _onchange_cash_out(self):
        if "cash" in self.mapped("type"):
            if self.cash_out == True:
                self.cash_in = False
        else:
            self.cash_out = False
