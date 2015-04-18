#!/usr/bin/env python2

from __future__ import print_function
import sys

print("Importing blpapi... ", end="")
try:
    import blpapi
    print("OK")
except ImportError:
    print("FAILED")
    print("Could not import blpapi, is it installed?")
    sys.exit(1)
