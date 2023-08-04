# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = "abstract.reports"
    _description = "Abstract Reports App for Task Reports"

    # --------------------------------------- Fields Declaration ----------------------------------
    name = fields.Char("Task Report Name")
