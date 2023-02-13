# -*- coding: utf-8 -*-
# Account Reconcile Classes Definition

from odoo import models


class AccountReconcileModelPartnerMapping(models.Model):
     _inherit = 'account.reconcile.model.partner.mapping'

class AccountReconcileModelLine(models.Model):
     _inherit = 'account.reconcile.model.line'

class AccountReconcileModel(models.Model):
     _inherit = 'account.reconcile.model'
     
