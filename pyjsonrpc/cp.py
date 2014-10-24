#!/usr/bin/env python
# coding: utf-8
"""
Use JSON-RPC with CherryPy

http://www.cherrypy.org/
http://cherrypy.readthedocs.org/
"""

import rpclib
import cherrypy
from cherrypy.lib.encoding import compress, decompress

# for simpler usage
rpcmethod = rpclib.rpcmethod


class CherryPyJsonRpc(rpclib.JsonRpc):
    """
    CherryPy JSON-RPC
    """

    @cherrypy.expose
    def request_handler(self, *args, **kwargs):
        """
        Json-RPC Handler
        """


        # ToDo: Distinguish between GET and POST



        if "gzip" in cherrypy.request.headers.get("Content-Encoding", ""):
            request_json = decompress(cherrypy.request.body.read())
        else:
            request_json = cherrypy.request.body.read()

        # Call method
        result_string = self.call(request_json)

        # Return JSON-String
        cherrypy.response.headers["Cache-Control"] = "no-cache"
        cherrypy.response.headers["Pragma"] = "no-cache"
        cherrypy.response.headers["Content-Type"] = "application/json"
        if "gzip" in cherrypy.request.headers.get("Accept-Encoding", ""):
            # Gzip-compressed
            cherrypy.response.headers["Content-Encoding"] = "gzip"
            return compress(result_string, compress_level = 5)
        else:
            # uncompressed
            return result_string

