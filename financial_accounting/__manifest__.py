# manifest file consists of a dictionary which must include                                                                                           
# two necessary fields (name field, depends field).                                                                                                   
# Test for archiving files into odoo15@probook
{
    'name': "Estate Account",
    'depends': ["base", "account"],
    'application': "True",
    'license': "LGPL-3",
    'data': ['security/ir.model.access.csv', 'views/menu_tree.xml'],
}

 # account_edi  

 # 'views/account_account_views.xml', \
 #       'views/chart_template.xml', 'views/account_journal_views.xml', \
 #       'views/account_journal_dashboard_view.xml', 
