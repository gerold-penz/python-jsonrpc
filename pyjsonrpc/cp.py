#!/usr/bin/env python
# coding: utf-8
"""
Use JSON-RPC with CherryPy

http://www.cherrypy.org/
http://cherrypy.readthedocs.org/
"""

import httplib
import rpclib
import rpcrequest
import cherrypy
import rpcjson
# ToDo: Replace compress and decompress with faster methods
from cherrypy.lib.encoding import compress, decompress

# for simpler usage
rpcmethod = rpclib.rpcmethod


class CherryPyJsonRpc(rpclib.JsonRpc):
    """
    CherryPy JSON-RPC
    """

    @cherrypy.expose
    @cherrypy.tools.encode(encoding = "utf-8")
    def request_handler(self, *args, **kwargs):
        """
        Json-RPC Handler
        """

        if cherrypy.request.method == "GET":
            # GET

            # jsonrpc
            jsonrpc = kwargs.get("jsonrpc")
            if jsonrpc:
                jsonrpc = jsonrpc[0]

            # id
            id = kwargs.get("id")
            if id:
                id = id[0]

            # method
            method = kwargs.get("method")
            if method:
                method = method[0]
            else:
                # Bad Request
                raise cherrypy.HTTPError(httplib.BAD_REQUEST)

            # params
            _args = []
            _kwargs = {}
            params = kwargs.get("params")
            if params:
                params = rpcjson.loads(params[0])
                if isinstance(params, list):
                    _args = params
                    _kwargs = {}
                elif isinstance(params, dict):
                    _args = []
                    _kwargs = params

            # Create JSON request string
            request_dict = rpcrequest.create_request_dict(method, *_args, **_kwargs)
            request_dict["jsonrpc"] = jsonrpc
            request_dict["id"] = id
            request_json = rpcjson.dumps(request_dict)
        else:
            # POST
            if "gzip" in cherrypy.request.headers.get("Content-Encoding", ""):
                request_json = decompress(cherrypy.request.body.read())
            else:
                request_json = cherrypy.request.body.read()

        # Call method
        result_string = self.call(request_json) or ""

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

