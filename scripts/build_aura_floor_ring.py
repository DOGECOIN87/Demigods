#!/usr/bin/env python3
"""Render the DG-015 blue elliptical floor ring analytically at vector quality.

The ring is pure geometry, so it does not need an image generator. Alpha comes
from a signed distance to the centerline ellipse rather than from keying a
rendered background, which is what produced the dark matte fringe in candidate
attempt 001. Colour stays bright at every alpha value, so the layer only ever
adds light: composited over white it tints, never darkens.

Emits a matching SVG so the design stays re-renderable at any size.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

# Locked rig values (config/collection.json).
CANVAS = 1254
CENTER_X = 627
FOOT_BASELINE_Y = 1139
MAX_BOUNDS = (233, 129, 1021, 1139)  # inclusive

# Ring geometry. The near edge stops just above the foot baseline because the
# trait gate measures bounds from every pixel whose alpha is not exactly zero.
RADIUS_X = 300.0
RADIUS_Y = 78.0
BAND = 46.0          # solid band thickness in pixels
GLOW = 26.0          # falloff beyond the band, reaching exactly zero alpha
BOTTOM_MARGIN = 3    # px of clearance under the foot baseline

INTERIOR_ALPHA = 16  # faint luminous wash inside the ring; never a solid fill

# Palette sampled from the reference cell: pale blue-white inner edge grading to
# cornflower/periwinkle at the outer edge.
INNER_RGB = (226, 240, 255)
MID_RGB = (150, 190, 252)
OUTER_RGB = (120, 162, 248)
GLOW_RGB = (132, 178, 250)
WASH_RGB = (232, 244, 255)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c0: tuple[int, int, int], c1: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return (
        round(lerp(c0[0], c1[0], t)),
        round(lerp(c0[1], c1[1], t)),
        round(lerp(c0[2], c1[2], t)),
    )


def center_y() -> float:
    """Place the ring so its lowest glow pixel clears the foot baseline."""
    half_height = RADIUS_Y + BAND / 2.0 + GLOW
    return FOOT_BASELINE_Y - BOTTOM_MARGIN - half_height


def signed_distance(x: float, y: float, cy: float) -> float:
    """First-order signed pixel distance to the centerline ellipse."""
    dx = (x - CENTER_X) / RADIUS_X
    dy = (y - cy) / RADIUS_Y
    value = dx * dx + dy * dy - 1.0
    gx = 2.0 * (x - CENTER_X) / (RADIUS_X * RADIUS_X)
    gy = 2.0 * (y - cy) / (RADIUS_Y * RADIUS_Y)
    gradient = (gx * gx + gy * gy) ** 0.5
    if gradient == 0.0:
        return -RADIUS_Y
    return value / gradient


def shade(distance: float) -> tuple[int, int, int, int] | None:
    """Colour and alpha for a signed distance, or None for full transparency."""
    half = BAND / 2.0
    magnitude = abs(distance)

    if magnitude <= half:
        # Solid band: pale inner edge grading to saturated outer edge.
        t = (distance + half) / BAND  # 0 at inner edge, 1 at outer edge
        rgb = mix(INNER_RGB, MID_RGB, t * 2.0) if t < 0.5 else mix(MID_RGB, OUTER_RGB, (t - 0.5) * 2.0)
        return (*rgb, 255)

    if magnitude <= half + GLOW:
        # Falloff. Squared ramp reaches exactly zero at the glow limit, so no
        # alpha-1 dust survives outside the asset.
        t = (magnitude - half) / GLOW
        alpha = round(255 * (1.0 - t) ** 2)
        if alpha <= 0:
            return None
        return (*GLOW_RGB, alpha)

    if distance < 0:
        # Interior wash: faint, bright, and open rather than a filled disc.
        fade = min(1.0, (magnitude - half) / max(RADIUS_Y, 1.0))
        alpha = round(INTERIOR_ALPHA * (1.0 - fade))
        if alpha <= 0:
            return None
        return (*WASH_RGB, alpha)

    return None


def render() -> Image.Image:
    image = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    pixels = image.load()
    cy = center_y()

    reach = RADIUS_X + BAND / 2.0 + GLOW + 2
    x0 = max(0, int(CENTER_X - reach))
    x1 = min(CANVAS - 1, int(CENTER_X + reach))
    y0 = max(0, int(cy - RADIUS_Y - BAND / 2.0 - GLOW - 2))
    y1 = min(CANVAS - 1, int(cy + RADIUS_Y + BAND / 2.0 + GLOW + 2))

    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            # Sample at the pixel centre for correct analytic anti-aliasing.
            value = shade(signed_distance(x + 0.5, y + 0.5, cy))
            if value is not None:
                pixels[x, y] = value
    return image


def build_svg() -> str:
    cy = center_y()
    half = BAND / 2.0
    inner = RADIUS_Y - half
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS}" height="{CANVAS}" viewBox="0 0 {CANVAS} {CANVAS}">
  <defs>
    <linearGradient id="band" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="rgb{INNER_RGB}"/>
      <stop offset="0.5" stop-color="rgb{MID_RGB}"/>
      <stop offset="1" stop-color="rgb{OUTER_RGB}"/>
    </linearGradient>
    <radialGradient id="wash">
      <stop offset="0" stop-color="rgb{WASH_RGB}" stop-opacity="{INTERIOR_ALPHA / 255:.3f}"/>
      <stop offset="1" stop-color="rgb{WASH_RGB}" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow" x="-25%" y="-60%" width="150%" height="220%">
      <feGaussianBlur stdDeviation="{GLOW / 2:.1f}"/>
    </filter>
  </defs>
  <ellipse cx="{CENTER_X}" cy="{cy:.1f}" rx="{RADIUS_X - half:.1f}" ry="{inner:.1f}" fill="url(#wash)"/>
  <ellipse cx="{CENTER_X}" cy="{cy:.1f}" rx="{RADIUS_X:.1f}" ry="{RADIUS_Y:.1f}"
           fill="none" stroke="rgb{GLOW_RGB}" stroke-width="{BAND + GLOW:.1f}"
           opacity="0.55" filter="url(#glow)"/>
  <ellipse cx="{CENTER_X}" cy="{cy:.1f}" rx="{RADIUS_X:.1f}" ry="{RADIUS_Y:.1f}"
           fill="none" stroke="url(#band)" stroke-width="{BAND:.1f}"/>
</svg>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("images/trait_candidates/rear_auras/aura_rear_001_blue_floor_ring_candidate_attempt_004.png"),
    )
    parser.add_argument("--svg", type=Path, help="also write the vector source")
    parser.add_argument("--band", type=float, help="solid band thickness in px")
    parser.add_argument("--glow", type=float, help="falloff width beyond the band in px")
    parser.add_argument("--radius-x", type=float, help="ellipse semi-major axis in px")
    parser.add_argument("--radius-y", type=float, help="ellipse semi-minor axis in px")
    args = parser.parse_args(argv)

    # Shape overrides let the ring be tuned without editing the module.
    global BAND, GLOW, RADIUS_X, RADIUS_Y
    if args.band is not None:
        BAND = args.band
    if args.glow is not None:
        GLOW = args.glow
    if args.radius_x is not None:
        RADIUS_X = args.radius_x
    if args.radius_y is not None:
        RADIUS_Y = args.radius_y

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

    if args.svg:
        args.svg.parent.mkdir(parents=True, exist_ok=True)
        args.svg.write_text(build_svg(), encoding="utf-8")
        print(f"Wrote {args.svg}")

    return 0 if within else 1


if __name__ == "__main__":
    raise SystemExit(main())
