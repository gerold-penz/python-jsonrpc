#!/usr/bin/env python
# coding: utf-8
"""
Nosetests for *rpcjson.py*.
"""

import pyjsonrpc.rpcjson


def test_dumps_list():
    example_list = [1, u"a", u"Ä"]
    example_json = '[1, "a", "\u00c4"]'
    assert pyjsonrpc.rpcjson.dumps(example_list) == example_json


def test_dumps_dict():
    example_dict = {"a": u"Ä"}
    example_json = '{"a": "\u00c4"}'
    assert pyjsonrpc.rpcjson.dumps(example_dict) == example_json


def test_loads_list():
    example_json = '[1, "a", "\u00c4"]'
    example_list = [1, u"a", u"Ä"]
    assert pyjsonrpc.rpcjson.loads(example_json) == example_list


def test_loads_dict():
    example_json = '{"a": "\u00c4"}'
    example_dict = {"a": u"Ä"}
    assert pyjsonrpc.rpcjson.loads(example_json) == example_dict

