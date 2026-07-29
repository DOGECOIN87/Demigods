#!/usr/bin/env python3
"""Validate the legendary 1-of-1 pieces.

Every other gate in this repository assumes a modular layer. `--trait` and
`--floor-aura` check a silhouette inside a transparent canvas; `--global-finish`
checks a peak-alpha ceiling. A legendary is a complete flattened illustration —
opaque, full-bleed, character and environment painted together — so all three
fail it by design, and `validate_assets.py` skips the folder entirely because
`legendary` is not a trait category.

That leaves them unchecked, which is the gap this closes. The properties that
actually matter for a 1-of-1:

* native 1254 x 1254, never upscaled to reach it;
* fully opaque with no transparent pixel anywhere — a stray transparent corner
  means the generator keyed a background it should have painted;
* decodes completely, so a truncated upload cannot register;
* distinct from every other piece, since "1 of 1" is the entire premise and a
  duplicate digest silently destroys it.

Two things stay human checks and are deliberately not faked here: that no text,
signature or watermark appears in frame, and that the piece's required 1-of-1
element is actually present. Neither is decidable from pixel statistics, and a
green check that does not mean anything is worse than no check.

Usage:
    python scripts/validate_legendary.py
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LEGENDARY_DIR = ROOT / "assets" / "legendary"
CANVAS = (1254, 1254)
EXPECTED_COUNT = 7


def check(path: Path) -> tuple[list[tuple[str, bool, str]], str]:
    checks: list[tuple[str, bool, str]] = []
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        with Image.open(path) as image:
            image.load()  # full decode; a truncated upload raises here
            size, mode, fmt = image.size, image.mode, image.format
            alpha = image.convert("RGBA").getchannel("A").getextrema()
    except Exception as exc:  # noqa: BLE001 - report any decode failure verbatim
        return [("decode", False, f"{type(exc).__name__}: {exc}")], digest

    checks.append(("decode", True, "full decode ok"))
    checks.append(("format", fmt == "PNG", str(fmt)))
    checks.append(("dimensions", size == CANVAS, f"{size[0]}x{size[1]}"))
    checks.append(("fully_opaque", alpha[0] == 255, f"alpha_min={alpha[0]}"))
    checks.append(("mode", mode in ("RGB", "RGBA"), mode))
    return checks, digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=LEGENDARY_DIR)
    parser.add_argument("--expect", type=int, default=EXPECTED_COUNT)
    args = parser.parse_args(argv)

    if not args.dir.is_dir():
        print(f"error: {args.dir} is not a directory", file=sys.stderr)
        return 1

    pieces = sorted(args.dir.glob("*.png"))
    failures = 0
    digests: dict[str, str] = {}

    for path in pieces:
        checks, digest = check(path)
        bad = [c for c in checks if not c[1]]
        mark = "PASS" if not bad else "FAIL"
        print(f"[{mark}] {path.name}  sha {digest[:12]}…")
        for name, ok, value in checks:
            if not ok:
                print(f"         {name}: {value}")
        failures += bool(bad)
        digests.setdefault(digest, path.name)
        if digests[digest] != path.name:
            print(f"         duplicate of {digests[digest]} — a 1-of-1 cannot repeat")
            failures += 1

    print()
    if len(digests) != len(pieces):
        print(f"FAIL duplicate artwork: {len(pieces)} files, {len(digests)} distinct digests")
        failures += 1
    if args.expect and len(pieces) != args.expect:
        print(f"FAIL expected {args.expect} pieces, found {len(pieces)}")
        failures += 1

    print(f"{len(pieces) - failures}/{len(pieces)} legendary piece(s) passed automated checks.")
    print(
        "Still requires a human pass: no text/signature/watermark in frame, and the "
        "piece's required 1-of-1 element present."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
