#!/usr/bin/env python3
"""Widen an outfit's sleeve until it covers the arm it is drawn over.

A strip of bare arm runs the whole length of each sleeve's outer edge on most of
the outfits - a median of 13 px on `outfit_010` and 14 px on `outfit_009`, over
eight thousand pixels each. It is the defect the boot pass fixed at the ankle,
never checked above it, and it shows on every token those outfits appear in.

No existing gate saw it. The exposed-leg gate stops at the knee; canvas, alpha,
bounds and width ratio are all satisfied by a coat whose sleeves are too narrow.

## Why the sleeve is warped rather than patched

Five repairs were tried on the way here and each traded the strip for something
worse, so the reasoning is worth keeping:

- **Resampling the whole garment run** across the strip stretched the lapels and
  the coat body along with the sleeve, because at the waist the two are one run.
- **Resampling an outer reach scaled to the gap** moved the stretched zone's
  inner boundary from row to row and tore notches through the lapels.
- **Repeating the edge pixel** across the strip banded it horizontally - which is
  the failure the boot pass was written to avoid in the first place.
- **Averaging that band down its length** turned it into a grey smear, because
  the pixel it repeats is the sleeve's dark contour line, not its fabric.
- **Carrying the outer margin outward over a flat fill** tore the shoulder open
  and laid navy bars across the hands, because a per-row search for "any narrow
  bare run touching the silhouette" catches the shoulder cut and the gaps
  between the fingers, not just the sleeve.

What works is a warp with a smooth reach. Both earlier resampling attempts
banded because the resampled span changed shape from row to row. Here the span
is a fixed `REACH` inward from the sleeve's own outer edge, and the distance it
is pushed out is the measured gap smoothed down the arm, so neighbouring rows
stretch by almost the same factor and the fabric shades across the seam. The
sleeve's outer contour is resampled with the rest, so it stays one crisp line
instead of being duplicated.

Only the sleeve is touched. The gap is measured inward from the silhouette's own
outer edge, outside the torso window, and a row is repaired only when what sits
beyond the sleeve is bare arm the width of a seam - not a sleeveless arm, not the
open front of a coat, not the space between fingers.

    python scripts/widen_sleeves.py --all --in-place
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
METHOD = "sleeve_widening_2026-09-10"
QA_REPORT = "docs/qa/sleeve_widening_2026-09-10.md"

OPAQUE = 128
# Shoulder seam down. Where the band ends is measured per pose rather than
# fixed: below the wrist the hand takes over the silhouette, and a gap measured
# against the fingers is not a seam.
# The band starts below the deltoid. Every outfit, including the two with no
# seam at all, sits 30-40 px inside the silhouette across rows 510-535: the
# base body's shoulder cap is wider than any garment drawn for it, and pushing
# fabric out to meet it flattens the shoulder line instead of fixing anything.
ARM_BAND = (540, 806)
WRIST_SEARCH = (640, 760)
# The torso is excluded: a chest opening is an exposed strip too, and the
# neckline work has its own pass.
TORSO_X = (556, 698)
DEFAULT_MAX_PX = 44
# A run this wide beyond the gap is a sleeve. Anything narrower is trim, a
# finger, or the edge of an open panel.
MIN_SLEEVE_RUN = 26
# A single bare column at the silhouette's edge is the body's own outline, which
# the art draws outside the garment everywhere. Two or more is a seam.
MIN_GAP = 2
# A seam runs the length of the arm. A short run is a finger gap or a fold.
MIN_SLEEVE_ROWS = 40
# ...and it runs *to the cuff*. A run that stops well above the wrist is the hem
# of a short sleeve with bare arm below it, which is the design, not a defect.
CUFF_REACH = 30
# How far inward from the sleeve's outer edge the warp reaches.
REACH = 90
# The outer margin - contour line and rim shading - is carried outward rigidly,
# so the outline is translated rather than stretched and stays one crisp line.
MARGIN = 8
# Rows the measured gap is averaged over. Two is enough to take the sampling
# jitter off the silhouette; more than that and the sleeve stops reaching it.
SMOOTH = 2
# Rows over which the widening eases off above the cuff. Without it the sleeve
# ends in a step: the cuff is already the width of the wrist and does not move,
# so the fabric above it has to come back in to meet it.
TAPER = 24
# Rows over which it eases on below the shoulder, for the same reason.
TAPER_TOP = 14


def outfit_base_pairs() -> dict[str, str]:
    rules = json.loads(COMPATIBILITY.read_text())
    return {
        rule["trait"]: rule["requires"]
        for rule in rules.get("requires", [])
        if rule.get("trait", "").startswith("outfit_") and rule.get("requires", "").startswith("base_")
    }


def wrist_rows(body: np.ndarray) -> dict[str, int]:
    """The narrowest row of each forearm - where the sleeve ends and the hand begins."""
    solid = body[..., 3] > OPAQUE
    narrowest = {}
    for side, step in (("left", 1), ("right", -1)):
        best = (10**6, ARM_BAND[1])
        for y in range(*WRIST_SEARCH):
            limb = solid[y].copy()
            limb[TORSO_X[0]:TORSO_X[1]] = False
            arm = np.nonzero(limb)[0]
            if arm.size == 0:
                continue
            edge = int(arm[0]) if side == "left" else int(arm[-1])
            best = min(best, (_run_length(limb, edge, step), y))
        narrowest[side] = best[1]
    return narrowest


def _run_length(mask: np.ndarray, start: int, step: int) -> int:
    length, x = 0, start
    while 0 <= x < mask.size and mask[x]:
        length += 1
        x += step
    return length


def measure(garment: np.ndarray, body: np.ndarray, max_px: int) -> dict[str, dict[int, tuple[int, int]]]:
    """Per row and side, the bare gap and the sleeve edge it sits beside.

    A single row tells you almost nothing: the same measurement that finds the
    seam finds the space between two fingers, and a gap that widens past
    `max_px` for three rows in the middle of a sleeve is the same seam, not a
    different feature. So the rows are grouped into runs and only the longest
    run down each arm is kept - the sleeve is the one thing on that side of the
    silhouette that is bare for hundreds of rows in a row.
    """
    covered = garment[..., 3] > OPAQUE
    solid = body[..., 3] > OPAQUE
    wrist = wrist_rows(body)
    raw: dict[str, dict[int, tuple[int, int]]] = {"left": {}, "right": {}}
    for y in range(ARM_BAND[0], ARM_BAND[1] + 1):
        limb = solid[y].copy()
        limb[TORSO_X[0]:TORSO_X[1]] = False
        arm = np.nonzero(limb)[0]
        if arm.size == 0:
            continue
        for side, edge, step in (("left", int(arm[0]), 1), ("right", int(arm[-1]), -1)):
            if y > wrist[side]:
                continue
            gap = 0
            x = edge
            while 0 <= x < covered.shape[1] and not covered[y, x] and limb[x]:
                gap += 1
                x += step
            if gap < MIN_GAP or gap > max_px:
                continue
            if not (0 <= x < covered.shape[1] and covered[y, x]):
                continue
            if _run_length(covered[y], x, step) < MIN_SLEEVE_RUN:
                continue
            raw[side][y] = (gap, x)
    return {side: _longest_run(rows, wrist[side]) for side, rows in raw.items()}


def _longest_run(rows: dict[int, tuple[int, int]], wrist: int) -> dict[int, tuple[int, int]]:
    if not rows:
        return {}
    best: list[int] = []
    current: list[int] = []
    for y in sorted(rows):
        if current and y != current[-1] + 1:
            best = max(best, current, key=len)
            current = []
        current.append(y)
    best = max(best, current, key=len)
    if len(best) < MIN_SLEEVE_ROWS or best[-1] < wrist - CUFF_REACH:
        return {}
    return {y: rows[y] for y in best}


def _smoothed(rows: dict[int, tuple[int, int]]) -> dict[int, float]:
    """The gap averaged down the arm, so neighbouring rows stretch alike."""
    out: dict[int, float] = {}
    for y in rows:
        nearby = [rows[o][0] for o in range(y - SMOOTH, y + SMOOTH + 1) if o in rows]
        out[y] = float(np.mean(nearby))
    return out


def warp_row(result: np.ndarray, premultiplied: np.ndarray, y: int, edge: int,
             step: int, shift: float, reach: int) -> None:
    """Move one row's garment edge outward by `shift`, in place.

    The outermost `MARGIN` columns - the contour line and the rim shading behind
    it - ride out as a block, so the drawn outline is translated rather than
    resampled. Everything behind them takes up the difference on a ramp that
    reaches zero at the inner end, so the join is seamless. `shift` must be a
    whole number of pixels, or the margin lands off the column grid and the
    outline comes back dotted.
    """
    inward = np.arange(reach, dtype=np.float64)
    travel = np.where(
        inward <= MARGIN,
        shift,
        shift * (1.0 - (inward - MARGIN) / (reach - 1 - MARGIN)),
    )
    src = edge + step * inward
    dst = src - step * travel
    order = np.argsort(dst)
    lo, hi = int(np.floor(dst.min())), int(np.ceil(dst.max()))
    column = np.arange(lo, hi + 1, dtype=np.float64)
    for channel in range(4):
        values = premultiplied[y, src.astype(int), channel]
        result[y, lo:hi + 1, channel] = np.interp(column, dst[order], values[order])


def premultiply(source: np.ndarray) -> np.ndarray:
    out = source.astype(np.float64)
    out[..., :3] *= out[..., 3:4] / 255.0
    return out


def unpremultiply(result: np.ndarray) -> Image.Image:
    alpha = np.clip(result[..., 3:4], 0.0, 255.0)
    rgb = np.where(alpha > 0.0, result[..., :3] * 255.0 / np.maximum(alpha, 1e-6), 0.0)
    out = np.concatenate([np.clip(rgb, 0, 255), alpha], axis=2)
    return Image.fromarray(np.round(out).astype(np.uint8), "RGBA")


def widen(outfit: Image.Image, base: Image.Image, max_px: int) -> tuple[Image.Image, dict]:
    source = np.array(outfit.convert("RGBA"))
    body = np.asarray(base.convert("RGBA"))
    found = measure(source, body, max_px)
    if not any(found.values()):
        return outfit, {"rows": 0, "pixels_added": 0}

    premultiplied = premultiply(source)
    result = premultiplied.copy()

    rows, added = set(), 0
    for side, measured in found.items():
        push = _smoothed(measured)
        step = 1 if side == "left" else -1
        if not measured:
            continue
        cuff, shoulder = max(measured), min(measured) - 1
        for y, (gap, edge) in measured.items():
            reach = min(REACH, _run_length(source[y, :, 3] > OPAQUE, edge, step))
            reach = min(reach, abs((TORSO_X[0] - 1 if side == "left" else TORSO_X[1]) - edge))
            ease = min(1.0, (cuff - y) / TAPER, (y - shoulder) / TAPER_TOP)
            # One pixel short of the silhouette. Landing on it, or past it, puts
            # the sleeve's own soft edge over the arm's drawn outline and breaks
            # that outline into dashes; stopping just inside leaves the figure
            # outlined the way the art draws it, with the sleeve tucked behind.
            # Whole pixels: the margin then lands on the column grid and the
            # contour line is copied rather than resampled across two columns,
            # which is what turns a drawn outline into a dotted one.
            shift = float(round(min(push[y] - 1.0, gap - 1.0) * ease))
            if reach < MIN_SLEEVE_RUN or shift <= 0:
                continue
            # Where the sleeve is too narrow to absorb the whole push - across
            # the shoulder cap, where the coat body is the next thing inward -
            # it takes what it can rather than dropping the row and leaving a
            # notch between two rows that did move.
            shift = min(shift, reach - MARGIN - 1.0)
            warp_row(result, premultiplied, y, edge, step, shift, reach)
            rows.add(y)
            added += gap

    return unpremultiply(result), {"rows": len(rows), "pixels_added": added}


def exposed_strip_pixels(outfit: Image.Image, base: Image.Image, max_px: int = DEFAULT_MAX_PX) -> int:
    source = np.array(outfit.convert("RGBA"))
    body = np.asarray(base.convert("RGBA"))
    found = measure(source, body, max_px)
    return sum(gap for side in found.values() for gap, _ in side.values())


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
    manifest = json.loads(MANIFEST.read_text())
    by_path = {entry["path"]: entry for entry in manifest["registered_production_assets"]}

    changed = 0
    for name in chosen:
        source = ROOT / "assets" / "outfits" / name
        base = Image.open(ROOT / "assets" / "base_bodies" / pairs[name])
        before_image = Image.open(source)
        exposed_before = exposed_strip_pixels(before_image, base, args.max_px)
        widened, stats = widen(before_image, base, args.max_px)
        if not stats["rows"]:
            print(f"{name}: no bare sleeve edge")
            continue
        exposed_after = exposed_strip_pixels(widened, base, args.max_px)
        before = hashlib.sha256(source.read_bytes()).hexdigest()

        destination = source if args.in_place else args.out_dir / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        widened.save(destination)
        note = (
            f"sleeve edge warped outward over {stats['rows']} rows; "
            f"bare arm along the sleeve {exposed_before} px -> {exposed_after} px"
        )
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
            provenance["sleeve_script"] = "scripts/widen_sleeves.py"
            provenance[f"pre_{METHOD}_sha256"] = before
            provenance[f"post_{METHOD}_sha256"] = after
            provenance["sleeve_note"] = note
            entry["qa_report"] = QA_REPORT
        changed += 1

    if args.in_place and changed:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{changed} outfit(s) widened")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
