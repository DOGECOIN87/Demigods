"""Build native transparent DG-145 and DG-146 front-aura candidates.

The effects are analytic transparent layers: no backdrop is rendered or keyed out.
Both designs stay below the face and within the locked trait bounds.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

CANVAS = 1254
BOUNDS = (233, 129, 1021, 1139)


def alpha_layer() -> Image.Image:
    return Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))


def composite(base: Image.Image, layer: Image.Image) -> Image.Image:
    return Image.alpha_composite(base, layer)


def flame_candidate() -> Image.Image:
    image = alpha_layer()
    glow = alpha_layer()
    gd = ImageDraw.Draw(glow)
    # Warm lower foreground glow, deliberately below the face and mouth.
    gd.ellipse((320, 780, 934, 1050), fill=(255, 116, 20, 34))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    image = composite(image, glow)
    draw = ImageDraw.Draw(image)
    flames = [
        ((305, 1136), (350, 820), (405, 1112), (430, 1138)),
        ((420, 1138), (470, 720), (535, 1098), (560, 1138)),
        ((700, 1138), (748, 760), (820, 1088), (850, 1138)),
        ((820, 1138), (900, 690), (960, 1010), (995, 1138)),
    ]
    for p0, p1, p2, p3 in flames:
        draw.polygon([p0, p1, p2, p3], fill=(255, 104, 18, 150))
        inner = (
            ((p0[0] + p1[0]) // 2, p0[1]),
            ((p1[0] + p2[0]) // 2, p1[1] + 45),
            ((p2[0] + p3[0]) // 2, p2[1] - 15),
            ((p0[0] + p3[0]) // 2, p0[1]),
        )
        draw.polygon(inner, fill=(255, 212, 72, 170))
    # Small ember motes, all safely below the mouth line.
    motes = [(275, 895, 7), (380, 760, 5), (455, 680, 4), (855, 720, 5), (930, 815, 6), (1000, 930, 4)]
    for x, y, r in motes:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 181, 45, 150))
    return image


def pillars_candidate() -> Image.Image:
    image = alpha_layer()
    # Soft vertical gold columns positioned on the outer silhouette; they begin
    # below the mouth and keep the face readable.
    for x, width, peak in [(300, 46, 82), (420, 28, 66), (834, 30, 70), (954, 46, 86)]:
        glow = alpha_layer()
        gd = ImageDraw.Draw(glow)
        gd.rectangle((x-width//2, 610, x+width//2, 1108), fill=(255, 207, 78, peak))
        glow = glow.filter(ImageFilter.GaussianBlur(12))
        image = composite(image, glow)
        draw = ImageDraw.Draw(image)
        draw.rectangle((x-width//4, 650, x+width//4, 1118), fill=(255, 225, 125, min(110, peak + 20)))
        draw.line((x, 640, x, 1128), fill=(255, 248, 205, min(160, peak + 55)), width=3)
    # Floating gold sparks stay below eye and mouth lines.
    draw = ImageDraw.Draw(image)
    for x, y, r in [(320, 690, 4), (440, 820, 3), (812, 710, 4), (930, 860, 3), (1010, 1010, 4)]:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 238, 158, 130))
    return image


def check(image: Image.Image) -> tuple[int, int, int, int]:
    if image.size != (CANVAS, CANVAS) or image.mode != "RGBA":
        raise ValueError("candidate must be native 1254x1254 RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("candidate has no visible pixels")
    bounds = (bbox[0], bbox[1], bbox[2]-1, bbox[3]-1)
    if not (bounds[0] >= BOUNDS[0] and bounds[1] >= BOUNDS[1] and bounds[2] <= BOUNDS[2] and bounds[3] <= BOUNDS[3]):
        raise ValueError(f"bounds {bounds} exceed locked bounds {BOUNDS}")
    return bounds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("images/trait_candidates/front_auras"))
    args = parser.parse_args()
    outputs = [
        ("aura_front_001_orange_rising_flame_candidate.png", flame_candidate()),
        ("aura_front_002_gold_light_pillars_candidate.png", pillars_candidate()),
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, image in outputs:
        bounds = check(image)
        path = args.out_dir / name
        image.save(path)
        print(f"Wrote {path} bounds={bounds} size={image.size} mode={image.mode}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
