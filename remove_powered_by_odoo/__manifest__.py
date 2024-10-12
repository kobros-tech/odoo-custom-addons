# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#############################################################################
#
#    kobros-tech Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY kobros-tech(<https://www.linkedin.com/company/kobros-tech/>).
#    Author: Mohamed Alkobrosli(<https://www.linkedin.com/in/mohamed-alkobrosly/>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': "Custom module for Amd Megastore that removes Powered by Odoo label",
    'description': """
        Custom module for Amd Megastore that removes Powered by Odoo label.
    """,
    'author': 'Abou Sajid (Mohamed Alkobrosli)',
    'company': 'kobros-tech',
    'maintainer': 'Mohamed Moustafa Alkobrosli',
    'website': "https://www.kobros-tech.com",
    'license': "AGPL-3",
    'depends': [
        'web',
        'mail',
        'portal',
        'point_of_sale', 
    ],
    'data': [
        'views/webclient_templates.xml',
        'views/pos_assets_index.xml',
        'views/discuss_public_templates.xml',
        'views/portal_templates.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'remove_powered_by_odoo/static/src/app/navbar/navbar.xml',
            'remove_powered_by_odoo/static/src/app/screens/receipt_screen/receipt/order_receipt.xml',
            # 'remove_powered_by_odoo/static/src/app/customer_display/customer_display_template.xml',
        ],
        'web.assets_backend': [
            'remove_powered_by_odoo/static/src/remove_odoo_title.js',
        ],
    },
}
