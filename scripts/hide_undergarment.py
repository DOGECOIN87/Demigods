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
import json
from collections import deque
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ((627, 560), (627, 780))
TOLERANCE = 26      # generous: find enough garment to repaint
VERIFY_TOLERANCE = 14  # strict: does *fabric* still show?
MARGIN = 4  # px of repaint carried under the garment edge
# A gap wider and taller than this is a neckline the outfit means to leave open,
# not a fit error. outfit_007's chest V is 82 x 77 px and reads as a linen
# undershirt; outfit_009's shoulder slivers are 14 x 24 and read as a mistake.
# Repainting only the small gaps fixes the errors without redesigning a garment.
MAX_FIT_GAP = 40
RELAX = 60  # Laplace relaxation passes that remove fill-order streaking

COMPATIBILITY = ROOT / "config" / "compatibility.json"


def base_outfit_pairs(compatibility: Path = COMPATIBILITY) -> dict[str, list[str]]:
    """Read each base's outfits out of the locked compatibility rules.

    This was once a hardcoded list of five 1:1 pairs, which silently went stale
    the moment outfits 006-010 were registered against the neutral master: four
    of them expose the tank and none of them was in the list. Deriving the
    mapping means a newly bound outfit is covered the next time this runs.

    A base with several outfits needs the union of the gaps they leave. That is
    safe because a region one outfit exposes is hidden by any outfit that covers
    it, so repainting the union never shows through a garment.
    """
    rules = json.loads(compatibility.read_text())
    pairs: dict[str, list[str]] = {}
    for rule in rules.get("requires", []):
        trait, required = rule.get("trait", ""), rule.get("requires", "")
        if trait.startswith("outfit_") and required.startswith("base_"):
            pairs.setdefault(required, []).append(trait)
    return {base: sorted(outfits) for base, outfits in sorted(pairs.items())}


def cover_alpha(outfits: Image.Image | Iterable[Image.Image]) -> Image.Image:
    """The alpha a base is covered by: the minimum across every paired outfit."""
    if isinstance(outfits, Image.Image):
        return outfits.getchannel("A")
    channels = [outfit.getchannel("A") for outfit in outfits]
    if not channels:
        raise ValueError("at least one outfit is required")
    combined = channels[0]
    for channel in channels[1:]:
        combined = ImageChops.darker(combined, channel)
    return combined


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


def exposed_count(base: Image.Image, outfit: Image.Image | Iterable[Image.Image],
                  tolerance: int = VERIFY_TOLERANCE, max_gap: int | None = None) -> int:
    """Count pixels where the neutral garment is still visibly showing.

    This uses a tighter tolerance than the repaint mask, and the split matters.
    The repaint mask should be generous so it covers enough garment; verification
    asks a different question — is *fabric* still visible — and skin repainted
    from neighbouring skin lands within ~26 levels of the tank's colour simply
    because the tank and skin are that close. Verifying at the mask's tolerance
    therefore re-flags the script's own correct output as a defect.
    """
    garment = undergarment_mask(base, tolerance=tolerance)
    ml = garment.load()
    total = Image.new("L", base.size, 0)
    for single in ([outfit] if isinstance(outfit, Image.Image) else list(outfit)):
        sal = single.getchannel("A").load()
        layer_gap = Image.new("L", base.size, 0)
        lg = layer_gap.load()
        for y in range(300, 1140):
            for x in range(200, 1054):
                if ml[x, y] > 0 and sal[x, y] < 40:
                    lg[x, y] = 255
        if max_gap is not None:
            layer_gap = fit_gaps_only(layer_gap, max_gap, base=base, garment=garment)
        total = ImageChops.lighter(total, layer_gap)
    return sum(1 for value in total.tobytes() if value)


def fit_gaps_only(exposed: Image.Image, max_gap: int = MAX_FIT_GAP,
                  base: Image.Image | None = None,
                  garment: Image.Image | None = None) -> Image.Image:
    """Keep only the exposed regions that are repairable fit gaps.

    A region qualifies on two counts, and both are needed:

    * It is smaller than `max_gap` in at least one axis. A region larger than
      that in both is a neckline the outfit means to leave open - outfit_007's
      chest V is 82 x 77 - not a place where the garment failed to meet the arm.
    * Some of its boundary is genuine skin. The repaint sources colour from
      adjacent skin, so a region enclosed entirely by more undergarment has
      nothing to diffuse from and would only stall. outfit_008 has one such
      region, 20 x 34 under the cloak's neck opening, which passes the size test
      and still cannot be repainted.
    """
    from collections import deque as _deque

    pixels = exposed.load()
    width, height = exposed.size
    mask_pixels = garment.load() if garment is not None else None
    base_pixels = base.load() if base is not None else None
    kept = Image.new("L", (width, height), 0)
    kp = kept.load()
    seen: set[tuple[int, int]] = set()
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0 or (x, y) in seen:
                continue
            queue = _deque([(x, y)])
            component = []
            while queue:
                cx, cy = queue.popleft()
                if (cx, cy) in seen:
                    continue
                if not (0 <= cx < width and 0 <= cy < height) or pixels[cx, cy] == 0:
                    continue
                seen.add((cx, cy))
                component.append((cx, cy))
                queue.extend(((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)))
            xs = [p[0] for p in component]
            ys = [p[1] for p in component]
            if (max(xs) - min(xs) + 1) > max_gap and (max(ys) - min(ys) + 1) > max_gap:
                continue
            if mask_pixels is not None and base_pixels is not None:
                touches_skin = any(
                    0 <= nx < width and 0 <= ny < height
                    and pixels[nx, ny] == 0
                    and base_pixels[nx, ny][3] > 200
                    and mask_pixels[nx, ny] == 0
                    for cx, cy in component
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1))
                )
                if not touches_skin:
                    continue
            for px_, py_ in component:
                kp[px_, py_] = 255
    return kept


def gap_target(base: Image.Image, outfit: Image.Image | Iterable[Image.Image],
               margin: int = MARGIN, max_gap: int = MAX_FIT_GAP) -> Image.Image:
    """The region to repaint, decided once against the untouched base.

    This has to be frozen before the first pass. Repainting changes the colours
    the mask is grown from, so re-deriving the target on a later pass reclassifies
    a designed neckline as a fit gap and lets the fill bleed into it - which
    showed up as a blotchy patch inside outfit_007's chest V and a dirty smear in
    outfit_009's collar.
    """
    garment = undergarment_mask(base)
    ml = garment.load()
    width, height = base.size
    exposed = Image.new("L", (width, height), 0)
    for single in ([outfit] if isinstance(outfit, Image.Image) else list(outfit)):
        sal = single.getchannel("A").load()
        layer_gap = Image.new("L", (width, height), 0)
        lg = layer_gap.load()
        for y in range(300, 1140):
            for x in range(200, width - 200):
                if ml[x, y] > 0 and sal[x, y] < 60:
                    lg[x, y] = 255
        if max_gap is not None:
            layer_gap = fit_gaps_only(layer_gap, max_gap, base=base, garment=garment)
        exposed = ImageChops.lighter(exposed, layer_gap)

    grown = exposed.filter(ImageFilter.MaxFilter(2 * margin + 1))
    gp, mp = grown.load(), ml
    target = Image.new("L", (width, height), 0)
    tp = target.load()
    for y in range(300, 1140):
        for x in range(200, width - 200):
            if gp[x, y] > 0 and mp[x, y] > 0:
                tp[x, y] = 255
    return target


def repaint(base: Image.Image, outfit: Image.Image | Iterable[Image.Image],
            margin: int = MARGIN, relax: int = RELAX,
            max_gap: int = MAX_FIT_GAP,
            target_mask: Image.Image | None = None) -> tuple[Image.Image, dict]:
    result = base.copy()
    px = result.load()
    width, height = result.size
    mask = undergarment_mask(result)
    ml = mask.load()

    if target_mask is None:
        target_mask = gap_target(base, outfit, margin, max_gap)
    tp = target_mask.load()
    target = {
        (x, y)
        for y in range(300, 1140)
        for x in range(200, width - 200)
        if tp[x, y] > 0
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
    parser.add_argument("--all", action="store_true",
                        help="process every base against all outfits bound to it in config/compatibility.json")
    parser.add_argument("--base", type=Path)
    parser.add_argument("--outfit", type=Path, nargs="+")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--margin", type=int, default=MARGIN)
    parser.add_argument("--relax", type=int, default=RELAX)
    parser.add_argument("--max-gap", type=int, default=MAX_FIT_GAP,
                        help="a gap wider AND taller than this is treated as a designed neckline "
                             "opening and left alone; pass 0 to repaint every exposed pixel")
    parser.add_argument("--max-passes", type=int, default=6)
    args = parser.parse_args(argv)

    if args.all:
        pairs = [
            (ROOT / "assets" / "base_bodies" / base,
             [ROOT / "assets" / "outfits" / outfit for outfit in outfits])
            for base, outfits in base_outfit_pairs().items()
        ]
    elif args.base and args.outfit:
        pairs = [(args.base, list(args.outfit))]
    else:
        print("error: pass --all, or both --base and --outfit")
        return 1

    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir")
        return 1

    for base_path, outfit_paths in pairs:
        base = Image.open(base_path).convert("RGBA")
        outfit = [Image.open(path).convert("RGBA") for path in outfit_paths]
        max_gap = args.max_gap or None
        before = exposed_count(base, outfit, max_gap=max_gap)

        # Iterate to convergence. One pass is not always enough: the relaxation
        # can nudge a boundary pixel back across the mask's tolerance, and the
        # tank and skin are close enough in colour that "back across" is only a
        # few levels. Each pass re-detects whatever is still showing.
        frozen = gap_target(base, outfit, args.margin, max_gap)
        result, report = repaint(base, outfit, args.margin, args.relax, max_gap, frozen)
        after = exposed_count(result, outfit, max_gap=max_gap)
        for _ in range(args.max_passes - 1):
            if after == 0:
                break
            result, extra = repaint(result, outfit, args.margin, args.relax, max_gap, frozen)
            report["repainted"] += extra["repainted"]
            previous, after = after, exposed_count(result, outfit, max_gap=max_gap)
            if after >= previous:
                break
        if args.in_place and after >= before:
            # Rewriting a registered base that gained nothing costs it a new
            # SHA-256, a manifest entry and a re-QA for no visible change.
            print(
                f"{base_path.name}: exposed {before} -> {after}; unchanged, not rewritten"
            )
            continue
        destination = base_path if args.in_place else args.out_dir / base_path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        result.save(destination)
        print(
            f"{base_path.name}: exposed {before} -> {after}"
            f"  (repainted {report['repainted']}/{report['target']} px"
            f" across {len(outfit_paths)} outfit(s))"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
