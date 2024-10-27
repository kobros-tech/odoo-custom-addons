# -*- coding: utf-8 -*-
# Part of kobros-tech. See LICENSE file for full copyright and licensing details.

import re
import werkzeug.exceptions
import werkzeug.urls
from odoo import http, _
from odoo.http import request, route, Controller
from odoo import http, tools, _, SUPERUSER_ID, release
from odoo.addons.web_editor.controllers.main import Web_Editor

class Main(http.Controller):


    @http.route("/hello-world", type='http', auth="public", methods=['GET', 'POST'], csrf=False, website=True, sitemap=True, save_session=False)
    def hello(self, **kwargs):
        
        print("==================================")
        print(kwargs)
        print(request)
        print("==================================")
        
        return request.make_response("Hello world!")
    

    @http.route("/empty", type='http', auth="public", methods=['GET', 'POST'], csrf=False, website=True, sitemap=True, save_session=False)
    def empty(self, **kwargs):
        
        print("==================================")
        print(kwargs)
        print(request)
        print("==================================")
        
        page = "hello_world.hello"
        return request.render(page)
    

    @http.route("/name/<name>", type='http', auth="public", methods=['GET', 'POST'], csrf=False, website=True, sitemap=True, save_session=False)
    def name(self, name, **kwargs):
        
        print("==================================")
        print("1")
        print(name)
        print(kwargs)
        print(request)
        print("==================================")
        
        page = "hello_world.hello"
        return request.render(page)
    

    @http.route([
    "/name/<name>/<nicknames>", 
    ], 
    type='http', 
    auth="public", 
    methods=['GET', 'POST'], 
    csrf=False, 
    website=True, 
    sitemap=True, 
    save_session=False)
    def nickname(self, name, nicknames=None, **kwargs):
        
        print("==================================")
        print("2")
        print(name)
        print(nicknames)
        print(kwargs)
        print(request)
        print("==================================")
        
        page = "hello_world.hello"
        return request.render(page)
    

    @http.route([
    "/name/<name>",
    "/name/<name>/<middle>/<nicknames>", 
    ], 
    type='http', 
    auth="public", 
    methods=['GET', 'POST'], 
    csrf=False, 
    website=True, 
    sitemap=True, 
    save_session=False)
    def middle(self, name, **kwargs):
        
        print("==================================")
        print("3")
        print(name)
        print(kwargs)
        print(request)
        print("==================================")
        
        page = "hello_world.hello"
        return request.render(page)
    
    
    @http.route([
    "/name/<name>/<middle>/<nicknames>", 
    ], 
    type='http', 
    auth="public", 
    methods=['GET', 'POST'], 
    csrf=False, 
    website=True, 
    sitemap=True, 
    save_session=False)
    def age(self, name, age=None, **kwargs):

        # /name/mohamed/moustafa/alkobrosli?male=true&age=31
        
        print("==================================")
        print("4")
        print(name)
        print(age, type(age))
        
        if age:
            age = int(age)
            print(age, type(age))
        
        print(kwargs)
        print(request)
        print("==================================")

        value = {'name': name}
        page = "hello_world.hello"
        return request.render(page, value)
    
    
