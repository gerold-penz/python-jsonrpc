#!/usr/bin/env python
# coding: utf-8

import sys
import traceback
import uuid
try:
    import jsonlib2 as json
    _ParseError = json.ReadError
except ImportError:
    import json
    _ParseError = ValueError
import errors


def parse_json_request(json_string):
    """
    Returns list with RPC-requests as dictionaries.

    :return: List with RPC-request-dictionaries.
        Syntax::

            [
                {
                    "jsonrpc": "<json_rpc_version>",
                    "method": "<method_name>",
                    "id": "<id>",
                    "params": [<param>, ...]|{"<param_name>": <param_value>}
                },
                ...
            ]
    """

    # No JSON-String
    if json_string is None:
        raise errors.InvalidRequest()

    # Parse
    try:
        data = json.loads(json_string)
    except _ParseError:
        traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        raise errors.ParseError(data = traceback_info)

    # Finished
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return [data]
    else:
        raise errors.InvalidRequest()


def create_json_request(method, *args, **kwargs):
    """
    Returns a JSON-RPC-String for one method
    """

    if kwargs:
        params = kwargs
        if args:
            params["__args"] = args
    else:
        params = args
    data = {
        "method": unicode(method),
        "id": unicode(uuid.uuid4()),
        "jsonrpc": "2.0",
        "params": params
    }
    return json.dumps(data)


def parse_json_response(json_string):
    """
    Returns RPC-Response(s) as dictionary or as list with dictionaries
    """

    return json.loads(json_string)


class Response(object):
    """
    Represents a successful response.
    """

    def __init__(self, jsonrpc = None, id = None, result = None):
        """
        :param jsonrpc: JSON-RPC version string
        :param id: JSON-RPC transaction id
        :param result: Result data
        """

        self.jsonrpc = jsonrpc
        self.id = id
        self.result = result


    def to_dict(self):
        """
        Returns the response object as dictionary.
        """

        retdict = {}
        if self.jsonrpc:
            retdict["jsonrpc"] = self.jsonrpc
        if not self.id is None:
            retdict["id"] = self.id
        if not self.result is None:
            retdict["result"] = self.result

        return retdict


class JsonRpc(object):
    """
    JSON-RPC
    """

    def __init__(self, methods = None):
        """
        Initializes the JSON-RPC-Class

        :param methods: Json-RPC-Methods. `None` or dictionary with
            method names as keys and functions as values. Syntax::

                {
                    "<method_name>": <method_function>,
                    ...
                }
        """

        self.methods = methods or {}
        self.methods["system.describe"] = self.system_describe


    def call(self, json_request):
        """
        Do the work

        :param json_request: JSON-RPC-string with one or more JSON-RPC-requests

        :return: JSON-RPC-string with one or more responses.
        """

        # List for the responses
        responses = []

        # List with requests
        requests = parse_json_request(json_request)

        # Every JSON-RPC request in a batch of requests
        for request in requests:

            # Request-Data
            jsonrpc = request.get("jsonrpc")
            method = str(request.get("method", ""))
            id = request.get("id")

            # split positional and named params
            positional_params = []
            named_params = {}
            params = request.get("params", [])
            if isinstance(params, list):
                positional_params = params
            elif isinstance(params, dict):
                positional_params = params.get("__args", [])
                if positional_params:
                    del params["__args"]
                named_params = params

            if not method in self.methods:
                # Method not found
                responses.append(
                    errors.MethodNotFound(jsonrpc = jsonrpc, id = id)
                )
                continue

            # Call the method with parameters
            try:
                rpc_function = self.methods[method]
                result = rpc_function(*positional_params, **named_params)
                # No return value is OK if we don´t have an ID (=notification)
                if result is None:
                    if id:
                        responses.append(
                            errors.InternalError(
                                jsonrpc = jsonrpc,
                                id = id,
                                data = u"No result from JSON-RPC method."
                            )
                        )
                else:
                    # Successful response
                    responses.append(
                        Response(jsonrpc = jsonrpc, id = id, result = result)
                    )
            except TypeError, err:
                traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
                if "takes exactly" in unicode(err) and "arguments" in unicode(err):
                    responses.append(
                        errors.InvalidParams(
                            jsonrpc = jsonrpc,
                            id = id,
                            data = traceback_info
                        )
                    )
                else:
                    responses.append(
                        errors.InternalError(
                            jsonrpc = jsonrpc,
                            id = id,
                            data = traceback_info
                        )
                    )
            except BaseException, err:
                traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
                if hasattr(err, "data"):
                    error_data = err.data
                else:
                    error_data = None
                responses.append(
                    errors.InternalError(
                        jsonrpc = jsonrpc,
                        id = id,
                        data = error_data or traceback_info
                    )
                )

        # Convert responses and errors to dictionaries
        responses_ = []
        for response in responses:
            responses_.append(response.to_dict())
        responses = responses_

        # Return as JSON-string (batch or normal)
        if len(requests) == 1:
            return json.dumps(responses[0])
        elif len(requests) > 1:
            return json.dumps(responses)
        else:
            return None


    def __call__(self, json_request):
        """
        Redirects the requests to *self.call*
        """

        return self.call(json_request)


    def __getitem__(self, key):
        """
        Gets back the method
        """

        return self.methods[key]


    def __setitem__(self, key, value):
        """
        Appends or replaces a method
        """

        self.methods[key] = value


    def __delitem__(self, key):
        """
        Deletes a method
        """

        del self.methods[key]


    def system_describe(self):
        """
        Returns a system description

        See: http://web.archive.org/web/20100718181845/http://json-rpc.org/wd/JSON-RPC-1-1-WD-20060807.html#ServiceDescription
        """

        return u"[not finished]"
