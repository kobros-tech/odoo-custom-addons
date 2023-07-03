# -*- coding: utf-8 -*-
# Defining New Class of the Real Estate Property Model

from odoo import fields, models, api
    
    
class Property(models.Model):
    _inherit = "estate.property"

    
    def action_property_sold(self):
        
        """Adding small functionality to the action"""

        partner_name = self.partner_id.display_name
        partner_id = self.partner_id.id
        company_name = self.user_id.company_id.display_name
        company_id = self.env['res.company'].browse([self.user_id.id]).id
        
        journal_vals = {'name': "General Journal for X Company",
                        'code': "GJXC",
                        'type': "sale",
                        'invoice_reference_type': "invoice",
                        'invoice_reference_model': "odoo",
                        'company_id': self.user_id.company_id.id,
                        }

        #import pdb; pdb.set_trace() 
        self.env['account.journal'].create(journal_vals)
        #journal_id = self.env['account.journal'].browse([self.partner_id.parent_id.id]).id
        
        
        invoice_vals = {'partner_id': self.partner_id.id,
                        'state': "draft",
                        'move_type': 'out_invoice',
                        'journal_id': 1,
                        'company_id': self.user_id.company_id.id,
                        }
            
            
        self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_vals)
        
        return super().action_property_sold()


class Move(models.Model):
    _inherit = "account.move"


class Journal(models.Model):
    _inherit = "account.journal"
