#!/usr/bin/env python
# coding: utf-8

import urllib2
import base64
import BaseHTTPServer
import SocketServer
import httplib
import urllib
import urlparse
import rpcrequest
import rpcresponse
import rpcerror
import rpclib
from rpcjson import json


def http_request(url, json_string, username = None, password = None):
    """
    Fetch data from webserver (POST request)

    :param json_string: JSON-String
    :param username: If *username* is given, BASE authentication will be used.
    """

    request = urllib2.Request(url, data = json_string)
    request.add_header("Content-Type", "application/json")
    if username:
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)

    response = urllib2.urlopen(request)
    response_string = response.read()
    response.close()

    return response_string


class HttpClient(object):


    class _Method(object):

        def __init__(self, http_client_instance, method):
            self.http_client_instance = http_client_instance
            self.method = method

        def __call__(self, *args, **kwargs):
            return self.http_client_instance.call(self.method, *args, **kwargs)


    def __init__(
        self,
        url,
        username = None,
        password = None
    ):
        """
        :param: URL to the JSON-RPC handler on the HTTP-Server.
            Example: ``"https://example.com/jsonrpc"``

        :param username: If *username* is given, BASE authentication will be used.
        :param password: Password for BASE authentication.
        """

        self.url = url
        self.username = username
        self.password = password


    def call(self, method, *args, **kwargs):
        """
        Creates the JSON-RPC request string, calls the HTTP server, converts
        JSON-RPC response string to python and returns the result.

        :param method: Name of the method which will be called on the HTTP server.
            Or a list with RPC-Request-Dictionaries. Syntax::

                "<MethodName>" or [<JsonRpcRequestDict>, ...]

            RPC-Request-Dictionaries will be made with the function
            *rpcrequest.create_request_dict()*.
        """

        # Create JSON-RPC-request
        if isinstance(method, basestring):
            request_json = rpcrequest.create_request_json(method, *args, **kwargs)
        else:
            request_json = json.dumps(method)
            assert not args and not kwargs

        # Call the HTTP-JSON-RPC server
        response_json = http_request(
            url = self.url,
            json_string = request_json,
            username = self.username,
            password = self.password
        )

        # Convert JSON-RPC-response to python-object
        response = rpcresponse.parse_response_json(response_json)

        if response.error:
            # Raise error
            raise rpcerror.jsonrpcerrors[response.error.code](
                message = response.error.message,
                data = response.error.data
            )
        else:
            # Return result
            return response.result


    def __call__(self, method, *args, **kwargs):
        """
        Redirects the direct call to *self.call*
        """

        return self.call(method, *args, **kwargs)


    def __getattr__(self, method):
        """
        Allows the usage of attributes as *method* names.
        """

        return self._Method(http_client_instance = self, method = method)


class ThreadingHttpServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """
    Threading HTTP Server
    """
    pass


class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler, rpclib.JsonRpc):
    """
    HttpRequestHandler for JSON-RPC-Requests

    Info: http://www.simple-is-better.org/json-rpc/transport_http.html
    """

    protocol_version = "HTTP/1.1"
    #server_version = "BaseHTTP/" + __version__


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

        # Parse URL query
        query = urlparse.parse_qs(urllib.splitquery(self.path)[1])

        # jsonrpc
        jsonrpc = query.get("jsonrpc")
        if jsonrpc:
            jsonrpc = jsonrpc[0]

        # id
        id = query.get("id")
        if id:
            id = id[0]

        # method
        method = query.get("method")
        if method:
            method = method[0]

        # params
        args = []
        kwargs = {}
        params = query.get("params")
        if params:
            params = json.loads(params[0])
            if isinstance(params, list):
                args = params
                kwargs = {}
            elif isinstance(params, dict):
                args = []
                kwargs = params

        # Create JSON reqeust string
        request_dict = rpcrequest.create_request_dict(method, *args, **kwargs)
        request_dict["jsonrpc"] = jsonrpc
        request_dict["id"] = id
        request_json = json.dumps(request_dict)

        # Call
        response_json = self.call(request_json)

        # Return result
        self.send_response(code = httplib.OK)
        self.set_content_type_json()
        self.set_content_length(len(response_json))
        self.end_headers()
        self.wfile.write(response_json)

