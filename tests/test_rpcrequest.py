#!/usr/bin/env python
# coding: utf-8
"""
Nosetests for *rpcerror.py*.
"""

import json
import pyjsonrpc.rpcrequest

TESTMETHOD = u"TESTMETHOD"
TESTID = u"TESTID"


def test_create_request_dict_with_positional_params():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, u"Ö", u"ß"
    )
    assert "id" in request_dict, u"No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": (u"\xd6", u"\xdf"),
        "id": TESTID
    }, u"Unexpected result"


def test_create_request_dict_with_named_params():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, k1 = u"Ä", k2 = u"Ö"
    )
    assert "id" in request_dict, u"No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": u"\xc4", "k2": u"\xd6"},
        "id": TESTID
    }, u"Unexpected result"


def test_create_request_dict_with_positional_and_named_params():
    request_dict = pyjsonrpc.rpcrequest.create_request_dict(
        TESTMETHOD, 1, 2, k1 = u"Ä", k2 = u"Ö"
    )
    assert "id" in request_dict, u"No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": u"\xc4", "k2": u"\xd6", "__args": (1, 2)},
        "id": TESTID
    }, u"Unexpected result"


def test_create_request_json_with_positional_params():
    request_json = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, u"Ö", u"ß"
    )
    request_dict = json.loads(request_json)
    assert "id" in request_dict, u"No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": [u"\xd6", u"\xdf"],
        "id": TESTID
    }, u"Unexpected result"


def test_create_request_json_with_named_params():
    request_json = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, k1 = u"Ä", k2 = u"Ö"
    )
    request_dict = json.loads(request_json)
    assert "id" in request_dict, u"No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": u"\xc4", "k2": u"\xd6"},
        "id": TESTID
    }, u"Unexpected result"


def test_create_request_json_with_positional_and_named_params():
    request_json = pyjsonrpc.rpcrequest.create_request_json(
        TESTMETHOD, 1, 2, k1 = u"Ä", k2 = u"Ö"
    )
    request_dict = json.loads(request_json)
    assert "id" in request_dict, u"No *id* found"
    request_dict["id"] = TESTID
    assert request_dict == {
        "jsonrpc": "2.0",
        "method": TESTMETHOD,
        "params": {"k1": u"\xc4", "k2": u"\xd6", "__args": [1, 2]},
        "id": TESTID
    }, u"Unexpected result"


