# manifest file consists of a dictionary which must include                                                                                           
# two necessary fields (name field, depends field).                                                                                                   
# Test for archiving files into odoo15@probook
{
    'name': "Estate Account",
    'depends': ["estate", "account"],
    'application': "True",
    'license': "LGPL-3",
    'data': [ ],
}
