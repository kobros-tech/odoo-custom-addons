# -*- coding: utf-8 -*-

{
    'name': 'Extra Custom Invoice From Stock Picking',
    'version': '16.0',
    'description': 
    """In this module we add a reference in Transfers and their invoices""",
    'category': 'Stock',
    'website': 'https://royalconsultants.net',
    'license': 'OPL-1',
    'author': 'RoyalConsultants',
    'summary': 'Create a new field',
    'depends': [
        'custom_stock_move_invoice',
        'sale',
        'purchase',
    ],
    'data': [
        'stock_picking_views.xml',
        'view_move_form.xml',
    ],
}
