# -*- coding: utf-8 -*-
{
    'name': 'Custom Force date in Stock Transfer and Inventory Adjustment',
    "author": "Edge Technologies",
    'version': '15',
    'live_test_url': "https://youtu.be/dPuODkkjbDA",
    "images": ['static/description/main_screenshot.png'],
    'summary': "Stock Force Date Inventory force date Inventory Adjustment force date Stock Transfer "
               "force date stock picking force date receipt force date shipment force date delivery force date "
               "in stock backdate stock back date inventory back date receipt back date",
    'description': """ 
    	This Odoo module will helps you to allow stock force date in picking operations and 
    	inventory adjustment. auto pass stock force date in stock move when validate picking 
    	operations and inventory adjustment.
    """,
    "license": "OPL-1",
    'depends': ['stock_force_date_app'],
    'data': [
        'views/stock_picking_view.xml',
    ],
}
