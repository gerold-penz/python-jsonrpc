#!/usr/bin/env python
# coding: utf-8

import os
import gzip
import StringIO
import tempfile


# Workaround for Google App Engine
if "APPENGINE_RUNTIME" in os.environ:
    TmpFile = StringIO.StringIO
    google_app_engine = True
else:
    TmpFile = tempfile.SpooledTemporaryFile
    google_app_engine = False


MAX_SIZE_IN_MEMORY = 1024 * 1024 * 10  # 10 MiB
CHUNK_SIZE = 1024 * 1024  # 1 MiB


def gzip_str_to_file(raw_text, dest_file):
    with gzip.GzipFile(filename = "", mode = "wb", fileobj = dest_file) as gz:
        gz.write(raw_text)


def gunzip_file(source_file):
    with gzip.GzipFile(filename = "", mode = "rb", fileobj = source_file) as gz:
        return gz.read()


class SpooledFile(TmpFile):
    """
    Spooled temporary file.

    StringIO with fallback to temporary file if size > MAX_SIZE_IN_MEMORY.
    """

    def __init__(
        self,
        max_size = MAX_SIZE_IN_MEMORY,
        mode = "w+b",
        source_file = None,
        *args, **kwargs
    ):

        # Init
        if google_app_engine:
            TmpFile.__init__(self)
        else:
            TmpFile.__init__(self, max_size = max_size, mode = mode)

        if source_file:
            for chunk in iter(lambda: source_file.read(CHUNK_SIZE), ""):
                self.write(chunk)
            self.seek(0)


    def __len__(self):
        current_pos = self.tell()
        try:
            self.seek(0, 2)
            return self.tell()
        finally:
            self.seek(current_pos)


