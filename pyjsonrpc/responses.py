#!/usr/bin/env python
# coding: utf-8


class SuccessfulResponse(object):
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


class ErrorResponse(object):
    """
    Represents an error response object
    """

    code = None
    message = None


    def __init__(self, jsonrpc = None, id = None, data = None):
        """
        :param jsonrpc: JSON-RPC version string
        :param id: JSON-RPC transaction id
        :param data: Additional error informations. Can be any, to JSON
            translatable, data structure.
        """
        self.jsonrpc = jsonrpc
        self.id = id
        self.data = data


    def to_dict(self):
        """
        Returns the response object as dictionary.
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


class ParseErrorResponse(ErrorResponse):
    code = -32700
    message = u"Invalid JSON was received by the server."


class InvalidRequestResponse(ErrorResponse):
    code = -32600
    message = u"The JSON sent is not a valid Request object."


class MethodNotFoundResponse(ErrorResponse):
    code = -32601
    message = u"The method does not exist / is not available."


class InvalidParamsResponse(ErrorResponse):
    code = -32602
    message = u"Invalid method parameter(s)."


class InternalErrorResponse(ErrorResponse):
    code = -32603
    message = u"Internal JSON-RPC error."
