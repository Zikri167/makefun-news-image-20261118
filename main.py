"""Copy the bundled front-page image to the output directory.

Reads entry.png next to this file, checks it is a whole PNG or JPEG
within the competition's size and dimension limits, and writes the
bytes unchanged to entry.png in MAKEFUN_OUTPUT_DIR (or /output).
Standard library only; no network, no randomness, same bytes every run.
"""

import os
import struct
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_START = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"
MIN_BYTES = 1024
MAX_BYTES = 1048576
MAX_DIM = 1024


def validate_png(data: bytes) -> None:
    if len(data) < 29 or data[12:16] != b"IHDR":
        raise ValueError("PNG file is missing a valid IHDR chunk")
    chunk_len = struct.unpack(">I", data[8:12])[0]
    if chunk_len < 13:
        raise ValueError("PNG file has a truncated IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"PNG dimensions {width}x{height} exceed {MAX_DIM}px")


def validate_jpeg(data: bytes) -> None:
    pos = 2
    total = len(data)
    while pos < total:
        if data[pos] != 0xFF:
            pos += 1
            continue
        while pos < total and data[pos] == 0xFF:
            pos += 1
        if pos >= total:
            break
        marker = data[pos]
        pos += 1
        if marker in (0x00, 0x01, 0xD8) or 0xD0 <= marker <= 0xD7:
            continue
        if marker in (0xD9, 0xDA) or pos + 2 > total:
            break
        seg_len = struct.unpack(">H", data[pos : pos + 2])[0]
        if seg_len < 2 or pos + seg_len > total:
            break
        if marker in (0xC0, 0xC1, 0xC2):
            if seg_len < 7:
                break
            height, width = struct.unpack(">HH", data[pos + 3 : pos + 7])
            if width > MAX_DIM or height > MAX_DIM:
                raise ValueError(f"JPEG dimensions {width}x{height} exceed {MAX_DIM}px")
            return
        pos += seg_len
    raise ValueError("JPEG file has no SOF0, SOF1, or SOF2 frame")


def load_and_validate(src: Path) -> bytes:
    if not src.is_file():
        raise FileNotFoundError(f"Bundled image not found: {src}")
    data = src.read_bytes()
    size = len(data)
    if size == 0:
        raise ValueError("Bundled image is empty")
    if size < MIN_BYTES:
        raise ValueError(f"Bundled image is {size} bytes, below minimum {MIN_BYTES}")
    if size > MAX_BYTES:
        raise ValueError(f"Bundled image is {size} bytes, above maximum {MAX_BYTES}")
    if data.startswith(PNG_SIG):
        validate_png(data)
    elif data.startswith(JPEG_START) and data.endswith(JPEG_END):
        validate_jpeg(data)
    else:
        raise ValueError("Bundled image is neither a valid PNG nor a JPEG")
    return data


def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    payload = load_and_validate(src)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    dest.write_bytes(payload)
    print(f"Copied {len(payload)} bytes to {dest}")


if __name__ == "__main__":
    main()
