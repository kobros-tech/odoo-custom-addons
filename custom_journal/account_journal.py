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

    @api.onchange("cash_in")
    def _onchange_cash_in(self):
        if self.cash_in:
            self.cash_out = False

    @api.onchange("cash_out")
    def _onchange_cash_out(self):
        if self.cash_out:
            self.cash_in = False
