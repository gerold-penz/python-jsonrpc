#!/usr/bin/env python
# coding: utf-8

from bunch import Bunch
from rpcjson import json


class Response(Bunch):
    """
    Represents a JSON-RPC-response.
    """

    class Error(Bunch):

        def __init__(self, code, message, data):
            """
            :param code: Error code
            :param message: Error message
            :param data: Additional error informations
            """

            Bunch.__init__(self)
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
        error = None
    ):
        """
        :param jsonrpc: JSON-RPC version string
        :param id: JSON-RPC transaction id
        :param result: Result data
        """

        Bunch.__init__(self)
        self.jsonrpc = jsonrpc
        self.id = id
        self.result = result if not error else None
        self.error = error


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
            error = cls.Error(
                code = error.get("code"),
                message = error.get("message"),
                data = error.get("data")
            )
        else:
            result = response_dict.get("result")
            error = None

        return cls(
            jsonrpc = response_dict.get("jsonrpc"),
            id = response_dict.get("id"),
            result = result,
            error = error
        )


def parse_response_json(json_string):
    """
    Returns a RPC-Response or a list with RPC-Responses
    """

    if not json_string:
        return

    data = json.loads(json_string)

    if isinstance(data, list):
        retlist = []
        for response in data:
            retlist.append(Response.from_dict(response))
        return retlist
    else:
        return Response.from_dict(data)
