#!/usr/bin/env python3
"""news-image-20261118 v2: copy the front-page image to the output dir.

The front page itself (entry.png, 1024x1024) is drawn by
draw_frontpage.py at build time and committed in this repository; this
program only validates the image and copies it to the grader's output
directory. Standard library only, no network, deterministic.
"""
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"

MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) of a PNG file by reading its IHDR chunk."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    if not SRC.is_file():
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    size = SRC.stat().st_size
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    width, height = png_size(SRC)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"entry.png is {width}x{height}, over the 1024x1024 limit",
              file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    # Determinism check: the copy must be byte-identical to the source.
    if dest.stat().st_size != size or dest.read_bytes() != SRC.read_bytes():
        print("copy mismatch: output differs from entry.png", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({width}x{height}, {size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
