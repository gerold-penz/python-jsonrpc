#!/usr/bin/env python
# coding: utf-8

import sys
import traceback
import uuid
import rpcerror
from bunch import Bunch
from rpcjson import json, JsonParseError


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
        self.jsonrpc = jsonrpc
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
        params = self.get("params", [])
        if isinstance(params, list):
            positional_params = params
        elif isinstance(params, dict):
            positional_params = params.get("__args", [])
            if positional_params:
                del params["__args"]
            named_params = params

        return positional_params, named_params


def parse_request_json(json_string):
    """
    Returns RPC-request as dictionary or as list with requests
    """

    # No JSON-String
    if json_string is None:
        raise rpcerror.InvalidRequest()

    # Parse
    try:
        data = json.loads(json_string)
    except JsonParseError:
        traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        raise rpcerror.ParseError(data = traceback_info)

    # Create request(s)
    if isinstance(data, list):
        requests = []
        for item in data:
            requests.append(Request(
                jsonrpc = item.get("jsonrpc"),
                method = str(item.get("method", "")),
                id = item.get("id"),
                params = item.get("params", [])
            ))
        return requests
    else:
        return Request(
            jsonrpc = data.get("jsonrpc"),
            method = str(data.get("method", "")),
            id = data.get("id"),
            params = data.get("params", [])
        )


def create_request_dict(method, *args, **kwargs):
    """
    Returns a JSON-RPC-Dictionary for a method

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
        "jsonrpc": u"2.0",
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

    return json.dumps(create_request_dict(method, *args, **kwargs))
