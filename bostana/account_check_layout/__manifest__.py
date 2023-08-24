# -*- coding: utf-8 -*-
{
    'name': 'Account Check Layout',

    'summary': 'Custom Account Check Layout',

    'version': '16.0',

    'category': 'Account',

    'website': "https://royalconsultants.net",

    'license': 'OPL-1',

    'author': "RoyalConsultants",

    'sequence': '-16',

    'depends': ['account', ], # 'account_check'

    'data': [
        'reports/check_layout.xml',
        'views/res_users.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
