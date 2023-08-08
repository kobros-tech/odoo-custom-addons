from odoo import api, fields, models, _


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    sample_request_id = fields.Many2one('sample.request', string='Origin')
