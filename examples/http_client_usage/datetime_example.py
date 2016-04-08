#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
import datetime
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDIR)
# END --- required only for testing, remove in real world code --- END


import pyjsonrpc
import pyjsonrpc.rpcjson

# Activate encoder and decoder for DateTime-ISO strings and NDB keys
pyjsonrpc.rpcjson.activate_iso_date_and_ndb_conversion()


rpc_client = pyjsonrpc.HttpClient("http://localhost:8080")
now = datetime.datetime.now()


print repr(now)  # datetime.datetime(2016, 4, 7, 16, 51, 12, 483694)
print repr(rpc_client.add_one_hour(timestamp = now))  # datetime.datetime(2016, 4, 7, 17, 51, 12)
