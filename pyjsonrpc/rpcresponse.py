#!/usr/bin/env python
# coding: utf-8

import rpcjson
from bunch import Bunch
from rpcerror import InternalError


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


    def to_string(self):
        """
        Returns the response as JSON-string
        """

        return rpcjson.dumps(self.to_dict())


    # Alias
    dumps = to_string


    @classmethod
    def from_dict(cls, response_dict):
        """
        Returns a Response-object, created from dictionary
        """

        error = response_dict.get("error")
        if error:
            result = None
            if "code" in error:
                # JSON-RPC Standard Error
                error = cls.Error(
                    code = error.get("code"),
                    message = error.get("message"),
                    data = error.get("data")
                )
            elif "fault" in error:
                # Workaround for other library? I don't know it.
                error = cls.Error(
                    code = error.get("faultCode"),
                    message = error.get("fault"),
                    data = error.get("faultString")
                )
            else:
                error = cls.Error(
                    code = InternalError.code,
                    message = InternalError.message,
                    data = "\n".join(["%s: %s" % (k, v) for k, v in error])
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


    @classmethod
    def from_string(cls, json_string):
        """
        Returns a Response-object or a list with Response-objects
        """

        if not json_string:
            return

        data = rpcjson.loads(json_string)

        if isinstance(data, list):
            retlist = []
            for response in data:
                retlist.append(cls.from_dict(response))
            return retlist
        else:
            return cls.from_dict(data)


    # Alias
    loads = from_string


# Aliases
parse_response_json = Response.from_string
parse_response_string = Response.from_string
