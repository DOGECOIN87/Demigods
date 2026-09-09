#!/usr/bin/env python3
"""Build the collection's 60 facial traits from the approved master's own face.

The backlog cites cells of a `FACE` reference sheet for all 60. That sheet exists
in this repository only as `images/reference_sheets/anime_character_creation_asset_sheet.webp`,
which is 128x96 px - a browsing preview, as its own index says. A 1254 px eye pair
cannot be reconstructed from a thumbnail, and pretending otherwise would put a
false provenance claim in the manifest. So the family is built from the art the
collection already approved.

The base body is not a blank mannequin: `prompts/16` specifies "large warm-brown
eyes, small nose, and gentle closed-mouth smile", and every registered base has
them painted in. That has two consequences the collection had never written down.

1. A face trait must *cover* the feature underneath it, or the original shows
   through beside the new one.
2. The approved face already is the collection's face - on-model, on-rig, painted
   in the locked style and positioned by the artist rather than by a placement
   rule.

`scripts/extract_face_features.py` separates that painted face from the skin it is
painted on. This module turns the separated features into families:

- **Eyes** keep the approved silhouette and shading and vary the iris. The lash
  line, sclera and catchlight are the master's own; only the iris body is remapped
  through a three-stop ramp, which keeps the pupil dark and the rim light where the
  painting put them.
- **Eyebrows** keep the approved brow and vary its mood by a per-column vertical
  remap - shift, tilt about the inner end, arch gain and thickness. A brow is a thin
  arc, so that family of transforms expresses every mood without redrawing it.
- **Mouths** and **expression marks** are drawn, because there is only one baked
  mouth and no baked marks to vary. Both are rasterized with soft round brushes in
  the master's own ink colour.

## Covering what is underneath

Every eye, eyebrow and mouth layer carries a skin patch beneath its art, shaped to
the union of where the baked feature lands across *all* registered bases and
feathered at its rim. Without it a mood that raises the brows, or a mouth smaller
than the baked smile, leaves the original showing. The patch colour is the harmonic
reconstruction of the skin behind the feature, so it is continuous with the cheek
and forehead around it rather than a flat fill; the bases agree on skin tone to
within about 10/255, which the feather absorbs.

Expression marks carry no patch. They are additive overlays on skin that is
already there.

    python scripts/build_face_traits.py --out-dir incoming/face_traits_2026-09-09
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

try:  # run as `python scripts/build_face_traits.py`
    from extract_face_features import IRIS, _box_blur, _grow, known_skin, reconstruct_skin, unmix
except ModuleNotFoundError:  # imported as `scripts.build_face_traits`, as the tests do
    from scripts.extract_face_features import (
        IRIS, _box_blur, _grow, known_skin, reconstruct_skin, unmix,
    )

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
MASTER = ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png"
BASES = ROOT / "assets" / "base_bodies"

# Rig anchors this module places against.
EYE_LINE_Y = 370
MOUTH_CENTER = (627, 441)
CENTER_X = 627

# Regions enclosing each baked feature on the master, widened from the extraction
# regions so the right eye's outer corner (which reaches X 759) is not clipped.
FEATURE_REGIONS = {
    "eye_left": (486, 326, 604, 414),
    "eye_right": (650, 326, 768, 414),
    "eyebrows": (496, 290, 760, 340),
    "mouth": (590, 422, 666, 462),
}

# Boxes the baked-feature footprint is searched in, across every registered base.
FOOTPRINT_BOXES = {
    "eyes": [(470, 300, 610, 430), (645, 300, 785, 430)],
    "eyebrows": [(495, 288, 760, 340)],
    "mouth": [(590, 424, 665, 460)],
}

# How far the skin patch is grown past the baked footprint before it is feathered.
COVER_DILATE = 3
COVER_FEATHER = 5

MOUTH_INK = (150, 74, 46)          # the master's own mouth line, at full opacity
MOUTH_INTERIOR = (128, 62, 58)     # inside an open mouth
MOUTH_TONGUE = (214, 118, 122)
MOUTH_TEETH = (250, 244, 240)
BLUSH = (240, 138, 148)


# ---------------------------------------------------------------------------
# Palettes and variant tables
# ---------------------------------------------------------------------------

# 24 iris colours, in the backlog's order. Where the backlog repeats an adjective
# - "dark neutral" at r1c1 and r3c1, "charcoal" at r2c7 and r3c7, "black" at r2c8
# and r3c8 - the two are separated by temperature rather than shipped identical,
# and `--check` asserts that no two irises are closer than MIN_IRIS_DISTANCE.
MIN_IRIS_DISTANCE = 18.0

EYE_PALETTES: list[tuple[str, tuple[int, int, int]]] = [
    ("dark_neutral", (92, 78, 70)),
    ("dark_umber", (78, 58, 46)),
    ("dark_slate", (64, 52, 58)),
    ("deep_olive", (96, 104, 52)),
    ("deep_blue", (52, 78, 146)),
    ("violet", (122, 86, 176)),
    ("near_black", (48, 42, 52)),
    ("dark_brown", (110, 72, 42)),
    ("gold", (214, 166, 54)),
    ("yellow_green", (168, 190, 64)),
    ("cyan", (76, 190, 204)),
    ("emerald", (46, 150, 102)),
    ("crimson", (176, 44, 52)),
    ("magenta", (196, 70, 158)),
    ("charcoal", (86, 88, 92)),
    ("black", (30, 30, 30)),
    ("warm_neutral", (120, 92, 72)),
    ("gray", (140, 142, 146)),
    ("rose", (198, 110, 120)),
    ("pink", (232, 146, 180)),
    ("amber", (206, 132, 44)),
    ("orange_gold", (222, 150, 70)),
    ("cool_charcoal", (70, 74, 92)),
    ("blue_black", (16, 22, 44)),
]

# A brow is a thin arc, so a per-column vertical remap covers every mood: how far
# it sits from the eye (`drop`), how much the inner end lifts or falls (`tilt`,
# positive lifts the inner end), how much of the painted arch is kept (`arch`),
# how heavy the line is (`weight`), and how far apart the pair sits (`spread`).
# `lopsided` raises the viewer-right brow alone, for a quizzical read.
BROW_MOODS: list[dict] = [
    dict(name="neutral", drop=0, tilt=0.0, arch=1.0, weight=1.0, spread=0, lopsided=0),
    dict(name="raised", drop=-8, tilt=0.0, arch=1.0, weight=1.0, spread=0, lopsided=0),
    dict(name="lowered", drop=6, tilt=0.0, arch=1.0, weight=1.05, spread=0, lopsided=0),
    dict(name="angry", drop=2, tilt=-7.0, arch=0.9, weight=1.1, spread=0, lopsided=0),
    dict(name="furious", drop=4, tilt=-12.0, arch=0.7, weight=1.25, spread=-4, lopsided=0),
    dict(name="worried", drop=1, tilt=6.0, arch=0.9, weight=0.95, spread=0, lopsided=0),
    dict(name="pleading", drop=-2, tilt=11.0, arch=0.8, weight=0.9, spread=0, lopsided=0),
    dict(name="arched", drop=-4, tilt=0.0, arch=1.7, weight=0.95, spread=0, lopsided=0),
    dict(name="flat", drop=1, tilt=0.0, arch=0.3, weight=1.0, spread=0, lopsided=0),
    dict(name="thin", drop=0, tilt=0.0, arch=1.0, weight=0.6, spread=0, lopsided=0),
    dict(name="thick", drop=1, tilt=0.0, arch=1.0, weight=1.6, spread=0, lopsided=0),
    dict(name="bold_raised", drop=-7, tilt=0.0, arch=1.1, weight=1.45, spread=0, lopsided=0),
    dict(name="fine_arched", drop=-5, tilt=0.0, arch=1.5, weight=0.65, spread=0, lopsided=0),
    dict(name="wide_set", drop=0, tilt=0.0, arch=1.0, weight=1.0, spread=11, lopsided=0),
    dict(name="close_set", drop=1, tilt=-3.0, arch=1.0, weight=1.05, spread=-10, lopsided=0),
    dict(name="quizzical", drop=0, tilt=0.0, arch=1.1, weight=1.0, spread=0, lopsided=-10),
]

# Mouths are drawn, because there is one baked mouth and no second to vary it
# against. `curve` is how far the line's midpoint sits below its ends, in pixels,
# which is what makes a smile - the master's own mouth spans X 605-650 and drops
# 7 px from end to centre, and those are the numbers the family is calibrated to.
# `width` is the span, `weight` the stroke, and `open` the interior a parted mouth
# carries. `source` marks the one variant that is the master's mouth itself: it is
# the approved closed neutral mouth, so it is used rather than redrawn.
MOUTHS: list[dict] = [
    dict(name="closed_neutral", source=True),
    dict(name="small_open_smile", width=34, curve=4, weight=2.4,
         open=dict(rx=17, ry=11, tongue=True, teeth=False, lift=2)),
    dict(name="small_dark_open", width=28, curve=2, weight=2.4,
         open=dict(rx=14, ry=13, tongue=False, teeth=True, lift=3)),
    dict(name="wide_open_smile", width=60, curve=7, weight=2.6,
         open=dict(rx=30, ry=15, tongue=True, teeth=True, lift=2)),
    dict(name="short_line", width=26, curve=3, weight=2.4),
    dict(name="soft_curve", width=38, curve=9, weight=2.6),
    dict(name="flat_line", width=42, curve=0, weight=2.4),
    dict(name="small_downturned", width=32, curve=-7, weight=2.6,
         open=dict(rx=13, ry=9, tongue=False, teeth=False, lift=1)),
    dict(name="tiny_neutral", width=18, curve=1, weight=2.2),
    dict(name="tiny_curve", width=20, curve=5, weight=2.2),
    dict(name="pink_open_pout", width=24, curve=2, weight=2.2,
         open=dict(rx=13, ry=14, tongue=True, teeth=False, lift=1)),
    dict(name="tiny_round", width=14, curve=0, weight=2.0,
         open=dict(rx=8, ry=9, tongue=False, teeth=False, lift=0)),
]

# Expression marks sit on the cheeks. Two constraints fix that: hair_front renders
# above expression marks, so anything on the forehead would be hidden by most of
# the hair in the collection; and the face narrows fast below the eyes - it spans
# X 492-763 at Y 422 and X 524-731 at Y 446 - so a mark much outside these anchors
# lands on the ear or off the silhouette. The eyes end at Y 404, so Y 422 clears
# them with room for a mark's own radius.
RIGHT_CHEEK = (720, 422)
LEFT_CHEEK = (534, 422)
MARK_RADIUS = 22

MARKS: list[dict] = [
    dict(name="pink_blush_strokes", kind="blush_strokes"),
    dict(name="yellow_stress_marks", kind="stress", colour=(246, 206, 84)),
    dict(name="dark_gloom_lines", kind="gloom", colour=(96, 96, 116)),
    dict(name="gold_sparkle", kind="sparkle", colour=(250, 214, 108)),
    dict(name="cyan_sweat_drop", kind="sweat", colour=(142, 214, 238)),
    dict(name="pink_anger_cross", kind="anger", colour=(236, 96, 118)),
    dict(name="yellow_green_emphasis", kind="emphasis", colour=(190, 214, 92)),
    dict(name="pink_curved_mark", kind="curve", colour=(240, 140, 170)),
]


# ---------------------------------------------------------------------------
# Measuring what is baked into the bases
# ---------------------------------------------------------------------------

def _blob(mask: np.ndarray, seed: np.ndarray) -> np.ndarray:
    current = seed & mask
    while True:
        grown = _grow(current) & mask
        if grown.sum() == current.sum():
            return grown
        current = grown


def baked_footprints() -> dict[str, np.ndarray]:
    """Where each baked feature lands, unioned over every registered base.

    A trait is one layer shared by all of them, so what it has to cover is the
    union rather than the master's own footprint. The eyes are found as the
    connected dark blob seeded at each iris, which keeps the ear outline and the
    jaw shadow at the search box's edge out of it.
    """
    union = {name: np.zeros((CANVAS, CANVAS), bool) for name in FOOTPRINT_BOXES}
    for path in sorted(BASES.glob("*.png")):
        with Image.open(path) as image:
            rgba = np.asarray(image.convert("RGBA")).astype(float)
        luminance = 0.299 * rgba[..., 0] + 0.587 * rgba[..., 1] + 0.114 * rgba[..., 2]

        eyes = np.zeros((CANVAS, CANVAS), bool)
        for (left, top, right, bottom), guess in zip(FOOTPRINT_BOXES["eyes"], (548, 708)):
            patch = luminance[top:bottom, left:right]
            ink = _grow(patch < np.percentile(patch, 85) - 22)
            window = np.full(patch.shape, np.inf)
            band = slice(330 - top, 400 - top), slice(guess - left - 20, guess - left + 20)
            window[band] = patch[band]
            row, column = np.unravel_index(np.argmin(window), window.shape)
            seed = np.zeros_like(ink)
            seed[row, column] = True
            eyes[top:bottom, left:right] |= _blob(ink, seed)
        union["eyes"] |= eyes

        left, top, right, bottom = FOOTPRINT_BOXES["eyebrows"][0]
        patch = luminance[top:bottom, left:right]
        union["eyebrows"][top:bottom, left:right] |= (
            (patch < np.percentile(patch, 80) - 18) & ~eyes[top:bottom, left:right]
        )

        left, top, right, bottom = FOOTPRINT_BOXES["mouth"][0]
        patch = luminance[top:bottom, left:right]
        union["mouth"][top:bottom, left:right] |= patch < np.percentile(patch, 90) - 10
    return union


# ---------------------------------------------------------------------------
# Skin, and the patch that erases a baked feature
# ---------------------------------------------------------------------------

class Face:
    """The master's face, separated into skin and the features painted on it."""

    def __init__(self) -> None:
        with Image.open(MASTER) as image:
            self.rgb = np.asarray(image.convert("RGBA")).astype(float)[..., :3]
        self.skin: dict[str, np.ndarray] = {}
        self.alpha: dict[str, np.ndarray] = {}
        self.feature: dict[str, np.ndarray] = {}
        for name, (left, top, right, bottom) in FEATURE_REGIONS.items():
            patch = self.rgb[top:bottom, left:right]
            skin = reconstruct_skin(patch, known_skin(patch))
            core = _grow(np.abs(patch - skin).max(axis=2) > 26.0).astype(float)
            alpha, feature = unmix(patch, skin, core)
            self.skin[name] = skin
            self.alpha[name] = alpha
            self.feature[name] = feature

    def eye_art(self, side: str) -> tuple[np.ndarray, np.ndarray, tuple[int, int, int, int]]:
        """The master's eye, isolated from the ear and brow tail sharing its box."""
        name = f"eye_{side}"
        left, top, right, bottom = FEATURE_REGIONS[name]
        alpha = self.alpha[name]
        height, width = alpha.shape
        rows, columns = np.mgrid[0:height, 0:width]
        cx, cy, rx, ry = IRIS[name]
        inside = (((columns + left - cx) / rx) ** 2 + ((rows + top - cy) / ry) ** 2) <= 1.0
        keep = _grow(_blob(alpha > 0.15, inside), 2)
        return np.where(keep, alpha, 0.0), self.feature[name], (left, top, right, bottom)


def cover(footprint: np.ndarray, face: Face, region: str) -> tuple[np.ndarray, np.ndarray, tuple]:
    """A feathered skin patch over the baked feature, in the master's own skin.

    The patch is grown a little past the footprint so a soft edge is covered too,
    then ramped to nothing over a few pixels. A hard patch would read as a
    rectangle of slightly wrong tone on the four bases whose skin differs from the
    master's by up to 10/255; ramped, that difference is below the threshold.
    """
    left, top, right, bottom = FEATURE_REGIONS[region]
    inside = footprint[top:bottom, left:right]
    hard = _grow(inside, COVER_DILATE)
    ramp = _box_blur(hard.astype(float)[..., None], COVER_FEATHER)[..., 0]
    alpha = np.clip(np.where(hard, 1.0, ramp * 1.8), 0.0, 1.0)
    return alpha, face.skin[region], (left, top, right, bottom)


# ---------------------------------------------------------------------------
# Compositing and drawing
# ---------------------------------------------------------------------------

def compose(layers: list[tuple[np.ndarray, np.ndarray, tuple]]) -> Image.Image:
    """Composite alpha/rgb patches onto the locked canvas, back to front."""
    canvas_rgb = np.zeros((CANVAS, CANVAS, 3), float)
    canvas_alpha = np.zeros((CANVAS, CANVAS), float)
    for alpha, rgb, (left, top, right, bottom) in layers:
        under_rgb = canvas_rgb[top:bottom, left:right]
        under_alpha = canvas_alpha[top:bottom, left:right]
        out_alpha = alpha + under_alpha * (1 - alpha)
        safe = np.maximum(out_alpha, 1e-6)[..., None]
        canvas_rgb[top:bottom, left:right] = (
            rgb * alpha[..., None] + under_rgb * under_alpha[..., None] * (1 - alpha[..., None])
        ) / safe
        canvas_alpha[top:bottom, left:right] = out_alpha
    out = np.zeros((CANVAS, CANVAS, 4), np.uint8)
    out[..., :3] = np.round(np.clip(canvas_rgb, 0, 255)).astype(np.uint8)
    out[..., 3] = np.round(np.clip(canvas_alpha, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


class Brush:
    """A soft round brush over one patch, in the painted style's edge softness."""

    def __init__(self, box: tuple[int, int, int, int]) -> None:
        self.box = box
        left, top, right, bottom = box
        self.alpha = np.zeros((bottom - top, right - left), float)
        self.rgb = np.zeros((bottom - top, right - left, 3), float)
        self.rows, self.columns = np.mgrid[top:bottom, left:right].astype(float)

    def _blend(self, coverage: np.ndarray, colour) -> None:
        coverage = np.clip(coverage, 0.0, 1.0)
        colour = np.asarray(colour, float)
        self.rgb = (
            colour * coverage[..., None] + self.rgb * self.alpha[..., None] * (1 - coverage[..., None])
        ) / np.maximum(coverage + self.alpha * (1 - coverage), 1e-6)[..., None]
        self.alpha = coverage + self.alpha * (1 - coverage)

    def stroke(self, points: np.ndarray, half_width, colour, softness: float = 1.1,
               opacity: float = 1.0) -> None:
        """Stamp a polyline whose half-width may vary along its length."""
        distance = np.full(self.alpha.shape, np.inf)
        width = np.zeros(self.alpha.shape)
        steps = len(points) - 1
        for index in range(steps):
            (x0, y0), (x1, y1) = points[index], points[index + 1]
            dx, dy = x1 - x0, y1 - y0
            length = max(dx * dx + dy * dy, 1e-9)
            t = np.clip(((self.columns - x0) * dx + (self.rows - y0) * dy) / length, 0.0, 1.0)
            near = np.hypot(self.columns - (x0 + t * dx), self.rows - (y0 + t * dy))
            along = (index + t) / steps
            local = half_width(along) if callable(half_width) else np.full_like(near, half_width)
            closer = near < distance
            distance = np.where(closer, near, distance)
            width = np.where(closer, local, width)
        self._blend(np.clip((width - distance) / softness + 0.5, 0, 1) * opacity, colour)

    def ellipse(self, cx: float, cy: float, rx: float, ry: float, colour,
                softness: float = 1.1, opacity: float = 1.0, above: float | None = None) -> None:
        """A soft filled ellipse, optionally clipped to the rows below `above`."""
        scaled = np.hypot((self.columns - cx) / max(rx, 1e-6), (self.rows - cy) / max(ry, 1e-6))
        coverage = np.clip((1.0 - scaled) * min(rx, ry) / softness + 0.5, 0, 1)
        if above is not None:
            coverage *= np.clip((self.rows - above) / softness + 0.5, 0, 1)
        self._blend(coverage * opacity, colour)

    def layer(self) -> tuple[np.ndarray, np.ndarray, tuple]:
        return self.alpha, self.rgb, self.box


def arc(x0: float, x1: float, y: float, sag: float, samples: int = 41) -> np.ndarray:
    """A quadratic arc from (x0, y) to (x1, y) whose midpoint is `sag` px lower."""
    t = np.linspace(0.0, 1.0, samples)
    return np.stack([x0 + (x1 - x0) * t, y + 4 * sag * t * (1 - t)], axis=1)


# ---------------------------------------------------------------------------
# Eyes
# ---------------------------------------------------------------------------

def iris_ramp(base: tuple[int, int, int]) -> np.ndarray:
    """Three stops the iris luminance is remapped through.

    The painting runs from a near-black pupil through the iris body to a light rim.
    Remapping through stops rather than tinting keeps that structure: the pupil
    stays dark whatever the colour, and a pale iris does not wash the pupil out.
    """
    colour = np.asarray(base, float)
    return np.stack([colour * 0.10, colour, colour + (255.0 - colour) * 0.72])


def recoloured_eye(face: Face, side: str, base: tuple[int, int, int]):
    alpha, rgb, box = face.eye_art(side)
    left, top, right, bottom = box
    height, width = alpha.shape
    rows, columns = np.mgrid[0:height, 0:width]
    cx, cy, rx, ry = IRIS[f"eye_{side}"]
    inside = (((columns + left - cx) / rx) ** 2 + ((rows + top - cy) / ry) ** 2) <= 1.0

    luminance = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    spread = rgb.max(axis=2) - rgb.min(axis=2)
    # The catchlight is the one near-neutral bright patch inside the iris; it is the
    # shared upper-left highlight the whole collection uses, so it is left alone.
    catchlight = inside & (luminance > 175) & (spread < 26)
    target = inside & (alpha > 0.05) & ~catchlight
    if not target.any():
        raise ValueError(f"{side}: no iris pixels found")

    low, high = np.percentile(luminance[target], [2, 98])
    t = np.clip((luminance - low) / max(high - low, 1e-6), 0.0, 1.0)
    stops = iris_ramp(base)
    mid = 0.5
    lower = t < mid
    weight = np.where(lower, t / mid, (t - mid) / (1 - mid))[..., None]
    ramped = np.where(
        lower[..., None],
        stops[0] * (1 - weight) + stops[1] * weight,
        stops[1] * (1 - weight) + stops[2] * weight,
    )
    out = np.where(target[..., None], ramped, rgb)
    return alpha, np.clip(out, 0, 255), box


def build_eyes(face: Face, footprints: dict[str, np.ndarray]) -> list[tuple[str, Image.Image]]:
    built = []
    for index, (name, base) in enumerate(EYE_PALETTES, start=1):
        layers = [
            cover(footprints["eyes"], face, "eye_left"),
            cover(footprints["eyes"], face, "eye_right"),
            recoloured_eye(face, "left", base),
            recoloured_eye(face, "right", base),
        ]
        built.append((f"eyes_{index:03d}_{name}.png", compose(layers)))
    return built


# ---------------------------------------------------------------------------
# Eyebrows
# ---------------------------------------------------------------------------

def brow_halves(face: Face) -> list[tuple[int, int]]:
    """Column ranges of the two painted brows inside the eyebrow region."""
    alpha = face.alpha["eyebrows"]
    columns = np.nonzero((alpha > 0.05).any(axis=0))[0]
    runs, start, previous = [], columns[0], columns[0]
    for column in columns[1:]:
        if column > previous + 6:
            runs.append((int(start), int(previous)))
            start = column
        previous = column
    runs.append((int(start), int(previous)))
    if len(runs) != 2:
        raise ValueError(f"expected two brows, found {len(runs)}")
    return runs


def _brow_spine(weights: np.ndarray, columns: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The brow's centre line, fitted rather than read column by column.

    Taking the ink centroid of each column directly gives a line that jitters by a
    pixel wherever a column carries only a few faint pixels, and every transform
    below rescales about it - so the jitter comes out as a comb along the brow. A
    weighted cubic through the centroids is the arc the painter drew, and rescaling
    about that keeps the edge clean.
    """
    rows = np.arange(weights.shape[0], dtype=float)[:, None]
    mass = weights[:, columns].sum(axis=0)
    present = mass > 1e-3
    centroid = np.where(present, (weights[:, columns] * rows).sum(axis=0) / np.maximum(mass, 1e-6), 0.0)
    normalized = (columns - columns.mean()) / max((columns.max() - columns.min()) / 2, 1)
    fit = np.polyfit(normalized[present], centroid[present], 3, w=mass[present])
    return np.polyval(fit, normalized), present


def _vertical_box_blur(field: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return field
    padded = np.pad(field, [(radius, radius)] + [(0, 0)] * (field.ndim - 1), mode="edge")
    cumulative = np.cumsum(padded, axis=0)
    cumulative = np.concatenate([np.zeros((1,) + cumulative.shape[1:]), cumulative], axis=0)
    window = 2 * radius + 1
    return (cumulative[window:] - cumulative[:-window]) / window


def reshaped_brows(face: Face, mood: dict):
    """Remap each brow column vertically: shift, tilt, arch gain and weight.

    A brow is a thin arc, so its whole expressive range is how high it sits, how
    much its inner end lifts or falls, how curved it is and how heavy the line is.
    Working per column on the painted brow keeps its taper and its soft edge
    instead of redrawing it as a stroke.

    The transform runs on the brow's *difference from the skin behind it* rather
    than on its separated alpha and colour. Minimum-alpha separation gives a soft
    edge pixel a low alpha against an extreme colour - the pair composites back
    exactly, but the colour alone is an extrapolation, and resampling the two
    independently breaks the cancellation. The first attempt did exactly that and
    hung a cream halo over every brow it moved. The difference field is bounded and
    resamples cleanly, so the layer is separated once, at the end, from the moved
    result.
    """
    left, top, right, bottom = FEATURE_REGIONS["eyebrows"]
    alpha = face.alpha["eyebrows"]
    skin = face.skin["eyebrows"]
    difference = alpha[..., None] * (face.feature["eyebrows"] - skin)
    height = alpha.shape[0]

    # Thinning samples the source at more than one row per output row, so it is
    # pre-filtered by the same factor; without that a 0.6x brow breaks into stipple.
    weight = max(mood["weight"], 0.05)
    radius = int(np.ceil((1.0 / weight - 1.0) / 2)) if weight < 1.0 else 0
    source = _vertical_box_blur(difference, radius)

    moved = np.zeros_like(difference)
    rows = np.arange(height, dtype=float)

    for side, (first, last) in enumerate(brow_halves(face)):
        columns = np.arange(first, last + 1)
        spine, present = _brow_spine(np.clip(alpha, 0, 1), columns)
        mean_centre = spine[present].mean()

        # The inner end is the one nearer the nose: the right end of the viewer-left
        # brow, the left end of the viewer-right brow.
        span = max(last - first, 1)
        inner = (columns - first) / span if side == 0 else (last - columns) / span
        shift = mood["drop"] + mood["tilt"] * inner + (mood["lopsided"] if side == 1 else 0.0)
        target = mean_centre + (spine - mean_centre) * mood["arch"] + shift

        spread = mood["spread"] * (1 if side == 1 else -1)
        for offset, column in enumerate(columns):
            source_column = column - spread
            if not (0 <= source_column < alpha.shape[1]) or not present[offset]:
                continue
            # Sample where the source column's spine sits, so a shifted column is
            # rescaled about its own arc rather than the target column's.
            source_spine = spine[np.clip(offset - spread, 0, len(spine) - 1)]
            sample = source_spine + (rows - target[offset]) / weight
            valid = (sample >= 0) & (sample <= height - 1)
            low = np.clip(np.floor(sample), 0, height - 1).astype(int)
            high = np.clip(low + 1, 0, height - 1)
            blend = (sample - low)[:, None]
            column_difference = source[:, source_column]
            moved[:, column] = np.where(
                valid[:, None],
                column_difference[low] * (1 - blend) + column_difference[high] * blend,
                0.0,
            )

    observed = np.clip(skin + moved, 0, 255)
    core = _grow(np.abs(moved).max(axis=2) > 26.0).astype(float)
    out_alpha, out_rgb = unmix(observed, skin, core)
    return np.clip(out_alpha, 0, 1), np.clip(out_rgb, 0, 255), (left, top, right, bottom)


def build_eyebrows(face: Face, footprints: dict[str, np.ndarray]) -> list[tuple[str, Image.Image]]:
    built = []
    for index, mood in enumerate(BROW_MOODS, start=1):
        layers = [cover(footprints["eyebrows"], face, "eyebrows"), reshaped_brows(face, mood)]
        built.append((f"eyebrows_{index:03d}_{mood['name']}.png", compose(layers)))
    return built


# ---------------------------------------------------------------------------
# Mouths
# ---------------------------------------------------------------------------

def build_mouth(face: Face, spec: dict, footprints: dict[str, np.ndarray]):
    cx, cy = MOUTH_CENTER
    box = FEATURE_REGIONS["mouth"]
    patch = cover(footprints["mouth"], face, "mouth")
    if spec.get("source"):
        # The approved closed neutral mouth is the one already painted on the
        # master, so it is carried through rather than redrawn beside itself.
        return [patch, (face.alpha["mouth"], face.feature["mouth"], box)]

    brush = Brush(box)
    half = spec["width"] / 2
    curve = spec["curve"]
    weight = spec["weight"]
    opening = spec.get("open")

    if opening:
        top = cy - opening["ry"] + opening["lift"]
        brush.ellipse(cx, cy + opening["lift"], opening["rx"], opening["ry"], MOUTH_INTERIOR)
        if opening["teeth"]:
            brush.ellipse(cx, top + 3, opening["rx"] * 0.86, 4.0, MOUTH_TEETH, softness=0.9)
        if opening["tongue"]:
            brush.ellipse(cx, cy + opening["lift"] + opening["ry"] * 0.45,
                          opening["rx"] * 0.62, opening["ry"] * 0.42, MOUTH_TONGUE, softness=0.9)
        # The lip line rides the opening's upper edge so the two read as one mouth.
        brush.stroke(arc(cx - opening["rx"], cx + opening["rx"], top, curve * 0.3),
                     lambda t: weight * 0.5 * (0.45 + 0.55 * np.sin(np.pi * t)), MOUTH_INK)
    else:
        brush.stroke(arc(cx - half, cx + half, cy, curve),
                     lambda t: weight * 0.5 * (0.3 + 0.7 * np.sin(np.pi * t) ** 0.7), MOUTH_INK)

    return [patch, brush.layer()]


def build_mouths(face: Face, footprints: dict[str, np.ndarray]) -> list[tuple[str, Image.Image]]:
    return [
        (f"mouth_{index:03d}_{spec['name']}.png", compose(build_mouth(face, spec, footprints)))
        for index, spec in enumerate(MOUTHS, start=1)
    ]


# ---------------------------------------------------------------------------
# Expression marks
# ---------------------------------------------------------------------------

def build_mark(spec: dict):
    box = (452, 380, 806, 470)
    brush = Brush(box)
    kind = spec["kind"]
    cx, cy = RIGHT_CHEEK
    colour = spec.get("colour")

    if kind == "blush_strokes":
        for (bx, by) in (LEFT_CHEEK, RIGHT_CHEEK):
            brush.ellipse(bx, by, 33, 16, BLUSH, softness=14.0, opacity=0.34)
            for offset, length in ((-13, 15), (0, 20), (13, 15)):
                brush.stroke(
                    np.array([[bx + offset - 4, by - length / 2], [bx + offset + 4, by + length / 2]]),
                    2.0, BLUSH, opacity=0.75)
    elif kind == "stress":
        # Three slashes fanning off a bracket - the shorthand for a rattled beat.
        for angle in (-1.35, -0.9, -0.45):
            direction = np.array([np.cos(angle), np.sin(angle)])
            start = np.array([cx - 8, cy + 17]) + direction * 4
            brush.stroke(np.stack([start, start + direction * 16]),
                         lambda t: 3.0 * (1 - 0.4 * t), colour)
        brush.stroke(arc(cx - 16, cx + 16, cy - 17, 6),
                     lambda t: 3.0 * np.sin(np.pi * t) ** 0.4, colour)
    elif kind == "gloom":
        for (bx, by) in (LEFT_CHEEK, RIGHT_CHEEK):
            for offset in (-16, -5, 6, 17):
                brush.stroke(np.array([[bx + offset, by - 16.0], [bx + offset, by + 14.0]]),
                             lambda t: 2.6 * (1 - 0.65 * t), colour, opacity=0.7)
    elif kind == "sparkle":
        for (sx, sy, size) in ((cx + 4, cy - 4, 17), (cx - 22, cy + 14, 9), (cx + 20, cy + 16, 7)):
            brush.stroke(np.array([[sx, sy - size], [sx, sy + size]]),
                         lambda t: 3.2 * np.sin(np.pi * t) ** 1.7, colour)
            brush.stroke(np.array([[sx - size, sy], [sx + size, sy]]),
                         lambda t: 3.2 * np.sin(np.pi * t) ** 1.7, colour)
    elif kind == "sweat":
        brush.ellipse(cx, cy + 5, 9, 11, colour, opacity=0.92)
        brush.stroke(np.array([[cx, cy - 15], [cx - 3, cy - 4], [cx, cy + 1]]),
                     lambda t: 1.8 + 5.2 * t, colour, opacity=0.92)
        brush.ellipse(cx - 3, cy + 3, 2.8, 3.8, (255, 255, 255), opacity=0.7)
    elif kind == "anger":
        # The popping-vein mark: two strokes each way, crossed into a hash and
        # tilted off square so it reads as a mark rather than a grid.
        tilt = np.radians(16)
        rotate = np.array([[np.cos(tilt), -np.sin(tilt)], [np.sin(tilt), np.cos(tilt)]])
        for offset in (-6.5, 6.5):
            for along in ((np.array([offset, -14.0]), np.array([offset, 14.0])),
                          (np.array([-14.0, offset]), np.array([14.0, offset]))):
                ends = np.stack([rotate @ point + (cx, cy) for point in along])
                brush.stroke(ends, lambda t: 2.7 * (0.6 + 0.4 * np.sin(np.pi * t)), colour)
    elif kind == "emphasis":
        # A square emphasis mark, set on its corner and ringed by four short
        # radiating dashes so it reads as a struck accent rather than a drawn box.
        half = 10.5
        corners = [(0, -half), (half, 0), (0, half), (-half, 0), (0, -half)]
        for index in range(4):
            (x0, y0), (x1, y1) = corners[index], corners[index + 1]
            brush.stroke(np.array([[cx + x0, cy + y0], [cx + x1, cy + y1]]), 3.0, colour)
        brush.ellipse(cx, cy, 4.0, 4.0, colour, softness=1.2)
        for turn in range(4):
            angle = turn * np.pi / 2 + np.pi / 4
            direction = np.array([np.cos(angle), np.sin(angle)])
            centre = np.array([cx, cy])
            brush.stroke(np.stack([centre + direction * 12, centre + direction * 19]), 2.4, colour)
    elif kind == "curve":
        # Two concentric arcs and a beat mark: the surprise / motion accent.
        for radius, sag in ((12, -9), (20, -14)):
            brush.stroke(arc(cx - radius, cx + radius, cy + 12, sag),
                         lambda t: 2.6 * np.sin(np.pi * t) ** 0.5, colour)
        brush.ellipse(cx, cy + 16, 3.2, 3.2, colour, softness=1.2)
    else:
        raise ValueError(f"unknown mark: {kind}")
    return [brush.layer()]


def build_marks() -> list[tuple[str, Image.Image]]:
    return [
        (f"expression_mark_{index:03d}_{spec['name']}.png", compose(build_mark(spec)))
        for index, spec in enumerate(MARKS, start=1)
    ]


# ---------------------------------------------------------------------------
# Checks and entry point
# ---------------------------------------------------------------------------

def check_palette_distinctness() -> None:
    """No two irises may ship visually identical.

    The backlog repeats three adjectives across its rows. Shipping two identical
    eye pairs under different filenames would be two trait values a holder cannot
    tell apart, so the repeats are separated by temperature and the separation is
    asserted here rather than left to the eye.
    """
    colours = np.array([rgb for _name, rgb in EYE_PALETTES], float)
    for i in range(len(colours)):
        for j in range(i + 1, len(colours)):
            distance = float(np.linalg.norm(colours[i] - colours[j]))
            if distance < MIN_IRIS_DISTANCE:
                raise SystemExit(
                    f"iris {EYE_PALETTES[i][0]} and {EYE_PALETTES[j][0]} are {distance:.1f} apart; "
                    f"the minimum is {MIN_IRIS_DISTANCE}"
                )


def coverage_shortfall(image: Image.Image, footprint: np.ndarray) -> int:
    """Baked pixels this layer leaves showing."""
    alpha = np.asarray(image.convert("RGBA"))[..., 3]
    return int((footprint & (alpha <= 200)).sum())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=Path("incoming/face_traits"))
    args = parser.parse_args(argv)
    out_root = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir

    check_palette_distinctness()
    footprints = baked_footprints()
    face = Face()

    families = {
        "eyes": (build_eyes(face, footprints), footprints["eyes"]),
        "eyebrows": (build_eyebrows(face, footprints), footprints["eyebrows"]),
        "mouths": (build_mouths(face, footprints), footprints["mouth"]),
        "expression_marks": (build_marks(), None),
    }

    summary = []
    for category, (built, footprint) in families.items():
        directory = out_root / category
        directory.mkdir(parents=True, exist_ok=True)
        for name, image in built:
            image.save(directory / name)
            box = image.getchannel("A").getbbox()
            entry = {
                "category": category,
                "name": name,
                "bounds": [box[0], box[1], box[2] - 1, box[3] - 1],
            }
            if footprint is not None:
                entry["uncovered_baked_pixels"] = coverage_shortfall(image, footprint)
            summary.append(entry)

    (out_root / "build_report.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for entry in summary:
        shortfall = entry.get("uncovered_baked_pixels")
        note = "" if shortfall is None else f"  uncovered {shortfall:5d}"
        print(f"{entry['name']:46s} bounds {str(entry['bounds']):26s}{note}")
    print(f"\n{len(summary)} facial traits written to {out_root.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
