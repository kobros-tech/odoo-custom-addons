# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    is_new_request = fields.Boolean()
    is_submitted = fields.Boolean()
    is_inprogress = fields.Boolean()
    is_test = fields.Boolean()
    is_cancel = fields.Boolean()
