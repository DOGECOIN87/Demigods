#!/usr/bin/env python3
"""Build DG-145, the orange rising foreground flame, as a rendered field.

The registered `aura_front_001` was deregistered on 2026-09-09 as a placeholder:
126,276 opaque pixels in three colour buckets - hard-edged triangles and solid
circles - composited over the front of every token it landed on. The lesson it
taught is that no gate in the collection can tell a flame from three triangles.
Canvas, alpha behaviour, bounds and width ratio are all satisfied by flat
geometry, so the replacement has to be built as an effect rather than drawn as a
shape and then measured to prove it.

## What makes it a flame rather than a silhouette

A flame reads from its *interior*, not its outline. Three things produce that
here, and each is checked at the end of the build:

- **Turbulence.** Fractal value noise, built from four octaves and advected
  upward so the licks lean and break the way rising gas does. A single smooth
  envelope would give a shape; the noise gives it structure.
- **Value range.** Density runs continuously from nothing to the core, and the
  colour ramp carries deep ember through orange to a pale gold core, so no single
  tone dominates the layer.
- **Transparency.** It renders *in front of* the character, so it has to be read
  through. Peak alpha is held near the registered `aura_front_002`'s 141, and the
  bulk sits far below that.

It is also kept clear of the face: nothing is drawn above Y 582, which is below
the shoulder line at Y 569, so the flame licks up the figure's body and never
across its expression.

    python scripts/build_front_aura_flame.py --install
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
MAX_BOUNDS = (233, 129, 1021, 1139)

TOP_Y = 582          # below the shoulder line at 569: the flame never reaches the face
BASELINE = 1139      # the locked foot baseline
LEFT_X, RIGHT_X = 249, 1014
PEAK_ALPHA = 152     # near the registered aura_front_002's 141; still read through

# Each tongue is (centre x, width, height, lean, strength). They are placed to
# frame the figure rather than mask it: two outside each leg, none up the centre.
TONGUES = [
    (286, 48, 340, -34, 0.92),
    (348, 62, 520, -22, 1.06),
    (410, 52, 400, -14, 0.96),
    (468, 44, 290, -8, 0.78),
    (786, 44, 300, 8, 0.78),
    (844, 54, 412, 14, 0.96),
    (906, 64, 530, 24, 1.06),
    (968, 48, 348, 34, 0.92),
]

# Ember through flame to a pale core, sampled by density.
RAMP = np.array([
    [128, 26, 8],
    [214, 62, 12],
    [255, 122, 26],
    [255, 182, 72],
    [255, 232, 168],
], float)


def _box_blur(field: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return field
    result = field
    for axis in (0, 1):
        padded = np.pad(result, [(radius, radius) if a == axis else (0, 0) for a in range(2)], mode="edge")
        cumulative = np.cumsum(padded, axis=axis)
        zero = np.zeros_like(np.take(cumulative, [0], axis=axis))
        cumulative = np.concatenate([zero, cumulative], axis=axis)
        window = 2 * radius + 1
        taken = (np.take(cumulative, range(window, cumulative.shape[axis]), axis=axis)
                 - np.take(cumulative, range(0, cumulative.shape[axis] - window), axis=axis))
        result = taken / window
    return result


def value_noise(shape: tuple[int, int], cells: int, rng: np.random.Generator) -> np.ndarray:
    """One octave: a coarse random grid, smoothly resampled to full size."""
    height, width = shape
    grid = rng.random((cells + 1, cells + 1))
    rows = np.linspace(0, cells, height)
    columns = np.linspace(0, cells, width)
    row_low, column_low = np.floor(rows).astype(int), np.floor(columns).astype(int)
    row_frac, column_frac = rows - row_low, columns - column_low
    # Smoothstep the interpolation weights, so octaves stack without grid creases.
    row_frac = (row_frac * row_frac * (3 - 2 * row_frac))[:, None]
    column_frac = (column_frac * column_frac * (3 - 2 * column_frac))[None, :]
    row_high = np.minimum(row_low + 1, cells)
    column_high = np.minimum(column_low + 1, cells)
    top = grid[np.ix_(row_low, column_low)] * (1 - column_frac) + grid[np.ix_(row_low, column_high)] * column_frac
    bottom = grid[np.ix_(row_high, column_low)] * (1 - column_frac) + grid[np.ix_(row_high, column_high)] * column_frac
    return top * (1 - row_frac) + bottom * row_frac


def turbulence(shape: tuple[int, int], seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    field = np.zeros(shape)
    amplitude, total = 1.0, 0.0
    for cells in (9, 19, 41, 83, 167):
        field += amplitude * value_noise(shape, cells, rng)
        total += amplitude
        amplitude *= 0.62
    field /= total
    # Stretched to its own 2nd-98th percentile. Summed octaves pile up near the
    # middle of the range, and an unstretched field only dents the envelope -
    # which leaves smooth cones rather than torn licks.
    low, high = np.percentile(field, [2, 98])
    return np.clip((field - low) / max(high - low, 1e-6), 0.0, 1.0)


def density_field() -> np.ndarray:
    """Tongue envelopes broken up by upward-advected turbulence.

    Tongues are combined by **maximum**, not by sum. Summing eight overlapping
    Gaussians saturates everywhere they meet, and after the intensity compression
    that came out as a filled slab with a hard bottom edge and hard sides - two
    orange rectangles washing over the character's coat, which is the placeholder's
    failure in a different costume. Taking the maximum keeps each tongue its own
    shape, so the licks stay separate and the character reads between them.

    The noise is subtracted at every height rather than only high up, for the same
    reason: a flame is gaps as much as it is fire, and a base that is solid across
    its whole width is a block with flames drawn on top.
    """
    rows, columns = np.mgrid[0:CANVAS, 0:CANVAS].astype(float)
    coarse = turbulence((CANVAS, CANVAS), seed=20260909)
    fine = turbulence((CANVAS, CANVAS), seed=20260910)

    field = np.zeros((CANVAS, CANVAS))
    for centre_x, width, height, lean, strength in TONGUES:
        rise = np.clip((BASELINE - rows) / height, 0.0, 1.0)
        # The tongue narrows and drifts sideways as it rises.
        axis = centre_x + lean * rise ** 1.6
        spread = width * (1.0 - 0.55 * rise)
        across = np.exp(-((columns - axis) / np.maximum(spread, 1.0)) ** 2)
        taper = np.clip(1.0 - rise, 0.0, 1.0) ** 0.35

        # Sampling the noise higher up than the pixel makes the licks lean and
        # tear rather than sit still inside the envelope; the two octave sets are
        # advected by different amounts so the structure does not move as a block.
        turbulent = (0.62 * np.roll(coarse, int(-height * 0.22), axis=0)
                     + 0.38 * np.roll(fine, int(-height * 0.40), axis=1))
        carved = strength * across * taper * (0.08 + 1.85 * turbulent) - (0.26 + 0.13 * rise)
        field = np.maximum(field, np.clip(carved, 0.0, None))

    # Nothing near the face, and a scalloped rather than sliced bottom: the licks
    # already end at different rows, so the baseline only has to stop the last of
    # them, over enough pixels that it is not a drawn line.
    field *= np.clip((rows - TOP_Y) / 120.0, 0.0, 1.0)
    field *= np.clip((BASELINE - rows) / 26.0, 0.0, 1.0)
    field *= np.clip((columns - LEFT_X) / 70.0, 0.0, 1.0)
    field *= np.clip((RIGHT_X - columns) / 70.0, 0.0, 1.0)
    return field


def render() -> Image.Image:
    density = density_field()
    # Compressed rather than clipped. A hard clip flattens every lick's core to one
    # value - it took the layer's top-value share to 0.26, which is the placeholder's
    # failure - while this approaches full intensity without ever landing on it.
    # Colour is compressed on a longer scale than opacity, so the body of the flame
    # reads orange and only its hottest cores reach the pale gold at the ramp's end.
    intensity = 1.0 - np.exp(-density / 0.26)
    heat = 1.0 - np.exp(-density / 0.85)

    position = heat * (len(RAMP) - 1)
    low = np.clip(np.floor(position), 0, len(RAMP) - 2).astype(int)
    blend = (position - low)[..., None]
    rgb = RAMP[low] * (1 - blend) + RAMP[low + 1] * blend

    alpha = np.clip(intensity ** 0.85, 0.0, 1.0) * PEAK_ALPHA
    out = np.zeros((CANVAS, CANVAS, 4), np.uint8)
    out[..., :3] = np.round(rgb).astype(np.uint8)
    out[..., 3] = np.round(alpha).astype(np.uint8)
    out[..., :3][out[..., 3] == 0] = 0
    return Image.fromarray(out, "RGBA")


def report(image: Image.Image) -> dict:
    rgba = np.asarray(image).astype(int)
    alpha = rgba[..., 3]
    visible = alpha > 0
    ys, xs = np.nonzero(visible)
    read = alpha > 8
    counts = Counter(map(tuple, rgba[read].tolist()))
    vertical = np.abs(np.diff(alpha.astype(float), axis=0))
    horizontal = np.abs(np.diff(alpha.astype(float), axis=1))
    gradient = np.zeros(alpha.shape, float)
    gradient[:-1] += vertical
    gradient[:, :-1] += horizontal
    return {
        "visible_pixels": int(visible.sum()),
        "peak_alpha": int(alpha.max()),
        "mean_alpha": round(float(alpha[visible].mean()), 1),
        "opaque_pixels": int((alpha >= 250).sum()),
        "alpha_levels": int(len(np.unique(alpha[read]))),
        "top_value_share": round(counts.most_common(1)[0][1] / max(int(read.sum()), 1), 4),
        "flat_neighbourhood_share": round(float((gradient[read] < 1.0).mean()), 3),
        "bounds": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
    }


def install(built: Path, measured: dict) -> None:
    """Copy into assets/ and refresh the manifest entry's hash and measurements.

    The measurements live in the manifest because they are the reason this asset
    is registered and its predecessor is not, so they have to describe the bytes
    that actually shipped rather than an earlier render.
    """
    destination = ROOT / "assets" / "front_auras" / built.name
    destination.write_bytes(built.read_bytes())
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()

    manifest_path = ROOT / "assets" / "asset_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest["registered_production_assets"]:
        if entry.get("id") != "aura_front_001":
            continue
        entry["sha256"] = digest
        provenance = entry.setdefault("provenance", {})
        provenance["output_bounds"] = measured["bounds"]
        note = provenance.setdefault("flatness_measurements", {})
        note.update({key: measured[key] for key in
                     ("opaque_pixels", "alpha_levels", "top_value_share",
                      "flat_neighbourhood_share", "peak_alpha", "visible_pixels")})
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
        print(f"installed {destination.relative_to(ROOT)}  {digest[:12]}")
        return
    raise SystemExit("aura_front_001 is not registered; run scripts/register_face_traits.py first")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path,
                        default=Path("incoming/front_auras/aura_front_001_orange_rising_flame.png"))
    parser.add_argument("--install", action="store_true",
                        help="also write assets/front_auras/ and refresh the manifest entry")
    args = parser.parse_args(argv)
    out = args.out if args.out.is_absolute() else ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)

    image = render()
    measured = report(image)
    left, top, right, bottom = measured["bounds"]
    if (left < MAX_BOUNDS[0] or top < MAX_BOUNDS[1]
            or right > MAX_BOUNDS[2] or bottom > MAX_BOUNDS[3]):
        raise SystemExit(f"bounds {measured['bounds']} escape {list(MAX_BOUNDS)}")
    if top < TOP_Y:
        raise SystemExit(f"flame reaches Y{top}; it must stay below Y{TOP_Y}")
    if measured["opaque_pixels"]:
        raise SystemExit(f"{measured['opaque_pixels']} fully opaque pixels; a front aura is read through")
    # Calibrated against the two front auras this collection already has: the
    # accepted aura_front_002 measures 83 alpha levels, a 0.067 top-value share and
    # a 0.219 flat-neighbourhood share; the rejected placeholder measures 28, 0.334
    # and 0.883. The limits sit between them, nearer the accepted asset.
    for key, limit, worse in (("alpha_levels", 64, "fewer"),
                              ("top_value_share", 0.10, "more"),
                              ("flat_neighbourhood_share", 0.60, "more")):
        value = measured[key]
        failed = value < limit if worse == "fewer" else value > limit
        if failed:
            raise SystemExit(
                f"{key} is {value} against a limit of {limit}; that is flat shading, which is "
                "what got the placeholder rejected"
            )

    image.save(out)
    if args.install:
        install(out, measured)
    for key, value in measured.items():
        print(f"{key:26s} {value}")
    print(f"\nwritten to {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
