#!/usr/bin/env python3
"""Render the layer-16 global-finish family.

The global-finish slot existed in the locked layer stack and the validator, but
no reference sheet defined it and no prompt described it, so the category sat
source-gated with nothing in it.

This closes that gate with a *narrow* definition rather than inventing artwork:
a global finish is a full-canvas directional light grade that restates the
collection's locked lighting — soft key from the upper left, form shadow toward
the lower right, subtle cool rim on the right. It adds atmosphere across the
whole frame without introducing any new object, so it cannot conflict with a
trait or a background.

Two properties keep it honest:

  - It is rendered analytically here rather than prompted. An image generator
    will not reproduce the same gradient angle and falloff across variants, and
    the same reasoning already applies to the background depth pass.
  - Peak alpha is capped well below opaque (see GLOBAL_FINISH_MAX_ALPHA). A
    finish may shift mood; it may never hide the art beneath it. The
    `--global-finish` gate mode enforces that ceiling.

Backgrounds already carry a corner vignette from `apply_background_depth.py`, so
this layer deliberately does NOT vignette — that would double-treat the frame.

Usage:
    python scripts/build_global_finish.py --out-dir assets/global_finish
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254

# name -> (tint RGB, peak alpha, gradient angle in degrees, falloff exponent)
#
# Angle 0 puts peak intensity at the upper-left corner and runs the falloff
# toward the lower right, matching the locked key-light direction. The cool veil
# inverts that axis to read as the shadow-side rim rather than a second key.
VARIANTS: dict[str, tuple[tuple[int, int, int], int, float, float]] = {
    "global_finish_001_soft_bloom": ((255, 246, 226), 40, 0.0, 1.6),
    "global_finish_002_gilded_warm": ((255, 214, 138), 56, 0.0, 1.9),
    "global_finish_003_cool_veil": ((176, 214, 255), 48, 180.0, 1.7),
}


def render(tint: tuple[int, int, int], peak_alpha: int, angle_deg: float, falloff: float) -> Image.Image:
    """Directional alpha ramp across the canvas diagonal.

    Colour is constant; only alpha varies. Keeping the colour channels fully
    saturated at every pixel means no partially transparent pixel ever darkens
    toward gray, which is the same matte-contamination failure the aura builders
    are written to avoid.
    """
    angle = math.radians(angle_deg)
    # Unit vector along the gradient; angle 0 => upper-left to lower-right.
    dx, dy = math.cos(angle + math.pi / 4), math.sin(angle + math.pi / 4)

    alpha = Image.new("L", (CANVAS, CANVAS))
    pixels = alpha.load()
    # Projection range over the canvas, used to normalise to 0..1.
    span = abs(dx) * (CANVAS - 1) + abs(dy) * (CANVAS - 1)
    offset = min(0.0, dx * (CANVAS - 1)) + min(0.0, dy * (CANVAS - 1))

    for y in range(CANVAS):
        base = dy * y - offset
        for x in range(CANVAS):
            t = (dx * x + base) / span          # 0 at the lit corner, 1 opposite
            value = (1.0 - t) ** falloff        # brightest at the key-light side
            pixels[x, y] = int(round(peak_alpha * max(0.0, min(1.0, value))))

    layer = Image.new("RGBA", (CANVAS, CANVAS), (*tint, 0))
    layer.putalpha(alpha)
    return layer


def display(path: Path) -> str:
    """Repo-relative when inside the repo, absolute otherwise (e.g. a scratch dir)."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "assets" / "global_finish")
    parser.add_argument("--only", help="render a single named variant")
    args = parser.parse_args(argv)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    selected = {args.only: VARIANTS[args.only]} if args.only else VARIANTS

    for name, (tint, peak, angle, falloff) in selected.items():
        image = render(tint, peak, angle, falloff)
        out_path = args.out_dir / f"{name}.png"
        image.save(out_path)
        low, high = image.getchannel("A").getextrema()
        print(f"{display(out_path)}  alpha {low}-{high}  tint {tint}")

    print(
        "\nGate with: python scripts/rig_gate_report.py --global-finish "
        f"{display(args.out_dir)}/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
