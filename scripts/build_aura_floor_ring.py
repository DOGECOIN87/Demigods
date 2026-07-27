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

# Ring geometry. The ring is seated on the foot baseline so its far arc passes
# behind the ankles and its near arc in front of the toes, which is what makes
# the character read as standing inside it. That puts the near arc below Y 1139,
# so the candidate is gated with `rig_gate_report.py --floor-aura`.
RADIUS_X = 300.0
RADIUS_Y = 72.0
BAND = 7.0           # stroke thickness of each ring in pixels
GLOW = 9.0           # falloff beyond the stroke, reaching exactly zero alpha
CENTER_Y_OVERRIDE: float | None = None

# Second, slightly larger ring set a little lower, as in the approved references.
OUTER_SCALE_X = 1.073
OUTER_SCALE_Y = 1.103
OUTER_OFFSET_Y = 10.0

INTERIOR_ALPHA = 0   # open interior; the double ring carries the design

# Palettes sampled from images/reference_sheets/floor_ring_aura_variants_sheet.png.
# Only the pure-neon cells are listed: fire, lightning, ice, smoke, water, and
# cosmic rings carry organic texture that a distance field cannot express, and
# those are routed to the image generator instead.
PALETTES: dict[str, dict[str, tuple[int, int, int]]] = {
    "blue": {"inner": (226, 240, 255), "mid": (150, 190, 252), "outer": (120, 162, 248),
             "glow": (132, 178, 250), "wash": (232, 244, 255)},
    "green": {"inner": (232, 255, 236), "mid": (140, 240, 150), "outer": (86, 214, 104),
              "glow": (120, 235, 134), "wash": (236, 255, 240)},
    "gold": {"inner": (255, 250, 226), "mid": (255, 219, 120), "outer": (250, 194, 68),
             "glow": (255, 214, 110), "wash": (255, 250, 232)},
    "pink": {"inner": (255, 236, 249), "mid": (255, 150, 214), "outer": (250, 108, 188),
             "glow": (255, 140, 204), "wash": (255, 238, 250)},
    "white": {"inner": (255, 255, 255), "mid": (236, 241, 250), "outer": (208, 219, 240),
              "glow": (230, 238, 250), "wash": (250, 252, 255)},
}

INNER_RGB = PALETTES["blue"]["inner"]
MID_RGB = PALETTES["blue"]["mid"]
OUTER_RGB = PALETTES["blue"]["outer"]
GLOW_RGB = PALETTES["blue"]["glow"]
WASH_RGB = PALETTES["blue"]["wash"]


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c0: tuple[int, int, int], c1: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return (
        round(lerp(c0[0], c1[0], t)),
        round(lerp(c0[1], c1[1], t)),
        round(lerp(c0[2], c1[2], t)),
    )


# Seat the ring just above the contact point so the near arc clears the canvas
# edge while the feet still sit inside the ellipse.
RING_SEAT_LIFT = 19.0


def center_y() -> float:
    """Seat the ring on the foot baseline so the character stands inside it."""
    if CENTER_Y_OVERRIDE is not None:
        return CENTER_Y_OVERRIDE
    return FOOT_BASELINE_Y - RING_SEAT_LIFT


def signed_distance(x: float, y: float, cy: float, rx: float, ry: float) -> float:
    """First-order signed pixel distance to a centerline ellipse."""
    dx = (x - CENTER_X) / rx
    dy = (y - cy) / ry
    value = dx * dx + dy * dy - 1.0
    gx = 2.0 * (x - CENTER_X) / (rx * rx)
    gy = 2.0 * (y - cy) / (ry * ry)
    gradient = (gx * gx + gy * gy) ** 0.5
    if gradient == 0.0:
        return -ry
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


def rings() -> list[tuple[float, float, float]]:
    """(center_y, radius_x, radius_y) for the inner and outer ring."""
    cy = center_y()
    return [
        (cy, RADIUS_X, RADIUS_Y),
        (cy + OUTER_OFFSET_Y, RADIUS_X * OUTER_SCALE_X, RADIUS_Y * OUTER_SCALE_Y),
    ]


def render() -> Image.Image:
    image = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    pixels = image.load()
    shapes = rings()

    reach_x = max(rx for _, rx, _ in shapes) + BAND / 2.0 + GLOW + 2
    reach_y = max(cy + ry for cy, _, ry in shapes) + BAND / 2.0 + GLOW + 2
    top_y = min(cy - ry for cy, _, ry in shapes) - BAND / 2.0 - GLOW - 2
    x0 = max(0, int(CENTER_X - reach_x))
    x1 = min(CANVAS - 1, int(CENTER_X + reach_x))
    y0 = max(0, int(top_y))
    y1 = min(CANVAS - 1, int(reach_y))

    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            best = None
            for cy, rx, ry in shapes:
                # Sample at the pixel centre for correct analytic anti-aliasing.
                value = shade(signed_distance(x + 0.5, y + 0.5, cy, rx, ry))
                if value is not None and (best is None or value[3] > best[3]):
                    best = value
            if best is not None:
                pixels[x, y] = best
    return image


def build_svg() -> str:
    cy = center_y()
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
  <g fill="none" stroke="rgb{GLOW_RGB}" stroke-width="{BAND + GLOW:.1f}" opacity="0.5" filter="url(#glow)">
    <ellipse cx="{CENTER_X}" cy="{cy:.1f}" rx="{RADIUS_X:.1f}" ry="{RADIUS_Y:.1f}"/>
    <ellipse cx="{CENTER_X}" cy="{cy + OUTER_OFFSET_Y:.1f}" rx="{RADIUS_X * OUTER_SCALE_X:.1f}" ry="{RADIUS_Y * OUTER_SCALE_Y:.1f}"/>
  </g>
  <g fill="none" stroke="url(#band)" stroke-width="{BAND:.1f}">
    <ellipse cx="{CENTER_X}" cy="{cy:.1f}" rx="{RADIUS_X:.1f}" ry="{RADIUS_Y:.1f}"/>
    <ellipse cx="{CENTER_X}" cy="{cy + OUTER_OFFSET_Y:.1f}" rx="{RADIUS_X * OUTER_SCALE_X:.1f}" ry="{RADIUS_Y * OUTER_SCALE_Y:.1f}"/>
  </g>
</svg>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("images/trait_candidates/rear_auras/aura_rear_001_blue_floor_ring_candidate_attempt_005.png"),
    )
    parser.add_argument("--svg", type=Path, help="also write the vector source")
    parser.add_argument("--band", type=float, help="solid band thickness in px")
    parser.add_argument("--glow", type=float, help="falloff width beyond the band in px")
    parser.add_argument("--radius-x", type=float, help="ellipse semi-major axis in px")
    parser.add_argument("--radius-y", type=float, help="ellipse semi-minor axis in px")
    parser.add_argument("--palette", choices=sorted(PALETTES), default="blue",
                        help="neon colour variant from the floor-ring reference sheet")
    parser.add_argument("--center-y", type=float,
                        help="ellipse center Y (default: the foot baseline, so the character "
                             "stands inside the ring)")
    args = parser.parse_args(argv)

    # Shape overrides let the ring be tuned without editing the module.
    global BAND, GLOW, RADIUS_X, RADIUS_Y, CENTER_Y_OVERRIDE
    global INNER_RGB, MID_RGB, OUTER_RGB, GLOW_RGB, WASH_RGB
    palette = PALETTES[args.palette]
    INNER_RGB, MID_RGB = palette["inner"], palette["mid"]
    OUTER_RGB, GLOW_RGB, WASH_RGB = palette["outer"], palette["glow"], palette["wash"]
    if args.center_y is not None:
        CENTER_Y_OVERRIDE = args.center_y
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
    # Floor auras are gated with --floor-aura: the near arc may pass below the
    # foot baseline, so only the canvas edge bounds the bottom.
    bottom_limit = CANVAS - 1
    within = (
        left >= MAX_BOUNDS[0]
        and top >= MAX_BOUNDS[1]
        and right <= MAX_BOUNDS[2]
        and bottom <= bottom_limit
    )
    print(f"Wrote {args.out}")
    print(f"  visible bounds [{left},{top},{right},{bottom}] "
          f"within [{MAX_BOUNDS[0]},{MAX_BOUNDS[1]},{MAX_BOUNDS[2]},{bottom_limit}]: {within}")
    print(f"  clearance below near arc: {bottom_limit - bottom} px to canvas edge")
    print(f"  center X {(left + right) / 2:.1f} (locked {CENTER_X})")

    if args.svg:
        args.svg.parent.mkdir(parents=True, exist_ok=True)
        args.svg.write_text(build_svg(), encoding="utf-8")
        print(f"Wrote {args.svg}")

    return 0 if within else 1


if __name__ == "__main__":
    raise SystemExit(main())
