# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    code_of_machine = fields.Char(string='Code of Machine', index=True)

    equipment_function = fields.Char(string='Equipment Function')
    country_of_origin_id = fields.Many2one('res.country', string='Country of Origin', required=True)
    manufacturing_year = fields.Selection(selection='_get_years', string='Manufacturing Year', required=True)
    s_n = fields.Char(string='S.N')
    has_catalog = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Has Catalog')

    company_name = fields.Char(string='Company') 

    @api.model
    def _get_years(self):
        current_year = fields.Date.today().year
        return [(str(year), str(year)) for year in range(current_year, current_year - 100, -1)]
        # return [(str(year), str(year)) for year in reversed(range(current_year - 100, current_year + 1))]
        # selection = []
        # for year in range(current_year - 100, current_year + 1):
        #     selection.append(((str(year)), (str(year))))
        # return selection

    @api.constrains('code_of_machine')
    def _check_unique_code_of_machine(self):
        for rec in self:
            if rec.code_of_machine:
                existing_equipment = self.search([('code_of_machine', '=ilike', rec.code_of_machine)])
                if existing_equipment and existing_equipment != rec:
                    raise ValidationError(_('The code of machine must be unique.'))
