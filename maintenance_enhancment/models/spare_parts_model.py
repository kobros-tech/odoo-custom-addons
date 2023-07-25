# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SparePart(models.Model):
    _name = 'spare.part'
    _description = 'Spare Part Model'

    maintenance_request_id = fields.Many2one('maintenance.request', string='Maintenance Request')
    spare_part_id = fields.Many2one('product.product', string='Spare Part', required=True)
    # , domain='[('','','')]'
    # planned_quantity = fields.Float(string='Planned Quantity', required=True)
    used_quantity = fields.Float(string='Quantity')    
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="UOM",
        compute='_compute_product_uom',
        store=True, readonly=False, precompute=True, ondelete='restrict',
        domain="[('category_id', '=', product_uom_category_id)]")
    
    product_uom_category_id = fields.Many2one(related='spare_part_id.uom_id.category_id', depends=['spare_part_id'])

    available_qty = fields.Selection([('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], compute='_compute_available_qty')


    @api.depends('spare_part_id')
    def _compute_product_uom(self):
        for line in self:
            if not line.uom_id or (line.spare_part_id.uom_id.id != line.uom_id.id):
                line.uom_id = line.spare_part_id.uom_id

    @api.depends('spare_part_id')
    def _compute_available_qty(self):
        for rec in self:
            location_ids = self.env['stock.location'].search([('is_spare_parts_location', '=', True)])
            free_qty_location = rec.spare_part_id.with_context({'location': location_ids.ids}).free_qty
            if rec.spare_part_id:
                if free_qty_location > 0:
                    rec.available_qty = 'in_stock'
                else:
                    rec.available_qty = 'out_of_stock'
            else:
                rec.available_qty = False
