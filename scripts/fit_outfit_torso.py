#!/usr/bin/env python3
"""Widen an outfit's body until it covers the base body's undergarment.

The base bodies wear a cream tank and shorts so they read as dressed on their
own. Every token puts an outfit over them, and most of the outfits are drawn
narrower than the body: the tank shows down the flank, the shorts show at the
hip, and on `outfit_002` a cream band runs from the armpit to below the knee on
both sides. It reads as underwear sticking out of the armour.

It is the same defect the sleeve pass fixed on the arms, in a different place,
and nothing could see it either. The neckline gate measures a window across the
chest, so a garment can miss the body's sides by 20 px and pass.

## What counts as a shortfall

Per row, the base body's own runs decide the target:

- **Torso**, above the hips: the run containing the centre line, but only on
  rows where the arms are separate runs. Where an arm merges into the torso the
  bare strip beside the garment is that arm, not the body, and a sleeveless
  outfit is meant to leave it bare.
- **Legs**, below the hips: each run wide enough to be a thigh, which keeps the
  fingers out of it.

A strip is closed only if it is narrow, runs down a long stretch of rows, and
the garment covers most of the run it sits beside - so an open coat that shows
a leg between its panels is left alone.

    python scripts/fit_outfit_torso.py --all --in-place
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

from widen_sleeves import (
    MARGIN,
    OPAQUE,
    outfit_base_pairs,
    premultiply,
    unpremultiply,
    warp_row,
)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
METHOD = "outfit_body_fit_2026-09-10"
QA_REPORT = "docs/qa/outfit_body_fit_2026-09-10.md"

# Columns a run has to cross to be the body rather than an arm or a hand.
# Which garments this pass may reshape, and why the rest are excluded.
#
# Moving a garment's edge means stretching the fabric behind it, and that is
# only safe where the fabric is plain. Every one of the other eight was tried,
# rendered and rejected: warping the coats drags a lapel, a belt end or a trim
# line out with the edge, and warping the robes narrows a skirt and moves the
# sash. The `PLAIN_LIMIT` gate below catches most of that on its own, but not
# reliably enough to be the only thing standing between a coat and a torn
# lapel, so the two that were checked by eye are named here.
FITTED = {
    "outfit_002_storm_guardian_pose_002.png":
        "plain armour vest and trousers; a cream band of the base body's tank "
        "and shorts ran from the armpit to below the knee on both sides",
    "outfit_003_verdant_alchemist_pose_003.png":
        "plain shorts and leggings; the base body's shorts showed at both hips",
}

CORE_X = (545, 710)
# Shoulder junction down to the ankles. Above the junction the garment meets the
# neck, which the neckline pass owns.
BAND = (556, 1120)
MIN_LIMB_WIDTH = 45
# Wider than this and the arms have merged into the torso for these rows - at
# the shoulder on every pose, and wherever a pose holds its hands in front of
# the body. The bare strip beside the garment there is an arm, and a sleeveless
# outfit is meant to leave it bare.
MAX_BODY_WIDTH = 250
DEFAULT_MAX_PX = 40
# A run this long is a seam down the body. Shorter is a fold or a buckle.
MIN_ROWS = 24
# How far an edge may move sideways from one row to the next and still be the
# same edge.
MATCH = 14
# A hole wider than this between two parts of a garment is the design - an open
# robe over a leg, a slashed sleeve - not a seam that failed to meet.
MAX_HOLE = 26
# How far inside each side of a hole its colour is read, past that side's own
# contour line, so the fill carries the fabric rather than the outline.
SAMPLE_IN = 3
# Rows a hole has to span before it is filled.
MIN_HOLE_ROWS = 20
# How much the fabric may vary across the stretch a warp would take up. Above
# this the edge has structure behind it - a lapel, a belt end, a trim line -
# and moving the edge moves that with it. Those edges are reported and left
# alone rather than torn.
PLAIN_LIMIT = 22.0
# The body's own outline is drawn outside every garment, so the last bare
# column at a run's edge is that outline, not a shortfall.
MIN_GAP = 2
# What counts as covered. A translucent drape - the side panels on the sun
# temple tunic, the pleats on the celestial scholar - is still garment, and
# reading it as bare body warps it into a hard-edged block.
COVER_ALPHA = 16
REACH = 90
TAPER = 12


def _run_length(mask: np.ndarray, start: int, step: int) -> int:
    length, x = 0, start
    while 0 <= x < mask.size and mask[x]:
        length += 1
        x += step
    return length


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    index = np.nonzero(mask)[0]
    if index.size == 0:
        return []
    out, start, previous = [], index[0], index[0]
    for value in index[1:]:
        if value > previous + 1:
            out.append((int(start), int(previous)))
            start = value
        previous = value
    out.append((int(start), int(previous)))
    return out


def body_regions(solid_row: np.ndarray) -> list[tuple[int, int]]:
    """The parts of this row the outfit is supposed to cover: torso, hips, legs."""
    found = [
        r for r in runs(solid_row)
        if r[0] < CORE_X[1] and r[1] > CORE_X[0] and MIN_LIMB_WIDTH <= r[1] - r[0]
    ]
    if any(r[1] - r[0] > MAX_BODY_WIDTH for r in found):
        return []
    return found


def shortfalls(garment: np.ndarray, body: np.ndarray, max_px: int) -> tuple[list, list]:
    """Where the body shows through, split by what is on either side of it.

    A strip at the end of a body region has garment on one side only: the
    garment is narrower than the hip, and closing it means moving its edge -
    contour line and all - outward.

    A strip between two runs of the same garment is a hole, and an armhole that
    does not meet the coat is the common one. Moving an edge there drags a
    lapel or a belt end with it, which is what tore `outfit_009` apart in the
    attempt before this. Both of its sides are garment, so the hole can simply
    be filled between them instead, leaving every drawn line where it is.
    """
    covered = garment[..., 3] > COVER_ALPHA
    solid = body[..., 3] > OPAQUE
    ends, holes = [], []
    for y in range(BAND[0], BAND[1] + 1):
        for lo, hi in body_regions(solid[y]):
            width = hi - lo + 1
            worn = covered[y][lo:hi + 1]
            if worn.sum() < 0.55 * width:
                # An open coat showing a leg between its panels is not a shortfall.
                continue
            for a, b in runs(~worn):
                gap = b - a + 1
                if gap < MIN_GAP:
                    continue
                # Whether there is garment on each side, looked up in the row
                # rather than inside the region: on the coats the strip at the
                # waist has the coat's body on one side and its own sleeve on
                # the other, and the sleeve is over the arm, in the next region
                # along. Reading only inside the region calls that an edge and
                # drags the lapel out to meet it.
                left_x, right_x = lo + a - 1, lo + b + 1
                inner = left_x >= 0 and covered[y, left_x]
                outer = right_x < covered.shape[1] and covered[y, right_x]
                if inner and outer:
                    if gap <= MAX_HOLE:
                        holes.append((y, lo + a, lo + b))
                elif gap <= max_px:
                    if inner:
                        ends.append((y, lo + a - 1, -1, gap))
                    elif outer:
                        ends.append((y, lo + b + 1, 1, gap))
    return ends, holes


def edges(garment: np.ndarray, body: np.ndarray, max_px: int) -> list[tuple[int, int, int, int]]:
    return shortfalls(garment, body, max_px)[0]


def chains(found: list[tuple[int, int, int, int]]) -> list[dict[int, tuple[int, int]]]:
    """Follow each garment edge down the body as one chain.

    Grouping by side alone breaks the chain where the hips split into two legs,
    and the taper at that false end leaves a notch of bare hip on both sides.
    An edge is instead matched to the chain that ended within a few pixels of it
    on the row above, so the outer edge of the hip carries on as the outer edge
    of the leg and the inner edges simply start where the legs part.
    """
    open_chains: list[dict] = []
    done: list[dict] = []
    by_row: dict[int, list] = {}
    for y, edge, step, gap in found:
        by_row.setdefault(y, []).append((edge, step, gap))
    for y in sorted(by_row):
        matched = set()
        carried = []
        for edge, step, gap in by_row[y]:
            best, distance = None, MATCH + 1
            for index, chain in enumerate(open_chains):
                if index in matched or chain["step"] != step or chain["last_y"] != y - 1:
                    continue
                if abs(chain["last_x"] - edge) < distance:
                    best, distance = index, abs(chain["last_x"] - edge)
            if best is None:
                chain = {"step": step, "rows": {}}
                open_chains.append(chain)
                best = len(open_chains) - 1
            else:
                chain = open_chains[best]
            matched.add(best)
            chain["rows"][y] = (gap, edge)
            chain["last_y"], chain["last_x"] = y, edge
            carried.append(best)
        for index, chain in enumerate(open_chains):
            if chain["last_y"] != y:
                done.append(chain)
        open_chains = [c for c in open_chains if c["last_y"] == y]
    done.extend(open_chains)
    return [c for c in done if len(c["rows"]) >= MIN_ROWS]


def shortfall(garment: np.ndarray, body: np.ndarray, max_px: int) -> int:
    ends, holes = shortfalls(garment, body, max_px)
    return sum(gap for *_, gap in ends) + sum(b - a + 1 for _, a, b in holes)


def segments(ys: list[int]) -> list[list[int]]:
    out, current = [], [ys[0]]
    for y in ys[1:]:
        if y != current[-1] + 1:
            out.append(current)
            current = []
        current.append(y)
    out.append(current)
    return out


def close_holes(result: np.ndarray, premultiplied: np.ndarray, holes: list) -> int:
    """Bridge each hole with a blend between the fabric on either side of it."""
    by_column: dict[int, list] = {}
    for y, a, b in holes:
        by_column.setdefault((a + b) // 2 // 8, []).append((y, a, b))
    closed = 0
    for group in by_column.values():
        if len(group) < MIN_HOLE_ROWS:
            continue
        for y, a, b in group:
            left = premultiplied[y, max(a - 1 - SAMPLE_IN, 0)]
            right = premultiplied[y, min(b + 1 + SAMPLE_IN, premultiplied.shape[1] - 1)]
            span = np.linspace(0.0, 1.0, b - a + 3)[1:-1][:, None]
            result[y, a:b + 1] = left[None, :] * (1.0 - span) + right[None, :] * span
            closed += b - a + 1
    return closed


def plainness(tone: np.ndarray, fabric: np.ndarray, y: int, edge: int, step: int) -> float:
    """How much the fabric varies over the stretch a warp of this edge would take up."""
    reach = min(REACH, _run_length(fabric[y], edge, step))
    if reach < 2 * MARGIN + 2:
        return float("inf")
    lo, hi = (edge, edge + reach - 1) if step > 0 else (edge - reach + 1, edge)
    return float(tone[y, lo:hi + 1].std(axis=0).mean())


def fit(outfit: Image.Image, base: Image.Image, max_px: int) -> tuple[Image.Image, dict]:
    source = np.array(outfit.convert("RGBA"))
    body = np.asarray(base.convert("RGBA"))
    ends, holes = shortfalls(source, body, max_px)
    found = chains(ends)
    if not found and not holes:
        return outfit, {"rows": 0, "pixels_closed": 0, "left_alone": 0}

    premultiplied = premultiply(source)
    result = premultiplied.copy()
    fabric = source[..., 3] > COVER_ALPHA

    tone = source[..., :3].astype(np.float64)
    rows, closed, skipped = set(), 0, 0
    for chain in found:
        step = chain["step"]
        ys = sorted(chain["rows"])
        spread = np.median([plainness(tone, fabric, y, chain["rows"][y][1], step) for y in ys])
        if not np.isfinite(spread) or spread > PLAIN_LIMIT:
            skipped += sum(gap for gap, _ in chain["rows"].values())
            continue
        top, bottom = ys[0] - 1, ys[-1] + 1
        for y in ys:
            gap, edge = chain["rows"][y]
            reach = min(REACH, _run_length(fabric[y], edge, step))
            ease = min(1.0, (y - top) / TAPER, (bottom - y) / TAPER)
            shift = float(round((gap - 1) * ease))
            if reach < 2 * MARGIN + 2 or shift <= 0:
                continue
            shift = min(shift, reach - MARGIN - 1.0)
            warp_row(result, premultiplied, y, edge, step, shift, reach)
            rows.add(y)
            closed += gap
    filled = close_holes(result, premultiplied, holes)
    rows.update(y for y, _, _ in holes)
    return unpremultiply(result), {
        "rows": len(rows), "pixels_closed": closed + filled, "left_alone": skipped,
    }


def exposed_body_pixels(outfit: Image.Image, base: Image.Image, max_px: int = DEFAULT_MAX_PX) -> int:
    return shortfall(np.array(outfit.convert("RGBA")), np.asarray(base.convert("RGBA")), max_px)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--outfit", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--max-px", type=int, default=DEFAULT_MAX_PX)
    args = parser.parse_args(argv)
    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir")
        return 1

    pairs = outfit_base_pairs()
    chosen = sorted(pairs) if args.all else [args.outfit.name]
    chosen = [name for name in chosen if name in FITTED]
    manifest = json.loads(MANIFEST.read_text())
    by_path = {entry["path"]: entry for entry in manifest["registered_production_assets"]}

    changed = 0
    for name in chosen:
        source = ROOT / "assets" / "outfits" / name
        base = Image.open(ROOT / "assets" / "base_bodies" / pairs[name])
        before_image = Image.open(source)
        exposed_before = exposed_body_pixels(before_image, base, args.max_px)
        fitted, stats = fit(before_image, base, args.max_px)
        if not stats["rows"]:
            print(f"{name}: nothing showing beside the garment")
            continue
        exposed_after = exposed_body_pixels(fitted, base, args.max_px)
        before = hashlib.sha256(source.read_bytes()).hexdigest()

        destination = source if args.in_place else args.out_dir / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        fitted.save(destination)
        note = (
            f"garment closed over {stats['rows']} rows; base body showing beside it "
            f"{exposed_before} px -> {exposed_after} px"
        )
        if stats["left_alone"]:
            note += f"; {stats['left_alone']} px left alone behind structured fabric"
        print(f"{name}: {note}")
        if args.in_place:
            entry = by_path[f"assets/outfits/{name}"]
            after = hashlib.sha256(destination.read_bytes()).hexdigest()
            entry["sha256"] = after
            provenance = entry.setdefault("provenance", {})
            steps = list(provenance.get("postprocessing", []))
            if METHOD not in steps:
                steps.append(METHOD)
            provenance["postprocessing"] = steps
            provenance["body_fit_script"] = "scripts/fit_outfit_torso.py"
            provenance[f"pre_{METHOD}_sha256"] = before
            provenance[f"post_{METHOD}_sha256"] = after
            provenance["body_fit_note"] = note
            entry["qa_report"] = QA_REPORT
        changed += 1

    if args.in_place and changed:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{changed} outfit(s) fitted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
