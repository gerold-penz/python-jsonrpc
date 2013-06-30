#!/usr/bin/env python
# coding: utf-8

import urllib2
import base64
import rpcrequest
import rpcresponse
import rpcerror
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


    def __getattr__(self, method):
        """
        Allows the usage of attributes as *method* names.
        """

        return self._Method(http_client_instance = self, method = method)


