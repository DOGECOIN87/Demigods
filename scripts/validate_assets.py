#!/usr/bin/env python3
"""Validate dimensions, alpha, naming, and visible bounds for modular PNG assets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.(?:png|jpg|jpeg)$")
TRANSPARENT_CATEGORIES = {
    "base", "hair", "eyes", "eyebrows", "mouth", "expression", "outfit",
    "head", "neck", "hand", "back", "aura"
}


def validate_file(path: Path, width: int, height: int) -> list[str]:
    errors: list[str] = []
    if not NAME_PATTERN.match(path.name):
        errors.append("filename is not lowercase snake_case")

    try:
        with Image.open(path) as image:
            if image.size != (width, height):
                errors.append(f"size is {image.size}, expected {(width, height)}")

            category = path.name.split("_", 1)[0]
            if path.suffix.lower() == ".png" and category in TRANSPARENT_CATEGORIES:
                if "A" not in image.getbands():
                    errors.append("missing alpha channel")
                else:
                    alpha = image.getchannel("A")
                    extrema = alpha.getextrema()
                    if extrema == (255, 255):
                        errors.append("alpha channel is fully opaque")
                    bbox = alpha.getbbox()
                    if bbox is None:
                        errors.append("asset is fully transparent")
                    elif bbox[0] == 0 or bbox[1] == 0 or bbox[2] == width or bbox[3] == height:
                        errors.append(f"visible pixels touch a canvas edge: bbox={bbox}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"could not read image: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--width", type=int, default=2048)
    parser.add_argument("--height", type=int, default=2048)
    args = parser.parse_args()

    files = sorted(p for p in args.directory.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    failed = 0
    for path in files:
        errors = validate_file(path, args.width, args.height)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    print(f"\nChecked {len(files)} file(s); {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
