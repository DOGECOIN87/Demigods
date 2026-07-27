#!/usr/bin/env python3
"""Recolour the registered silver hair-back layer into additional palettes.

A 50-token random sample showed identical hair on every single token: `hair_back`
holds one registered asset, so the most visible repetition in the collection is
the hair, not the robes. These recolours reduce that until painted hair lands.

The method keeps every painted detail. Luminance is normalised across the source's
actual opaque range (78-185) and remapped through a three-stop palette, so strand
separation, wave structure and the upper-left key light all survive; only hue and
value shift. Alpha is copied through untouched.

Scope, stated plainly: this varies COLOUR only. The silhouette is identical in
every output, so eight recolours give eight hair colours and one hair *shape*.
The eight cells in the HAIR sheet are genuinely different cuts — see the backlog
note — so these do NOT satisfy DG-029 to DG-036 and must not be filed as them.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

SOURCE = Path("assets/hair_back/hair_back_003_silver_long_wavy.png")

# Measured from the source's opaque pixels; normalising to this range rather than
# 0-255 keeps the remap from crushing the midtones.
SOURCE_FLOOR = 78
SOURCE_CEILING = 185

PALETTES: dict[str, dict[str, tuple[int, int, int]]] = {
    "gold":   {"shadow": (120, 84, 34),   "mid": (208, 162, 74),  "light": (252, 232, 176)},
    "black":  {"shadow": (18, 18, 24),    "mid": (48, 48, 60),    "light": (122, 124, 142)},
    "violet": {"shadow": (58, 36, 86),    "mid": (118, 84, 168),  "light": (204, 178, 240)},
    "blue":   {"shadow": (24, 44, 92),    "mid": (58, 96, 168),   "light": (166, 202, 246)},
    "pink":   {"shadow": (128, 54, 92),   "mid": (216, 116, 160), "light": (252, 204, 224)},
    "teal":   {"shadow": (18, 74, 78),    "mid": (46, 138, 136),  "light": (168, 226, 220)},
    "red":    {"shadow": (94, 24, 28),    "mid": (168, 52, 50),   "light": (238, 150, 132)},
}


def palette_lut(palette: dict[str, tuple[int, int, int]]) -> tuple[list[int], list[int], list[int]]:
    shadow, mid, light = palette["shadow"], palette["mid"], palette["light"]
    channels: list[list[int]] = [[], [], []]
    span = max(1, SOURCE_CEILING - SOURCE_FLOOR)
    for level in range(256):
        t = min(1.0, max(0.0, (level - SOURCE_FLOOR) / span))
        for index in range(3):
            if t < 0.5:
                local = t / 0.5
                value = shadow[index] + (mid[index] - shadow[index]) * local
            else:
                local = (t - 0.5) / 0.5
                value = mid[index] + (light[index] - mid[index]) * local
            channels[index].append(max(0, min(255, round(value))))
    return channels[0], channels[1], channels[2]


def recolour(source: Image.Image, palette_name: str) -> Image.Image:
    source = source.convert("RGBA")
    luminance = source.convert("L")
    red, green, blue = palette_lut(PALETTES[palette_name])
    toned = Image.merge(
        "RGB", (luminance.point(red), luminance.point(green), luminance.point(blue))
    )
    result = toned.convert("RGBA")
    result.putalpha(source.getchannel("A"))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out-dir", type=Path,
                        default=Path("images/trait_candidates/hair_back"))
    parser.add_argument("--palette", choices=sorted(PALETTES),
                        help="render one palette; default renders all")
    args = parser.parse_args(argv)

    source = Image.open(args.source).convert("RGBA")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    names = [args.palette] if args.palette else sorted(PALETTES)

    for name in names:
        image = recolour(source, name)
        destination = args.out_dir / f"hair_back_recolour_{name}.png"
        image.save(destination)
        bbox = image.getchannel("A").getbbox()
        same = bbox == source.getchannel("A").getbbox()
        print(f"  {name:7s} -> {destination.name}  alpha preserved: {same}")

    print(f"\n{len(names)} recolours. Colour varies; silhouette does not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
