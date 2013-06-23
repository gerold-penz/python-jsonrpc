#!/usr/bin/env python
# coding: utf-8


class JsonRpcError(RuntimeError):
    """
    Represents a JSON-RPC-Error
    """

    def __init__(
        self, code = None, message = None, jsonrpc = None, id = None, data = None
    ):
        """
        Initializes the JSON-RPC-Error
        """

        self.code = code
        self.message = message
        self.jsonrpc = jsonrpc
        self.id = id
        self.data = data


    def to_dict(self):
        """
        Returns the error object as dictionary.
        """

        retdict = {"error": {}}
        if self.jsonrpc:
            retdict["jsonrpc"] = self.jsonrpc
        retdict["id"] = self.id
        retdict["error"]["code"] = self.code
        retdict["error"]["message"] = self.message
        if self.data:
            retdict["error"]["data"] = self.data
            if isinstance(self.data, basestring):
                if self.message:
                    retdict["error"]["message"] = \
                        self.message + u" " + self.data.capitalize()
                else:
                    retdict["error"]["message"] = self.data.capitalize()
        return retdict


class ParseError(JsonRpcError):

    def __init__(self, jsonrpc = None, id = None, data = None):
        JsonRpcError.__init__(
            self,
            code = -32700,
            message = u"Invalid JSON was received by the server.",
            jsonrpc = jsonrpc,
            id = id,
            data = data
        )


class InvalidRequest(JsonRpcError):
    def __init__(self, jsonrpc = None, id = None, data = None):
        JsonRpcError.__init__(
            self,
            code = -32600,
            message = u"The JSON sent is not a valid Request object.",
            jsonrpc = jsonrpc,
            id = id,
            data = data
        )


class MethodNotFound(JsonRpcError):
    def __init__(self, jsonrpc = None, id = None, data = None):
        JsonRpcError.__init__(
            self,
            code = -32601,
            message = u"The method does not exist / is not available.",
            jsonrpc = jsonrpc,
            id = id,
            data = data
        )


class InvalidParams(JsonRpcError):
    def __init__(self, jsonrpc = None, id = None, data = None):
        JsonRpcError.__init__(
            self,
            code = -32602,
            message = u"Invalid method parameter(s).",
            jsonrpc = jsonrpc,
            id = id,
            data = data
        )


class InternalError(JsonRpcError):
    def __init__(self, jsonrpc = None, id = None, data = None):
        JsonRpcError.__init__(
            self,
            code = -32603,
            message = u"Internal JSON-RPC error.",
            jsonrpc = jsonrpc,
            id = id,
            data = data
        )


