# -*- coding: utf-8 -*-
# Part of kobros-tech. See LICENSE file for full copyright and licensing details.

import re
import werkzeug.exceptions
import werkzeug.urls
from odoo.http import request, route, Controller
from odoo import http, tools, _, SUPERUSER_ID, release

class App(http.Controller):


    @http.route([
    "/",
    "/home", 
    ], 
    type='http', 
    auth="public", 
    methods=['GET', 'POST'], 
    csrf=False, 
    website=True, 
    sitemap=True, 
    save_session=False)
    def age(self, **kwargs):

        # /name/mohamed/moustafa/alkobrosli?male=true&age=31
        
        print("==================================")
        print(kwargs)
        print(request)
        print("==================================")

        value = {'name': "Foo", 'title': "kobros-tech", 'x_icon': "hello_world/static/img/favicon.ico"}
        page = "hello_world.home"
        return request.render(page, value)
    
