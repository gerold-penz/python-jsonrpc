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

# Example with *call*
print rpc_client.call("add", 1, 2)

# Example with direct *call*
print rpc_client("add", 3, 4)

# Example with *attribute* name
print rpc_client.add(5, 6)

# Example with *notify* (no response)
rpc_client.notify("add", 7, 8)
