#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Copies the front-page image drawn for Thursday 19 November 2026 into
/output/entry.png, verifying it on the way. Pure Python 3.13 stdlib:
shutil, hashlib, os, struct, zlib. Deterministic: same input bytes give
the same output bytes on every run.
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photo.jpg")
DST = "/output/entry.png"

MAX_BYTES = 1 * 1024 * 1024
MAX_DIM = 1024


def png_dimensions(data):
    """Read width/height from a PNG header; raise on bad magic."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("photo.jpg is not a PNG image")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    width, height = png_dimensions(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("image %dx%d exceeds %d" % (width, height, MAX_DIM))
    if len(data) > MAX_BYTES:
        raise ValueError("image %d bytes exceeds 1 MiB" % len(data))
    sha = hashlib.sha256(data).hexdigest()
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "wb") as f:
        f.write(data)
    # Self-check: read the written file back and prove it is byte-identical
    # and a structurally valid PNG (all chunk CRCs + IDAT decompress).
    with open(DST, "rb") as f:
        back = f.read()
    if hashlib.sha256(back).hexdigest() != sha:
        raise ValueError("round-trip sha256 mismatch")
    pos = 8
    idat = bytearray()
    while pos < len(back):
        ln, tag = struct.unpack(">I4s", back[pos:pos + 8])
        chunk_data = back[pos + 8:pos + 8 + ln]
        crc_stored, = struct.unpack(">I", back[pos + 8 + ln:pos + 12 + ln])
        if zlib.crc32(tag + chunk_data) & 0xffffffff != crc_stored:
            raise ValueError("bad CRC in %s chunk" % tag.decode())
        if tag == b"IDAT":
            idat += chunk_data
        pos += 12 + ln
    raw = zlib.decompress(bytes(idat))
    if len(raw) != height * (1 + width * 3):
        raise ValueError("IDAT payload size mismatch")
    print("entry.png: %dx%d, %d bytes, sha256 %s" % (width, height, len(data), sha))


if __name__ == "__main__":
    main()
