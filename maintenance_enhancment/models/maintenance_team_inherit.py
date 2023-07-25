# -*- coding: utf-8 -*-

from odoo import fields, models


class MaintenanceTeam(models.Model):
    _inherit = 'maintenance.team'

    specialized_equipment_category_ids = fields.Many2many('maintenance.equipment.category', string='Specialized Equipment Category')
