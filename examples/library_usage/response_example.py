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


# Create Response-object
response1 = pyjsonrpc.Response(jsonrpc = "2.0", id = "1234", result = "Hello")
print response1
# -> Response(error=None, id='1234', jsonrpc='2.0', result='Hello')
print response1.to_string()
# -> {"jsonrpc": "2.0", "id": "1234", "result": "Hello"}


# Create Response-object, direct from JSON-String
json_str = '{"jsonrpc": "2.0", "result": "Hello", "id": "1234"}'
response2 = pyjsonrpc.Response.from_string(json_str)
print response2
# -> Response(error=None, id=u'1234', jsonrpc=u'2.0', result=u'Hello')
print response2.to_string()
# -> {"jsonrpc": "2.0", "id": "1234", "result": "Hello"}
