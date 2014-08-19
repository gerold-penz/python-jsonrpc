#!/usr/bin/env python
# coding: utf-8

import sys
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


def http_request(url, json_string, username = None, password = None, timeout = None):
    """
    Fetch data from webserver (POST request)

    :param json_string: JSON-String

    :param username: If *username* is given, BASE authentication will be used.

    :param timeout: Specifies a timeout in seconds for blocking operations
        like the connection attempt (if not specified, the global default
        timeout setting will be used).
        See: https://github.com/gerold-penz/python-jsonrpc/pull/6
    """

    request = urllib2.Request(url, data = json_string)
    request.add_header("Content-Type", "application/json")
    if username:
        base64string = base64.encodestring("%s:%s" % (username, password))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)

    response = urllib2.urlopen(request, timeout = timeout)
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
        password = None,
        timeout = None
    ):
        """
        :param: URL to the JSON-RPC handler on the HTTP-Server.
            Example: ``"https://example.com/jsonrpc"``

        :param username: If *username* is given, BASE authentication will be used.

        :param password: Password for BASE authentication.

        :param timeout: Specifies a timeout in seconds for blocking operations
            like the connection attempt (if not specified, the global default
            timeout setting will be used).
        """

        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout


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
            assert not args and not kwargs
            request_json = json.dumps(method)

        # Call the HTTP-JSON-RPC server
        response_json = http_request(
            url = self.url,
            json_string = request_json,
            username = self.username,
            password = self.password,
            timeout = self.timeout
        )
        if not response_json:
            return

        # Convert JSON-RPC-response to python-object
        response = rpcresponse.parse_response_json(response_json)
        if isinstance(response, rpcresponse.Response):
            if response.error:
                # Raise error
                raise rpcerror.jsonrpcerrors[response.error.code](
                    message = response.error.message,
                    data = response.error.data
                )
            else:
                # Return result
                return response.result
        elif isinstance(response, list):
            # Bei Listen wird keine Fehlerauswerung gemacht
            return response


    def notify(self, method, *args, **kwargs):
        """
        Sends a notification or multiple notifications to the server.

        A notification is a special request which does not have a response.
        """

        methods = []

        # Create JSON-RPC-request
        if isinstance(method, basestring):
            request_dict = rpcrequest.create_request_dict(method, *args, **kwargs)
            request_dict["id"] = None
            methods.append(request_dict)
        else:
            assert not args and not kwargs
            for request_dict in method:
                request_dict["id"] = None
                methods.append(request_dict)

        # Redirect to call-method
        self.call(methods)

        # Fertig
        return


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


    def set_content_type_json(self):
        """
        Set content-type to "application/json"
        """

        self.send_header("Content-Type", "application/json")


    def set_no_cache(self):
        """
        Disable caching
        """

        self.send_header("Cache-Control", "no-cache")
        self.send_header("Pragma", "no-cache")


    def set_content_length(self, length):
        """
        Set content-length-header
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
        response_json = self.call(request_json) or ""

        # Return result
        self.send_response(code = httplib.OK)
        self.set_content_type_json()
        self.set_no_cache()
        self.set_content_length(len(response_json))
        self.end_headers()
        self.wfile.write(response_json)


    def do_POST(self):
        """
        Handles HTTP-POST-Request
        """

        # Read JSON request
        content_length = int(self.headers.get("Content-Length", 0))
        request_json = self.rfile.read(content_length)

        # Call
        response_json = self.call(request_json) or ""

        # Return result
        self.send_response(code = httplib.OK)
        self.set_content_type_json()
        self.set_no_cache()
        self.set_content_length(len(response_json))
        self.end_headers()
        self.wfile.write(response_json)
        return


def handle_cgi_request(methods = None):
    """
    Gets the JSON-RPC request from CGI environment and returns the
    result to STDOUT
    """

    import cgi
    import cgitb
    cgitb.enable()

    # get response-body
    request_json = sys.stdin.read()
    if request_json:
        # POST
        request_json = urlparse.unquote(request_json)
    else:
        # GET
        args = []
        kwargs = {}
        fields = cgi.FieldStorage()
        jsonrpc = fields.getfirst("jsonrpc")
        id = fields.getfirst("id")
        method = fields.getfirst("method")
        params = fields.getfirst("params")
        if params:
            params = json.loads(params)
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
    response_json = rpclib.JsonRpc(methods = methods).call(request_json)

    # Return headers
    print "Content-Type: application/json"
    print "Cache-Control: no-cache"
    print "Pragma: no-cache"
    print

    # Return result
    print response_json

