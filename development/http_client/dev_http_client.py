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
import logging

logging.basicConfig(level = logging.DEBUG)

rpc_client = pyjsonrpc.HttpClient("http://localhost:8080", gzipped = False, debug = True)

try:
    print rpc_client.format_it({
        "a.b": "A.B",
        "c.d": "C.D",
    })
except pyjsonrpc.JsonRpcError, err:
    print err.code
    print err.message
    print err.data

