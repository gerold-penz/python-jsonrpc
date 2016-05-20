#!/usr/bin/env python
# coding: utf-8

import json as _json
import datetime
try:
    # Google App Engine NDB - for automatic Key and BlobKey conversion
    from google.appengine.ext import ndb
except ImportError:
    ndb = None


# Date ISO formats
ISO8601_10_DIGITS = "%Y-%m-%d"

ISO8601_17_DIGITS = "%Y-%m-%dT%H%M%S"
ISO8601_17_DIGITS_V2 = "%Y-%m-%d %H%M%S"

ISO8601_19_DIGITS = "%Y-%m-%dT%H:%M:%S"
ISO8601_19_DIGITS_V2 = "%Y-%m-%d %H:%M:%S"

ISO8601_20_DIGITS = "%Y-%m-%dT%H:%M:%SZ"
ISO8601_20_DIGITS_V2 = "%Y-%m-%d %H:%M:%SZ"


# Different JSON parsers have got different ParseError objects.
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

    # Named parameters for *loads*
    kwargs = {
        "encoding": loads_encoding,
        "cls": loads_cls,
        "object_hook": loads_object_hook,
        "parse_float": loads_parse_float,
        "parse_int": loads_parse_int,
        "parse_constant": loads_parse_constant
    }
    if loads_object_pairs_hook is not None:
        kwargs["object_pairs_hook"] = loads_object_pairs_hook

    # Finished
    return _json.loads(s, **kwargs)


def date_time_decoder(obj):
    """
    Recursive decoder for ISO date and datetime strings

    Global activation::

        import pyjsonrpc.rpcjson
        pyjsonrpc.rpcjson.loads_object_hook = pyjsonrpc.rpcjson.date_time_decoder
    """

    if isinstance(obj, basestring):

        # Check min length and if "-" exists
        check_string = obj[0:10]
        if len(check_string) < 10:
            return obj
        if not check_string[4] == "-":
            return obj
        if not check_string[7] == "-":
            return obj

        # Get length
        obj_len = len(obj)

        # Length checks ordered by priority
        if obj_len == 10:
            try:
                date_obj = datetime.datetime.strptime(obj, ISO8601_10_DIGITS)
                return date_obj.date()
            except (ValueError, TypeError):
                return obj
        elif obj_len == 17:
            try:
                return datetime.datetime.strptime(obj, ISO8601_17_DIGITS)
            except (ValueError, TypeError):
                try:
                    return datetime.datetime.strptime(obj, ISO8601_17_DIGITS_V2)
                except (ValueError, TypeError):
                    return obj
        elif obj_len == 19:
            try:
                return datetime.datetime.strptime(obj, ISO8601_19_DIGITS)
            except (ValueError, TypeError):
                try:
                    return datetime.datetime.strptime(obj, ISO8601_19_DIGITS_V2)
                except (ValueError, TypeError):
                    return obj
        elif obj_len == 20:
            try:
                return datetime.datetime.strptime(obj, ISO8601_20_DIGITS)
            except (ValueError, TypeError):
                try:
                    return datetime.datetime.strptime(obj, ISO8601_20_DIGITS_V2)
                except (ValueError, TypeError):
                    return obj
        elif obj_len == 25:
            # "2016-05-20T10:31:50+02:00"
            if obj[19] in ["+", "-"]:
                return date_time_decoder(obj[0:19])
        else:
            return obj

    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            obj[index] = date_time_decoder(value)

    elif isinstance(obj, dict):
        for key, value in obj.iteritems():
            obj[key] = date_time_decoder(value)

    return obj


def iso_date_and_ndb_encoder(obj):
    """
    Encoder for date, datetime, Google App Engine NDB - Key and BlobKey

    Global activation::

        import pyjsonrpc.rpcjson
        pyjsonrpc.rpcjson.dumps_default = pyjsonrpc.rpcjson.iso_date_and_ndb_encoder
    """

    if isinstance(obj, datetime.datetime):
        return obj.strftime(ISO8601_19_DIGITS)
    elif isinstance(obj, datetime.date):
        return obj.strftime(ISO8601_10_DIGITS)
    elif ndb and isinstance(obj, ndb.BlobKey):
        return str(obj)
    elif ndb and isinstance(obj, ndb.Key):
        return obj.urlsafe()
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")


def activate_iso_date_and_ndb_conversion():
    """
    Activates the automatic conversion between ISO-Date and date/datetime and
    Google App Engine NDB - Key and BlobKeys
    """

    global loads_object_hook
    global dumps_default

    loads_object_hook = date_time_decoder
    dumps_default = iso_date_and_ndb_encoder
