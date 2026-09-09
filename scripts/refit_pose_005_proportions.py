#!/usr/bin/env python3
"""Put base_pose_005's head and shoulders back on the collection's proportions.

Four of the five registered base bodies agree closely on where the character's
anatomy sits: the eye line falls at Y 368.5-371.8, the chin at Y 475-477 and the
shoulder junction at Y 495-497. `base_pose_005_centered_two_hand_grip` sits ~20 px
off on the eyes and ~24 px off on the chin and shoulders, which reads as a smaller
head on a longer body - a different character build in one token out of five.

The existing rig gate cannot see it. It measures the silhouette: canvas, top of
head, foot baseline, centre X and maximum bounds. Pose 005 passes all five,
because the outline is only ever checked at its extremes and both of those are
locked to the same rows as everything else. The deviation is entirely interior.

It blocks the facial system. Eyes, eyebrows and mouths are one layer each, shared
by every base, and they are placed by rig anchor rather than per base. A pair
seated on the collection's eye line lands 20 px below pose 005's baked eyes,
leaving a band of the original eye showing above the new one; seating them for
pose 005 breaks the other four. There is no single seat that fits both, so the
base has to come to the rig.

## The correction

A monotone piecewise-linear remap of the Y axis, holding the two locked rows
fixed and moving each measured landmark onto the four-base consensus:

    141   -> 141     top of head, locked
    350.8 -> 370.3   eye line
    452   -> 476.5   chin
    472   -> 496.3   shoulder junction
    1139  -> 1139    foot baseline, locked

Between landmarks the scale is constant, so the head stretches by 9.3 % on its
vertical axis and the body below the shoulder compresses by 3.6 %. Nothing moves
horizontally, which is what the measurements ask for: pose 005's head is already
the collection's width (356 px against 353 px on the master) and only its height
is short. The body absorbs the difference over 667 px, where 3.6 % is well under
the eye's threshold for a figure of this proportion.

`outfit_005_sun_temple_pose_005` is drawn to this base and bound to it by a
compatibility rule, so it takes the identical map. Applying the same function to
both preserves their fit exactly.

Resampling is linear on premultiplied alpha along Y only. Premultiplying matters
at the silhouette edge: interpolating straight RGBA blends transparent pixels'
colour into the edge and leaves a dark or white fringe around the figure.

    python scripts/refit_pose_005_proportions.py --out-dir incoming/pose_005_refit
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
TOP_OF_HEAD = 141
FOOT_BASELINE = 1139

# (source row on pose 005, target row from the four-base consensus)
# The canvas endpoints are carried so the map is the identity outside the figure.
# Without them `np.interp` clamps, which replicates the top-of-head row upward and
# the baseline row downward and fills the empty canvas with a smear of the figure.
LANDMARKS = [
    (0.0, 0.0),          # canvas top - identity
    (141.0, 141.0),      # top of head - locked by the rig
    (350.8, 370.3),      # eye line
    (452.0, 476.5),      # chin
    (472.0, 496.3),      # shoulder junction
    (1139.0, 1139.0),    # foot baseline - locked by the rig
    (1253.0, 1253.0),    # canvas bottom - identity
]

TARGETS = [
    ROOT / "assets" / "base_bodies" / "base_pose_005_centered_two_hand_grip.png",
    ROOT / "assets" / "outfits" / "outfit_005_sun_temple_pose_005.png",
]


def inverse_map(y_out: np.ndarray) -> np.ndarray:
    """Source row for each output row, by inverting the piecewise map."""
    source = np.array([a for a, _ in LANDMARKS])
    target = np.array([b for _, b in LANDMARKS])
    return np.interp(y_out, target, source)


def remap(image: Image.Image) -> Image.Image:
    """Resample along Y through the landmark map, on premultiplied alpha."""
    rgba = np.asarray(image.convert("RGBA")).astype(np.float64)
    alpha = rgba[..., 3:4] / 255.0
    premultiplied = np.concatenate([rgba[..., :3] * alpha, rgba[..., 3:4]], axis=2)

    height = rgba.shape[0]
    rows = inverse_map(np.arange(height, dtype=np.float64))
    inside = (rows >= 0) & (rows <= height - 1)
    low = np.clip(np.floor(rows), 0, height - 1).astype(int)
    high = np.clip(low + 1, 0, height - 1)
    blend = (rows - low)[:, None, None]

    sampled = premultiplied[low] * (1 - blend) + premultiplied[high] * blend
    sampled[~inside] = 0.0

    out_alpha = np.clip(sampled[..., 3:4], 0, 255)
    safe = np.maximum(out_alpha / 255.0, 1e-6)
    out = np.concatenate([np.clip(sampled[..., :3] / safe, 0, 255), out_alpha], axis=2)
    return Image.fromarray(np.round(out).astype(np.uint8), "RGBA")


def landmarks_of(path: Path) -> dict[str, float]:
    """Measure the anatomy this correction is aimed at."""
    rgba = np.asarray(Image.open(path).convert("RGBA")).astype(float)
    solid = rgba[..., 3] > 128
    rows = np.nonzero(solid.any(axis=1))[0]
    widths = solid.sum(axis=1)
    measured = {"top_of_head": float(rows.min()), "foot_baseline": float(rows.max())}

    luminance = 0.299 * rgba[..., 0] + 0.587 * rgba[..., 1] + 0.114 * rgba[..., 2]
    centres = []
    for (left, top, right, bottom), guess in (((500, 286, 600, 430), 548),
                                              ((655, 286, 755, 430), 708)):
        patch = luminance[top:bottom, left:right]
        ink = _grow(patch < np.percentile(patch, 85) - 22)
        window = np.full(patch.shape, np.inf)
        band = slice(330 - top, 400 - top), slice(guess - left - 20, guess - left + 20)
        window[band] = patch[band]
        row, column = np.unravel_index(np.argmin(window), window.shape)
        seed = np.zeros_like(ink)
        seed[row, column] = True
        ys = np.nonzero(_blob(ink, seed))[0]
        centres.append(top + (ys.min() + ys.max()) / 2)
    measured["eye_line"] = sum(centres) / 2

    band = widths[int(measured["eye_line"]) + 40:640]
    chin = int(measured["eye_line"]) + 40 + int(band.argmin())
    measured["chin"] = float(chin)
    neck = widths[chin]
    measured["shoulder"] = float(next(y for y in range(chin, 700) if widths[y] >= 2 * neck))
    return measured


def _grow(mask: np.ndarray, steps: int = 1) -> np.ndarray:
    grown = mask.copy()
    for _ in range(steps):
        nudged = grown.copy()
        nudged[1:, :] |= grown[:-1, :]
        nudged[:-1, :] |= grown[1:, :]
        nudged[:, 1:] |= grown[:, :-1]
        nudged[:, :-1] |= grown[:, 1:]
        grown = nudged
    return grown


def _blob(mask: np.ndarray, seed: np.ndarray) -> np.ndarray:
    current = seed & mask
    while True:
        grown = _grow(current) & mask
        if grown.sum() == current.sum():
            return grown
        current = grown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=Path("incoming/pose_005_refit"))
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args(argv)
    out_dir = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    report = []
    for path in TARGETS:
        # Read the input hash before writing, so an --in-place run still records
        # what it replaced rather than what it produced.
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        with Image.open(path) as image:
            corrected = remap(image)
        destination = path if args.in_place else out_dir / path.name
        corrected.save(destination)

        entry = {
            "asset": path.name,
            "output": str(destination.relative_to(ROOT)),
            "sha256_before": before,
            "sha256_after": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "landmark_map": [list(pair) for pair in LANDMARKS],
        }
        if "base_pose_005" in path.name:
            entry["landmarks_after"] = landmarks_of(destination)
        report.append(entry)
        print(f"{path.name}: {entry['sha256_before'][:12]} -> {entry['sha256_after'][:12]}")
        if "landmarks_after" in entry:
            for key, value in entry["landmarks_after"].items():
                print(f"    {key:14s} {value:.1f}")

    (out_dir / "refit_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
