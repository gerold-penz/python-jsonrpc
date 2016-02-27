##################################################################################################
Python JSON-RPC Client Server Library With Additional Support for BaseHTTPServer, CherryPy And CGI
##################################################################################################

by Gerold Penz 2013-2016


- ToDo: Urllib3 for faster client requests

- ToDo: Notifications must not have an ID-Field


=============
Version 0.8.4
=============

2016-02-27

- Notifications must not have an ID-field. Until now the *notify*-method had
  an ID-field with `null`-value. Since now notifications will not have an
  ID-field. Thank you brandonkimbk! Issue #41 closed.


=============
Version 0.8.3
=============

2015-11-27

- Added coverage

- Added badges to README & Python version to Travis

- Merged pull request #35 from ZuluPro

- Images in README commented out

- Replaced ``except <Error>, err`` with ``except <Error> as err``

- Version-Push: Version 0.8.3


=============
Version 0.8.2
=============

2015-09-10

- The new function *get_traceback_string* returns the traceback string of the
  last error.

- Error handling changed


=============
Version 0.8.1
=============

2015-09-04

- Error repared in *_SpooledFile* in Google App Engine

- Gzip changes

- Recognize Google App Engine


=============
Version 0.8.0
=============

2015-09-03

- Changed the usage of username and password in HTTP-requests.


==============
Version 0.7.12
==============

2015-07-18

- New method *rpcrequest.Request.to_dict()*

- New method *rpcrequest.Request.from_dict()*

- Nosetests added


==============
Version 0.7.11
==============

2015-07-17

- Nosetests for *rpcerror.py* added.

- Nosetests for *rpcrequest.py* added.


==============
Version 0.7.10
==============

2015-07-11

- *rpcjson.loads* now supports Python 2.6.
  Changed in Python version 2.7: Added support for object_pairs_hook.

- Wheel setup added (http://pythonwheels.com/).


=============
Version 0.7.9
=============

2015-07-11

- Nosetests included and Travis (https://travis-ci.org/) aktivated.
  Thank you *scls19fr*. Extended tests will follow.


=============
Version 0.7.8
=============

2015-07-10

- Pull request by ilius merged: rpcresponse.py: handle string error;
  Thank you, ilius!

- Never again: Raising an error if a RPC-method returns `None`.
  Now, it is OK if the return value of a function is `None`.
  Until now only notifications were allowed to return `None`.


=============
Version 0.7.7
=============

2015-05-29

- Bug fixed: Library does not respect 0-value IDs

  A request is a notification if:

  - JSON-RPC version 2.0: no id
  - JSON-RPC version 1.0: id is `null`

  Thank you "lonelycode" and "pieceofchalk".


=============
Version 0.7.6
=============

2015-05-18

- SSL-Import deleted

- Http: Debugging of JSON messages added


=============
Version 0.7.5
=============

2015-05-18

- *rpclib*: Error-Logging --> *logging.error()*


=============
Version 0.7.4
=============

2015-05-14

- HttpClient: Added option to disable SSL certificate checks

- Example added: *custom_ssl_context.py*


=============
Version 0.7.3
=============

2015-04-01

- *JsonRpcError*-Class: *__str__*- and *__unicode__*-Function added. For better
  error message when using ``unicde(err)``.


=============
Version 0.7.2
=============

2015-03-20

- Better checking if empty json string.

- Cherrypy:

  - Workaround for false "Content-Types": If the request is a POST-request,
    the body will not read by cherrypy.

  - Bug in GET-requests fixed: GET-requests are possible now.


=============
Version 0.7.1
=============

2015-03-14

- Now, it is possible to raise *JsonRpcError* with any integer as error code.

  Pull request #20 built in. Thanks OrangeTux.

  - https://github.com/gerold-penz/python-jsonrpc/issues/1
  - https://github.com/gerold-penz/python-jsonrpc/pull/20

  Examples: "raise_error_example_server.py" and "raise_error_example_client.py"


=============
Version 0.7.0
=============

2015-03-14

- Possibly **incompatible** changes in background: Now, *pyjsonrpc* uses
  only the builtin JSON-library. *jsonlib2* and *simplejson* are no longer
  supported.

- All parameters of the functions *json.loads* and *json.dumps* can now be
  customized.

- New examples: "ordered_dict_example_server.py", "ordered_dict_example_client.py"


=============
Version 0.6.2
=============

2015-02-03

- For Google App Engine: *SpooledTemporaryFile* replaced with StringIO.


=============
Version 0.6.1
=============

2014-10-24

- CherryPy-Handler distinguishes between GET and POST.

- WSGI-Examples added


==================
Version 0.6.0.BETA
==================

2014-10-24

- Added CherryPy handler :-)


=============
Version 0.5.7
=============

2014-10-23

- Usage of SpooledTemporaryFile cleaned.


=============
Version 0.5.6
=============

2014-10-22

- Gzip-compression cleaned. I'm not sure, if the usage of
  *tempfile.SpooledTemporaryFile* is a good idea. I must test it.


=============
Version 0.5.5
=============

2014-10-22

- Httpclient and HttpRequestHandler: Added the possibility to compress
  HTTP-requests and HTTP-responses with *gzip*. @ajtag: Thanks :-)

- Workaround in Response-class for other external library (I don't know which one.
  ask @ajtag): Response accepts "faultCode", "fault" and "faultString".


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
