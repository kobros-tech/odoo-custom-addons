# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
 
    request_date = fields.Datetime(string='Request Date', readonly=True)
    repair_start = fields.Datetime(string=' Repair Start')
    repair_end = fields.Datetime(string=' Repair End')
    description_repairs = fields.Text(string='Description Of Done Repairs')
    spare_parts_ids = fields.One2many('spare.part', 'maintenance_request_id', 'Spare Parts')

    is_an_issue = fields.Boolean('Is there an issue')
    
    is_new_request = fields.Boolean(related='stage_id.is_new_request')
    is_submitted = fields.Boolean(related='stage_id.is_submitted')
    is_inprogress = fields.Boolean(related='stage_id.is_inprogress')
    is_test = fields.Boolean(related='stage_id.is_test')
    is_cancelled = fields.Boolean(related='stage_id.is_cancel')


    maintenance_worker_description = fields.Text()
    require_spare_parts = fields.Selection([('yes', 'yes'), ('no', 'no')])
    
    def action_submit(self):
        for rec in self:
            stage = self.env.ref('maintenance_enhancment.stage_0_1')
            rec.stage_id = stage

    def action_start_repair(self):
        for rec in self:
            stage = self.env.ref('maintenance.stage_1')
            if rec.require_spare_parts == 'no':
                rec.stage_id = stage
            elif rec.require_spare_parts == 'yes':
                if len(rec.spare_parts_ids) == 0:
                    raise UserError('Spare parts are required!')
                elif len(rec.spare_parts_ids.filtered(lambda x: x.available_qty == 'in_stock')) == len(rec.spare_parts_ids):
                    rec.stage_id = stage
                else:
                    requisition_blanket = self.env['purchase.request'].create({
                        'line_ids': [(0,0, {
                            'product_id': line.spare_part_id.id,
                            'product_uom_id': line.uom_id.id,
                            'product_qty': line.used_quantity,
                        }) for line in rec.spare_parts_ids.filtered(lambda x: x.available_qty == 'out_of_stock')],

                        'origin': rec.name,
                        # 'vendor_id': vendor2.id,
                        # 'currency_id': self.env.ref("base.USD").id,
                    })
                    rec.message_post(body=_("Purchase Request: <a href=# data-oe-model=purchase.request data-oe-id=%d>%s</a> has been created.") % (
                    requisition_blanket.id, requisition_blanket.name))
                    rec.stage_id = stage
            
            rec.repair_start = fields.Datetime.now()


    def action_end_repair(self):
        for rec in self:
            stage = self.env.ref('maintenance_enhancment.stage_1_1')
            rec.stage_id = stage
            rec.repair_end = fields.Datetime.now()

            duration = rec.repair_end - rec.repair_start
            rec.duration = (duration.total_seconds() /60)/60

    def action_done(self):
        for rec in self:
            stage = self.env.ref('maintenance.stage_3')
            rec.stage_id = stage
    
    def action_back_to_repair(self):
        for rec in self:
            stage = self.env.ref('maintenance.stage_1')
            rec.stage_id = stage


    def action_cancel(self):
        view_id = self.env.ref('maintenance_enhancment.view_cancel_reason_form').id
        return {
            'name': 'Cancel Reason',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cancel.reason',
            'views': [(view_id, 'form')],
            'type': 'ir.actions.act_window',
            'context': {'line_id': self.id},
            'target': 'new',
        }
