#!/usr/bin/env python3
"""Widen an outfit's footwear until it covers the base body's leg.

The base bodies have bare legs and feet; an outfit's boots are drawn over them.
Nine of the ten registered outfits have footwear narrower than the leg it covers
— by 7 to 17 px a side — so a strip of bare skin shows along the outer edge of
every boot. It is small per row and unmistakable once seen, and it is present on
every token those outfits appear in.

The cause is proportional rather than positional. Outfits 001–005 were rig-refit
at scales of 0.756–0.929 and 006–010 were normalized to widths of 390–447 px; in
both cases the garment was sized by its torso fit, and the footwear came along at
whatever width that implied. `outfit_001` happens to be wider than the leg at
every row and shows nothing, which is what the correct case looks like.

## What this does

For each row below `--from-y`, it finds every strip of leg the garment leaves
exposed and stretches the garment run beside it across the strip. Resampling
rather than smearing matters: repeating the edge column drags whatever is at the
boot's rim into horizontal stripes, which is glaring on a laced sandal or a
patterned boot. Resampling stretches the run's own pixels, so a 10-15 px
correction on a ~110 px boot reads as the boot simply being that width.

It is bounded on every axis. It only ever fills a strip the base body already
occupies, never one wider than `--max-px`, never a row where the garment already
covers the leg, and never anything outside the silhouette. An outfit that already
fits is untouched.

This is a repair, not a production method. The clean fix is footwear drawn to the
leg it covers, and every use must be recorded in the manifest's `postprocessing`.

    python scripts/fit_boots_to_legs.py --all --in-place
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
COMPATIBILITY = ROOT / "config" / "compatibility.json"
FOOT_BASELINE = 1139
DEFAULT_FROM_Y = 900
DEFAULT_MAX_PX = 28
OPAQUE = 128


def outfit_base_pairs(compatibility: Path = COMPATIBILITY) -> dict[str, str]:
    rules = json.loads(compatibility.read_text())
    return {
        rule["trait"]: rule["requires"]
        for rule in rules.get("requires", [])
        if rule.get("trait", "").startswith("outfit_") and rule.get("requires", "").startswith("base_")
    }


def runs_of(mask: np.ndarray) -> list[tuple[int, int]]:
    index = np.nonzero(mask)[0]
    if index.size == 0:
        return []
    runs, start, previous = [], index[0], index[0]
    for value in index[1:]:
        if value > previous + 1:
            runs.append((start, previous))
            start = value
        previous = value
    runs.append((start, previous))
    return runs


def widen(outfit: Image.Image, base: Image.Image, from_y: int = DEFAULT_FROM_Y,
          max_px: int = DEFAULT_MAX_PX) -> tuple[Image.Image, dict]:
    """Close each strip of exposed leg by stretching the garment beside it.

    Working from the exposed strips rather than from the garment's outer edge
    matters on an outfit with more than one element in a row. `outfit_009`'s
    cape is the outermost run at boot height and already reaches past the leg,
    so a rule that only extends the outermost run leaves the boot's own gap -
    an interior one - untouched.
    """
    source = np.array(outfit.convert("RGBA"))
    result = source.copy()
    body = np.asarray(base.convert("RGBA"))[..., 3] > OPAQUE

    rows, added = 0, 0
    for y in range(from_y, FOOT_BASELINE + 1):
        covered = source[y, :, 3] > OPAQUE
        leg = body[y]
        if not leg.any() or not covered.any():
            continue
        garment = runs_of(covered)
        touched = False
        for gap_start, gap_end in runs_of(leg & ~covered):
            gap = gap_end - gap_start + 1
            if gap > max_px:
                continue
            # the garment runs immediately either side of this strip
            left = next((r for r in reversed(garment) if r[1] == gap_start - 1), None)
            right = next((r for r in garment if r[0] == gap_end + 1), None)
            if left is None and right is None:
                continue
            # stretch whichever neighbour has more pixels to stretch
            if right is None or (left is not None and (left[1] - left[0]) >= (right[1] - right[0])):
                start, end = left
                new_start, new_end = start, gap_end
            else:
                start, end = right
                new_start, new_end = gap_start, end

            run = source[y, start:end + 1, :].astype(np.float32)
            width = new_end - new_start + 1
            positions = np.linspace(0, run.shape[0] - 1, width)
            low = np.floor(positions).astype(int)
            high = np.minimum(low + 1, run.shape[0] - 1)
            blend = (positions - low)[:, None]
            stretched = run[low] * (1 - blend) + run[high] * blend
            result[y, new_start:new_end + 1, :] = np.clip(stretched, 0, 255).astype(np.uint8)
            added += gap
            touched = True
        rows += int(touched)

    return Image.fromarray(result, "RGBA"), {"rows": rows, "pixels_added": added}


def exposed_leg_pixels(outfit: Image.Image, base: Image.Image, from_y: int = 1000) -> int:
    """Bare base-body skin still visible below `from_y` once the outfit is on."""
    body = np.asarray(base.convert("RGBA")).astype(int)
    garment = np.asarray(outfit.convert("RGBA"))[..., 3]
    red, green, blue = body[..., 0], body[..., 1], body[..., 2]
    skin = (red > 200) & (green > 140) & (blue > 100) & ((red - blue) > 25) & ((red - green) > 8)
    visible = (body[..., 3] > OPAQUE) & (garment <= OPAQUE) & skin
    return int(visible[from_y:FOOT_BASELINE + 1].sum())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--all", action="store_true", help="process every outfit bound to a base")
    parser.add_argument("--outfit", type=Path)
    parser.add_argument("--base", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--from-y", type=int, default=DEFAULT_FROM_Y)
    parser.add_argument("--max-px", type=int, default=DEFAULT_MAX_PX)
    args = parser.parse_args(argv)

    if args.all:
        pairs = [
            (ROOT / "assets" / "outfits" / outfit, ROOT / "assets" / "base_bodies" / base)
            for outfit, base in outfit_base_pairs().items()
        ]
    elif args.outfit and args.base:
        pairs = [(args.outfit, args.base)]
    else:
        print("error: pass --all, or both --outfit and --base")
        return 1
    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir")
        return 1

    for outfit_path, base_path in sorted(pairs):
        outfit = Image.open(outfit_path).convert("RGBA")
        base = Image.open(base_path).convert("RGBA")
        before = exposed_leg_pixels(outfit, base)
        fixed, report = widen(outfit, base, args.from_y, args.max_px)
        after = exposed_leg_pixels(fixed, base)
        if report["pixels_added"] == 0:
            print(f"{outfit_path.name}: already covers the leg ({before} px exposed)")
            continue
        destination = outfit_path if args.in_place else args.out_dir / outfit_path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        fixed.save(destination)
        print(f"{outfit_path.name}: exposed {before} -> {after}"
              f"  ({report['pixels_added']} px added across {report['rows']} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
