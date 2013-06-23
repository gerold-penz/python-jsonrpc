#!/usr/bin/env python

import os
import sys
import shutil
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))

## Delete *dist* dir
#dist_dir = os.path.join(THISDIR, "dist")
#if os.path.isdir(dist_dir):
#    shutil.rmtree(dist_dir)

## Delete *cherrypy_cgiserver.egg-info* dir
#egginfo_dir = os.path.join(THISDIR, "cherrypy_cgiserver.egg-info")
#if os.path.isdir(egginfo_dir):
#    shutil.rmtree(egginfo_dir)

# Create new distributable files
args = [sys.executable, "setup.py", "sdist"]
returncode = subprocess.call(args, cwd = THISDIR)
if returncode != 0:
    raw_input("Press ENTER to continue...")
