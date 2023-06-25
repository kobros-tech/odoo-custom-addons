# manifest file consists of a dictionary which must include 
# two necessary fields (name field, depends field).

{
    'name': "Real Estate",
    'depends': ['base'],
    'application': "True",
    'license': "LGPL-3",
    'data': [
        'security/ir.model.access.csv',

        'views/property_list_view.xml',
        'views/users_view.xml',
        'views/partner_view.xml',
        'views/offers_view.xml',
        'views/tag_view.xml',
        'views/type_view.xml',
    	'views/res_property_views.xml',
    ],
}


