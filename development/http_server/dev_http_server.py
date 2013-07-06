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
import httplib
import urllib
import urlparse
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer


class ThreadingHttpServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass



class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler, pyjsonrpc.JsonRpc):
    """
    HttpRequestHandler for JSON-RPC-Requests
    """

    protocol_version = "HTTP/1.1"
    methods = None


    def set_content_type_json(self):
        """
        Setzt den Content-Type-Header auf "application/json"
        """

        self.send_header("Content-Type", "application/json")


    def set_content_length(self, length):
        """
        Setzt den Content-Lenght-Header
        """

        self.send_header("Content-Length", str(length))


    def do_GET(self):
        """
        Handles HTTP-GET-Request
        """

        # # self.headers
        # # self.path
        # self.query = urlparse.parse_qs(urllib.splitquery(self.path)[1])



        message = self.call(pyjsonrpc.create_request_json("add", 1, 2))


        self.send_response(code = httplib.OK)
        self.set_content_type_json()
        self.set_content_length(len(message))
        self.end_headers()

        self.wfile.write(message)





def add(a, b):
    """
    Ich bin eine Funktion
    """

    return a + b


class MyJsonRpcHandler(HttpRequestHandler):

    methods = {
        "add": add
    }



httpd = ThreadingHttpServer(('localhost', 9090), MyJsonRpcHandler)
print "Serving HTTP..."

httpd.serve_forever()
