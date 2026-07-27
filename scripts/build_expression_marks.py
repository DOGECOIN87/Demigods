#!/usr/bin/env python3
"""Render the eight expression-mark glyphs (DG-107 to DG-114) procedurally.

Expression marks are flat anime emote glyphs — blush strokes, a sweat drop, an
anger cross, a sparkle — not painted artwork. Drawing them from primitives at 4x
and downsampling gives cleaner, more consistent edges than an image generator
manages at this size, and every glyph lands on an exact rig anchor.

Completing this category also unblocks generation: the collection space is the
product of non-empty category counts, currently 4 x 6 x 1 x 5 = 120. Eight
expression marks take it to 960, past the 777 supply.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw

CANVAS = 1254
CENTER_X = 627
MAX_BOUNDS = (233, 129, 1021, 1139)  # inclusive

SS = 4  # supersample factor; downsampling is what produces the clean edges

# Face anchors from config/collection.json.
EYE_LINE_Y = 367
HEAD_CENTER_Y = 343

# Cheek and temple positions, measured from the base body silhouette.
CHEEK_Y = 415
LEFT_CHEEK_X = 512
RIGHT_CHEEK_X = 742
TEMPLE_X = 792
TEMPLE_Y = 236


def tile(size: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    return image, ImageDraw.Draw(image)


def place(canvas: Image.Image, tile_image: Image.Image, center: tuple[int, int]) -> None:
    size = tile_image.width // SS
    reduced = tile_image.resize((size, size), Image.LANCZOS)
    canvas.alpha_composite(reduced, (center[0] - size // 2, center[1] - size // 2))


def blush_cluster(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """Three stacked tapered strokes, the standard blush glyph."""
    mid = size * SS // 2
    for index, (width, offset) in enumerate([(0.62, -0.10), (0.78, 0.0), (0.60, 0.10)]):
        half = int(size * SS * width / 2)
        y = int(mid + size * SS * offset)
        thickness = int(size * SS * 0.052)
        draw.rounded_rectangle(
            [mid - half, y - thickness, mid + half, y + thickness],
            radius=thickness,
            fill=(*colour, 235 - index * 10),
        )


def draw_sparkle(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """Four-point star with concave sides."""
    mid = size * SS // 2
    long_arm = size * SS * 0.46
    waist = size * SS * 0.085
    points = []
    for step in range(4):
        angle = math.radians(step * 90)
        points.append((mid + long_arm * math.cos(angle), mid + long_arm * math.sin(angle)))
        mid_angle = math.radians(step * 90 + 45)
        points.append((mid + waist * math.cos(mid_angle), mid + waist * math.sin(mid_angle)))
    draw.polygon(points, fill=(*colour, 245))
    draw.ellipse(
        [mid - waist * 0.9, mid - waist * 0.9, mid + waist * 0.9, mid + waist * 0.9],
        fill=(255, 255, 250, 240),
    )


def draw_anger_cross(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """The anime anger vein: four tapered lobes meeting at a central knot."""
    mid = size * SS // 2
    arm = size * SS * 0.30
    for angle_deg in (45, 135, 225, 315):
        angle = math.radians(angle_deg)
        tip = (mid + arm * math.cos(angle), mid + arm * math.sin(angle))
        spread = math.radians(26)
        base = size * SS * 0.115
        left = (mid + base * math.cos(angle - spread), mid + base * math.sin(angle - spread))
        right = (mid + base * math.cos(angle + spread), mid + base * math.sin(angle + spread))
        waist = size * SS * 0.20
        mid_l = (mid + waist * math.cos(angle - spread * 0.75),
                 mid + waist * math.sin(angle - spread * 0.75))
        mid_r = (mid + waist * math.cos(angle + spread * 0.75),
                 mid + waist * math.sin(angle + spread * 0.75))
        draw.polygon([left, mid_l, tip, mid_r, right], fill=(*colour, 245))
    knot = size * SS * 0.105
    draw.ellipse([mid - knot, mid - knot, mid + knot, mid + knot], fill=(*colour, 255))


def draw_sweat_drop(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    mid = size * SS // 2
    radius = size * SS * 0.26
    top = mid - size * SS * 0.42
    draw.polygon(
        [(mid, top), (mid + radius * 0.92, mid + radius * 0.30), (mid - radius * 0.92, mid + radius * 0.30)],
        fill=(*colour, 225),
    )
    draw.ellipse([mid - radius, mid - radius * 0.22, mid + radius, mid + radius * 1.78], fill=(*colour, 225))
    highlight = radius * 0.30
    draw.ellipse(
        [mid - radius * 0.45 - highlight, mid + radius * 0.35 - highlight,
         mid - radius * 0.45 + highlight, mid + radius * 0.35 + highlight],
        fill=(255, 255, 255, 215),
    )


def draw_gloom_lines(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """Vertical hatching that fades downward."""
    span = size * SS
    count = 7
    for index in range(count):
        x = int(span * (0.20 + index * 0.10))
        width = int(span * 0.017)
        top = int(span * 0.12)
        bottom = int(span * (0.60 + 0.10 * math.sin(index * 1.1)))
        for step in range(24):
            y0 = top + (bottom - top) * step // 24
            y1 = top + (bottom - top) * (step + 1) // 24
            alpha = int(255 * (1 - step / 24) ** 0.8)
            if alpha > 0:
                draw.rectangle([x - width, y0, x + width, y1], fill=(*colour, alpha))


def draw_stress_marks(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """Short radiating emphasis strokes plus a small accent dot."""
    span = size * SS
    mid = span // 2
    angle = math.radians(64)
    width = int(span * 0.048)
    for index, (offset, length) in enumerate(((-0.17, 0.30), (0.0, 0.38), (0.17, 0.28))):
        cx = mid + span * offset
        half = span * length / 2
        draw.line(
            [(cx - half * math.cos(angle), mid - half * math.sin(angle)),
             (cx + half * math.cos(angle), mid + half * math.sin(angle))],
            fill=(*colour, 245 - index * 12), width=width,
        )


def draw_emphasis_square(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """Rounded emphasis tile with a soft inner shine and a lighter rim."""
    mid = size * SS // 2
    half = size * SS * 0.245
    radius = size * SS * 0.075
    draw.rounded_rectangle(
        [mid - half, mid - half, mid + half, mid + half],
        radius=radius, fill=(*colour, 205),
    )
    inner = half * 0.62
    lighter = tuple(min(255, channel + 26) for channel in colour)
    draw.rounded_rectangle(
        [mid - inner, mid - inner, mid + inner, mid + inner],
        radius=radius * 0.7, fill=(*lighter, 255),
    )


def draw_curved_mark(draw: ImageDraw.ImageDraw, size: int, colour: tuple[int, int, int]) -> None:
    """Curved motion swoosh, thick at the centre and tapering at both ends."""
    span = size * SS
    steps = 40
    for step in range(steps):
        t0, t1 = step / steps, (step + 1) / steps
        taper = math.sin(math.pi * (t0 * 0.9 + 0.05))
        width = max(1, int(span * 0.105 * taper))
        a0 = math.radians(205 + 130 * t0)
        a1 = math.radians(205 + 130 * t1)
        radius = span * 0.34
        draw.line(
            [(span / 2 + radius * math.cos(a0), span / 2 + radius * math.sin(a0)),
             (span / 2 + radius * math.cos(a1), span / 2 + radius * math.sin(a1))],
            fill=(*colour, 240), width=width,
        )


def render_blush() -> Image.Image:
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    for x in (LEFT_CHEEK_X, RIGHT_CHEEK_X):
        image, draw = tile(150)
        blush_cluster(draw, 150, (255, 138, 165))
        place(canvas, image, (x, CHEEK_Y))
    return canvas


def single(size: int, centre: tuple[int, int], drawer, colour) -> Image.Image:
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    image, draw = tile(size)
    drawer(draw, size, colour)
    place(canvas, image, centre)
    return canvas


MARKS: list[tuple[str, str, callable]] = [
    ("expression_mark_001_pink_blush_strokes", "DG-107", render_blush),
    ("expression_mark_002_yellow_stress_marks", "DG-108",
     lambda: single(160, (TEMPLE_X + 10, TEMPLE_Y + 10), draw_stress_marks, (206, 198, 66))),
    ("expression_mark_003_dark_gloom_lines", "DG-109",
     lambda: single(230, (627, HEAD_CENTER_Y - 88), draw_gloom_lines, (96, 100, 118))),
    ("expression_mark_004_gold_sparkle", "DG-110",
     lambda: single(190, (486, 230), draw_sparkle, (255, 206, 84))),
    ("expression_mark_005_cyan_sweat_drop", "DG-111",
     lambda: single(170, (TEMPLE_X + 6, TEMPLE_Y + 34), draw_sweat_drop, (146, 216, 226))),
    ("expression_mark_006_pink_anger_cross", "DG-112",
     lambda: single(150, (TEMPLE_X + 2, TEMPLE_Y + 4), draw_anger_cross, (240, 96, 124))),
    ("expression_mark_007_yellow_green_emphasis", "DG-113",
     lambda: single(170, (486, 250), draw_emphasis_square, (206, 224, 108))),
    ("expression_mark_008_pink_curved_mark", "DG-114",
     lambda: single(210, (766, 224), draw_curved_mark, (255, 150, 182))),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path,
                        default=Path("images/trait_candidates/expression_marks"))
    args = parser.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for name, backlog_id, builder in MARKS:
        image = builder()
        bbox = image.getchannel("A").getbbox()
        if bbox is None:
            print(f"  {backlog_id} {name}: FAIL — fully transparent")
            failures += 1
            continue
        left, top, right, bottom = bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1
        within = (left >= MAX_BOUNDS[0] and top >= MAX_BOUNDS[1]
                  and right <= MAX_BOUNDS[2] and bottom <= MAX_BOUNDS[3])
        destination = args.out_dir / f"{name}.png"
        image.save(destination)
        print(f"  {backlog_id} {name}: [{left},{top},{right},{bottom}] within bounds: {within}")
        if not within:
            failures += 1

    print(f"\n{len(MARKS) - failures}/{len(MARKS)} marks rendered inside the locked bounds.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
