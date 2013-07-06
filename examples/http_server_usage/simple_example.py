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


class MyJsonRpcHandler(pyjsonrpc.HttpRequestHandler):

    # Public JSON-RPC methods
    methods = dict(
        add = add
    )


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = MyJsonRpcHandler
)
print "Serving HTTP"
print "URL: http://localhost:8080"
http_server.serve_forever()
