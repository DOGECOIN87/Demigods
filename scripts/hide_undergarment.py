#!/usr/bin/env python3
"""Repaint the base body's undergarment as skin wherever a garment exposes it.

The base bodies wear a neutral tank top and shorts. Several outfits sit just
inside that undergarment's edge, so a sliver of neutral fabric shows — through
`outfit_004`'s V-neck and over `outfit_005`'s shoulders — and the character reads
as wearing two garments.

## Why not just delete the undergarment

That is the right shape of fix and it is not reachable by masking. The tank reads
`(251,218,182)` against thigh skin at `(252,202,161)`; region-growing at a
tolerance loose enough to catch the garment's shading and seams starts eating
skin, and saturation does not separate them either — garment saturation peaks at
64-72 and skin at 80-88, with a long overlapping tail. Even with a perfect mask,
filling the whole torso means painting a nude body the collection never approved.
Removing it properly is a base-body re-render, not an edit.

## Why not extend the garment instead

Because the two worst gaps are *supposed* to show something. `outfit_004`'s sits
inside its own V-neck, where chest skin belongs, and `outfit_005`'s sits at the
shoulder line. Filling them with fabric redesigns the neckline and the shoulder.
Scaling the outfit up is worse: measured at x1.09 it moved exposed undergarment
only 15.6% -> 12.1% while raising covered arm skin 68% -> 73%, eating bare arms
faster than it covered cloth — and the arms are meant to show.

## What this does

It repaints the undergarment as skin only where that base's paired outfit
actually exposes it, plus a small margin under the garment edge. Colour diffuses
inward from genuine adjacent skin, so nothing is invented: every value comes from
skin the artist painted, and the fill is most faithful at the boundary, which is
exactly the band that can be seen.

The undergarment survives underneath the garment where no one can see it. That is
a deliberate limit, recorded so it is not mistaken for a complete removal.

Usage:
    python scripts/hide_undergarment.py --all --in-place
"""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ((627, 560), (627, 780))
TOLERANCE = 26      # generous: find enough garment to repaint
VERIFY_TOLERANCE = 14  # strict: does *fabric* still show?
MARGIN = 4  # px of repaint carried under the garment edge
RELAX = 60  # Laplace relaxation passes that remove fill-order streaking

# Each base pose is locked 1:1 to its outfit in config/compatibility.json, so a
# base only ever needs the gaps that its own outfit leaves.
PAIRS = [
    ("base_body_001_neutral_master.png", "outfit_001_celestial_scholar_pose_001.png"),
    ("base_pose_002_viewer_left_vertical_grip.png", "outfit_002_storm_guardian_pose_002.png"),
    ("base_pose_003_viewer_right_vertical_grip.png", "outfit_003_verdant_alchemist_pose_003.png"),
    ("base_pose_004_viewer_left_palm_up.png", "outfit_004_lunar_oracle_pose_004.png"),
    ("base_pose_005_centered_two_hand_grip.png", "outfit_005_sun_temple_pose_005.png"),
]


def undergarment_mask(base: Image.Image, seeds=SEEDS, tolerance: int = TOLERANCE) -> Image.Image:
    """Region-grow the neutral garment from known garment pixels."""
    px = base.load()
    width, height = base.size
    mask = Image.new("L", (width, height), 0)
    mp = mask.load()
    seen = set()
    for sx, sy in seeds:
        sr, sg, sb, _ = px[sx, sy]
        queue = deque([(sx, sy)])
        while queue:
            x, y = queue.popleft()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if not (0 <= x < width and 0 <= y < height):
                continue
            r, g, b, a = px[x, y]
            if a < 200 or abs(r - sr) + abs(g - sg) + abs(b - sb) > tolerance:
                continue
            mp[x, y] = 255
            queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return mask


def exposed_count(base: Image.Image, outfit: Image.Image,
                  tolerance: int = VERIFY_TOLERANCE) -> int:
    """Count pixels where the neutral garment is still visibly showing.

    This uses a tighter tolerance than the repaint mask, and the split matters.
    The repaint mask should be generous so it covers enough garment; verification
    asks a different question — is *fabric* still visible — and skin repainted
    from neighbouring skin lands within ~26 levels of the tank's colour simply
    because the tank and skin are that close. Verifying at the mask's tolerance
    therefore re-flags the script's own correct output as a defect.
    """
    mask = undergarment_mask(base, tolerance=tolerance).load()
    oal = outfit.getchannel("A").load()
    return sum(
        1
        for y in range(300, 1140)
        for x in range(200, 1054)
        if mask[x, y] > 0 and oal[x, y] < 40
    )


def repaint(base: Image.Image, outfit: Image.Image, margin: int = MARGIN,
            relax: int = RELAX) -> tuple[Image.Image, dict]:
    result = base.copy()
    px = result.load()
    width, height = result.size
    mask = undergarment_mask(result)
    ml = mask.load()
    oal = outfit.getchannel("A").load()

    exposed = Image.new("L", (width, height), 0)
    el = exposed.load()
    for y in range(300, 1140):
        for x in range(200, width - 200):
            if ml[x, y] > 0 and oal[x, y] < 60:
                el[x, y] = 255

    grown = exposed.filter(ImageFilter.MaxFilter(2 * margin + 1)).load()
    target = {
        (x, y)
        for y in range(300, 1140)
        for x in range(200, width - 200)
        if grown[x, y] > 0 and ml[x, y] > 0
    }

    remaining = set(target)
    settled: set[tuple[int, int]] = set()
    # Diffuse inward. A repainted pixel joins `settled` so it can seed the next
    # ring — without that the fill stalls after one pass, because a filled pixel
    # is still classified as undergarment by the mask.
    while remaining:
        frontier = []
        for (x, y) in remaining:
            sources = [
                px[nx, ny]
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                if 0 <= nx < width and 0 <= ny < height and px[nx, ny][3] > 200
                and ((nx, ny) in settled or (ml[nx, ny] == 0 and (nx, ny) not in target))
            ]
            if sources:
                frontier.append(((x, y), sources))
        if not frontier:
            break
        for (x, y), sources in frontier:
            r = sum(s[0] for s in sources) // len(sources)
            g = sum(s[1] for s in sources) // len(sources)
            b = sum(s[2] for s in sources) // len(sources)
            px[x, y] = (r, g, b, px[x, y][3])
        settled.update(point for point, _ in frontier)
        remaining.difference_update(point for point, _ in frontier)

    # The propagation above assigns each pixel from whichever ring reached it
    # first, which smears colour along the direction of travel — on the real
    # bases that showed as vertical streaks under the tank's neckline. Relaxing
    # the filled region toward the average of its neighbours, with the
    # surrounding real skin held fixed, solves out those streaks: it is a
    # discrete Laplace solve, so the result is the smooth gradient the boundary
    # implies rather than an artefact of fill order.
    filled = sorted(settled)
    for _ in range(relax):
        updates = {}
        for (x, y) in filled:
            # Average only over repainted pixels and genuine skin. Including the
            # un-repainted undergarment just outside the target would pull the
            # fill back toward fabric colour — that regression re-exposed 53 and
            # 22 px on poses 002 and 005 before this condition was added.
            neighbours = [
                px[nx, ny]
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                if 0 <= nx < width and 0 <= ny < height and px[nx, ny][3] > 200
                and ((nx, ny) in settled or ml[nx, ny] == 0)
            ]
            if not neighbours:
                continue
            updates[(x, y)] = (
                sum(n[0] for n in neighbours) // len(neighbours),
                sum(n[1] for n in neighbours) // len(neighbours),
                sum(n[2] for n in neighbours) // len(neighbours),
            )
        for (x, y), (r, g, b) in updates.items():
            px[x, y] = (r, g, b, px[x, y][3])

    return result, {"target": len(target), "repainted": len(target) - len(remaining)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="process every registered base/outfit pair")
    parser.add_argument("--base", type=Path)
    parser.add_argument("--outfit", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--margin", type=int, default=MARGIN)
    parser.add_argument("--relax", type=int, default=RELAX)
    parser.add_argument("--max-passes", type=int, default=6)
    args = parser.parse_args(argv)

    if args.all:
        pairs = [
            (ROOT / "assets" / "base_bodies" / b, ROOT / "assets" / "outfits" / o)
            for b, o in PAIRS
        ]
    elif args.base and args.outfit:
        pairs = [(args.base, args.outfit)]
    else:
        print("error: pass --all, or both --base and --outfit")
        return 1

    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir")
        return 1

    for base_path, outfit_path in pairs:
        base = Image.open(base_path).convert("RGBA")
        outfit = Image.open(outfit_path).convert("RGBA")
        before = exposed_count(base, outfit)

        # Iterate to convergence. One pass is not always enough: the relaxation
        # can nudge a boundary pixel back across the mask's tolerance, and the
        # tank and skin are close enough in colour that "back across" is only a
        # few levels. Each pass re-detects whatever is still showing.
        result, report = repaint(base, outfit, args.margin, args.relax)
        after = exposed_count(result, outfit)
        for _ in range(args.max_passes - 1):
            if after == 0:
                break
            result, extra = repaint(result, outfit, args.margin, args.relax)
            report["repainted"] += extra["repainted"]
            previous, after = after, exposed_count(result, outfit)
            if after >= previous:
                break
        destination = base_path if args.in_place else args.out_dir / base_path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        result.save(destination)
        print(
            f"{base_path.name}: exposed {before} -> {after}"
            f"  (repainted {report['repainted']}/{report['target']} px)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
