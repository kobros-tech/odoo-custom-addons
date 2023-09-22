# -*- coding: utf-8 -*-

{
    'name': 'Custom Invoice From Stock Picking',
    'version': '16.0',
    'description': 
    """In this module we solve bugs in the original one
    that we prevent creating more than one invoice/bill for each transfer""",
    'category': 'Stock',
    'website': 'https://royalconsultants.net',
    'license': 'OPL-1',
    'author': 'RoyalConsultants',
    'summary': 'Create a new field',
    'depends': [
        'stock_move_invoice',
        'sale',
        'purchase',
    ],
    'data': [

    ],
}
