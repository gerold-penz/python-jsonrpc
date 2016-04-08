#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
import datetime
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDIR)
# END --- required only for testing, remove in real world code --- END


import pyjsonrpc
import pyjsonrpc.rpcjson


# Activate encoder and decoder for DateTime-ISO strings and NDB keys
pyjsonrpc.rpcjson.activate_iso_date_and_ndb_conversion()


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add_one_hour(self, timestamp):
        """
        Adds one hour to the timestamp
        """

        return timestamp + datetime.timedelta(hours = 1)


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
