#!/usr/bin/env python3
"""Give the open-necked outfits an inner garment, and open the hollow collar.

Three outfits fail at the neck, and all three failed silently: canvas, alpha,
bounds, width ratio and the exposed-leg gate are all satisfied by a coat with a
hole at the collar.

**`outfit_007` and `outfit_009`** are cut open at the chest. What shows through is
the base body's neutral tank: a flat cream panel with the tank's own neckline
shading crossing it as a hard horizontal step. `base_body_001`'s manifest note
already recorded the diagnosis and declined the fix - "covering those needs the
outfit to carry its own inner garment, which is a re-render, not an edit". It does
not need a re-render. The garment can be painted into the opening, which is what
this does: a shirt with its own rounded neckline, shaded down from the collar's
shadow, filling the coat's opening below the throat and leaving the neck as skin.

**`outfit_010`** has a stand collar whose interior is painted as a flat slate disc.
The outfit renders above the base, so the disc hides the neck and the collar reads
as an empty tube. The disc is cleared where the neck rises through it, keeping a
crescent at the top as the collar's far wall, so the neck comes out of the collar
instead of being capped by it.

Every edit is confined to the opening the garment itself encloses, found by
flood-filling the transparent region inside the collar rather than by a box.

    python scripts/fix_outfit_necklines.py --in-place
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
METHOD = "outfit_neckline_inner_garment_2026-09-10"
QA_REPORT = "docs/qa/outfit_necklines_2026-09-10.md"

# Skin and the neutral tank are close in tone - the base manifest notes the overlap
# - but they separate on red minus green: 49 on the thigh skin, 33 on the tank. The
# test is only applied between the collarbone and the waist, because lit highlights
# on the jaw pass it too.
TANK_RED_GREEN = 42
CHEST_BAND = (506, 700)

# Skin and tank overlap so far in tone that a lit highlight on a bare arm passes
# the tank test - measured against the whole silhouette it reported 2,661 px on
# outfit_002, which has no opening at all. So the test is confined to the torso's
# core, between the arms, which is where the tank is and where every opening is.
TORSO_X = (556, 698)

# The shirt is bounded by a neckline of its own, measured per outfit and written
# here, not by where the tank happens to be detected. Detection was tried twice:
# pulling the neckline to the tank column by column followed the detection's noise
# and gave the shirt a torn, stepped edge, and painting the detected tank directly
# left a mottled band along its speckly boundary. `neckline` is the row the shirt
# starts at on the centre line and `sag` how far it dips below that at the sides.
INNER_GARMENTS = {
    "outfit_004_lunar_oracle_pose_004.png": dict(
        neckline=503.0, sag=8.0, light=(152, 140, 163), dark=(118, 108, 133),
        note="muted violet-grey underlayer inside the wrap"),
    "outfit_005_sun_temple_pose_005.png": dict(
        neckline=502.0, sag=5.0, light=(243, 233, 216), dark=(213, 200, 180),
        note="warm cream underlayer inside the tunic's round neck"),
    "outfit_007_brown_leather_long_coat.png": dict(
        neckline=504.0, sag=13.0, light=(246, 236, 213), dark=(214, 195, 163),
        note="cream linen under a brown leather coat"),
    "outfit_008_olive_ragged_cloak.png": dict(
        neckline=502.0, sag=7.0, light=(186, 176, 141), dark=(152, 144, 113),
        note="olive linen tunic under a ragged cloak"),
    "outfit_009_navy_high_collar_coat.png": dict(
        neckline=504.0, sag=10.0, light=(236, 238, 243), dark=(190, 197, 212),
        note="pale grey-blue shirt under a navy coat"),
    "outfit_010_celestial_robe_white_gold.png": dict(
        neckline=503.0, sag=4.0, light=(232, 236, 243), dark=(196, 203, 216),
        note="pale shirt inside the stand collar"),
}

# Two outfits also measured as showing the tank at the shoulder seams. They do
# not: skin and the tank overlap so far in tone that a lit highlight on a bare
# shoulder passes the test, which is why every measurement here is confined to the
# torso between the arms. Filling those "gaps" with diffused fabric was tried and
# smeared dark blotches up both arms of `outfit_004` and `outfit_005`.

# The collar whose interior is painted shut.
HOLLOW_COLLARS = {
    "outfit_010_celestial_robe_white_gold.png": dict(
        box=(584, 470, 674, 512), keep_top=5,
        note="stand collar; the slate interior capped the neck"),
}


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


def outfit_base_pairs() -> dict[str, str]:
    rules = json.loads(COMPATIBILITY.read_text())
    return {
        rule["trait"]: rule["requires"]
        for rule in rules.get("requires", [])
        if rule.get("trait", "").startswith("outfit_") and rule.get("requires", "").startswith("base_")
    }


def collar_opening(garment: np.ndarray, body: np.ndarray) -> np.ndarray:
    """The uncovered body the garment's own collar encloses."""
    hole = (garment[..., 3] < 128) & (body[..., 3] > 128)
    band = np.zeros(hole.shape, bool)
    band[440:760, 500:760] = True
    hole &= band
    column = np.nonzero(hole[:, 627])[0]
    if column.size == 0:
        return np.zeros(hole.shape, bool)
    seed = np.zeros(hole.shape, bool)
    seed[column.max(), 627] = True
    return _blob(hole, seed)


def exposed_tank(garment: np.ndarray, body: np.ndarray) -> np.ndarray:
    """Where the base's neutral tank is visible through the garment, on the chest.

    This replaced a flood fill of the garment's opening. The fill was seeded at the
    lowest transparent pixel on the centre column, so painting part of the opening
    moved the seed and the next pass measured a different region - the count went
    *up* after a fix. What is wrong is simply that the tank is visible, and that is
    what both the repair and the test now measure.
    """
    tone = body.astype(int)
    red, green, blue = tone[..., 0], tone[..., 1], tone[..., 2]
    tank = (red > 235) & (blue > 150) & ((red - green) < TANK_RED_GREEN) & (body[..., 3] > 128)
    band = np.zeros(tank.shape, bool)
    band[CHEST_BAND[0]:CHEST_BAND[1], TORSO_X[0]:TORSO_X[1]] = True
    return tank & band & (garment[..., 3] < 128)


def paint_inner_garment(garment: np.ndarray, body: np.ndarray, spec: dict) -> tuple[np.ndarray, int]:
    """Fill the garment's opening below a stated neckline with a shaded shirt."""
    height, width = garment.shape[:2]
    rows, columns = np.mgrid[0:height, 0:width].astype(float)
    left, right = float(TORSO_X[0]), float(TORSO_X[1])
    span = np.clip((columns - left) / (right - left), 0.0, 1.0)
    neckline = spec["neckline"] + 4 * spec["sag"] * span * (1 - span)

    window = np.zeros((height, width), bool)
    window[:CHEST_BAND[1], TORSO_X[0]:TORSO_X[1]] = True
    room = window & (garment[..., 3] < 128) & (body[..., 3] > 128)
    shirt = room * np.clip((rows - neckline) / 3.0, 0.0, 1.0)
    if (shirt > 0.5).sum() < 20:
        return garment, 0

    depth = np.clip((rows - neckline) / 46.0, 0.0, 1.0)[..., None]
    light = np.asarray(spec["light"], float)
    dark = np.asarray(spec["dark"], float)
    colour = dark * (1 - depth) + light * depth

    coverage = shirt[..., None]
    out = garment.astype(float).copy()
    out[..., :3] = out[..., :3] * (1 - coverage) + colour * coverage
    out[..., 3] = np.maximum(out[..., 3], shirt * 255.0)
    return np.clip(out, 0, 255).astype(np.uint8), int((shirt > 0.5).sum())


def open_collar(garment: np.ndarray, body: np.ndarray, spec: dict) -> tuple[np.ndarray, int]:
    """Clear a collar's painted interior so the neck rises through it."""
    left, top, right, bottom = spec["box"]
    window = (slice(top, bottom), slice(left, right))
    patch = garment[window].astype(int)
    alpha = patch[..., 3]
    red, green, blue = patch[..., 0], patch[..., 1], patch[..., 2]
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    # The interior is the cool, mid-toned, unlit region the rim encloses.
    interior = (alpha > 200) & (blue > red + 6) & (luminance > 90) & (luminance < 205)
    if not interior.any():
        return garment, 0
    seed = np.zeros(interior.shape, bool)
    centre = (interior.shape[0] // 2, interior.shape[1] // 2)
    if not interior[centre]:
        rows, columns = np.nonzero(interior)
        centre = (int(rows.mean()), int(columns.mean()))
    seed[centre] = True
    disc = _blob(interior, seed)

    rows = np.arange(disc.shape[0])[:, None]
    disc_rows = np.nonzero(disc.any(axis=1))[0]
    # Keep the top few rows: that is the far wall of the collar, seen from above.
    fade = np.clip((rows - (disc_rows.min() + spec["keep_top"])) / 5.0, 0.0, 1.0)
    clear = disc * fade * (body[window][..., 3:4][..., 0] > 128)

    out = garment.astype(float).copy()
    out[window][..., 3] = out[window][..., 3] * (1 - clear)
    cleared = int((clear > 0.5).sum())
    return np.clip(out, 0, 255).astype(np.uint8), cleared


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args(argv)
    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir")
        return 1

    pairs = outfit_base_pairs()
    manifest = json.loads(MANIFEST.read_text())
    by_path = {entry["path"]: entry for entry in manifest["registered_production_assets"]}

    changed = 0
    for name in sorted(set(INNER_GARMENTS) | set(HOLLOW_COLLARS)):
        source = ROOT / "assets" / "outfits" / name
        base_path = ROOT / "assets" / "base_bodies" / pairs[name]
        garment = np.asarray(Image.open(source).convert("RGBA"))
        body = np.asarray(Image.open(base_path).convert("RGBA"))
        before = hashlib.sha256(source.read_bytes()).hexdigest()

        # An outfit can need more than one of these - outfit_010 needs its collar
        # opened *and* a shirt behind it - so the steps accumulate rather than each
        # overwriting the last one's result.
        notes, painted = [], 0
        if name in HOLLOW_COLLARS:
            spec = HOLLOW_COLLARS[name]
            garment, cleared = open_collar(garment, body, spec)
            if cleared:
                notes.append(f"{cleared} px of painted collar interior cleared: {spec['note']}")
            painted += cleared
        if name in INNER_GARMENTS:
            spec = INNER_GARMENTS[name]
            garment, shirt = paint_inner_garment(garment, body, spec)
            if shirt:
                notes.append(f"{shirt} px of inner garment painted into the opening: {spec['note']}")
            painted += shirt
        note = ". ".join(notes) + "." if notes else None
        if not painted:
            print(f"{name}: nothing to change")
            continue

        destination = source if args.in_place else args.out_dir / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(garment, "RGBA").save(destination)
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
            provenance["neckline_script"] = "scripts/fix_outfit_necklines.py"
            provenance[f"pre_{METHOD}_sha256"] = before
            provenance[f"post_{METHOD}_sha256"] = after
            provenance["neckline_note"] = note
            entry["qa_report"] = QA_REPORT
        changed += 1

    if args.in_place and changed:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{changed} outfit(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
