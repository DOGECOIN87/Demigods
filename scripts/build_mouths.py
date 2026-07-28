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


def curve(dx: float, dip: float, half: float, r0: float, r1: float) -> dict:
    """A closed mouth: an arc through the anchor. Positive dip curves upward."""
    x, y = ANCHOR
    return {
        "kind": "stroke",
        "points": bezier((x - half, y - dx), (x, y + dip), (x + half, y - dx)),
        "r0": r0, "r1": r1,
    }


def opening(rx: float, ry: float, tongue: bool = True, fang: bool = False,
            drop: float = 0.0) -> dict:
    x, y = ANCHOR
    return {"kind": "fill", "cx": x, "cy": y + drop, "rx": rx, "ry": ry,
            "tongue": tongue, "fang": fang}


# Twelve designs, tracking the backlog's descriptions of the FACE sheet cells.
MOUTHS: list[tuple[str, dict]] = [
    ("fine_closed_neutral",  curve(-2, 12, 26, 2.6, 1.4)),
    ("short_line",           curve(0, 0, 15, 2.2, 1.4)),
    ("flat_line",            curve(0, 0, 23, 2.2, 1.4)),
    ("soft_curve",           curve(-1, 8, 18, 2.4, 1.4)),
    # A 3 px arc reads as a straight line at face scale; this drops 7 px, which
    # matches the smile's rise and is the smallest that reads as a frown.
    ("small_downturned",     curve(-3, -11, 22, 2.4, 1.4)),
    ("tiny_neutral",         curve(0, 0, 8, 2.0, 1.6)),
    ("tiny_curve",           curve(-1, 5, 11, 2.2, 1.4)),
    ("small_open_smile",     opening(19, 12, tongue=True)),
    ("wide_open_smile",      opening(29, 15, tongue=True)),
    ("tiny_round",           opening(9, 11, tongue=False)),
    ("pink_open_pout",       opening(13, 11, tongue=True, drop=1)),
    ("small_dark_open_fang", opening(17, 13, tongue=True, fang=True)),
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
                if stroke_distance(px, py, design["points"],
                                   design["r0"], design["r1"]) <= 0.0:
                    paint["ink"][sx, sy] = 255
                continue

            distance = ellipse_distance(px, py, design["cx"], design["cy"],
                                        design["rx"], design["ry"])
            if distance > 0.0:
                continue
            if distance > -OUTLINE:
                paint["ink"][sx, sy] = 255
                continue
            paint["inner"][sx, sy] = 255
            # Tongue fills the lower third of the opening.
            if design["tongue"] and py > design["cy"] + design["ry"] * 0.15:
                paint["tongue"][sx, sy] = 255
            if design["fang"] and py < design["cy"] - design["ry"] * 0.25:
                fang_x = design["cx"] - design["rx"] * 0.42
                if abs(px - fang_x) < 3.4 - (py - (design["cy"] - design["ry"])) * 0.30:
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
