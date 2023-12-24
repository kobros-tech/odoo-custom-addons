{    
    'name':'Logo Printing Portal',
    'version': '1.1',
    'author': 'kobros-tech',
    'website':'https://www.kobros-tech.com',
    'summary': "Custom Website Portal",
    'sequence': 1,
    'description':"Custom Website Portal",
    'category':'Portal',
    'depends': [
        'website_sale', 'mail', 'portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/logo_library_menus.xml',
        'views/logo_library_view.xml',
        'views/portal_template.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend':[            
    #         'wb_portal/static/src/js/new_student_validation.js',
    #     ],  
    # }
}