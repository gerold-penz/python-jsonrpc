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


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    # Register public JSON-RPC methods
    methods = dict(
        add = add
    )


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.shutdown()
print "Stopping HTTP server ..."
