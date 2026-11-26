#!/usr/bin/env python3
"""Entrypoint: write the bundled front page to the output directory.

Standard library only, no network, deterministic: it copies the image
entry.png (rendered by render_news.py) to /output/entry.png, so two runs
write the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, OUT)
os.chmod(OUT, 0o644)
