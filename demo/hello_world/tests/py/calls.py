# -*- coding: utf-8 -*-


import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8070
DB = 'shp_api_db'
USER = 'admin'
PASS = 'admin'


def json_rpc(url, method, params):

    # print("method: \n", method)
    # print("params: \n", params)

    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }

    # print("data: \n", data)

    req = urllib.request.Request(
        url=url, 
        data=json.dumps(data).encode(), 
        headers={"Content-Type":"application/json",},)
    
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])

    
    print(reply["result"])

    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

##########################################################
##########################################################


# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)

# query user
domain = ("login", "=", "admin")
note_id = call(url, "object", "execute", DB, uid, PASS, 'res.users', 'search_read', [domain], {'name': "name", 'login': "login"})

