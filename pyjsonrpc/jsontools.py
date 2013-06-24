#!/usr/bin/env python
# coding: utf-8

try:
    import jsonlib2 as json
    ParseError = json.ReadError
except ImportError:
    import json
    ParseError = ValueError

