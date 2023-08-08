# -*- coding: utf-8 -*-

import datetime

from odoo import api, fields, models, _


class SampleRequest(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "sample.request"
    _description = "Sample Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char(string='Reference', copy=False, readonly=True)
    READONLYSTATES = {'confirmed': [('readonly', True)]}
    validity_date = fields.Date(string='Expiration', states=READONLYSTATES)
    request_date = fields.Date(states=READONLYSTATES)
    order_date = fields.Date(states=READONLYSTATES)
    reject_reason = fields.Char(string='Reject Reason', readonly=True)
    payment_status = fields.Selection(
        selection=[
            ('paid', 'Paid'), ('unpaid', 'Unpaid')
        ], 
        required=True, 
        states=READONLYSTATES,
        default="unpaid",
    )
    show_invoice = fields.Boolean()
    sample_wh = fields.Selection([('r&d', 'R&D'), ('wh', 'WH')], states=READONLYSTATES)
    
    # Special
    state = fields.Selection(
        [
            ('sales_persons', 'Sales Persons'), 
            ('sales_manger', 'Sales Manger'), 
            ('r&d', 'R&D'),
            ('confirmed', 'Confirmed'), 
            ('rejected', 'Rejected')
        ],
        default='sales_persons', 
        tracking=True,
    )
    
    # Relational
    partner_id = fields.Many2one('res.partner', string='Customer', states=READONLYSTATES)
    wh_source_ids = fields.Many2one('stock.location', states=READONLYSTATES)
    represent_user_id  = fields.Many2one('res.users','Representative', default=lambda self: self.env.user)
    team_id = fields.Many2one('crm.team', string="Team", compute='_compute_team_id', store=True)
    request_line_ids = fields.One2many('sample.request.line', 'sample_request_id', states=READONLYSTATES)

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends('represent_user_id')
    def _compute_team_id(self):
        """ First, team id is chosen, then, user. If user from ticket have a
        team_id, use this user and his team."""
        for request in self:
            if request.represent_user_id:
                team = self.env['crm.team']._get_default_team_id(user_id=request.represent_user_id.id, domain=None)
                request.team_id = team.id
            else:
                request.team_id = False

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.onchange('sample_wh')
    def _onchange_sample_wh(self):
        if self.sample_wh == 'r&d':
            return {'domain': {'wh_source_ids': [('location_type', '=', 'r&d')]}}
        elif self.sample_wh == 'wh':
            return {'domain': {'wh_source_ids': [('location_type', '=', 'wh')]}}

    """
    @api.onchange("payment_status")
    def _onchange_payment_status(self):
        for rec in self:
            if rec.payment_status == "unpaid":
                for price in rec.request_line_ids.mapped("unit_price"):
                    if not price:
                        price = 0.0
    """
    
    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sample.request.sequence') or _('New')
        res = super(SampleRequest, self).create(vals)
        return res

    # ---------------------------------------- Action Methods -------------------------------------

    def action_send_to_sm(self):
        self.state = 'sales_manger'

    def action_sm_approve(self):
        self.state = 'r&d'

    def action_confirm(self):
        if self.payment_status in ['paid']:
            invoice_line_vals = []
            for rec in self.request_line_ids:
                line_vals = (0, 0, {
                    'quantity': rec.quantity,
                    'product_id': rec.product_id.id,
                    'price_unit': rec.unit_price,
                })
                invoice_line_vals.append(line_vals)
            inv_vals = {
                'sample_request_id': self.id,
                'partner_id': self.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_date': datetime.date.today(),
                'invoice_line_ids': invoice_line_vals,
            }
            self.env['account.move'].create(inv_vals)
            self.show_invoice = True

        if self.payment_status in ['paid', 'unpaid']:
            # stock_line_vals = []
            # pick_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
            # pick_location = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
            # pick_dest_location = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
            # for rec in self.request_line_ids:
            #     line_vals = (0, 0, {
            #         'product_id': rec.product_id.id,
            #         'product_uom_id': rec.product_uom.id,
            #         'product_uom_qty': rec.quantity,
            #         'location_id': pick_location.id if pick_location else False,
            #         'location_dest_id': pick_dest_location.id if pick_dest_location else False,
            #     })
            #     stock_line_vals.append(line_vals)
            # stock_vals = {
            #     'sample_request_id': self.id,
            #     'origin': self.name,
            #     'partner_id': self.partner_id.id,
            #     'picking_type_id': pick_type.id if pick_type else False,
            #     'location_id': pick_location.id if pick_location else False,
            #     'location_dest_id': pick_dest_location.id if pick_dest_location else False,
            #     'force_date': datetime.date.today(),
            #     'move_line_ids_without_package': stock_line_vals,
            # }
            pick_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
            print('pssssssssst', pick_type.default_location_dest_id)
            if pick_type:
                picking_type_id = pick_type.id
                location = pick_type.default_location_src_id.id
                location_dest = pick_type.default_location_dest_id.id

                picking = self.env['stock.picking'].create(
                    {'picking_type_id': picking_type_id,
                     'partner_id': self.partner_id.id,
                     'sample_request_id': self.id,
                     'state': 'draft',
                     'origin': self.name,
                     'location_id': self.wh_source_ids.id,
                     'location_dest_id': location_dest,
                     })
                for line in self.request_line_ids:
                    stock_move = self.env['stock.move'].create({
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.product_uom.id,
                        'picking_id': picking.id,
                        'state': 'draft',
                        'location_id': self.wh_source_ids.id,
                        'location_dest_id': location_dest,
                        'picking_type_id': picking_type_id,
                    })

                # picking = self.env['stock.picking'].create(stock_vals)
                # if self.sample_wh == 'r&d':
                #     picking.send_to_qc()
        self.state = 'confirmed'

    def action_open_invoice(self):
        rec_id = self.env['account.move'].search([('sample_request_id', '=', self.id)]).id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'current',
            # 'domain': [('sample_request_id', '=', self.id)],
            'res_id': rec_id
        }

    def action_open_picking(self):
        rec_id = self.env['stock.picking'].search([('sample_request_id', '=', self.id)]).id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Order',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'target': 'current',
            # 'domain': [('sample_request_id', '=', self.id)],
            'res_id': rec_id
        }

    # def action_check_availability(self):
    #     for rec in self:
    #         for line in rec.request_line_ids:
    #             qty_on_hand = line.product_id.qty_available

    # ---------------------------------------- Other Methods -------------------------------------

    def btn_reject(self):
        view_id = self.env.ref('sample_request.view_set_sample_request_rejection_reason_wizard').id
        return {
            'name': _("Rejection Reason"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'sample.request.rejection.reason',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class SampleRequestLine(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "sample.request.line"

    # ---------------------------------------- Default Methods ------------------------------------

    # Basic
    description = fields.Char()
    quantity = fields.Float()
    unit_price = fields.Float()
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal')

    # Relational
    sample_request_id = fields.Many2one('sample.request')
    product_id = fields.Many2one('product.product')
    product_category = fields.Many2one('product.category', related='product_id.categ_id')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom = fields.Many2one('uom.uom', domain="[('category_id', '=', product_uom_category_id)]")
    
    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends('product_id', 'quantity', 'unit_price')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.quantity * rec.unit_price

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.onchange('product_id')
    def _onchange_product_id(self):
        internal_ref = self.product_id.default_code
        self.description = f"[{internal_ref}] {self.product_id.name}" if self.product_id else ''
        self.product_uom = self.product_id.uom_id
        self.unit_price = self.product_id.list_price    

    
