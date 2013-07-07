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


# Handles the JSON-RPC request and gets back the result to STDOUT
pyjsonrpc.handle_cgi_request(methods = dict(add = add))

