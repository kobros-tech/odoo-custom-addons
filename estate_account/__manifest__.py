# manifest file consists of a dictionary which must include                                                                                           
# two necessary fields (name field, depends field).                                                                                                   
# Test for archiving files into odoo15@probook
{
    'name': "Estate Account",
    'depends': ["estate", "account_edi", "account"],
    'application': "True",
    'license': "LGPL-3",
    'data': ['security/ir.model.access.csv', 'views/partner_view.xml', 'views/account_account_views.xml', \
        'views/chart_template.xml', 'views/bank_view.xml', 'views/company_view.xml', \
        'views/res_partner_views.xml', 'views/account_journal_views.xml',  \
        'views/menu_tree.xml' ],
}
