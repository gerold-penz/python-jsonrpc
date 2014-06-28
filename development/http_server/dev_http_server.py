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

    print "Function called with these arguments: {a} {b}".format(a = a, b = b)
    return a + b


class MyJsonRpcHandler(pyjsonrpc.HttpRequestHandler):

    methods = {
        "add": add
    }


httpd = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = MyJsonRpcHandler
)
print "Serving HTTP..."
httpd.serve_forever()

