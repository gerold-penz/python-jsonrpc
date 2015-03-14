#!/usr/bin/env python
# coding: utf-8

import json as _json
JsonParseError = ValueError


# Default-Parameters for the *dumps*-function
dumps_skipkeys = False
dumps_ensure_ascii = True
dumps_check_circular = True
dumps_allow_nan = True
dumps_cls = None
dumps_indent = None
dumps_separators = None
dumps_encoding = "utf-8"
dumps_default = None
dumps_sort_keys = False


# Default-Parameters for the *loads*-function
loads_encoding = None
loads_cls = None
loads_object_hook = None
loads_parse_float = None
loads_parse_int = None
loads_parse_constant = None
loads_object_pairs_hook = None


def dumps(obj):
    """
    Replacement function for *json.dumps*

    Uses the predefined default settings.
    """

    return _json.dumps(
        obj,
        skipkeys = dumps_skipkeys,
        ensure_ascii = dumps_ensure_ascii,
        check_circular = dumps_check_circular,
        allow_nan = dumps_allow_nan,
        cls = dumps_cls,
        indent = dumps_indent,
        separators = dumps_separators,
        encoding = dumps_encoding,
        default = dumps_default,
        sort_keys = dumps_sort_keys
    )


def loads(s):
    """
    Replacement function for *json.loads*

    Uses the predefined default settings.
    """

    return _json.loads(
        s,
        encoding = loads_encoding,
        cls = loads_cls,
        object_hook = loads_object_hook,
        parse_float = loads_parse_float,
        parse_int = loads_parse_int,
        parse_constant = loads_parse_constant,
        object_pairs_hook = loads_object_pairs_hook
    )


########################
# OLD IMPORTS
########################
# try:
#     import jsonlib2 as json
#     JsonParseError = json.ReadError
# except ImportError:
#     try:
#         import simplejson as json
#         JsonParseError = json.JSONDecodeError
#     except ImportError:
#         import json
#         JsonParseError = ValueError
########################
