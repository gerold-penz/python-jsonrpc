#!/usr/bin/env python
# coding: utf-8
"""
Nosetests for *rpcerror.py*.
"""

import pyjsonrpc.rpcerror
from nose.tools import raises


@raises(AssertionError)
def test_json_rpc_error_without_code():
    pyjsonrpc.rpcerror.JsonRpcError()


@raises(pyjsonrpc.rpcerror.JsonRpcError)
def test_json_rpc_error_raise():
    raise pyjsonrpc.rpcerror.JsonRpcError(code = 12345)


@raises(pyjsonrpc.rpcerror.ParseError)
def test_parse_error_raise():
    error = pyjsonrpc.rpcerror.ParseError()
    assert error.code == -32700
    raise error


@raises(pyjsonrpc.rpcerror.InvalidRequest)
def test_invalid_request_raise():
    error = pyjsonrpc.rpcerror.InvalidRequest()
    assert error.code == -32600
    raise error


@raises(pyjsonrpc.rpcerror.MethodNotFound)
def test_method_not_found_raise():
    error = pyjsonrpc.rpcerror.MethodNotFound()
    assert error.code == -32601
    raise error


@raises(pyjsonrpc.rpcerror.InvalidParams)
def test_invalid_params_raise():
    error = pyjsonrpc.rpcerror.InvalidParams()
    assert error.code == -32602
    raise error


@raises(pyjsonrpc.rpcerror.InternalError)
def test_internal_error_raise():
    error = pyjsonrpc.rpcerror.InternalError()
    assert error.code == -32603
    raise error
