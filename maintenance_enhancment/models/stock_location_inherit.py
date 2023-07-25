# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_spare_parts_location = fields.Boolean(string='Is Spare Parts Location?')
