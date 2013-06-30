#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDIR)
# END --- required only for testing, remove in real world code --- END


import pyjsonrpc


def add(a, b):

    # raise RuntimeError("Test Exception")
    return a + b


def positional_params_example():

    # Initialize JSON-RPC-Class with JSON-RPC-Methods
    rpc = pyjsonrpc.JsonRpc(methods = {"add": add})

    # Create JSON-RPC-string with positional params
    request_json = pyjsonrpc.create_request_json("add", 1, 2)
    # '{"params": [1, 2], "jsonrpc": "2.0", "method": "add", "id": "..."}'
    print "Request-JSON:", repr(request_json)

    # RPC-Call
    response_json = rpc.call(request_json)
    # '{"jsonrpc": "2.0", "id": "...", "result": 3}'
    print "Response-JSON:", repr(response_json)

    # Result
    response = pyjsonrpc.parse_response_json(response_json)
    if response.error:
        print "Error:", response.error.code, response.error.message
    else:
        # 3
        print "Result:", response.result


def named_params_example():

    # Initialize JSON-RPC-Class with JSON-RPC-Methods
    rpc = pyjsonrpc.JsonRpc(methods = {"add": add})

    # Create JSON-RPC-string with named params
    request_json = pyjsonrpc.create_request_json("add", a = 1, b = 2)
    # '{"params": {"a": 1, "b": 2}, "jsonrpc": "2.0", "method": "add", "id": "..."}'
    print "Request-JSON:", repr(request_json)

    # RPC-Call
    response_json = rpc.call(request_json)
    # '{"jsonrpc": "2.0", "id": "...", "result": 3}'
    print "Response-JSON:", repr(response_json)

    # Result
    response = pyjsonrpc.parse_response_json(response_json)
    if response.error:
        print "Error:", response.error.code, response.error.message
    else:
        # 3
        print "Result:", response.result


def mixed_params_example():

    # Initialize JSON-RPC-Class with JSON-RPC-Methods
    rpc = pyjsonrpc.JsonRpc(methods = {"add": add})

    # Create JSON-RPC-string with mixed params
    request_json = pyjsonrpc.create_request_json("add", 1, b = 2)
    # '{"params": {"b": 2, "__args": [1]}, "jsonrpc": "2.0", "method": "add", "id": "..."}'
    print "Request-JSON:", repr(request_json)

    # RPC-Call
    response_json = rpc.call(request_json)
    # '{"jsonrpc": "2.0", "id": "...", "result": 3}'
    print "Response-JSON:", repr(response_json)

    # Result
    response = pyjsonrpc.parse_response_json(response_json)
    if response.error:
        print "Error:", response.error.code, response.error.message
    else:
        # 3
        print "Result:", response.result


def main():

    print "-" * 30
    positional_params_example()

    print "-" * 30
    named_params_example()

    print "-" * 30
    mixed_params_example()


if __name__ == "__main__":
    main()

