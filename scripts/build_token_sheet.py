#!/usr/bin/env python3
"""Render a contact sheet of sampled tokens, using the real generator's rules.

Every QA sheet in this repository up to now was hand-rolled: walk the manifest,
pick a random path per category, composite in a hand-written order. That drifts
from what `generate_777.py` would actually produce, and it did — one sheet paired
a gold fringe with red back hair because the ad-hoc sampler did not know about
`config/compatibility.json`.

This imports the generator's own `discover_assets`, `choose_selection`,
`violates_rules` and `LAYER_ORDER`, so a cell here is a combination the real
generator could emit, composited in the real layer order. If the sheet looks
wrong, the collection is wrong.

Sampling is by rejection, the same as the generator: draw a selection, discard it
if it breaks a rule or repeats a signature already drawn.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_777 as generator  # noqa: E402

THUMB = 210

# Below this mean delta a category does not change what a thumbnail looks like.
SALIENCE_FLOOR = 3.0
MARGIN = 12
HEADER = 40


def load_font(size: int) -> ImageFont.ImageFont:
    path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(str(path), size) if path.is_file() else ImageFont.load_default()


def sample(rng: random.Random, assets: dict, rules: dict, count: int,
           max_attempts: int) -> list[dict]:
    selections = []
    seen: set[str] = set()
    attempts = 0
    while len(selections) < count:
        attempts += 1
        if attempts > max_attempts:
            raise SystemExit(
                f"only found {len(selections)} unique valid combinations in "
                f"{max_attempts} attempts; the rules may be over-constrained"
            )
        selection = generator.choose_selection(rng, assets)
        if generator.violates_rules(selection, rules):
            continue
        signature = generator.raw_signature(selection)
        if signature in seen:
            continue
        seen.add(signature)
        selections.append(selection)
    return selections


def composite(selection: dict) -> Image.Image:
    canvas = Image.new("RGBA", (generator.CANVAS_SIZE, generator.CANVAS_SIZE)
                       if hasattr(generator, "CANVAS_SIZE") else (1254, 1254),
                       (0, 0, 0, 0))
    for category in generator.LAYER_ORDER:
        path = selection.get(category)
        if path is None:
            continue
        with Image.open(path) as source:
            source.load()
            canvas = Image.alpha_composite(canvas, source.convert("RGBA"))
    return canvas


def thumbnail(selection: dict, size: int = 70) -> Image.Image:
    return composite(selection).convert("RGB").resize((size, size), Image.LANCZOS)


def mean_difference(a: Image.Image, b: Image.Image) -> float:
    pa, pb = a.load(), b.load()
    total = 0
    for y in range(a.height):
        for x in range(a.width):
            total += max(abs(pa[x, y][i] - pb[x, y][i]) for i in range(3))
    return total / (a.width * a.height)


def salience(assets: dict, rules: dict, seed: int) -> dict[str, float]:
    """Mean thumbnail change from swapping one category, holding the rest fixed.

    A category whose swaps barely move the thumbnail contributes nothing to how
    varied the collection looks in a marketplace grid, however many assets it
    holds. That is the number worth knowing before counting combination space.
    """
    rng = random.Random(seed)
    base = generator.choose_selection(rng, assets)
    while generator.violates_rules(base, rules):
        base = generator.choose_selection(rng, assets)
    reference = thumbnail(base)

    scores = {}
    for category, files in assets.items():
        if not files:
            continue
        deltas = []
        for alternative in files:
            if alternative == base[category]:
                continue
            trial = dict(base)
            trial[category] = alternative
            # Carry any partner a requires rule names, so the swap stays legal.
            for rule in rules.get("requires", []):
                if rule.get("trait") != alternative.name:
                    continue
                partner = rule.get("requires")
                for other, others in assets.items():
                    match = next((p for p in others if p.name == partner), None)
                    if match is not None:
                        trial[other] = match
            if generator.violates_rules(trial, rules):
                continue
            deltas.append(mean_difference(reference, thumbnail(trial)))
        if deltas:
            scores[category] = sum(deltas) / len(deltas)
    return scores


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--columns", type=int, default=10)
    parser.add_argument("--seed", type=int, default=777)
    parser.add_argument("--assets", type=Path, default=Path("assets"))
    parser.add_argument("--compatibility", type=Path,
                        default=Path("config/compatibility.json"))
    parser.add_argument("--out", type=Path,
                        default=Path("docs/qa/composites/token_sheet.png"))
    parser.add_argument("--max-attempts", type=int, default=200000)
    parser.add_argument("--salience", action="store_true",
                        help="report how much each category changes the thumbnail")
    args = parser.parse_args(argv)

    assets = generator.discover_assets(args.assets)
    rules = generator.load_json(args.compatibility)
    populated = {c: files for c, files in assets.items() if files}

    if args.salience:
        import math
        scores = salience(assets, rules, args.seed)
        print(f"{'category':18s} {'assets':>7} {'mean thumbnail delta':>22s}")
        for category in generator.LAYER_ORDER:
            if category in scores:
                print(f"{category:18s} {len(assets[category]):>7} {scores[category]:>22.1f}")
        visible = [c for c, v in scores.items() if v >= SALIENCE_FLOOR]
        space = math.prod(len(assets[c]) for c in visible)
        distinct = space * (1 - (1 - 1 / space) ** 777) if space else 0
        print(f"\nreads at {THUMB} px (delta >= {SALIENCE_FLOOR}): {', '.join(visible)}")
        print(f"distinct thumbnail appearances: {space}")
        print(f"777 tokens -> about {distinct:.0f} distinct looks, "
              f"{777 - distinct:.0f} sharing one with another token")
        return 0

    rng = random.Random(args.seed)
    selections = sample(rng, assets, rules, args.count, args.max_attempts)

    columns = args.columns
    rows = (len(selections) + columns - 1) // columns
    width = MARGIN * 2 + columns * THUMB
    height = HEADER + MARGIN + rows * THUMB + MARGIN

    sheet = Image.new("RGB", (width, height), (250, 250, 252))
    draw = ImageDraw.Draw(sheet)
    draw.text((MARGIN, 10), f"Demigods 777 — {len(selections)} sampled tokens at {THUMB} px",
              fill=(18, 18, 28), font=load_font(19))
    draw.text((MARGIN, 30),
              f"seed {args.seed}; {sum(len(v) for v in populated.values())} assets across "
              f"{len(populated)} categories; {len(rules.get('requires', []))} requires and "
              f"{len(rules.get('excludes', []))} excludes rules applied",
              fill=(90, 90, 112), font=load_font(13))

    for index, selection in enumerate(selections):
        token = composite(selection).convert("RGB").resize((THUMB, THUMB), Image.LANCZOS)
        x = MARGIN + (index % columns) * THUMB
        y = HEADER + MARGIN + (index // columns) * THUMB
        sheet.paste(token, (x, y))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print(f"{len(selections)} tokens -> {args.out}  {sheet.size}")

    for category in generator.LAYER_ORDER:
        if not assets.get(category):
            continue
        used = len({selection[category] for selection in selections
                    if category in selection})
        print(f"  {category:18s} {used:>3} of {len(assets[category]):>3} distinct assets used")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
