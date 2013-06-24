#!/usr/bin/env python
# coding: utf-8

from rpcjson import json


class Response(dict):
    """
    Represents a JSON-RPC-response.
    """

    class Error(dict):

        def __init__(self, code, message, data):
            dict.__init__(self, code = code, message = message, data = data)
            self.code = code
            self.message = message
            self.data = data

        def __len__(self):
            return 1 if self.code else 0


    def __init__(
        self,
        jsonrpc = None,
        id = None,
        result = None,
        # error_code = None,
        # error_message = None,
        # error_data = None,
        error = None
    ):
        """
        :param jsonrpc: JSON-RPC version string
        :param id: JSON-RPC transaction id
        :param result: Result data
        :param error_code: Error code
        :param error_message: Error message
        :param error_data: Additional error informations
        """

        self.jsonrpc = jsonrpc
        self.id = id
        self.result = result if not error_code else None
        self.error = self.Error(
            code = error_code, message = error_message, data = error_data
        )

        dict.__init__(
            self,
            jsonrpc = jsonrpc,
            id = id,
            result = result,
            error = self.error
        )


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

        # Error
        if self.error:
            retdict.pop("result", None)
            retdict["error"] = error = {}
            error["code"] = self.error.code
            error["message"] = self.error.message
            if self.error.data:
                error["data"] = self.error.data

        # Finished
        return retdict


    @classmethod
    def from_dict(cls, response_dict):
        """
        Returns a Response-object, created from dictionary
        """

        error = response_dict.get("error")
        if error:
            result = None
            error_code = error.get("code")
            error_message = error.get("message")
            error_data = error.get("data")
        else:
            result = response_dict.get("result")
            error_code = None
            error_message = None
            error_data = None

        return cls(
            jsonrpc = response_dict.get("jsonrpc"),
            id = response_dict.get("id"),
            result = result,
            error_code = error_code,
            error_message = error_message,
            error_data = error_data
        )


    @classmethod
    def from_error(cls, rpc_error):
        """
        Returns a Response-object, created from a RPC-Error
        """


        # ToDo: Diese Funktion sollte entfernt werden. Es muss eine
        # schönere Lösung dafür geben. Es kann doch nicht sein, dass
        # im *Error* die Felder *jsonrpc* und *id* mitgeführt werden müssen.


        return cls(
            jsonrpc = rpc_error.jsonrpc,
            id = rpc_error.id,
            error_code = rpc_error.code,
            error_message = rpc_error.message,
            error_data = rpc_error.data
        )


def parse_response_json(json_string):
    """
    Returns a RPC-Response or a list with RPC-Responses
    """

    data = json.loads(json_string)

    if isinstance(data, list):
        retlist = []
        for response in data:
            retlist.append(Response.from_dict(response))
        return retlist
    else:
        return Response.from_dict(data)
