#####################################
Python JSON-RPC Client Server Library
#####################################


============
Installation
============

::

    pip install python-jsonrpc


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

    # Notifications send messages to the server, without response.
    http_client.notify("add", 3, 4)


===================
HTTP Server Example
===================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc


    class RequestHandler(pyjsonrpc.HttpRequestHandler):

      @pyjsonrpc.rpcmethod
      def add(self, a, b):
          """Test method"""
          return a + b


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


=====================
Library Usage Example
=====================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import pyjsonrpc


    class JsonRpc(pyjsonrpc.JsonRpc):

        @pyjsonrpc.rpcmethod
        def add(self, a, b):
            """Test method"""
            return a + b


    # 1. Initialize JSON-RPC class
    rpc = JsonRpc()

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


========
Licenses
========

- GNU Library or Lesser General Public License (LGPL)
- MIT License 

