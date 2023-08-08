from odoo import api, fields, models, _


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    sample_request_id = fields.Many2one('sample.request', string='Origin')
