# -*- coding: utf-8 -*-
{
    "name": "Sample Request",
    "version": "1.0",
    "category": "Sales",
    "author": "Tarek Galal <tgalal@zadsolutions.com>",
    "website": "http://zadsolutions.com",
    "summary": """ Sample Request  """,
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        'wizard/rejection_reason.xml',
        "views/sample_request.xml",
        "views/account_move.xml",
        "views/stock_picking.xml",
        "views/stock_location.xml",
        "data/data.xml",
    ],
    "images": [],
    "installable": True,
    "auto_install": False,
    "application": False,
}
