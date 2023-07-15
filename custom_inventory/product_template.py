# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "product.template"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Computed
    default_code = fields.Char(compute='_compute_default_new_code')

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.onchange("default_code")
    def _compute_default_new_code(self):

        # Make a list of all internal references
        product_ids = self.env["product.template"].search([])
        items = product_ids.mapped("default_code")

        # Make sure if there are any internal references
        # Then make sure if there are numeric internal references
        num_items = []
        if items:
            if not self.default_code:
                for item in items:
                    is_num_item = str(item).isnumeric()
                    if is_num_item:
                        # Increment the list of only numeric internal reference by a new numeric item
                        num_items.append(item)
                # If there are no numeric internal references add a default one which is a million
                # Else increment the maximum present number by 1
                if not num_items:
                    self.default_code = str("1000000")
                else:
                    new_item = int(max(num_items)) + 1
                    self.default_code = str(new_item)

