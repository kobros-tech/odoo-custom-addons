# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AttachmentsTypes(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "attachments.types"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char("Attachment Name")

    # Relational
    picking_id = fields.Many2one('stock.picking')

    move_id = fields.Many2one('account.move')


class StockPicking(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'stock.picking'

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    attachments_types_ids = fields.One2many('attachments.types', 'picking_id')

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("attachments_types_ids", "state")
    def _check_attachments_types(self):
        for rec in self:
            if rec.state == "done" and rec.mapped("attachments_types_ids.name") == []:
                raise ValidationError(
                    "The attachment name is required when the state is done!"
                )


class AccountAccount(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'account.move'

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    attachments_types_ids = fields.One2many('attachments.types', 'move_id')
