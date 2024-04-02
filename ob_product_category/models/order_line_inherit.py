# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    title = fields.Char(string="Title", required=False)

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['title'] = self.title

        return invoice_vals

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            if so.picking_ids:
                for line in so.picking_ids:
                    for lin in line.move_ids_without_package:
                        for rec in so.order_line:
                            if rec.product_id == lin.product_id:
                                lin.ob_categ_id = rec.ob_categ_id.id
                                lin.startDate = rec.startDate
                                lin.endDate = rec.endDate
                                lin.dayes = rec.dayes
        return res

    def write(self, vals):
        # Your logic goes here or call your method
        res = super(SaleOrder, self).write(vals)
        for so in self:
            if so.picking_ids:
                for line in so.picking_ids:
                    for lin in line.move_ids_without_package:
                        for rec in so.order_line:
                            if rec.product_id == lin.product_id:
                                lin.ob_categ_id = rec.ob_categ_id.id
                                lin.startDate = rec.startDate
                                lin.endDate = rec.endDate
                                lin.dayes = rec.dayes
        return res

class saleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ob_categ_id = fields.Many2one('product.category', string='Category', store=True)
    startDate = fields.Date(string="Start Date")
    endDate = fields.Date(string="End Date")
    dayes = fields.Char(string="Duration", readonly=True)


    @api.onchange('startDate', 'endDate')
    def calculate_date(self):
        if self.startDate and self.endDate:
            d1 = datetime.strptime(str(self.startDate), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.endDate), '%Y-%m-%d')
            dayes = abs(d2 - d1)
            self.dayes = str(dayes.days)

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'ob_categ_id': self.ob_categ_id,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'dayes': self.dayes,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'sale_line_ids': [(4, self.id)],

        }
        if self.order_id.analytic_account_id and not self.display_type:
            res['analytic_account_id'] = self.order_id.analytic_account_id.id
        if self.analytic_tag_ids and not self.display_type:
            res['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res

    @api.onchange('ob_categ_id')
    def ob_domain_product_id(self):
        for rec in self:
            if rec.ob_categ_id:
                rec.product_id = False
                rec.name = ''
                if self.ob_categ_id:
                    return {'domain': {'product_id': [('categ_id', '=', self.ob_categ_id.id)],
                                       'product_template_id': [('categ_id', '=', self.ob_categ_id.id)]
                                       }}
                else:
                    return {'domain': {'product_id': []}}


class accountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ob_categ_id = fields.Many2one('product.category', string='Category', store=True)
    startDate = fields.Date(string="Start Date")
    endDate = fields.Date(string="End Date")
    dayes = fields.Char(string="Duration", readonly=True, store=True)
    
    # custom
    move_type = fields.Selection("account.move", related="move_id.move_type")
    # custom


    @api.onchange('ob_categ_id')
    def ob_domain_product_id(self):
        for rec in self:
            if rec.ob_categ_id:
                rec.product_id = False
                rec.name = ''
                if self.ob_categ_id:
                    return {'domain': {'product_id': [('categ_id', '=', self.ob_categ_id.id)]}}
                else:
                    return {'domain': {'product_id': []}}

    @api.onchange('startDate', 'endDate')
    def calculate_date(self):
        if self.startDate and self.endDate:
            d1 = datetime.strptime(str(self.startDate), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.endDate), '%Y-%m-%d')
            dayes = abs(d2 - d1)
            self.dayes = str(dayes.days)

    @api.onchange('startDate')
    def end_date_domain(self):
        if self.endDate:
            self.endDate = ''
        if self.startDate:
            return {'domain': {'endDate': [('endDate', '<=', datetime.today())]}}


class AccountMove(models.Model):
    _inherit = 'account.move'

    title = fields.Char(string="Title", required=False)
    ob_categ_id = fields.Many2one('product.category', string='Category', store=True)


class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    ob_categ_id = fields.Many2one('product.category', string='Category', store=True)
    startDate = fields.Date(string="Start Date")
    endDate = fields.Date(string="End Date")
    dayes = fields.Char(string="Duration", readonly=True)

    @api.onchange('ob_categ_id')
    def domain_product_id(self):
        if self.ob_categ_id:
            self.ob_categ_id = False
            if self.ob_categ_id:
                return {'domain': {'product_id': [('categ_id', '=', self.ob_categ_id.id)]}}
            else:
                return {'domain': {'product_id': []}}




