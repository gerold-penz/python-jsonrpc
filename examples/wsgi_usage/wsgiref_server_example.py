#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDIR)
# END --- required only for testing, remove in real world code --- END


import cherrypy
from wsgiref.simple_server import make_server
from pyjsonrpc.cp import CherryPyJsonRpc, rpcmethod


class Root(CherryPyJsonRpc):

    @rpcmethod
    def add(self, a, b):
        """Test method"""
        return a + b

    index = CherryPyJsonRpc.request_handler

# WSGI-Application
application = cherrypy.Application(Root())


# WsgiRef-WSGIServer
httpd = make_server('', 8080, application)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
httpd.serve_forever()



