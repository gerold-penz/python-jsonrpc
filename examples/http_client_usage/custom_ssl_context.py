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
import ssl

# NOTE/XXX/LOOKATME: This disables SSL cert checking.
# You should only be using this if you know what you are doing.
# Seriously.
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

rpc_client = pyjsonrpc.HttpClient(
    "https://localhost:8080", gzipped = True, ssl_context = context
)

print rpc_client.call("add", 1, 2)

