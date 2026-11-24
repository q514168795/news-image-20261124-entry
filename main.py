#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Copy the day's image to the output directory, as the house contract asks."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST, os.path.getsize(DST), "bytes")
