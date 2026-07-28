#!/usr/bin/env python3
"""Render every registered asset as one labelled contact sheet, by category.

The random-token sheets answer "does the collection look right"; they cannot
answer "what is actually in the library", because a 32-cell sample shows each
asset once if you are lucky. This walks the manifest instead, so every registered
asset appears exactly once and a missing or duplicated one is visible.

Each category gets the context and crop that make it legible. An eye layer shown
alone on transparency is a pair of floating irises, and a background shown at
figure crop is a wall — so eyes composite over the base body and are cropped to
the face, backgrounds are shown whole, and so on. The context layers are drawn
dimmed so the asset being catalogued is the thing you read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1254

# Crop windows, chosen so the subject fills its cell.
FULL = (0, 0, 1254, 1254)
FIGURE = (240, 118, 1014, 1160)
HEAD = (410, 108, 844, 512)
# Tight windows per feature. A single shared "face" crop was tried first and hid
# most of expression_marks: its temple glyphs sit at Y 236, above the crop, so
# seven of the eight cells came out blank.
EYES = (466, 300, 790, 436)
BROWS = (476, 268, 780, 370)
MOUTH = (536, 386, 718, 482)
# Union of all eight registered glyph bounds plus margin. Guessing a face-sized
# window clipped three of them and hid mark_008 entirely, which sits at Y 139.
MARKS = (386, 129, 855, 452)

BASE = "assets/base_bodies/base_body_001_neutral_master.png"
BACKDROP = (30, 32, 52)

# category -> (crop, context layers drawn under the asset, layers drawn over it)
PRESENTATION: dict[str, tuple[tuple[int, int, int, int], list[str], list[str]]] = {
    "backgrounds":      (FULL,   [], []),
    "rear_auras":       (FIGURE, [], [BASE]),
    "back_accessories": (FIGURE, [], [BASE]),
    "hair_back":        (FIGURE, [], [BASE]),
    "base_bodies":      (FIGURE, [], []),
    "outfits":          (FIGURE, [BASE], []),
    "neck_accessories": (HEAD,   [BASE], []),
    "eyes":             (EYES,   [BASE], []),
    "eyebrows":         (BROWS,  [BASE], []),
    "mouths":           (MOUTH,  [BASE], []),
    "expression_marks": (MARKS,  [BASE], []),
    "hair_front":       (HEAD,   [BASE], []),
    "head_accessories": (HEAD,   [BASE], []),
    "hand_objects":     (FIGURE, [BASE], []),
    "front_auras":      (FIGURE, [BASE], []),
    "global_finish":    (FIGURE, [BASE], []),
}

ORDER = list(PRESENTATION)

CELL = 190
LABEL = 26
COLUMNS = 8
HEADER = 34
MARGIN = 14


def load_font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ):
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def short_name(path: str) -> str:
    stem = Path(path).stem
    parts = stem.split("_")
    # Drop the repeated category prefix; keep the number and the description.
    while parts and not parts[0].isdigit() and len(parts) > 2:
        if parts[1].isdigit() or (len(parts[1]) == 3 and parts[1].isdigit()):
            break
        parts = parts[1:]
    return "_".join(parts)


def cell_for(path: str, category: str, cache: dict[str, Image.Image]) -> Image.Image:
    crop, under, over = PRESENTATION[category]

    def get(p: str) -> Image.Image:
        if p not in cache:
            cache[p] = Image.open(p).convert("RGBA")
        return cache[p]

    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    for layer in under:
        canvas.alpha_composite(get(layer))
    canvas.alpha_composite(get(path))
    for layer in over:
        canvas.alpha_composite(get(layer))

    flat = Image.new("RGB", (CANVAS, CANVAS), BACKDROP)
    flat.paste(canvas.convert("RGB"), mask=canvas.getchannel("A"))
    window = flat.crop(crop)
    width, height = window.size
    scale = min(CELL / width, CELL / height)
    resized = window.resize((max(1, round(width * scale)), max(1, round(height * scale))),
                            Image.LANCZOS)
    cell = Image.new("RGB", (CELL, CELL), BACKDROP)
    cell.paste(resized, ((CELL - resized.width) // 2, (CELL - resized.height) // 2))
    return cell


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("assets/asset_manifest.json"))
    parser.add_argument("--out", type=Path,
                        default=Path("docs/qa/composites/asset_catalogue.png"))
    args = parser.parse_args(argv)

    manifest = json.loads(args.manifest.read_text())
    grouped: dict[str, list[str]] = {}
    for entry in manifest["registered_production_assets"]:
        if entry.get("status") != "production_ready":
            continue
        grouped.setdefault(entry["category"], []).append(entry["path"])

    populated = [c for c in ORDER if grouped.get(c)]
    total = sum(len(grouped[c]) for c in populated)

    rows_per_category = {c: (len(grouped[c]) + COLUMNS - 1) // COLUMNS for c in populated}
    height = MARGIN * 2 + 44
    for category in populated:
        height += HEADER + rows_per_category[category] * (CELL + LABEL) + MARGIN
    width = MARGIN * 2 + COLUMNS * CELL

    sheet = Image.new("RGB", (width, height), (250, 250, 252))
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(20)
    header_font = load_font(15)
    label_font = load_font(11)

    draw.text((MARGIN, MARGIN), "Demigods 777 — registered asset catalogue",
              fill=(18, 18, 28), font=title_font)
    draw.text((MARGIN, MARGIN + 24),
              f"{total} assets across {len(populated)} populated categories; "
              f"{len(ORDER) - len(populated)} categories still empty",
              fill=(90, 90, 112), font=header_font)

    y = MARGIN + 44
    cache: dict[str, Image.Image] = {}
    for category in populated:
        paths = sorted(grouped[category])
        draw.rectangle([MARGIN, y, width - MARGIN, y + HEADER - 8], fill=(232, 234, 244))
        draw.text((MARGIN + 8, y + 5), f"{category}  ({len(paths)})",
                  fill=(28, 30, 48), font=header_font)
        y += HEADER
        for index, path in enumerate(paths):
            column = index % COLUMNS
            row = index // COLUMNS
            x = MARGIN + column * CELL
            cy = y + row * (CELL + LABEL)
            sheet.paste(cell_for(path, category, cache), (x, cy))
            draw.text((x + 3, cy + CELL + 5), short_name(path)[:34],
                      fill=(60, 60, 80), font=label_font)
        y += rows_per_category[category] * (CELL + LABEL) + MARGIN

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print(f"{total} assets, {len(populated)} categories -> {args.out}  {sheet.size}")
    for category in ORDER:
        if not grouped.get(category):
            print(f"  empty: {category}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
