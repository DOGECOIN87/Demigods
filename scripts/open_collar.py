#!/usr/bin/env python3
"""Open a sealed standing collar so the neck beneath reads through it.

`outfit_002` and `outfit_003` were painted with closed collars. In 002 the
opening is filled with the collar's own dark interior; in 003 a duller neck is
painted into the garment itself. Either way the base body's neck never showed and
the head read as sitting on a tube.

The cut has two properties, and both were arrived at by rejecting the
alternative.

**The boundary comes from the artwork, not from geometry I invent.** The collar
rim lies outside the neck's silhouette and the interior lies inside it, so the
base body's own anti-aliased neck alpha separates them exactly. Earlier attempts
that invented a boundary — a feathered hole, a colour region-grow, a fixed
column — produced mushy edges, ate the rim (rim and interior are both dark), or
left hard vertical edges where the column crossed the widening silhouette.

**The bottom edge is crisp, not faded.** A first working version crossfaded the
removal out over ~18 rows. It passed every measurement and looked wrong: skin and
dark interior blended into a muddy translucent smear, because a garment edge is a
hard line and a gradient does not read as fabric. The cut now ends on the
collar's own front rim, traced from the image as a shallow arc, with sub-pixel
accuracy from a fractional final row.

Rim parameters are per-garment because collars differ; trace them by finding the
row where the interior gives way to the garment's front face:

    outfit_002  rim_centre 502  rim_rise 12  half 32   (dark interior -> teal placket)
    outfit_003  rim_centre 520  rim_rise 27  half 30   (painted neck  -> white shirt)

Usage:
    python scripts/open_collar.py OUTFIT BASE --in-place \\
        --rim-centre 502 --rim-rise 12 --half 32
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

CENTER_X = 627
TOP = 472          # first row above the collar; nothing above this is touched
WALL_SOFTEN = 1.5  # px of horizontal falloff at the opening's walls


def open_collar(outfit: Image.Image, base: Image.Image, *, rim_centre: float,
                rim_rise: float, half: float, center_x: int = CENTER_X,
                top: int = TOP) -> tuple[Image.Image, int]:
    """Clear the collar interior above the rim arc. Returns (image, px cleared)."""
    out = outfit.copy()
    alpha = out.getchannel("A")
    oal = alpha.load()
    bal = base.getchannel("A").load()
    width, height = out.size
    cleared = 0

    for x in range(max(0, int(center_x - half) - 2), min(width, int(center_x + half) + 3)):
        distance = abs(x - center_x)
        if distance > half + 2:
            continue
        if distance <= half - WALL_SOFTEN:
            side = 1.0
        else:
            side = max(0.0, 1.0 - (distance - (half - WALL_SOFTEN)) / (WALL_SOFTEN + 2.0))
        if side <= 0.0:
            continue

        rim = rim_centre - rim_rise * ((x - center_x) / half) ** 2
        rim_row = int(rim)
        for y in range(top, min(rim_row + 1, height)):
            # Full removal above the rim; the final row takes the fractional
            # remainder so the edge lands with sub-pixel accuracy.
            fraction = 1.0 if y < rim_row else (rim - rim_row)
            mask = (bal[x, y] / 255.0) * side * fraction
            if mask <= 0.0:
                continue
            before = oal[x, y]
            oal[x, y] = max(0, min(255, round(before * (1.0 - mask))))
            if oal[x, y] != before:
                cleared += 1

    out.putalpha(alpha)
    return out, cleared


def neck_visibility(outfit: Image.Image, base: Image.Image,
                    jaw: int = 457, shoulder: int = 569) -> float:
    """Share of the base body's neck band left visible by the garment."""
    bal = base.getchannel("A").load()
    oal = outfit.getchannel("A").load()
    total = visible = 0
    for y in range(jaw, shoulder):
        for x in range(560, 700):
            if bal[x, y] > 200:
                total += 1
                if oal[x, y] < 40:
                    visible += 1
    return 100.0 * visible / max(total, 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outfit", type=Path)
    parser.add_argument("base", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--rim-centre", type=float, required=True,
                        help="rim row at the centre column")
    parser.add_argument("--rim-rise", type=float, required=True,
                        help="how far the rim rises toward the opening's edges")
    parser.add_argument("--half", type=float, required=True,
                        help="half-width of the opening in px")
    args = parser.parse_args(argv)

    outfit = Image.open(args.outfit).convert("RGBA")
    base = Image.open(args.base).convert("RGBA")
    before = neck_visibility(outfit, base)
    result, cleared = open_collar(
        outfit, base, rim_centre=args.rim_centre,
        rim_rise=args.rim_rise, half=args.half,
    )
    after = neck_visibility(result, base)

    destination = args.outfit if args.in_place else args.out
    if destination is None:
        print("error: pass --out or --in-place")
        return 1
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.save(destination)
    print(f"{args.outfit.name}: cleared {cleared} px")
    print(f"  neck visibility {before:.1f}% -> {after:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
