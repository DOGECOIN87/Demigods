#!/usr/bin/env python3
"""Build a fitted outfit layer from the registered base body.

Outfits are painted artwork, so this is not a substitute for a proper render. It
exists because `outfits` is a release blocker: with the category empty every
token shows the skin-toned mannequin garment and reads as unclothed at thumbnail
size. A procedural garment that clears the skin tone unblocks the pipeline and
gives the collection something honest to sit on until painted outfits arrive.

The approach avoids the usual failure of procedural clothing — lighting that does
not match the character — by deriving shading from the base body's own luminance
wherever the garment overlaps it. The skirt extends past the body, so folds there
are synthesised and blended to meet the inherited shading.

Every output is gated with:
    rig_gate_report.py --trait <file> --max-width-ratio 1.15 --min-skin-contrast 70
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

CANVAS = 1254
CENTER_X = 627
SS = 2

BASE_BODY = Path("assets/base_bodies/base_body_001_neutral_master.png")

COLLAR_Y = 498
SHOULDER_Y = 572
WAIST_Y = 808
HEM_Y = 1104
SLEEVE_BOTTOM_Y = 742   # above the hands, so they stay bare skin

# Half-width of the garment silhouette at each Y, measured against the base body.
PROFILE = [
    (COLLAR_Y, 84), (530, 112), (SHOULDER_Y, 131), (640, 128), (720, 123),
    (WAIST_Y, 118), (880, 133), (960, 152), (1040, 168), (HEM_Y, 176),
]

PALETTES: dict[str, dict[str, tuple[int, int, int]]] = {
    "navy":   {"shadow": (18, 22, 52),  "base": (38, 46, 96),   "light": (78, 92, 158),
               "trim": (206, 176, 104)},
    "black":  {"shadow": (14, 14, 20),  "base": (32, 32, 42),   "light": (72, 72, 88),
               "trim": (150, 150, 164)},
    "plum":   {"shadow": (44, 30, 54),  "base": (86, 64, 100),  "light": (140, 116, 156),
               "trim": (214, 200, 214)},
    "oxblood": {"shadow": (48, 20, 24), "base": (94, 40, 44),   "light": (150, 78, 74),
                "trim": (232, 226, 214)},
    "olive":  {"shadow": (40, 44, 26),  "base": (78, 84, 48),   "light": (128, 134, 86),
               "trim": (206, 202, 170)},
}


def half_width(y: float) -> float:
    """Linear interpolation through the profile table."""
    if y <= PROFILE[0][0]:
        return PROFILE[0][1]
    for (y0, w0), (y1, w1) in zip(PROFILE, PROFILE[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return w0 + (w1 - w0) * t
    return PROFILE[-1][1]


def garment_mask(body_alpha: Image.Image) -> Image.Image:
    """Robe silhouette: profile body and skirt, union the sleeves from the body."""
    size = CANVAS * SS
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    left_edge = []
    right_edge = []
    for y in range(COLLAR_Y, HEM_Y + 1, 2):
        w = half_width(y)
        left_edge.append(((CENTER_X - w) * SS, y * SS))
        right_edge.append(((CENTER_X + w) * SS, y * SS))
    draw.polygon(left_edge + list(reversed(right_edge)), fill=255)

    # Sleeves: the body's own upper-arm silhouette, stopping above the hands so
    # the hands composite as bare skin.
    sleeves = Image.new("L", (size, size), 0)
    band = body_alpha.crop((0, COLLAR_Y, CANVAS, SLEEVE_BOTTOM_Y)).point(
        lambda v: 255 if v > 8 else 0
    ).resize((size, (SLEEVE_BOTTOM_Y - COLLAR_Y) * SS), Image.NEAREST)
    sleeves.paste(band, (0, COLLAR_Y * SS))
    mask.paste(255, (0, 0), sleeves)

    # Neckline: a scooped opening so the neck and collar read.
    neck_w, neck_h = 43, 33
    # Sits on the neck line so the collar closes high rather than scooping open.
    neck_y = COLLAR_Y - 6
    draw.ellipse(
        [(CENTER_X - neck_w) * SS, (neck_y - neck_h) * SS,
         (CENTER_X + neck_w) * SS, (neck_y + neck_h) * SS],
        fill=0,
    )
    return mask.filter(ImageFilter.GaussianBlur(SS * 0.6))


def shading_field(body: Image.Image) -> Image.Image:
    """Luminance to drive the palette: inherited from the body, folds elsewhere."""
    size = CANVAS * SS
    inherited = body.convert("L").resize((size, size), Image.LANCZOS)

    folds = Image.new("L", (size, size), 128)
    pixels = folds.load()
    for x in range(0, size, 2):
        u = (x / SS - CENTER_X) / 180.0
        value = 128 + 52 * math.sin(u * 5.2) - 30 * u
        value = max(0, min(255, int(value)))
        for y in range(0, size, 2):
            pixels[x, y] = value
            if x + 1 < size:
                pixels[x + 1, y] = value
            if y + 1 < size:
                pixels[x, y + 1] = value
                if x + 1 < size:
                    pixels[x + 1, y + 1] = value
    folds = folds.filter(ImageFilter.GaussianBlur(SS * 3))

    # Body luminance where the body exists, folds beyond it; blended so the skirt
    # continues the inherited lighting instead of switching to a different scheme.
    body_mask = body.getchannel("A").resize((size, size), Image.LANCZOS)
    return Image.composite(Image.blend(folds, inherited, 0.72), folds, body_mask)


def palette_lut(palette: dict[str, tuple[int, int, int]]) -> list[list[int]]:
    shadow, base, light = palette["shadow"], palette["base"], palette["light"]
    channels: list[list[int]] = [[], [], []]
    for level in range(256):
        t = level / 255.0
        for index in range(3):
            if t < 0.55:
                local = t / 0.55
                value = shadow[index] + (base[index] - shadow[index]) * local
            else:
                local = (t - 0.55) / 0.45
                value = base[index] + (light[index] - base[index]) * local
            channels[index].append(max(0, min(255, round(value))))
    return channels


def draw_trim(mask: Image.Image, palette: dict, size: int) -> Image.Image:
    """Collar, cuff and hem bands, clipped to the garment."""
    trim = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(trim)
    thickness = int(9 * SS)

    for y in (COLLAR_Y + 42, HEM_Y - 20):
        w = half_width(y)
        draw.rectangle([(CENTER_X - w) * SS, y * SS - thickness // 2,
                        (CENTER_X + w) * SS, y * SS + thickness // 2], fill=255)
    # Centre placket, the vertical line that reads as a coat closure.
    draw.rectangle([CENTER_X * SS - thickness // 2, (COLLAR_Y + 42) * SS,
                    CENTER_X * SS + thickness // 2, (HEM_Y - 20) * SS], fill=255)
    trim = trim.filter(ImageFilter.GaussianBlur(SS * 0.5))
    trim.paste(0, (0, 0), mask.point(lambda v: 255 - v))
    return trim


def build(palette_name: str) -> Image.Image:
    body = Image.open(BASE_BODY).convert("RGBA")
    size = CANVAS * SS
    palette = PALETTES[palette_name]

    mask = garment_mask(body.getchannel("A"))
    shading = shading_field(body)
    red, green, blue = palette_lut(palette)
    fabric = Image.merge("RGB", (shading.point(red), shading.point(green), shading.point(blue)))

    trim = draw_trim(mask, palette, size)
    fabric.paste(Image.new("RGB", (size, size), palette["trim"]), (0, 0), trim)

    garment = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    garment.paste(fabric, (0, 0), mask)
    return garment.resize((CANVAS, CANVAS), Image.LANCZOS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--palette", choices=sorted(PALETTES), default="navy")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    image = build(args.palette)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.out)

    bbox = image.getchannel("A").getbbox()
    left, top, right, bottom = bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1
    print(f"Wrote {args.out}")
    print(f"  bounds [{left},{top},{right},{bottom}]  width {right - left + 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
