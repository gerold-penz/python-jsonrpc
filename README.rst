#####################################
Python JSON-RPC Library Client Server
#####################################

*Example*:

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc


    def add(a, b):
        return a + b


    # Initialize JSON-RPC-Class with JSON-RPC-Methods
    rpc = pyjsonrpc.JsonRpc(methods = {"add": add})

    # Create JSON-RPC-string with positional params
    request_json = pyjsonrpc.create_json_request("add", 1, 2)
    # '{"params": [1, 2], "jsonrpc": "2.0", "method": "add", "id": "..."}'
    print "Request-JSON:", repr(request_json)

    # RPC-Call
    response_json = rpc.call(request_json)
    # '{"jsonrpc": "2.0", "id": "...", "result": 3}'
    print "Response-JSON:", repr(response_json)

    # Result
    response = pyjsonrpc.parse_json_response(response_json)
    # 3
    print "Response:", response["result"]


