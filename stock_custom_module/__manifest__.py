# -*- coding: utf-8 -*-

{
    'name': 'Bostana Stock Module',
    'version': '16.0',
    'category': 'Sales/Sales',
    'website': 'https://royalconsultants.net',
    'license': 'OPL-1',
    'author': 'RoyalConsultants',
    'summary': 'Create a new model',
    'depends': [
        'stock',
        'sale',
    ],
    'data': [
        'ir.model.access.csv',
        'attachments_types.xml',
        'stock_picking_views.xml',
        'view_move_form.xml',
    ],
}
