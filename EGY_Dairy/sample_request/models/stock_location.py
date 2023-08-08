from odoo import api, fields, models, _


class StockLocationInherit(models.Model):
    _inherit = "stock.location"

    location_type = fields.Selection([('r&d', 'R&D'), ('wh', 'WH')], string='Type')
