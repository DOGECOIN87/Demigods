#!/usr/bin/env python3
"""Render a legible, cell-labelled copy of the HAIR reference sheet.

`images/reference_sheets/anime_hair_customization_asset_sheet.webp` is 128 x 96
pixels. Every hair prompt cites a cell in it ("upper row cell 4"), but at that
size each cell is roughly 16 x 24 px, which is hard to identify by eye and
useless as a model attachment.

This upscales the sheet with LANCZOS and overlays the cell index, backlog ID, and
canonical output filename for each of the sixteen cells, so the operator and the
image model can both see exactly which design a prompt refers to.

The output is a NAVIGATION AID, not production art. It is upscaled from a
compressed preview, so it carries none of the detail a production render needs;
`prompts/19` forbids enlarging a catalog cell into an asset. Attach it to show
*which* design is wanted, alongside the base master that carries the real
rendering language.

Usage:
    python scripts/annotate_hair_sheet.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SHEET = ROOT / "images" / "reference_sheets" / "anime_hair_customization_asset_sheet.webp"
DEFAULT_OUT = ROOT / "docs" / "qa" / "hair_reference_sheet_annotated.png"

SCALE = 10
COLUMNS = 8

# Both rows run the same eight colours in the same order, which is what makes
# hair_front_00N and hair_back_00N a matched pair.
COLOURS = ["gold", "black", "silver", "violet", "blue", "pink", "teal", "red"]

# (row label, first backlog ID, filename stems in cell order)
ROWS = [
    (
        "UPPER ROW — hair_back (layer 04, behind the head)",
        29,
        [
            "hair_back_001_gold_long_wavy", "hair_back_002_black_long_wavy",
            "hair_back_003_silver_long_wavy", "hair_back_004_violet_long_wavy",
            "hair_back_005_blue_long_wavy", "hair_back_006_pink_long_wavy",
            "hair_back_007_teal_long_wavy", "hair_back_008_red_long_wavy",
        ],
    ),
    (
        "LOWER ROW — hair_front (layer 12, bangs and face-framing strands)",
        115,
        [
            "hair_front_001_gold_parted_bangs", "hair_front_002_black_side_swept",
            "hair_front_003_silver_straight_bangs", "hair_front_004_violet_parted_bangs",
            "hair_front_005_blue_pointed_bangs", "hair_front_006_pink_soft_bangs",
            "hair_front_007_teal_open_center", "hair_front_008_red_short_bangs",
        ],
    ),
]

REGISTERED = {"hair_back_003_silver_long_wavy"}


def annotate(sheet: Image.Image, scale: int = SCALE) -> Image.Image:
    big = sheet.convert("RGB").resize((sheet.width * scale, sheet.height * scale), Image.LANCZOS)
    cell_w = big.width // COLUMNS
    row_h = big.height // len(ROWS)

    header, footer = 30, 96
    canvas = Image.new("RGB", (big.width, big.height + header + footer * len(ROWS)), (18, 18, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((10, 9), "DEMIGODS — HAIR reference sheet, cell map", fill=(245, 245, 245))
    draw.text(
        (10, 20),
        f"source: {SHEET.relative_to(ROOT)} ({sheet.width}x{sheet.height}) upscaled {scale}x — "
        "navigation aid only, never production pixels",
        fill=(150, 150, 165),
    )

    for row_index, (label, first_id, stems) in enumerate(ROWS):
        strip_y = header + row_index * (row_h + footer)
        canvas.paste(big.crop((0, row_index * row_h, big.width, (row_index + 1) * row_h)), (0, strip_y))
        draw.text((8, strip_y + row_h + 6), label, fill=(235, 235, 240))

        for column in range(COLUMNS):
            x = column * cell_w
            draw.line([(x, strip_y), (x, strip_y + row_h)], fill=(90, 90, 110), width=1)
            backlog_id = f"DG-{first_id + column:03d}"
            stem = stems[column]
            done = stem in REGISTERED
            draw.text((x + 4, strip_y + 4), f"cell {column + 1}", fill=(255, 210, 90))
            text_y = strip_y + row_h + 22
            draw.text((x + 4, text_y), backlog_id, fill=(120, 230, 140) if done else (235, 235, 240))
            draw.text((x + 4, text_y + 12), COLOURS[column], fill=(170, 170, 185))
            draw.text((x + 4, text_y + 24), "REGISTERED" if done else "pending",
                      fill=(120, 230, 140) if done else (230, 150, 150))
            # Filename wrapped to fit the column.
            name = stem + ".png"
            for line_index in range(0, len(name), 18):
                draw.text((x + 4, text_y + 38 + (line_index // 18) * 11),
                          name[line_index:line_index + 18], fill=(140, 140, 160))

    return canvas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--scale", type=int, default=SCALE)
    args = parser.parse_args(argv)

    result = annotate(Image.open(SHEET), args.scale)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.out)
    print(f"Wrote {args.out} ({result.width}x{result.height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
