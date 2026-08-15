#!/usr/bin/env python3
"""Render a contact sheet directly from dry-run token metadata."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

LAYER_ORDER = [
    "backgrounds", "rear_auras", "back_accessories", "hair_back",
    "base_bodies", "outfits", "neck_accessories", "eyes", "eyebrows",
    "mouths", "expression_marks", "hair_front", "head_accessories",
    "hand_objects", "front_auras", "global_finish",
]
# Visual stacking differs from metadata order so the base hand sits in front of
# the held object at the grip while the object remains visible outside the body.
RENDER_LAYER_ORDER = [
    "backgrounds", "rear_auras", "back_accessories", "hair_back",
    "hand_objects", "base_bodies", "outfits", "neck_accessories", "eyes", "eyebrows",
    "mouths", "expression_marks", "hair_front", "head_accessories",
    "front_auras", "global_finish",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--assets", type=Path, default=Path("assets"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--tile", type=int, default=240)
    args = parser.parse_args()

    files = sorted(args.metadata.glob("*.json"))
    if not files:
        raise SystemExit(f"no metadata JSON files in {args.metadata}")

    label_height = 26
    rows = math.ceil(len(files) / args.columns)
    sheet = Image.new(
        "RGB",
        (args.columns * args.tile, rows * (args.tile + label_height)),
        (28, 28, 42),
    )
    draw = ImageDraw.Draw(sheet)
    cache: dict[Path, Image.Image] = {}

    for index, metadata_path in enumerate(files):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        attributes = {
            item["trait_type"]: item["source_file"]
            for item in metadata["attributes"]
        }
        tile = Image.new("RGBA", (args.tile, args.tile), (0, 0, 0, 0))
        for category in RENDER_LAYER_ORDER:
            source_name = attributes.get(category)
            if source_name is None:
                continue
            source = args.assets / source_name
            if source not in cache:
                cache[source] = Image.open(source).convert("RGBA").resize(
                    (args.tile, args.tile), Image.Resampling.LANCZOS
                )
            tile.alpha_composite(cache[source])

        column = index % args.columns
        row = index // args.columns
        x = column * args.tile
        y = row * (args.tile + label_height)
        sheet.paste(tile.convert("RGB"), (x, y))
        label = f"{metadata['token_id']:04d}"
        draw.rectangle((x, y + args.tile, x + args.tile, y + args.tile + label_height), fill=(28, 28, 42))
        draw.text((x + 8, y + args.tile + 6), label, fill=(235, 235, 245))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out, compress_level=3)
    print(f"Wrote {args.out}: {len(files)} tokens, {args.columns} columns, {rows} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
