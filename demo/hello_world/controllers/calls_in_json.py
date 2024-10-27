# -*- coding: utf-8 -*-
# Part of kobros-tech. See LICENSE file for full copyright and licensing details.

import json

import re
import werkzeug.exceptions
import werkzeug.urls
from odoo.http import request, route, Controller
from odoo import http, tools, _, SUPERUSER_ID, release

import requests


class JSONCalls(http.Controller):

    """
        If type=json, most critical methods that are POST methods and usually return critical data if they are accepting JSON connection. 
        The returned data could be a dictionary, list or even a value, and this data is converted in the decorator into a value in the JSON response called "result".
        Such as:
        { jsonrpc: '2.0', id: 1, result: 2 }
        or
        { jsonrpc: '2.0', id: 1, result: [{...}] }
        or 
        { jsonrpc: '2.0', id: 1, result: {...} }

        This happens only when type=json.
        This is applied for "POST" request only!

        ==============================================================================
        ==============================================================================
        
        If type=http, the returned data should be in complete JSON format including headers/body. 
        Then you can read the returned data in the JSON request.
        This is applied for "GET" and "POST" requests
    """

    
    @route(["/json_call_post"], type="json", methods=['POST'], auth="public", cors="*", csrf=False)
    def json_calls_post(self):

        data = {'key': 1, 'value': True}
        json_data = request.get_json_data()

        if json_data['params']['index']:
            data['key'] = json_data['params']['index']

            print("===================================")
            print(request.httprequest.method)
            print(json_data)
            print(json_data['params']['index'])
            print(data)
            print("===================================")
        
        return data


    @route("/json_call_get", type="http", methods=['GET'], auth="public", cors="*", csrf=False)
    def json_calls_get(self):
        
        print("===================================")
        print("get method")
        print("===================================")

        data = {'key': 1, 'value': True}
        data = json.dumps(data)
        response = request.make_response(data=data, headers=[('Content-Type', 'application/json')], status=200)
        return response

    
    @route(["/json_call", "/json_call/<index>"], type="http", methods=['POST', 'GET'], auth="public", cors="*", csrf=False)
    def json_calls(self, index=None):

        data = {'key': 1, 'value': True}

        if request.httprequest.method == "POST":
            json_data = request.get_json_data()

            if json_data['params']['index']:
                data['key'] = json_data['params']['index']

                print("===================================")
                print(request.httprequest.method)
                print(json_data)
                print(index)
                print(json_data['params']['index'])
                print(data)
                print("===================================")
        
        data = json.dumps(data)
        response = request.make_response(data=data, headers=[('Content-Type', 'application/json')], status=200)
        
        print("response", response)
        
        return response