#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261125.

Writes the entry image to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
The image is drawn by draw.py (same repository) and shipped as entry.png;
this program copies it byte-for-byte, so both grading runs produce
identical output with no network, no wall-clock and no randomness.
Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else "."
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
