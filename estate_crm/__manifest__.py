# manifest file consists of a dictionary which must include                                                                                           
# two necessary fields (name field, depends field).  

{
    'name': "Estate CRM",
    'depends': ["crm"],
    'application': "True",
    'license': "LGPL-3",
    'data': ['security/ir.model.access.csv', 'views/crm_menu_views.xml'],
}

