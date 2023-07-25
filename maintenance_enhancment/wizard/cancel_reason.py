from odoo import models, fields, api


class CancelReason(models.TransientModel):
    _name = 'cancel.reason'

    reason = fields.Text(string='Reason', required=True)

    def done(self):
        active_id = self.env.context.get('line_id')
        maintenance_request = self.env['maintenance.request'].browse(active_id)
        cancel_stage = self.env.ref('maintenance_enhancment.stage_5')

        maintenance_request.write({'stage_id': cancel_stage.id})
        maintenance_request.message_post(body="""Cancel Reason: %s """ % (self.reason))
        return {'type': 'ir.actions.act_window_close'}

    def discard(self):
        return {'type': 'ir.actions.act_window_close'}
