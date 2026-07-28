#!/usr/bin/env python3
"""Build the mouth category: twelve procedural mouths on the locked anchor.

`mouths` held a single asset — the one recovered from the base master — so every
token in the collection shared a mouth. It was the thinnest category in the
library, and the asset catalogue made that obvious at a glance.

These twelve are drawn from signed distance fields at 4x supersampling inside a
144 x 78 band around the mouth anchor (627, 441). Closed mouths are tapered
strokes along a quadratic Bezier; open mouths are filled shapes with an outline
band taken from the same field, a darker interior, and a tongue where the design
calls for one.

Ink is `(136, 65, 33)`, sampled from the darkest pixels of the recovered mouth,
so a procedural mouth and the painted one read as the same hand.

Scope, stated plainly: these are **not** the twelve `FACE` sheet cells. Those are
distinct paintings; DG-095 to DG-106 stay pending. These are shapes built to the
same descriptions so the category stops being one asset wide.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image

CANVAS = 1254
ANCHOR = (627, 441)

# Evaluation window around the anchor. Everything drawn lives inside it.
BAND = (552, 404, 704, 490)
SUPERSAMPLE = 4

# Sampled from the recovered mouth's darkest opaque pixels.
INK = (136, 65, 33)
INNER = (86, 38, 32)
TONGUE = (198, 104, 106)
FANG = (250, 246, 240)

OUTLINE = 2.6

FIRST_NUMBER = 14

# Fang geometry, in pixels: length down from the upper lip and half-width at it.
FANG_LENGTH = 8.0
FANG_WIDTH = 3.6


def bezier(p0, p1, p2, steps: int = 24) -> list[tuple[float, float]]:
    points = []
    for index in range(steps + 1):
        t = index / steps
        u = 1.0 - t
        points.append((
            u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1],
        ))
    return points


def stroke_distance(px: float, py: float, points: list, r0: float, r1: float) -> float:
    """Smallest signed distance to a polyline whose radius tapers end to end."""
    best = 1e9
    span = max(1, len(points) - 1)
    for index in range(span):
        ax, ay = points[index]
        bx, by = points[index + 1]
        dx, dy = bx - ax, by - ay
        length_squared = dx * dx + dy * dy
        t = 0.0 if length_squared == 0 else ((px - ax) * dx + (py - ay) * dy) / length_squared
        t = min(1.0, max(0.0, t))
        cx, cy = ax + dx * t, ay + dy * t
        # Radius interpolates along the whole polyline, not each segment.
        along = (index + t) / span
        radius = r0 + (r1 - r0) * along
        best = min(best, math.hypot(px - cx, py - cy) - radius)
    return best


def ellipse_distance(px: float, py: float, cx: float, cy: float,
                     rx: float, ry: float) -> float:
    nx, ny = (px - cx) / rx, (py - cy) / ry
    length = math.hypot(nx, ny)
    if length == 0.0:
        return -min(rx, ry)
    # Scaled back into pixels so the outline band has a consistent width.
    return (length - 1.0) * min(rx, ry)


def catmull_rom(points: list, steps: int = 10) -> list[tuple[float, float]]:
    """Smooth a control polyline so wavy and cat mouths read as curves."""
    padded = [points[0]] + list(points) + [points[-1]]
    out = []
    for index in range(len(padded) - 3):
        p0, p1, p2, p3 = padded[index:index + 4]
        for step in range(steps):
            t = step / steps
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[i])
                       + (-p0[i] + p2[i]) * t
                       + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2
                       + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3)
                for i in range(2)))
    out.append(tuple(points[-1]))
    return out


def strokes(*specs) -> dict:
    """One or more tapered strokes. Coordinates are offsets from the anchor."""
    x, y = ANCHOR
    built = []
    for points, r0, r1 in specs:
        absolute = [(x + dx, y + dy) for dx, dy in points]
        built.append({"points": catmull_rom(absolute), "r0": r0, "r1": r1})
    return {"kind": "stroke", "strokes": built}


def opening(rx: float, ry: float, tongue: float | None = 0.15, fangs: int = 0,
            drop: float = 0.0, flat_top: float | None = None) -> dict:
    """An open mouth.

    `flat_top` clips the ellipse at that fraction of its height above centre,
    turning it into the D-shape a smiling open mouth actually has: a near-straight
    upper lip over a deep lower curve. Without it every open mouth is an ellipse
    and they measure 0.62-0.70 IoU against each other -- the same mouth at
    different sizes. `tongue` is the fraction of the height below centre where the
    tongue starts, or None for no tongue.
    """
    x, y = ANCHOR
    return {"kind": "fill", "cx": x, "cy": y + drop, "rx": rx, "ry": ry,
            "tongue": tongue, "fangs": fangs, "flat_top": flat_top}


# Twelve designs. An earlier set varied five closed mouths by LENGTH alone --
# short_line, flat_line, tiny_neutral, tiny_curve, soft_curve -- and measured
# 0.94 apart at thumbnail size against a 17.35 spread across the set, which is
# to say they were the same mouth. These vary by shape: curvature sign,
# asymmetry, waviness, and whether the line is broken.
MOUTHS: list[tuple[str, dict]] = [
    ("fine_closed_smile",   strokes(([(-26, 2), (0, 7), (26, 2)], 2.6, 1.4))),
    ("flat_line",           strokes(([(-23, 0), (0, 0), (23, 0)], 2.2, 1.4))),
    ("small_downturned",    strokes(([(-22, 3), (0, -4), (22, 3)], 2.4, 1.4))),
    ("smirk_asymmetric",    strokes(([(-24, -1), (-4, 6), (22, -8)], 2.6, 1.3))),
    ("cat_mouth",           strokes(([(-22, 0), (-11, 7), (0, -3), (11, 7), (22, 0)],
                                     2.4, 2.0))),
    ("wavy_unsure",         strokes(([(-24, 3), (-12, -3), (0, 3), (12, -3), (24, 3)],
                                     2.3, 1.8))),
    ("parted_line",         strokes(([(-24, 1), (-14, 3), (-6, 3)], 2.4, 1.6),
                                    ([(6, 3), (14, 3), (24, 1)], 1.6, 2.4))),
    # Open mouths differ by silhouette, not size: two D-shaped grins, a round
    # "o", a tall pout, and a wide flat snarl.
    ("small_open_smile",    opening(16, 11, tongue=0.15, flat_top=0.45)),
    ("wide_open_smile",     opening(30, 17, tongue=0.10, flat_top=0.55)),
    ("tiny_round",          opening(10, 11, tongue=None)),
    ("pink_open_pout",      opening(11, 15, tongue=-0.55, drop=1)),
    ("wide_open_fangs",     opening(23, 13, tongue=0.34, fangs=2, flat_top=0.45)),
]


def render(design: dict) -> Image.Image:
    x0, y0, x1, y1 = BAND
    width, height = (x1 - x0) * SUPERSAMPLE, (y1 - y0) * SUPERSAMPLE
    step = 1.0 / SUPERSAMPLE

    layers = {name: Image.new("L", (width, height), 0)
              for name in ("ink", "inner", "tongue", "fang")}
    paint = {name: image.load() for name, image in layers.items()}

    for sy in range(height):
        py = y0 + sy * step
        for sx in range(width):
            px = x0 + sx * step

            if design["kind"] == "stroke":
                for spec in design["strokes"]:
                    if stroke_distance(px, py, spec["points"],
                                       spec["r0"], spec["r1"]) <= 0.0:
                        paint["ink"][sx, sy] = 255
                        break
                continue

            distance = ellipse_distance(px, py, design["cx"], design["cy"],
                                        design["rx"], design["ry"])
            if design["flat_top"] is not None:
                # Intersection with a half-plane: the larger distance wins.
                clip = (design["cy"] - design["ry"] * design["flat_top"]) - py
                distance = max(distance, clip)
            if distance > 0.0:
                continue
            if distance > -OUTLINE:
                paint["ink"][sx, sy] = 255
                continue
            paint["inner"][sx, sy] = 255
            # Tongue fills the lower third of the opening.
            if (design["tongue"] is not None
                    and py > design["cy"] + design["ry"] * design["tongue"]):
                paint["tongue"][sx, sy] = 255
            if design["fangs"]:
                # Fangs hang from the shape's actual top edge. Measuring from the
                # unclipped ellipse top left them 1 px of room on a flat-topped
                # design and they never appeared.
                clip = design["flat_top"] if design["flat_top"] is not None else 1.0
                depth = py - (design["cy"] - design["ry"] * clip)
                if 0.0 <= depth < FANG_LENGTH:
                    for side in range(design["fangs"]):
                        offset = design["rx"] * (-0.44 if side == 0 else 0.44)
                        half = FANG_WIDTH - depth * (FANG_WIDTH / FANG_LENGTH)
                        if abs(px - (design["cx"] + offset)) < half:
                            paint["fang"][sx, sy] = 255

    result = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    for name, colour in (("inner", INNER), ("tongue", TONGUE),
                         ("fang", FANG), ("ink", INK)):
        mask = layers[name].resize((x1 - x0, y1 - y0), Image.BOX)
        patch = Image.new("RGBA", (x1 - x0, y1 - y0), (*colour, 0))
        patch.putalpha(mask)
        full = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
        full.paste(patch, (x0, y0))
        result.alpha_composite(full)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path,
                        default=Path("images/trait_candidates/mouths"))
    parser.add_argument("--only", help="build a single design by name")
    args = parser.parse_args(argv)

    if args.out_dir.resolve().is_relative_to(Path("assets").resolve()):
        raise SystemExit("refusing to write candidates under assets/")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # 001-012 are reserved for the painted FACE sheet cells and 013 is the
    # mouth recovered from the base master, so these start at 014.
    for index, (name, design) in enumerate(MOUTHS, start=FIRST_NUMBER):
        if args.only and args.only != name:
            continue
        image = render(design)
        destination = args.out_dir / f"mouth_{index:03d}_{name}.png"
        image.save(destination)
        bbox = image.getchannel("A").getbbox()
        centre = (bbox[0] + bbox[2] - 1) / 2 if bbox else 0
        print(f"  {name:22s} bounds {str(bbox):26s} centre X {centre:.1f}")

    print(f"\nAnchor {ANCHOR}; locked centre X 627.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
