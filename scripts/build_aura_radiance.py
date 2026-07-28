#!/usr/bin/env python3
"""Render a soft radiant rear aura analytically (DG-020 gold radiance).

Companion to build_aura_floor_ring.py for the aura cells that are a smooth
falloff rather than a drawn form. Alpha comes from an elliptical distance field,
so the glow is genuinely soft-edged instead of a keyed-out render, and colour
stays bright at every alpha: composited over white it tints, never darkens.

Unlike the floor ring this is not a ground-plane effect, so it is gated with
`rig_gate_report.py --trait` and stays inside the locked character bounds.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

CANVAS = 1254
CENTER_X = 627
MAX_BOUNDS = (233, 129, 1021, 1139)  # inclusive

# Glow field. Seated over the torso and legs so it reads as light behind the
# body, kept clear of the locked bounds on every side.
CENTER_Y = 780.0
RADIUS_X = 290.0
RADIUS_Y = 355.0

PEAK_ALPHA = 175     # soft enough that the body stays readable over it
FALLOFF_POWER = 1.5  # higher = tighter core, longer tail

# Warm gold, pale at the core. Bright at every alpha so the layer only adds light.
CORE_RGB = (255, 250, 232)
EDGE_RGB = (247, 214, 140)

# Named colour variants. Each keeps a pale luminous core grading to a saturated
# edge, so every variant only ever adds light. Gold is DG-020; violet is DG-016.
PALETTES: dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]] = {
    "gold": ((255, 250, 232), (247, 214, 140)),
    "violet": ((248, 240, 255), (176, 132, 236)),
    "blue": ((236, 246, 255), (128, 176, 248)),
    "rose": ((255, 240, 248), (244, 150, 196)),
}


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def shade(distance: float) -> tuple[int, int, int, int] | None:
    """Colour and alpha at a normalized elliptical distance, or None if clear."""
    if distance >= 1.0:
        return None
    intensity = (1.0 - distance) ** FALLOFF_POWER
    alpha = round(PEAK_ALPHA * intensity)
    if alpha <= 0:
        return None
    # Pale core grading to warm gold outward, never darkening toward the edge.
    t = min(1.0, distance)
    rgb = (
        round(lerp(CORE_RGB[0], EDGE_RGB[0], t)),
        round(lerp(CORE_RGB[1], EDGE_RGB[1], t)),
        round(lerp(CORE_RGB[2], EDGE_RGB[2], t)),
    )
    return (*rgb, alpha)


def render() -> Image.Image:
    image = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    pixels = image.load()

    x0 = max(0, int(CENTER_X - RADIUS_X) - 2)
    x1 = min(CANVAS - 1, int(CENTER_X + RADIUS_X) + 2)
    y0 = max(0, int(CENTER_Y - RADIUS_Y) - 2)
    y1 = min(CANVAS - 1, int(CENTER_Y + RADIUS_Y) + 2)

    for y in range(y0, y1 + 1):
        dy = (y + 0.5 - CENTER_Y) / RADIUS_Y
        for x in range(x0, x1 + 1):
            dx = (x + 0.5 - CENTER_X) / RADIUS_X
            value = shade((dx * dx + dy * dy) ** 0.5)
            if value is not None:
                pixels[x, y] = value
    return image


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("images/trait_candidates/rear_auras/aura_rear_006_gold_radiance_candidate_attempt_001.png"),
    )
    parser.add_argument("--peak-alpha", type=int, help="peak alpha at the glow core")
    parser.add_argument("--falloff", type=float, help="falloff power; lower = fuller glow")
    parser.add_argument("--palette", choices=sorted(PALETTES), default="gold",
                        help="named colour variant (gold=DG-020, violet=DG-016)")
    args = parser.parse_args(argv)

    global PEAK_ALPHA, FALLOFF_POWER, CORE_RGB, EDGE_RGB
    CORE_RGB, EDGE_RGB = PALETTES[args.palette]
    if args.peak_alpha is not None:
        PEAK_ALPHA = args.peak_alpha
    if args.falloff is not None:
        FALLOFF_POWER = args.falloff

    image = render()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.out)

    bbox = image.getchannel("A").getbbox()
    left, top, right, bottom = bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1
    within = (
        left >= MAX_BOUNDS[0]
        and top >= MAX_BOUNDS[1]
        and right <= MAX_BOUNDS[2]
        and bottom <= MAX_BOUNDS[3]
    )
    print(f"Wrote {args.out}")
    print(f"  visible bounds [{left},{top},{right},{bottom}] within {list(MAX_BOUNDS)}: {within}")
    print(f"  center X {(left + right) / 2:.1f} (locked {CENTER_X})")
    return 0 if within else 1


if __name__ == "__main__":
    raise SystemExit(main())
