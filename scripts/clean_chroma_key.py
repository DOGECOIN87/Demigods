#!/usr/bin/env python3
"""Remove green-screen residue from chroma-keyed trait layers.

Four of the five registered outfits were extracted from a green backdrop and
carry its residue: 16-49% of their alpha-edge pixels read green, peaking at 202
levels of green excess. `outfit_001` is clean only because it received an
`alpha_edge_contract_1` pass that the others never did.

Two passes, in order:

1. **Alpha contract.** Erode the alpha by one pixel. Keyed edges blend backdrop
   into the outermost pixel, so dropping that pixel removes most of the fringe
   without touching interior artwork.

2. **Edge-band despill.** Clamp green to `max(R, B)` — but *only* within a few
   pixels of the alpha edge, where spill actually lives.

The band restriction is the whole safety argument, and it is not theoretical. An
unrestricted despill measurably damages real artwork: run against
`outfit_003_verdant_alchemist`, it desaturated the green potion bottles on the
character's bandolier, shifting 173 pixels by more than 20 levels. Confined to a
3px band the same outfit loses 38, and the potions are untouched. A despill that
cannot tell spill from a green object is not safe to run on green objects.

Colour is only ever reduced toward neighbouring channels; nothing is invented,
and a pixel whose green already sits at or below max(R, B) is left alone.

Usage:
    python scripts/clean_chroma_key.py assets/outfits/outfit_002_*.png --in-place
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CONTRACT = 1
DEFAULT_BAND = 3
GREEN_EXCESS = 25  # G above max(R,B) by more than this counts as contaminated


def green_pixels(image: Image.Image, threshold: int = GREEN_EXCESS) -> int:
    px = image.load()
    alpha = image.getchannel("A").load()
    count = 0
    for y in range(image.height):
        for x in range(image.width):
            if alpha[x, y] < 20:
                continue
            r, g, b, _ = px[x, y]
            if g - max(r, b) > threshold:
                count += 1
    return count


def edge_band(image: Image.Image, width: int) -> Image.Image:
    """Opaque pixels within `width` px of a transparent neighbour."""
    solid = image.getchannel("A").point(lambda v: 255 if v > 20 else 0)
    eroded = solid
    for _ in range(width):
        eroded = eroded.filter(ImageFilter.MinFilter(3))
    return ImageChops.subtract(solid, eroded)


def clean(image: Image.Image, contract: int = DEFAULT_CONTRACT,
          band: int = DEFAULT_BAND) -> tuple[Image.Image, dict]:
    before = green_pixels(image)

    alpha = image.getchannel("A")
    for _ in range(contract):
        alpha = alpha.filter(ImageFilter.MinFilter(3))
    result = image.copy()
    result.putalpha(alpha)

    mask = edge_band(result, band).load()
    px = result.load()
    despilled = 0
    for y in range(result.height):
        for x in range(result.width):
            if mask[x, y] == 0:
                continue
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            cap = max(r, b)
            if g > cap:
                px[x, y] = (r, cap, b, a)
                despilled += 1

    source = image.load()
    shifted = sum(
        1
        for y in range(image.height)
        for x in range(image.width)
        if abs(source[x, y][1] - px[x, y][1]) > 20
    )
    after = green_pixels(result)
    return result, {
        "green_before": before,
        "green_after": after,
        "despilled_px": despilled,
        "artwork_shifts_over_20_levels": shifted,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--contract", type=int, default=DEFAULT_CONTRACT)
    parser.add_argument("--band", type=int, default=DEFAULT_BAND)
    parser.add_argument("--backup-dir", type=Path)
    args = parser.parse_args(argv)

    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir", file=sys.stderr)
        return 1

    for source in args.sources:
        image = Image.open(source).convert("RGBA")
        result, report = clean(image, args.contract, args.band)
        if args.backup_dir:
            args.backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, args.backup_dir / source.name)
        destination = source if args.in_place else args.out_dir / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        result.save(destination)
        print(
            f"{source.name}: green {report['green_before']} -> {report['green_after']}"
            f"  despilled {report['despilled_px']}"
            f"  artwork shifts>20 {report['artwork_shifts_over_20_levels']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
