# -*- coding: utf-8 -*-
{
    'name': 'Maintenance Enhancement',

    'summary': 'Maintenance Enhancement Equipment',

    'version': '16.0',

    'category': 'Maintenance',

    'website': "https://royalconsultants.net",

    'license': 'OPL-1',

    'author': "RoyalConsultants",

    'sequence': '-14',

    'depends': ['maintenance', 'stock'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/maintenance_data.xml',
        'wizard/cancel_reason_view.xml',
        'views/maintenance_equipment_views.xml',
        'views/maintenance_stage_view .xml',
        'views/maintenance_request_view.xml',
        'views/stock_location_inherit_view.xml',
        'views/maintenance_team_inherit_view.xml',
        'views/maintenance_equipment_category_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
