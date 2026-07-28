#!/usr/bin/env python3
"""Build the front hair layer: a scalp cap and fringe over the bald head.

`hair_back` sits behind the head and, measured against the registered base body,
covers **0%** of the scalp at every row from Y 150 to Y 340 — all eight
registered assets are wisps either side of the skull. The base master is
deliberately bald, so every token in the collection currently renders as a bald
head. That is the same class of defect as the outfit blocker, which was "reads as
unclothed"; this one reads as bald.

The cap is taken from the base body's own alpha rather than drawn as an ellipse,
so it follows the skull exactly and cannot drift from it. It is dilated a few
pixels so the hair sits proud of the scalp instead of looking painted onto it.

The fringe is drawn as tapered capsules — signed distance to a segment minus a
radius that shrinks along it — evaluated supersampled inside the hair band only.
Supersampling the whole canvas would be 14 million evaluations in pure Python;
the band is 380 x 330, which is a hundredth of that.

## Where the fringe has to stop

The recovered eyebrows occupy Y 292-343, and `hair_front` composites at layer 12,
above `eyebrows` at 09. A fringe reaching the brows would hide a whole category.
Locks therefore tip at Y 285-305: low enough to read as a fringe, high enough
that the brows survive underneath.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

CANVAS = 1254
CENTER_X = 627

# Evaluation window. Everything the layer draws lives inside it.
BAND = (430, 125, 830, 470)
SUPERSAMPLE = 3

BASE_BODY = Path("assets/base_bodies/base_body_001_neutral_master.png")

# How far the cap stands off the skull, and where it hands over to the fringe.
# The handover is a curve, not a row: cropping the cap at a single Y drew a hard
# horizontal line straight across the face, which is what a first attempt did.
# It sits high at the centre and low at the temples, so the locks hang over the
# forehead while the cap keeps covering the sides of the skull.
CAP_LIFT = 4
CAP_CENTER_Y = 232
CAP_TEMPLE_Y = 322
CAP_HALF_SPAN = 200

# Brow top measured on the recovered eyebrow layer. Locks must clear it.
BROW_TOP_Y = 292

# Fringe locks: (start x, start y, end x, end y, start radius, end radius).
# A centre part with locks sweeping outward. They overlap laterally on purpose --
# a sparse set leaves scalp showing between the tips and reads as a torn edge
# rather than a fringe. Tip depths alternate so the hairline is jagged.
LOCKS = [
    (627, 196, 566, 300, 32, 4),
    (627, 196, 690, 300, 32, 4),
    (604, 200, 536, 286, 30, 4),
    (650, 200, 720, 286, 30, 4),
    (580, 206, 508, 302, 30, 4),
    (674, 206, 748, 302, 30, 4),
    (556, 214, 484, 288, 28, 4),
    (698, 214, 772, 288, 28, 4),
    (532, 226, 466, 300, 28, 4),
    (722, 226, 790, 300, 28, 4),
    (612, 200, 592, 306, 22, 4),
    (642, 200, 664, 306, 22, 4),
    (508, 244, 458, 296, 26, 4),
    (746, 244, 798, 296, 26, 4),
]

# Side sweeps in front of the ears, past the cap.
SIDE_LOCKS = [
    (476, 250, 456, 404, 26, 8),
    (778, 250, 798, 404, 26, 8),
]

# Three-stop palettes, matched to the registered hair_back colours so a token can
# pair front and back.
PALETTES: dict[str, dict[str, tuple[int, int, int]]] = {
    "silver": {"shadow": (86, 88, 104), "mid": (150, 152, 170), "light": (226, 228, 240)},
    "gold":   {"shadow": (120, 84, 34), "mid": (208, 162, 74), "light": (252, 232, 176)},
    "black":  {"shadow": (18, 18, 24),  "mid": (48, 48, 60),   "light": (122, 124, 142)},
    "violet": {"shadow": (58, 36, 86),  "mid": (118, 84, 168), "light": (204, 178, 240)},
    "blue":   {"shadow": (24, 44, 92),  "mid": (58, 96, 168),  "light": (166, 202, 246)},
    "pink":   {"shadow": (128, 54, 92), "mid": (216, 116, 160), "light": (252, 204, 224)},
    "teal":   {"shadow": (18, 74, 78),  "mid": (46, 138, 136), "light": (168, 226, 220)},
    "red":    {"shadow": (94, 24, 28),  "mid": (168, 52, 50),  "light": (238, 150, 132)},
}

# Key light sits upper-left, matching the collection's lighting contract.
LIGHT = (548, 196)
LIGHT_RADIUS = 210.0


def tapered_capsule(px: float, py: float, lock: tuple) -> float:
    """Signed distance to a segment whose radius tapers from end to end."""
    ax, ay, bx, by, ra, rb = lock
    dx, dy = bx - ax, by - ay
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        t = 0.0
    else:
        t = ((px - ax) * dx + (py - ay) * dy) / length_squared
        t = min(1.0, max(0.0, t))
    cx, cy = ax + dx * t, ay + dy * t
    radius = ra + (rb - ra) * t
    return math.hypot(px - cx, py - cy) - radius


def fringe_mask(locks: list[tuple]) -> Image.Image:
    """Render the locks supersampled inside the band, then downsample."""
    x0, y0, x1, y1 = BAND
    width, height = (x1 - x0) * SUPERSAMPLE, (y1 - y0) * SUPERSAMPLE
    big = Image.new("L", (width, height), 0)
    paint = big.load()
    step = 1.0 / SUPERSAMPLE

    for sy in range(height):
        py = y0 + sy * step
        for sx in range(width):
            px = x0 + sx * step
            for lock in locks:
                if tapered_capsule(px, py, lock) <= 0.0:
                    paint[sx, sy] = 255
                    break

    small = big.resize((x1 - x0, y1 - y0), Image.BOX)
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    mask.paste(small, (x0, y0))
    return mask


def cap_bottom(x: int) -> float:
    """Where the cap gives way to the fringe, as a curve across the head."""
    offset = min(1.0, abs(x - CENTER_X) / CAP_HALF_SPAN)
    # Cosine so the transition is smooth at the centre and at the temples.
    blend = (1.0 - math.cos(offset * math.pi)) / 2.0
    return CAP_CENTER_Y + (CAP_TEMPLE_Y - CAP_CENTER_Y) * blend


def cap_mask(base: Image.Image) -> Image.Image:
    """The skull dome, taken from the base body's own alpha."""
    alpha = base.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    grown = alpha.filter(ImageFilter.MaxFilter(CAP_LIFT * 2 + 1))
    read = grown.load()

    mask = Image.new("L", (CANVAS, CANVAS), 0)
    paint = mask.load()
    x0, y0, x1, y1 = BAND
    for x in range(x0, x1):
        limit = cap_bottom(x)
        for y in range(y0, min(y1, int(limit) + 1)):
            if read[x, y]:
                paint[x, y] = 255
    return mask


def shade(mask: Image.Image, palette: dict[str, tuple[int, int, int]]) -> Image.Image:
    """Three-stop ramp driven by distance from the key light."""
    shadow, mid, light = palette["shadow"], palette["mid"], palette["light"]
    result = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    read = mask.load()
    write = result.load()
    x0, y0, x1, y1 = BAND

    for y in range(y0, y1):
        for x in range(x0, x1):
            alpha = read[x, y]
            if alpha == 0:
                continue
            distance = math.hypot(x - LIGHT[0], y - LIGHT[1]) / LIGHT_RADIUS
            t = min(1.0, max(0.0, 1.0 - distance))
            if t < 0.5:
                local = t / 0.5
                colour = tuple(round(shadow[i] + (mid[i] - shadow[i]) * local)
                               for i in range(3))
            else:
                local = (t - 0.5) / 0.5
                colour = tuple(round(mid[i] + (light[i] - mid[i]) * local)
                               for i in range(3))
            write[x, y] = (colour[0], colour[1], colour[2], alpha)
    return result


def build(palette_name: str, base: Image.Image) -> Image.Image:
    mask = cap_mask(base)
    fringe = fringe_mask(LOCKS + SIDE_LOCKS)
    # Union by taking the brighter of the two, NOT by pasting one over the other.
    # `paste(fringe, mask=fringe)` blends a lock's own antialiased edge against
    # the opaque cap -- a 180-alpha edge pixel over 255 lands at 202 -- which
    # cut a translucent scalloped groove into the dome wherever a lock outline
    # fell inside the cap. It showed as a wavy seam across the crown.
    combined = ImageChops.lighter(mask, fringe)
    combined = combined.filter(ImageFilter.GaussianBlur(0.6))
    return shade(combined, PALETTES[palette_name])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE_BODY)
    parser.add_argument("--out-dir", type=Path,
                        default=Path("images/trait_candidates/hair_front"))
    parser.add_argument("--palette", choices=sorted(PALETTES))
    args = parser.parse_args(argv)

    if args.out_dir.resolve().is_relative_to(Path("assets").resolve()):
        raise SystemExit("refusing to write candidates under assets/")

    base = Image.open(args.base).convert("RGBA")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    names = [args.palette] if args.palette else sorted(PALETTES)

    for index, name in enumerate(names, start=1):
        image = build(name, base)
        destination = args.out_dir / f"hair_front_{index:03d}_fringe_{name}.png"
        image.save(destination)
        bbox = image.getchannel("A").getbbox()
        print(f"  {name:7s} -> {destination.name}  bounds {bbox}")

    print(f"\n{len(names)} front-hair layers. Brow top is Y {BROW_TOP_Y}; "
          "locks must clear it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
