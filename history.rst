#####################################
Python JSON-RPC Client Server Library
#####################################

by Gerold Penz 2013-2014


=============
Version 0.5.4
=============

2014-10-21

- New Alias `ServiceProxy` added. For better compatibility to other libraries.

- *Request.from_string()* added

- *Request.to_string()* added

- Examples added


=============
Version 0.5.3
=============

2014-10-21

- New Alias `ServiceMethod` added, for the *@pyjsonrpc.rpcmethod*-decorator.


=============
Version 0.5.2
=============

2014-10-11

- HTTP-Server: The content-type is changeable, now. Default content-type stays
  "application/json". If you want to change the content-type::

    class RequestHandler(pyjsonrpc.HttpRequestHandler):

        content-type = "application/json-rpc"

        ...

- HTTP-Server GET-Request: Check if method name given


=============
Version 0.5.1
=============

2014-09-12

- Descriptions


=============
Version 0.5.0
=============

2014-09-12

- The new decorator *@pyjsonrpc.rpcmethod* signs methods as JSON-RPC-Methods.

- Examples with the new *rpcmethod*-decorator added.

- I think, *python-jsonrpc* is stable enough to set the classifier to
  "Development Status :: 5 - Production/Stable".


=============
Version 0.4.3
=============

2014-09-12

- HttpClient: *cookies*-parameter added. Now, it is possible to add
  simple cookie-items.


=============
Version 0.4.2
=============

2014-09-12

- HttpClient: New parameters added:
  - additional_headers: Possibility to add additional header items.
  - content_type: Possibility to change the content-type header.


=============
Version 0.4.1
=============

2014-08-19

- HttpClient: The new timeout parameter specifies a timeout in seconds for
  blocking operations like the connection attempt (if not specified,
  the global default timeout setting will be used). Thanks *geerk* :-)

  See: https://github.com/gerold-penz/python-jsonrpc/pull/6


=============
Version 0.4.0
=============

2014-06-28

- It is now possible to send multiple calls in one request.

- *multiple_example.py* added.


=============
Version 0.3.5
=============

2014-06-28

- Bunch is now a setup-dependency.

- The new method *HttpClient.notify* sends notifications to the server,
  without `id` as parameter.


=============
Version 0.3.4
=============

2013-07-07

- Tests with CGI reqeusts


=============
Version 0.3.3
=============

2013-07-07

- Better HTTP server example

- Deleted the *rpcjson.json* import from *__init__.py*.

- The Method *do_POST* handles HTTP-POST requests

- CGI handler created

- CGI example created


=============
Version 0.3.2
=============

2013-07-06

- Tests with BaseHTTPServer

- Moved *JsonRpc*-class from *__init__.py* to *rpclib.py*.

- *ThreadingHttpServer* created

- *HttpRequestHandler* created

- The Method *do_GET* handles HTTP-GET requests

- Created HTTP server example


=============
Version 0.3.1
=============

2013-07-06

- Small new feature in HttpClient: Class instance calls will be redirected to
  *self.call*. Now this is possible: ``http_client("add", 1, 2)``.


=============
Version 0.3.0
=============

2013-07-04

- Try to import fast JSON-libraries at first:

  1. try to use *jsonlib2*
  2. try to use *simplejson*
  3. use builtin *json*

- To simplify the code, now we use *bunch*. Bunch is a dictionary
  that supports attribute-style access.


=============
Version 0.2.6
=============

2013-07-03

- RPC-Errors are now better accessible


=============
Version 0.2.5
=============

2013-06-30

- Now, it is possible to use the *method* name as *attribute* name for
  HTTP-JSON-RPC Requests.


=============
Version 0.2.4
=============

2013-06-30

- *rcperror*-Module: Error classes shortened.

- *Response.from_error*-method deleted. I found a better way (not so complex)
  to deliver error messages.

- New *simple_example.py*

- Examples directory structure changed

- HTTP-Request

- HTTP-Client

- HTTP-Client examples


=============
Version 0.2.3
=============

2013-06-24

- Splitted into several modules

- New response-class


=============
Version 0.2.2
=============

2013-06-23

- Return of the Response-Object improved


=============
Version 0.2.1
=============

2013-06-23

- Added a *system.describe*-method (not finished yet)

- Added examples

- Added *parse_json_response*-function


=============
Version 0.2.0
=============

2013-06-23

- Responses module deleted

- *call*-method finished

- Simple example


=============
Version 0.1.1
=============

2013-06-23

- Responses splitted into successful response and errors

- call-function


=============
Version 0.1.0
=============

2013-06-23

- Error module created

- Responses module created

- Base structure


=============
Version 0.0.1
=============

2013-06-23

- Initialy imported
