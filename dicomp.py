#!/usr/bin/env python3

#
# dicomp.py
#
# simple compression utility for dicli
#

from __future__ import print_function

try:
    import lzma as xz
except ImportError:
    import pylzma as xz

import os

with open('test.txt', 'rb') as f, open('test.txt.enc', 'wb') as out:
    out.write(xz.compress(bytes(f.read())))

with open('test.txt.enc', 'rb') as f, open('test.txt.dec', 'wb') as out:
    out.write(xz.decompress(bytes(f.read())))
