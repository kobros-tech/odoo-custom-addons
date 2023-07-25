# -*- coding: utf-8 -*-
{
    'name': 'Maintenance Printout',

    'summary': 'Custom Maintenance Printout',

    'version': '16.0',

    'category': 'Maintenance',

    'website': "https://royalconsultants.net",

    'license': 'OPL-1',

    'author': "RoyalConsultants",

    'sequence': '-16',

    'depends': ['maintenance','maintenance_enhancment'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/printout_wizard_view.xml',
        'reports/paperformat_landscape.xml',
        'reports/maintenance_boiler_report.xml',
        'reports/maintenance_report.xml',
        'reports/maintenance_running_daily_report_1.xml',
        'reports/maintenance_running_daily_report_2.xml',
        'views/res_users.xml',
        'views/maintenance_printouts_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
