#!/usr/bin/env python
# coding: utf-8

import logging
import rpcrequest
import rpcresponse
import rpcerror
import rpcjson
from tools import safe_unicode


def rpcmethod(func):
    """
    Decorator
    Sign the decorated method as JSON-RPC-Method
    """

    # Sign the function as JSON-RPC-Method
    func.rpcmethod = True

    # Return the function itself
    return func


class JsonRpc(object):
    """
    JSON-RPC
    """

    methods = {}


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

        if methods:
            self.methods.update(methods)


    def call(self, json_request):
        """
        Parses the *json_request*, calls the function(s)
        and returns the *json_response*.

        :param json_request: JSON-RPC-string with one or more JSON-RPC-requests

        :return: JSON-RPC-string with one or more responses.
        """

        # List for the responses
        responses = []

        # List with requests
        requests = rpcrequest.parse_request_json(json_request)
        if not isinstance(requests, list):
            requests = [requests]

        # Every JSON-RPC request in a batch of requests
        for request in requests:

            # Request-Data
            jsonrpc = request.jsonrpc
            id = request.id
            method = request.get("method", "")

            if method not in self.methods:
                # Check if requested method is signed as *rpcmethod*
                _method = getattr(self, method, None)
                if (
                    _method and
                    callable(_method) and
                    getattr(_method, "rpcmethod", False)
                ):
                    self.methods[method] = _method

            if method not in self.methods:
                # Method not found error
                error = rpcerror.MethodNotFound(
                    data = u"Method name: '%s'" % method
                )
                responses.append(
                    rpcresponse.Response(
                        jsonrpc = jsonrpc,
                        id = id,
                        error = error
                    )
                )
                # Logging error
                logging.error(
                    u"{error} -- {data}".format(
                        error = safe_unicode(error),
                        data = safe_unicode(error.data)
                    )
                )

                continue

            # split positional and named params
            positional_params, named_params = request.get_splitted_params()

            # Call the method with parameters
            try:
                rpc_function = self.methods[method]
                result = rpc_function(*positional_params, **named_params)
                responses.append(
                    rpcresponse.Response(jsonrpc = jsonrpc, id = id, result = result)
                )
            except TypeError as err:
                traceback_info = rpcerror.get_traceback_string()
                if "takes exactly" in safe_unicode(err) and "arguments" in safe_unicode(err):
                    error = rpcerror.InvalidParams(data = traceback_info)
                    responses.append(
                        rpcresponse.Response(
                            jsonrpc = jsonrpc,
                            id = id,
                            error = error
                        )
                    )
                    # Logging error
                    logging.error(
                        u"{error} -- {data}".format(
                            error = safe_unicode(error),
                            data = safe_unicode(error.data)
                        )
                    )
                else:
                    error = rpcerror.InternalError(data = traceback_info)
                    responses.append(
                        rpcresponse.Response(
                            jsonrpc = jsonrpc,
                            id = id,
                            error = error
                        )
                    )
                    # Logging error
                    logging.error(
                        u"{error} -- {data}".format(
                            error = safe_unicode(error),
                            data = safe_unicode(error.data)
                        )
                    )
            except rpcerror.JsonRpcError as err:
                responses.append(
                    rpcresponse.Response(
                        jsonrpc = jsonrpc,
                        id = id,
                        error = err
                    )
                )
                # Logging error
                logging.error(
                    u"{error} -- {data}".format(
                        error = safe_unicode(err),
                        data = safe_unicode(err.data)
                    )
                )
            except Exception as err:
                traceback_info = rpcerror.get_traceback_string()
                if hasattr(err, "data"):
                    error_data = err.data
                else:
                    error_data = None
                error = rpcerror.InternalError(
                    message = safe_unicode(err),
                    data = safe_unicode(error_data or traceback_info)
                )
                responses.append(
                    rpcresponse.Response(
                        jsonrpc = jsonrpc,
                        id = id,
                        error = error
                    )
                )
                # Logging error
                logging.error(
                    u"{error} -- {data}".format(
                        error = safe_unicode(error),
                        data = safe_unicode(error.data)
                    )
                )

        # Convert responses to dictionaries and filter it
        responses_ = []
        for response in responses:
            if (
                bool(response.id) or
                bool(unicode(response.id)) if response.id is not None else False
            ):
                responses_.append(response.to_dict())
        responses = responses_

        # Return as JSON-string (batch or normal)
        if responses:
            if len(requests) == 1:
                return rpcjson.dumps(responses[0])
            elif len(requests) > 1:
                return rpcjson.dumps(responses)


    def __call__(self, json_request):
        """
        Redirects the requests to *self.call*
        """

        return self.call(json_request)


    def __getitem__(self, key):
        """
        Gets back the requested method
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

