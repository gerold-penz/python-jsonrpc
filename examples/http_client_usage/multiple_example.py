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

rpc_client = pyjsonrpc.HttpClient("http://localhost:8080")

# Example with *multiple calls* in one request
print rpc_client.call([
    pyjsonrpc.Request.create("add", 1, 2),
    pyjsonrpc.Request.create("add", 3, 4)
])

# Example with *multiple notifications* (no response) in one request
rpc_client.notify([
    pyjsonrpc.Request.create("add", 1, 2),
    pyjsonrpc.Request.create("add", 3, 4)
])
