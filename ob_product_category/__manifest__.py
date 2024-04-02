# -*- coding: utf-8 -*-
{
    'name': "Product Category",
    'sequence': -100,
    'summary': """
        This Is A Custom Product Category
        Made By Omar Al-Bayoumi 
    """,

    'description': "",

    'author': "Omar Al-Bayoumi",
    'website': "#",

    'category': '',
    'version': '15.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'stock', 'account', 'purchase', 'sale', 'sale_management', 'purchase_requisition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_views.xml',
        'views/category_to_report.xml',
        # 'views/res_config_settings_views.xml',
        # 'view/account_asset_depreciation.xml',
    ],
    'application': True,
}
