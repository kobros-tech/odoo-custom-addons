# -*- coding: utf-8 -*-
# Account Move Classes Definition

from odoo import models


class AccountMove(models.Model):
     _inherit = 'account.move'

class AccountMoveLine(models.Model):
     _inherit = 'account.move.line'
     
