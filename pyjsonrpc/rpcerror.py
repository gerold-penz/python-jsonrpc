#!/usr/bin/env python
# coding: utf-8


jsonrpcerrors = {}


class JsonRpcError(RuntimeError):
    code = None
    message = None
    data = None

    def __init__(self, message = None, data = None):
        RuntimeError.__init__(self)
        self.message = message or self.message
        self.data = data

jsonrpcerrors[JsonRpcError.code] = JsonRpcError


class ParseError(JsonRpcError):
    code = -32700
    message = u"Invalid JSON was received by the server."

jsonrpcerrors[ParseError.code] = ParseError


class InvalidRequest(JsonRpcError):
    code = -32600
    message = u"The JSON sent is not a valid Request object."

jsonrpcerrors[InvalidRequest.code] = InvalidRequest


class MethodNotFound(JsonRpcError):
    code = -32601
    message = u"The method does not exist / is not available."

jsonrpcerrors[MethodNotFound.code] = MethodNotFound


class InvalidParams(JsonRpcError):
    code = -32602
    message = u"Invalid method parameter(s)."

jsonrpcerrors[InvalidParams.code] = InvalidParams


class InternalError(JsonRpcError):
    code = -32603
    message = u"Internal JSON-RPC error."

jsonrpcerrors[InternalError.code] = InternalError

