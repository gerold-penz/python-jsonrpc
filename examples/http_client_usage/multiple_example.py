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

rpc_client = pyjsonrpc.HttpClient(url = "http://localhost:8080")

# Example with *multiple calls* in one request
methods = [
    pyjsonrpc.create_request_dict("addxxxxx", 1, 2),  # ERROR
    pyjsonrpc.create_request_dict("add", 3, 4),
    pyjsonrpc.create_request_dict("add", 5, 6)
]
print rpc_client.call(methods)

# Example with *multiple notifications* (no response) in one request
notifications = [
    pyjsonrpc.create_request_dict("addxxxxx", 1, 2),  # ERROR
    pyjsonrpc.create_request_dict("add", 3, 4),
    pyjsonrpc.create_request_dict("add", 5, 6)
]
rpc_client.notify(notifications)
