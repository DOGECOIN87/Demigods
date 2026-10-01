#!/usr/bin/env python3
"""Make a labeled contact sheet from already rendered generator output."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def trait_number(value: str | None) -> str:
    match = re.search(r"_(\d{3})_", value or "")
    return match.group(1) if match else "—"


def font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generated", type=Path, help="directory with images/, metadata/, manifest.json")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--tile", type=int, default=310)
    args = parser.parse_args()
    if args.columns < 1 or args.tile < 100:
        parser.error("columns must be positive and tile must be at least 100")

    manifest = json.loads((args.generated / "manifest.json").read_text())
    images = sorted((args.generated / "images").glob("*.png"))
    if len(images) != manifest["supply"]:
        raise ValueError("image count differs from manifest supply")

    pad, label_h, header = 12, 48, 88
    rows = math.ceil(len(images) / args.columns)
    sheet = Image.new(
        "RGB",
        (pad + args.columns * (args.tile + pad), header + pad + rows * (args.tile + label_h + pad)),
        "#202231",
    )
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, 13), "DEMIGODS · GENERATIVE TEST", font=font(28), fill="#f2ede7")
    draw.text(
        (pad, 53),
        f"{len(images)} deterministic samples  ·  seed: {manifest['seed']}",
        font=font(13),
        fill="#c4c1ca",
    )
    for index, path in enumerate(images):
        record = json.loads((args.generated / "metadata" / f"{path.stem}.json").read_text())
        attributes = {item["trait_type"]: item["value"] for item in record["attributes"]}
        with Image.open(path) as image:
            tile = image.convert("RGB").resize((args.tile, args.tile), Image.Resampling.LANCZOS)
        x = pad + (index % args.columns) * (args.tile + pad)
        y = header + pad + (index // args.columns) * (args.tile + label_h + pad)
        sheet.paste(tile, (x, y))
        draw.rectangle((x, y + args.tile, x + args.tile - 1, y + args.tile + label_h - 1), fill="#333346")
        draw.text(
            (x + 8, y + args.tile + 5),
            f"#{record['token_id']:04d}  ·  Outfit {trait_number(attributes.get('outfits'))}"
            f"  ·  Pose {trait_number(attributes.get('base_bodies'))}",
            font=font(16), fill="#f2ede7",
        )
        held = attributes.get("hand_objects", "none")
        draw.text((x + 8, y + args.tile + 27), f"Held: {held.replace('hand_object_', '')[:35]}",
                  font=font(13), fill="#c4c1ca")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out, optimize=True)
    print(f"Wrote {args.out}: {len(images)} samples, {sheet.width}×{sheet.height}")


if __name__ == "__main__":
    main()
