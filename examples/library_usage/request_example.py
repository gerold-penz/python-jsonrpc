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


# Create Request-object
request1 = pyjsonrpc.Request(method = "echo", id = "1234", params = ["foobar"])
print request1
# -> Request(id='1234', jsonrpc='2.0', method='echo', params=['foobar'])
print request1.to_string()
# -> {"params": ["foobar"], "jsonrpc": "2.0", "method": "echo", "id": "1234"}


# Create Request-object, direct from JSON-String
json_str = '{"method": "add", "params": [1, 2], "id": "1234"}'
request2 = pyjsonrpc.Request.from_string(json_str)
print request2
# -> Request(id=u'1234', jsonrpc='2.0', method=u'add', params=[1L, 2L])
print request2.to_string()
# -> {"params": [1, 2], "jsonrpc": "2.0", "method": "add", "id": "1234"}

