# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    
    _inherit = 'stock.picking'
    
    # ---------------------------------------- Additional methods ------------------------------------
    
    def action_create_multi_invoice_for_multi_transfer(self):
        
        for transfer in self:

            # Prevent the method from creating more than single account.move record for each transfer
            journals = transfer.env["account.move"].search([("transfer_ids", "=", transfer.id)])
            if len(journals ) >= 1:
                raise ValidationError(f"There is already invoice/bill {journals.mapped('name')} for {transfer.name} Transfer")

            # Prevent the method from creating any account.move record if there is a sale oreder invoice
            sale_invoice = transfer.sale_id.invoice_ids
            if len(sale_invoice) >= 1:
                raise ValidationError(
                    f"There is already sale order invoice {sale_invoice.mapped('name')} for {transfer.name} transfer")

            # Prevent the method from creating any account.move record if there is a purchase oreder bill
            purchase_bill = transfer.purchase_id.invoice_ids
            if len(purchase_bill) >= 1:
                raise ValidationError(
                    f"There is already purchase order bill {purchase_bill.mapped('name')} for {transfer.name} transfer")

        return super().action_create_multi_invoice_for_multi_transfer()
        

class SaleAdvancePaymentInv(models.TransientModel):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'sale.advance.payment.inv'

    # ---------------------------------------- Additional methods ------------------------------------

    def _create_invoices(self, sale_orders):

        for rec in self:
            for sale_order in rec.sale_order_ids:
                for transfer in sale_order.picking_ids:

                    # Prevent the method from creating more than single account.move record for each transfer
                    journals = transfer.env["account.move"].search([("transfer_ids", "=", transfer.id)])
                    if len(journals ) >= 1:
                        raise ValidationError(
                            f"There is already invoice/bill {journals.mapped('name')} for {transfer.name} Transfer")
        
        return super()._create_invoices(sale_orders)
    

    class PurchaseOrder(models.Model):

        # ---------------------------------------- Private Attributes ---------------------------------

        _inherit = "purchase.order"
        
        # ---------------------------------------- Action methods ------------------------------------

        def action_create_invoice(self):
            
            for transfer in self.picking_ids:
                # Prevent the method from creating more than single account.move record for each transfer
                journals = transfer.env["account.move"].search([("transfer_ids", "=", transfer.id)])
                if len(journals ) >= 1:
                    raise ValidationError(
                        f"There is already invoice/bill {journals.mapped('name')} for {transfer.name} Transfer")
            
            return super().action_create_invoice()
        