#!/usr/bin/env python3
"""Clip a trait layer's overhang back to the locked maximum character bounds.

Some layers overhang a locked bound by a few pixels of genuine geometry rather
than by stray dust. `outfit_001` is the worked example: its boot soles are drawn
with a rounded bottom taper that runs five pixels past the foot baseline, so the
character reads as standing slightly *through* the floor a background establishes
at Y 1139.

Two fixes exist for that, and the wrong one is tempting:

  - Rescaling the layer (`refit_trait_layer.py`) pulls the bottom up, but it
    shrinks the boots relative to the shared body underneath. For outfit_001 that
    exposed the base body's bare toes below both soles — trading a five-pixel
    bounds breach for visible skin, which is worse.
  - Clipping the overhang leaves the garment at its drawn size, so it still
    covers the body completely, and terminates the sole exactly on the ground
    plane. A sole resting on a floor *is* flat at the floor line.

Clipping is therefore right when the overhang is a soft taper meeting a ground
plane, and wrong when it would amputate real silhouette. The guardrails below
enforce that distinction rather than trusting the caller: the script refuses to
run when the overhang is deep or when it would remove a meaningful share of the
layer, because either signals a misplaced layer that needs a re-render.

Usage:
    python scripts/clip_trait_to_bounds.py assets/outfits/outfit_001_...png --in-place
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
MAX_BOUNDS = (233, 129, 1021, 1139)  # inclusive [x_min, y_min, x_max, y_max]

# An overhang deeper than this is not a taper meeting the ground; it is a layer
# drawn at the wrong scale or position, and clipping would amputate silhouette.
MAX_OVERHANG_PX = 12
# Likewise, a clip that removes a meaningful share of the visible layer is
# removing artwork rather than a soft edge.
MAX_REMOVED_SHARE = 0.01


def visible_box(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("layer is fully transparent")
    return bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1


def visible_pixels(image: Image.Image) -> int:
    """Count of pixels with any opacity, via the alpha histogram."""
    histogram = image.getchannel("A").histogram()
    return sum(histogram[1:])


def clip(image: Image.Image, bounds: tuple[int, int, int, int] = MAX_BOUNDS) -> tuple[Image.Image, dict]:
    """Zero every pixel outside `bounds`, refusing when that removes real artwork."""
    if image.size != (CANVAS, CANVAS):
        raise ValueError(f"layer must be {CANVAS} x {CANVAS}; got {image.size}")

    left, top, right, bottom = visible_box(image)
    x_min, y_min, x_max, y_max = bounds
    overhang = {
        "left": max(0, x_min - left),
        "top": max(0, y_min - top),
        "right": max(0, right - x_max),
        "bottom": max(0, bottom - y_max),
    }
    deepest = max(overhang.values())
    if deepest == 0:
        raise ValueError("layer is already within bounds; nothing to clip")
    if deepest > MAX_OVERHANG_PX:
        raise ValueError(
            f"overhang of {deepest}px exceeds the {MAX_OVERHANG_PX}px ceiling "
            f"({overhang}); this layer needs a re-render or a refit, not a clip"
        )

    before = visible_pixels(image)
    alpha = image.getchannel("A")
    pixels = alpha.load()
    for y in range(CANVAS):
        outside_row = y < y_min or y > y_max
        for x in range(CANVAS):
            if outside_row or x < x_min or x > x_max:
                pixels[x, y] = 0

    result = image.copy()
    result.putalpha(alpha)
    after = visible_pixels(result)
    removed = before - after
    share = removed / before if before else 0.0
    if share > MAX_REMOVED_SHARE:
        raise ValueError(
            f"clipping would remove {share:.2%} of the visible layer "
            f"({removed} px), above the {MAX_REMOVED_SHARE:.0%} ceiling; "
            "this is artwork, not a soft edge"
        )

    return result, {
        "overhang": overhang,
        "removed_pixels": removed,
        "removed_share": round(share, 6),
        "bounds_before": [left, top, right, bottom],
        "bounds_after": list(visible_box(result)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, help="output path (default: alongside, .clipped.png)")
    parser.add_argument("--in-place", action="store_true", help="overwrite the source file")
    parser.add_argument("--backup", type=Path, help="copy the original here before overwriting")
    args = parser.parse_args(argv)

    if args.in_place and args.out:
        print("error: use either --in-place or --out, not both", file=sys.stderr)
        return 1

    image = Image.open(args.source).convert("RGBA")
    try:
        result, report = clip(image)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    destination = args.source if args.in_place else (
        args.out or args.source.with_suffix(".clipped.png")
    )
    if args.backup:
        args.backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.source, args.backup)
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.save(destination)

    print(f"Wrote {destination}")
    print(f"  overhang        {report['overhang']}")
    print(f"  bounds  {report['bounds_before']} -> {report['bounds_after']}")
    print(f"  removed {report['removed_pixels']} px ({report['removed_share']:.4%} of the layer)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
