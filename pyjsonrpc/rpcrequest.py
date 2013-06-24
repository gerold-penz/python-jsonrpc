#!/usr/bin/env python
# coding: utf-8

import sys
import errors
import traceback
import uuid
from jsontools import json, ParseError


def parse_request_json(json_string):
    """
    Returns RPC-request as dictionary or as list with dictionaries

    :return: Dictionary or list with RPC-request-dictionaries.
        Syntax::

            {
                "jsonrpc": "<json_rpc_version>",
                "method": "<method_name>",
                "id": "<id>",
                "params": [<param>, ...]|{"<param_name>": <param_value>}
            }
            or
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
    except ParseError:
        traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        raise errors.ParseError(data = traceback_info)

    # Finished
    return data


def create_request_json(method, *args, **kwargs):
    """
    Returns a JSON-RPC-String for a method
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
