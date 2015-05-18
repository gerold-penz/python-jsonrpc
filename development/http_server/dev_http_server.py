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
import pyjsonrpc.rpcjson
import collections

# JSON-dumps settings
pyjsonrpc.rpcjson.loads_object_pairs_hook = collections.OrderedDict


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def format_it(self, keys_and_values):

        retstr = u""
        for key, value in keys_and_values.items():
            retstr += u"{key}: {value}\n".format(key = key, value = value)
        return retstr


httpd = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = RequestHandler
)
print "Serving HTTP..."
httpd.serve_forever()

