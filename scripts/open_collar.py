#!/usr/bin/env python3
"""Open a sealed standing collar so the neck beneath reads through it.

`outfit_002`'s collar was painted as a closed cone: the opening is opaque, so the
base body's fully-rendered neck never showed and the head read as sitting on a
tube rather than joining a body.

Four earlier approaches were tried and rejected, and the reason they failed is
the reason this one works. A geometric hole cut (feathered or crisp) and a
colour region-grow each **invent their own boundary**, so they produce hard box
edges, chewed corners, or eat the collar rim — rim and interior are both dark, so
colour cannot separate them.

The boundary already exists in the artwork. The collar rim lies OUTSIDE the
neck's silhouette and the painted interior lies INSIDE it, so the base body's
neck alpha separates them exactly:

    new_outfit_alpha = outfit_alpha * (1 - neck_mask)

Because that alpha is anti-aliased, the resulting edge is too — no feathering
required, and nothing invented.

Two shaping terms keep it reading as a garment rather than a hole:

* the opening narrows from `half_top` to `half_bottom` into a V, following the
  collar's own front line instead of a straight column, which is what removed
  the hard vertical edges of the column-based attempt;
* removal fades out over the lower part of the span, so the garment closes over
  the chest instead of ending on a horizontal cut.

Usage:
    python scripts/open_collar.py \\
        assets/outfits/outfit_002_storm_guardian_pose_002.png \\
        assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png \\
        --out out.png --top 474 --close-by 512 --half-top 33 --half-bottom 9
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CENTER_X = 627
WALL_SOFTEN = 3.0  # px of horizontal falloff at the V walls


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def open_collar(outfit: Image.Image, base: Image.Image, *, top: int, close_by: int,
                half_top: float, half_bottom: float, center_x: int = CENTER_X,
                fade_from: float = 0.55) -> tuple[Image.Image, int]:
    """Subtract the neck from the collar interior. Returns (image, px cleared)."""
    out = outfit.copy()
    alpha = out.getchannel("A")
    oal = alpha.load()
    bal = base.getchannel("A").load()
    width, height = out.size
    cleared = 0

    for y in range(max(0, top), min(height, close_by + 1)):
        t = (y - top) / max(close_by - top, 1)
        half = half_top + (half_bottom - half_top) * t
        strength = 1.0 - smoothstep(max(0.0, (t - fade_from) / max(1.0 - fade_from, 1e-6)))
        if strength <= 0.0:
            continue
        for x in range(max(0, int(center_x - half) - 1), min(width, int(center_x + half) + 2)):
            distance = abs(x - center_x)
            if distance <= half - 2:
                wall = 1.0
            else:
                wall = max(0.0, 1.0 - (distance - (half - 2)) / WALL_SOFTEN)
            mask = (bal[x, y] / 255.0) * strength * wall
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
    parser.add_argument("--top", type=int, required=True)
    parser.add_argument("--close-by", type=int, required=True)
    parser.add_argument("--half-top", type=float, required=True)
    parser.add_argument("--half-bottom", type=float, required=True)
    args = parser.parse_args(argv)

    outfit = Image.open(args.outfit).convert("RGBA")
    base = Image.open(args.base).convert("RGBA")
    before = neck_visibility(outfit, base)
    result, cleared = open_collar(
        outfit, base, top=args.top, close_by=args.close_by,
        half_top=args.half_top, half_bottom=args.half_bottom,
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
