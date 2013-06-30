#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDIR)
# END --- required only for testing, remove in real world code --- END


import pyjsonrpc


def add(a, b):
    """Test function"""
    return a + b


# 1. Initialize JSON-RPC class with JSON-RPC method(s)
rpc = pyjsonrpc.JsonRpc(methods = {"add": add})

# 2. Create JSON-RPC string with parameters (= request string)
request_json = pyjsonrpc.create_request_json("add", 1, 2)
# request_json = '{"method": "add", "params": [1, 2], "id": "...", "jsonrpc": "2.0"}'

# 3. Call the JSON-RPC function and get back the JSON-RPC result (= response string)
response_json = rpc.call(request_json)
# response_json = '{"result": 3, "id": "...", "jsonrpc": "2.0"}'

# 4. Convert JSON-RPC string to Python objects
response = pyjsonrpc.parse_response_json(response_json)

# 5. Print result or error
if response.error:
    print "Error:", response.error.code, response.error.message
else:
    print "Result:", response.result

