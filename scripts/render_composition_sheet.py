"""Render a contact sheet of sampled rule-valid compositions.

Reviewing the collection one composite at a time hides the faults that only
appear across a spread: a background that dominates every cell it lands in, a
hair colour that reads as the same asset twice, an aura that disappears behind
the body. This samples with the generator's own selection and rule code, so a
cell here is a token the real run could emit rather than an approximation.

    python scripts/render_composition_sheet.py --count 25 --seed review-2026-08-24

Compositions are deduplicated by trait signature, and the sidecar JSON records
the exact per-cell selection so a flagged cell can be traced back to its assets.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

try:
    from scripts.generate_777 import (
        LAYER_ORDER,
        RENDER_LAYER_ORDER,
        choose_selection,
        discover_assets,
        load_json,
        raw_signature,
        resolve_optional,
        violates_rules,
    )
except ImportError:  # invoked as scripts/render_composition_sheet.py
    from generate_777 import (  # type: ignore[no-redef]
        LAYER_ORDER,
        RENDER_LAYER_ORDER,
        choose_selection,
        discover_assets,
        load_json,
        raw_signature,
        resolve_optional,
        violates_rules,
    )

ROOT = Path(__file__).resolve().parent.parent

# Cell caption lines are drawn from these categories, in this order. They are the
# traits a reviewer can actually name from a thumbnail; eyebrow and expression
# layers are legible only at full size, so listing them just crowds the caption.
CAPTION_CATEGORIES = [
    "backgrounds",
    "outfits",
    "hair_front",
    "hair_back",
    "rear_auras",
    "hand_objects",
]

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(size: int) -> ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def trait_label(path: Path) -> str:
    """Turn hair_front_004_gold_short_bob.png into 'gold short bob'.

    The leading category words and the three-digit index are dropped: they are
    identical down a column and push the part that differs out of the caption.
    """
    stem = path.stem
    parts = stem.split("_")
    for index, part in enumerate(parts):
        if part.isdigit() and len(part) == 3:
            return " ".join(parts[index + 1 :]) or stem
    return stem


def sample_compositions(
    *,
    assets: dict[str, list[Path]],
    rules: dict[str, Any],
    optional: dict[str, float],
    count: int,
    seed: str,
    max_attempts: int,
) -> list[dict[str, Path]]:
    rng = random.Random(seed)
    seen: set[str] = set()
    picked: list[dict[str, Path]] = []
    attempts = 0

    while len(picked) < count and attempts < max_attempts:
        attempts += 1
        selection = choose_selection(rng, assets, optional)
        if violates_rules(selection, rules):
            continue
        signature = raw_signature(selection)
        if signature in seen:
            continue
        seen.add(signature)
        picked.append(selection)

    if len(picked) < count:
        raise ValueError(
            f"only {len(picked)} unique rule-valid compositions after {attempts} attempts; "
            "the library may be too small or the rules too strict"
        )
    return picked


def compose(selection: dict[str, Path], size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    for category in RENDER_LAYER_ORDER:
        path = selection.get(category)
        if path is None:
            continue
        with Image.open(path) as source:
            source.load()
            layer = source.convert("RGBA")
        if layer.size != size:
            raise ValueError(f"{path} is {layer.size}; expected {size}")
        canvas = Image.alpha_composite(canvas, layer)
    return canvas


def render_sheet(
    selections: list[dict[str, Path]],
    *,
    size: tuple[int, int],
    columns: int,
    thumb: int,
    title: str,
) -> Image.Image:
    caption_height = 14 * len(CAPTION_CATEGORIES) + 22
    pad = 16
    header = 64
    rows = (len(selections) + columns - 1) // columns

    cell_w = thumb + pad
    cell_h = thumb + caption_height + pad

    sheet = Image.new(
        "RGB",
        (columns * cell_w + pad, header + rows * cell_h + pad),
        (24, 24, 28),
    )
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(26)
    index_font = load_font(15)
    caption_font = load_font(12)

    draw.text((pad, 20), title, font=title_font, fill=(240, 240, 245))

    # A mid grey behind every thumbnail: a pure white or black backdrop hides
    # exactly the edge faults (light rim, dark halo) this sheet exists to catch.
    backdrop = (72, 72, 80)

    for index, selection in enumerate(selections):
        row, col = divmod(index, columns)
        x = pad + col * cell_w
        y = header + row * cell_h

        composite = compose(selection, size).resize((thumb, thumb), Image.LANCZOS)
        tile = Image.new("RGBA", (thumb, thumb), backdrop + (255,))
        tile = Image.alpha_composite(tile, composite)
        sheet.paste(tile.convert("RGB"), (x, y))

        draw.rectangle([x, y, x + thumb - 1, y + thumb - 1], outline=(90, 90, 100))
        draw.text((x + 2, y + thumb + 3), f"{index + 1:02d}", font=index_font, fill=(235, 235, 240))

        line_y = y + thumb + 20
        for category in CAPTION_CATEGORIES:
            path = selection.get(category)
            text = f"{category.split('_')[0][:4]}: " + (trait_label(path) if path else "—")
            colour = (198, 198, 208) if path else (120, 120, 130)
            draw.text((x + 2, line_y), text[:46], font=caption_font, fill=colour)
            line_y += 14

    return sheet


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=25, help="compositions to render (default 25)")
    parser.add_argument("--seed", default="composition-sheet", help="deterministic sampling seed")
    parser.add_argument("--columns", type=int, default=0, help="grid columns (default: near-square)")
    parser.add_argument("--thumb", type=int, default=320, help="thumbnail edge in px (default 320)")
    parser.add_argument("--assets", type=Path, default=ROOT / "assets")
    parser.add_argument("--collection", type=Path, default=ROOT / "config" / "collection.json")
    parser.add_argument(
        "--compatibility", type=Path, default=ROOT / "config" / "compatibility.json"
    )
    parser.add_argument("--out", type=Path, default=None, help="sheet PNG path")
    parser.add_argument("--json-report", type=Path, default=None, help="per-cell selection sidecar")
    parser.add_argument("--max-attempts", type=int, default=20000)
    parser.add_argument(
        "--optional",
        action="append",
        metavar="CATEGORY=PROBABILITY",
        help=(
            "override optional_categories for this sheet only, e.g. --optional hand_objects=0.5. "
            "Nothing on disk changes; it renders what the collection would look like under a "
            "proposed rule so the change can be judged before it is committed."
        ),
    )
    return parser


def parse_optional_overrides(values: list[str] | None) -> dict[str, float] | None:
    if not values:
        return None
    overrides: dict[str, float] = {}
    for item in values:
        category, _, raw = item.partition("=")
        if not _ or not category:
            raise ValueError(f"--optional expects CATEGORY=PROBABILITY, got {item!r}")
        if category not in LAYER_ORDER:
            raise ValueError(f"unknown category {category!r}")
        overrides[category] = float(raw)
    return overrides


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)

    collection = load_json(args.collection)
    rules = load_json(args.compatibility)
    canvas = collection.get("canvas", {})
    size = (int(canvas.get("width", 1254)), int(canvas.get("height", 1254)))

    assets = discover_assets(args.assets)

    # resolve_optional replaces the configured mapping wholesale, so merge first:
    # an override for one category must not silently drop the others.
    optional = resolve_optional(collection)
    overrides = parse_optional_overrides(args.optional)
    if overrides:
        optional = resolve_optional(collection, {**optional, **overrides})

    empty = [c for c in LAYER_ORDER if not assets.get(c)]
    selections = sample_compositions(
        assets=assets,
        rules=rules,
        optional=optional,
        count=args.count,
        seed=args.seed,
        max_attempts=args.max_attempts,
    )

    columns = args.columns or max(1, round(len(selections) ** 0.5))
    title = f"Demigods — {len(selections)} sampled compositions (seed {args.seed})"
    sheet = render_sheet(
        selections, size=size, columns=columns, thumb=args.thumb, title=title
    )

    out = args.out or ROOT / "docs" / "qa" / f"composition_sheet_{len(selections)}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG", optimize=True)

    report = {
        "seed": args.seed,
        "count": len(selections),
        "columns": columns,
        "thumb": args.thumb,
        "sheet": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),
        "categories_with_no_registered_assets": empty,
        "compositions": [
            {
                "cell": index + 1,
                "signature": raw_signature(selection),
                "traits": {
                    category: str(path.relative_to(args.assets))
                    for category, path in selection.items()
                },
            }
            for index, selection in enumerate(selections)
        ],
    }

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {out}")
    print(f"{len(selections)} unique rule-valid compositions, seed {args.seed}")
    if empty:
        print("categories with no registered assets (absent from every cell):")
        for category in empty:
            print(f"  - {category}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
