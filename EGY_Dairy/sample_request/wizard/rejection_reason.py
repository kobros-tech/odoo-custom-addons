from odoo import api, fields, models, _


class PurchaseOrderInherit(models.TransientModel):
    _name = 'sample.request.rejection.reason'

    reject_reason = fields.Char(string='Reject Reason', required=True)

    def action_set_reject_reason(self):
        active_ids = self.env['sample.request'].browse(self.env.context.get('active_ids', False))
        active_ids.reject_reason = self.reject_reason
        active_ids.state = 'rejected'
