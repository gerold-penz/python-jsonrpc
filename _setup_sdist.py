#!/usr/bin/env python

import os
import sys
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))

# Create new distributable files
args = [sys.executable, "setup.py", "sdist"]
returncode = subprocess.call(args, cwd = THISDIR)
if returncode != 0:
    raw_input("Press ENTER to continue...")
