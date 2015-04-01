#!/usr/bin/env python
# coding: utf-8


jsonrpcerrors = {}


class JsonRpcError(RuntimeError):
    code = None
    message = None
    data = None

    def __init__(self, message = None, data = None, code = None):
        RuntimeError.__init__(self)
        self.message = message or self.message
        self.data = data
        self.code = code or self.code
        assert self.code, "Error without code is not allowed."

    def __str__(self):
        return "JsonRpcError({code}): {message}".format(
            code = self.code,
            message = str(self.message)
        )

    def __unicode__(self):
        return u"JsonRpcError({code}): {message}".format(
            code = self.code,
            message = self.message
        )

jsonrpcerrors[JsonRpcError.code] = JsonRpcError


class ParseError(JsonRpcError):
    code = -32700
    message = u"Invalid JSON was received by the server."

    def __init__(self, message = None, data = None):
        JsonRpcError.__init__(self, message = message, data = data)

jsonrpcerrors[ParseError.code] = ParseError


class InvalidRequest(JsonRpcError):
    code = -32600
    message = u"The JSON sent is not a valid Request object."

    def __init__(self, message = None, data = None):
        JsonRpcError.__init__(self, message = message, data = data)

jsonrpcerrors[InvalidRequest.code] = InvalidRequest


class MethodNotFound(JsonRpcError):
    code = -32601
    message = u"The method does not exist / is not available."

    def __init__(self, message = None, data = None):
        JsonRpcError.__init__(self, message = message, data = data)

jsonrpcerrors[MethodNotFound.code] = MethodNotFound


class InvalidParams(JsonRpcError):
    code = -32602
    message = u"Invalid method parameter(s)."

    def __init__(self, message = None, data = None):
        JsonRpcError.__init__(self, message = message, data = data)

jsonrpcerrors[InvalidParams.code] = InvalidParams


class InternalError(JsonRpcError):
    code = -32603
    message = u"Internal JSON-RPC error."

    def __init__(self, message = None, data = None):
        JsonRpcError.__init__(self, message = message, data = data)

jsonrpcerrors[InternalError.code] = InternalError


