#!/usr/bin/env python
# coding: utf-8

import sys
import traceback
import responses
import errors
try:
    import jsonlib2 as json
    _ParseError = json.ReadError
except ImportError:
    import json
    _ParseError = ValueError


class JsonRpc(object):
    """
    """

    def __init__(self, methods = None):
        """
        Initializes the JSON-RPC-Class

        :param methods: Json-RPC-Methods. `None` or Dictionary with method
            names as key and functions as values. Syntax::

                {
                    "<method_name>": <method_function>,
                    ...
                }
        """

        self.methods = methods or {}


    def parse_requests(self, json_string):
        """
        Returns parsed JSON-RPC-Requests.

        :return: List with JSON-RPC-request-dictionaries or `None` if no
            request found. Syntax::

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
            return

        requests = []
        try:
            data = json.loads(json_string)
        except _ParseError, err:
            traceback_info = "".join(traceback.format_exception(*sys.exc_info()))

            raise

            return json.dumps(
                responses.ParseErrorResponse(
                    data = unicode(err)
                ).to_dict()
            )

        if isinstance(data, list):
            requests = data
        else:
            requests = [data]



        #     data = kwargs
        #     if "params" in data:
        #         if self.debug:
        #             cherrypy.log("")
        #             cherrypy.log(u"params (raw): " + repr(data["params"]))
        #             cherrypy.log("")
        #         try:
        #             data["params"] = json.loads(data["params"])
        #         except _ParseError, err:
        #             traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        #             cherrypy.log(traceback_info)
        #             return json.dumps(
        #                 responses.ParseErrorResponse(
        #                     data = unicode(err)
        #                 ).to_dict()
        #             )
        #     requests = [data]





    def get_responses(self, jsonrpc_requests):
        """
        """


        # try:
        #     data["params"] = json.loads(data["params"])
        # except _ParseError, err:
        #     traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        #     logging.error(traceback_info)
        #     return json.dumps(
        #         responses.ParseErrorResponse(
        #             data = unicode(err)
        #         ).to_dict()
        #     )

        # # Every JSON-RPC request in a batch of requests
        # for request in requests:
        #
        #     # jsonrpc
        #     jsonrpc = request.get("jsonrpc")
        #
        #     # method
        #     method = str(request.get("method", ""))
        #
        #     # id
        #     id = request.get("id")
        #
        #     # split positional and named params
        #     positional_params = []
        #     named_params = {}
        #     params = request.get("params", [])
        #     if isinstance(params, list):
        #         positional_params = params
        #     elif isinstance(params, dict):
        #         positional_params = params.get("__args", [])
        #         if positional_params:
        #             del params["__args"]
        #         named_params = params
        #
        #     # Debug
        #     if self.debug:
        #         cherrypy.log("")
        #         cherrypy.log(u"jsonrpc: " + repr(jsonrpc))
        #         cherrypy.log(u"request: " + repr(request))
        #         cherrypy.log(u"positional_params: " + repr(positional_params))
        #         cherrypy.log(u"named_params: " + repr(named_params))
        #         cherrypy.log(u"method: " + repr(method))
        #         cherrypy.log(u"id: " + repr(id))
        #         cherrypy.log("")
        #
        #     # Do we know the method name?
        #     if not method in self.rpc_methods:
        #         traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        #         cherrypy.log("JSON-RPC method '%s' not found" % method)
        #         responses.append(
        #             responses.MethodNotFoundResponse(jsonrpc = jsonrpc, id = id).to_dict()
        #         )
        #         continue
        #
        #     # Call the method with parameters
        #     try:
        #         rpc_function = self.rpc_methods[method]
        #         result = rpc_function(*positional_params, **named_params)
        #         # No return value is OK if we don´t have an ID (=notification)
        #         if result is None:
        #             if id:
        #                 cherrypy.log("No result from JSON-RPC method '%s'" % method)
        #                 responses.append(
        #                     responses.InternalErrorResponse(
        #                         jsonrpc = jsonrpc,
        #                         id = id,
        #                         data = u"No result from JSON-RPC method."
        #                     ).to_dict()
        #                 )
        #         else:
        #             # Successful response
        #             responses.append(
        #                 responses.SuccessfulResponse(
        #                     jsonrpc = jsonrpc, id = id, result = result
        #                 ).to_dict()
        #             )
        #     except TypeError, err:
        #         traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        #         cherrypy.log(traceback_info)
        #         if "takes exactly" in unicode(err) and "arguments" in unicode(err):
        #             responses.append(
        #                 responses.InvalidParamsResponse(jsonrpc = jsonrpc, id = id).to_dict()
        #             )
        #         else:
        #             responses.append(
        #                 responses.InternalErrorResponse(
        #                     jsonrpc = jsonrpc,
        #                     id = id,
        #                     data = unicode(err)
        #                 ).to_dict()
        #             )
        #     except BaseException, err:
        #         traceback_info = "".join(traceback.format_exception(*sys.exc_info()))
        #         cherrypy.log(traceback_info)
        #         if hasattr(err, "data"):
        #             error_data = err.data
        #         else:
        #             error_data = None
        #         responses.append(
        #             responses.InternalErrorResponse(
        #                 jsonrpc = jsonrpc,
        #                 id = id,
        #                 data = error_data or unicode(err)
        #             ).to_dict()
        #         )
        #
        # # Return as JSON-String (batch or normal)
        # if len(requests) == 1:
        #     return json.dumps(responses[0])
        # elif len(requests) > 1:
        #     return json.dumps(responses)
        # else:
        #     return None



    def __call__(self, *args, **kwargs):
        """
        """

        return self.get_responses(*args, **kwargs)




