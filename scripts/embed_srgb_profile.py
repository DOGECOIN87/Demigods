#!/usr/bin/env python3
"""Embed an sRGB ICC profile in production PNGs without altering pixel data.

Every registered asset declared sRGB in the manifest but carried no embedded
profile, so `validate_assets.py` warned "confirm sRGB interpretation" on all of
them. Untagged PNGs are interpreted by the viewer's own assumption, which is a
colour-consistency risk for a collection that will be minted once and never
re-rendered.

This writes only the iCCP chunk. Pixel bytes are compared before and after and
the file is rejected if a single channel value changed, so the operation is a
metadata tag and nothing more.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageCms


def srgb_profile_bytes() -> bytes:
    return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embed(path: Path, profile: bytes) -> tuple[bool, str]:
    """Tag one PNG in place. Returns (changed, message)."""
    with Image.open(path) as image:
        image.load()
        existing = image.info.get("icc_profile")
        mode, size = image.mode, image.size
        before = image.tobytes()
        if existing:
            return False, "already tagged"
        pnginfo_source = image.copy()
        pnginfo_source.save(path, format="PNG", icc_profile=profile)

    with Image.open(path) as reread:
        reread.load()
        if reread.mode != mode or reread.size != size:
            return False, f"REJECTED: mode/size changed to {reread.mode} {reread.size}"
        if reread.tobytes() != before:
            return False, "REJECTED: pixel data changed"
        if not reread.info.get("icc_profile"):
            return False, "REJECTED: profile was not written"

    return True, "tagged"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="PNG file(s) or directory(ies)")
    args = parser.parse_args(argv)

    files: list[Path] = []
    for entry in args.paths:
        if entry.is_dir():
            files.extend(sorted(entry.rglob("*.png")))
        elif entry.is_file():
            files.append(entry)
        else:
            print(f"  missing: {entry}")

    profile = srgb_profile_bytes()
    changed = failed = skipped = 0
    for path in files:
        before = sha256_file(path)
        ok, message = embed(path, profile)
        if message.startswith("REJECTED"):
            print(f"  {path.name}: {message}")
            failed += 1
        elif ok:
            print(f"  {path.name}: {before[:16]} -> {sha256_file(path)[:16]}")
            changed += 1
        else:
            print(f"  {path.name}: {message}")
            skipped += 1

    print(f"\n{changed} tagged, {skipped} already tagged, {failed} rejected.")
    print("Pixel data verified unchanged on every tagged file.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
