#####################################
Python JSON-RPC Library Client Server
#####################################


============
Installation
============

::

    pip install bunch
    pip install python-jsonrpc


=====================
Library Usage Example
=====================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc


    def add(a, b):
        """Test function"""
        return a + b


    # 1. Initialize JSON-RPC class with JSON-RPC method(s)
    rpc = pyjsonrpc.JsonRpc(methods = {"add": add})

    # 2. Create JSON-RPC string with parameters (= request string)
    request_json = pyjsonrpc.create_request_json("add", 1, 2)
    # request_json = '{"method": "add", "params": [1, 2], "id": "...", "jsonrpc": "2.0"}'

    # 3. Call the JSON-RPC function and get back the JSON-RPC result (= response string)
    response_json = rpc.call(request_json)
    # response_json = '{"result": 3, "id": "...", "jsonrpc": "2.0"}'

    # 4. Convert JSON-RPC string to Python objects
    response = pyjsonrpc.parse_response_json(response_json)

    # 5. Print result or error
    if response.error:
        print "Error:", response.error.code, response.error.message
    else:
        print "Result:", response.result


===================
HTTP Client Example
===================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc

    http_client = pyjsonrpc.HttpClient(
        url = "http://example.com/jsonrpc",
        username = "Username",
        password = "Password"
    )
    print http_client.call("add", 1, 2)
    # Result: 3

    # It is also possible to use the *method* name as *attribute* name.
    print http_client.add(1, 2)
    # Result: 3


===================
HTTP Server Example
===================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc

    def add(a, b):
        """Test function"""
        return a + b

    class RequestHandler(pyjsonrpc.HttpRequestHandler):

        # Register public JSON-RPC methods
        methods = {
            "add": add
        }

    # Threading HTTP-Server
    http_server = pyjsonrpc.ThreadingHttpServer(
        server_address = ('localhost', 8080),
        RequestHandlerClass = RequestHandler
    )
    print "Starting HTTP server ..."
    print "URL: http://localhost:8080"
    http_server.serve_forever()


===========
CGI Example
===========

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc

    def add(a, b):
        """Test function"""
        return a + b

    # Handles the JSON-RPC request and gets back the result to STDOUT
    pyjsonrpc.handle_cgi_request(methods = dict(add = add))


========
Licenses
========

- GNU Library or Lesser General Public License (LGPL)
- MIT License 

