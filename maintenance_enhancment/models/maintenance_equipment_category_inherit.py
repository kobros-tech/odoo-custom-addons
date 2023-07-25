from odoo import models, fields

class MaintenanceEquipmentCategoryInherit(models.Model):
    _inherit = 'maintenance.equipment.category'

    printout_type = fields.Selection([
        ('boiler', 'Boiler Printout'),
        ('compressor', 'Compressor Printout'),
        ('panel', 'Panel Printout'),
    ], string='Printout Type', required=True)
