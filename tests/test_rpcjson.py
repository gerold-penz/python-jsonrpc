#!/usr/bin/env python
# coding: utf-8
"""
Nosetests for *rpcjson.py*.
"""

import pyjsonrpc.rpcjson


EXAMPLE_LIST = [1, u"a", u"Ä"]
EXAMPLE_LIST_JSON = '[1, "a", "\u00c4"]'

EXAMPLE_DICT = {"a": u"Ä"}
EXAMPLE_DICT_JSON = '{"a": "\u00c4"}'


def test_dumps_list():
    assert pyjsonrpc.rpcjson.dumps(EXAMPLE_LIST) == EXAMPLE_LIST_JSON


def test_dumps_dict():
    assert pyjsonrpc.rpcjson.dumps(EXAMPLE_DICT) == EXAMPLE_DICT_JSON


def test_loads_list():
    assert pyjsonrpc.rpcjson.loads(EXAMPLE_LIST_JSON) == EXAMPLE_LIST


def test_loads_dict():
    assert pyjsonrpc.rpcjson.loads(EXAMPLE_DICT_JSON) == EXAMPLE_DICT

