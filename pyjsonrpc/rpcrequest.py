#!/usr/bin/env python
# coding: utf-8

import sys
import traceback
import uuid
import rpcerror
import rpcjson
try:
    from munch import Munch as Bunch
except ImportError as err:
    from bunch import Bunch


class Request(Bunch):
    """
    JSON-RPC-Request
    """

    def __init__(
        self,
        jsonrpc = None,
        method = None,
        id = None,
        params = None
    ):
        Bunch.__init__(self)

        self.jsonrpc = jsonrpc or "2.0"
        self.method = method
        self.id = id
        self.params = params


    def get_splitted_params(self):
        """
        Split positional and named params

        :returns: positional_params, named_params
        """

        positional_params = []
        named_params = {}
        params = self.params or []
        if isinstance(params, list):
            positional_params = params
        elif isinstance(params, dict):
            positional_params = params.get("__args", [])
            if positional_params:
                del params["__args"]
            named_params = params

        return positional_params, named_params


    @classmethod
    def from_string(cls, json_string):
        """
        Parses the Json-string and returns a Request-object or a
        list with Request-objects.

        :returns: Request-object or list with Request-objects

        :rtype: Request
        """

        # No JSON-String
        if not json_string:
            raise rpcerror.InvalidRequest()

        # Parse
        try:
            data = rpcjson.loads(json_string)
        except rpcjson.JsonParseError:
            traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
            raise rpcerror.ParseError(data = traceback_info)

        # Create request(s)
        if isinstance(data, list):
            requests = []
            for item in data:
                requests.append(cls(
                    jsonrpc = item.get("jsonrpc"),
                    method = item.get("method"),
                    id = item.get("id"),
                    params = item.get("params")
                ))
            return requests
        else:
            return cls(
                jsonrpc = data.get("jsonrpc"),
                method = data.get("method"),
                id = data.get("id"),
                params = data.get("params")
            )


    # Alias
    loads = from_string


    def to_string(self):
        """
        Returns a Json-string
        """

        positional_params, named_params = self.get_splitted_params()

        # Create dictionary
        if named_params:
            params = named_params
            if positional_params:
                params["__args"] = positional_params
        else:
            params = positional_params
        data = {
            "method": self.method,
            "id": self.id,
            "jsonrpc": self.jsonrpc or "2.0",
            "params": params
        }

        # Return Json
        return rpcjson.dumps(data)


    # Alias
    dumps = to_string


    def to_dict(self):
        """
        Returns the request as dictionary
        """

        return self.toDict()


    @classmethod
    def from_dict(cls, data):
        """
        Returns a request-object, created from Dictionary.

        :rtype: Request
        """

        return cls(
            jsonrpc = data.get("jsonrpc"),
            method = data.get("method"),
            id = data.get("id"),
            params = data.get("params")
        )


    @classmethod
    def create(cls, method, *args, **kwargs):
        """
        Returns a request-object with unique id.

        :param method: Name of the method
        :param args: Positional parameters
        :param kwargs: Named parameters
        """

        return Request.from_dict(create_request_dict(method, *args, **kwargs))


# Alias for *Request.loads*
parse_request_json = Request.from_string


# Alias for *Request.create*
create_request = Request.create


def create_request_dict(method, *args, **kwargs):
    """
    Returns a JSON-RPC-dictionary for a method

    :param method: Name of the method
    :param args: Positional parameters
    :param kwargs: Named parameters
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
    return data


def create_request_json(method, *args, **kwargs):
    """
    Returns a JSON-RPC-String for a method

    :param method: Name of the method
    :param args: Positional parameters
    :param kwargs: Named parameters
    """

    return rpcjson.dumps(create_request_dict(method, *args, **kwargs))

# Alias
create_request_string = create_request_json


