#!/usr/bin/env python

import os
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))

args = ["git", "commit"]
returncode = subprocess.call(args, cwd = THISDIR)
if returncode != 0:
    raw_input("Press ENTER to continue...")
