#!/usr/bin/env python3
"""Render the before/after approval sheet for the undergarment fit-gap repaint.

The base bodies wear a neutral tank and shorts so the mannequin is never nude.
Outfits are meant to cover it. Outfits 006-010 were registered after the original
`hide_undergarment` run and were never in its hardcoded pair list, so four of them
left the tank showing.

The sheet separates the two things that were showing, because only one of them is
fixable by editing pixels:

* **Fit gaps** - narrow strips where a garment fails to meet the arm or shoulder
  and a tank strap shows through. These touch genuine skin, so colour diffuses
  into them cleanly. Fixed.
* **Neckline openings** - the chest V of the long coat, the collar of the high
  collar coat, the neck of the cloak. These are enclosed by more tank, so there
  is no skin to diffuse from, and the tank reads there as a linen undershirt.
  Left alone; covering them means the outfit carrying its own inner garment.

    python scripts/render_undergarment_approval_sheet.py --before <dir> \
      --out docs/qa/aligned_candidates_2026-09-07/undergarment_approval.png
"""
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.hide_undergarment import MAX_FIT_GAP, undergarment_mask  # noqa: E402

CANVAS = 1254
INK = (238, 240, 246)
DIM = (150, 156, 172)
GOLD = (255, 214, 120)
BAD = (255, 138, 138)
GOOD = (140, 232, 168)
PANEL = (22, 23, 28)
PAPER = (13, 14, 18)

ROWS = [
    ("outfit_007_brown_leather_long_coat.png", "3569 -> 2858 px", "side strips fixed; 82x77 chest V left as an undershirt"),
    ("outfit_008_olive_ragged_cloak.png", "749 -> 391 px", "upper gap fixed; enclosed neck opening left"),
    ("outfit_009_navy_high_collar_coat.png", "1362 -> 467 px", "both shoulder slivers fixed; 44x41 collar V left"),
    ("outfit_010_celestial_robe_white_gold.png", "344 -> 0 px", "fully fixed"),
]

_fonts: dict[int, ImageFont.FreeTypeFont] = {}


def font(size: int):
    if size not in _fonts:
        for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            if Path(path).exists():
                _fonts[size] = ImageFont.truetype(path, size)
                break
        else:
            _fonts[size] = ImageFont.load_default()
    return _fonts[size]


def highlight(base: Image.Image, outfit: Image.Image, max_gap: int = MAX_FIT_GAP) -> Image.Image:
    """Composite with exposed tank marked: red for a fit gap, amber for an opening."""
    shot = Image.new("RGBA", (CANVAS, CANVAS), (250, 250, 252, 255))
    shot.alpha_composite(base)
    shot.alpha_composite(outfit)
    ml = undergarment_mask(base, tolerance=14).load()
    oal = outfit.getchannel("A").load()
    points = {(x, y) for y in range(300, 1140) for x in range(200, 1054)
              if ml[x, y] > 0 and oal[x, y] < 40}
    pixels = shot.load()
    seen: set[tuple[int, int]] = set()
    for point in sorted(points):
        if point in seen:
            continue
        queue, component = deque([point]), []
        while queue:
            current = queue.popleft()
            if current in seen or current not in points:
                continue
            seen.add(current)
            component.append(current)
            cx, cy = current
            queue.extend(((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)))
        xs = [p[0] for p in component]
        ys = [p[1] for p in component]
        designed = (max(xs) - min(xs) + 1) > max_gap and (max(ys) - min(ys) + 1) > max_gap
        colour = (255, 176, 60, 255) if designed else (255, 40, 40, 255)
        for px, py in component:
            pixels[px, py] = colour
    return shot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--before", type=Path, required=True,
                        help="directory holding the pre-repaint base_body_001 PNG")
    parser.add_argument("--out", type=Path,
                        default=Path("docs/qa/aligned_candidates_2026-09-07/undergarment_approval.png"))
    args = parser.parse_args(argv)

    before_dir = args.before if args.before.is_absolute() else ROOT / args.before
    out = args.out if args.out.is_absolute() else ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)

    name = "base_body_001_neutral_master.png"
    before_base = Image.open(before_dir / name).convert("RGBA")
    after_base = Image.open(ROOT / "assets" / "base_bodies" / name).convert("RGBA")

    size, crop = 300, (455, 470, 800, 815)
    tiles = []
    for outfit_name, counts, note in ROWS:
        outfit = Image.open(ROOT / "assets" / "outfits" / outfit_name).convert("RGBA")
        tile = Image.new("RGBA", (size * 4 + 36, size + 68), PANEL)
        shots = [
            ("before", Image.new("RGBA", (CANVAS, CANVAS), (250, 250, 252, 255))),
            ("marked", highlight(before_base, outfit)),
            ("after", Image.new("RGBA", (CANVAS, CANVAS), (250, 250, 252, 255))),
            ("marked", highlight(after_base, outfit)),
        ]
        shots[0][1].alpha_composite(before_base); shots[0][1].alpha_composite(outfit)
        shots[2][1].alpha_composite(after_base); shots[2][1].alpha_composite(outfit)
        draw = ImageDraw.Draw(tile)
        for index, (label, shot) in enumerate(shots):
            tile.paste(shot.crop(crop).resize((size, size), Image.LANCZOS), (index * (size + 12), 26))
            colour = BAD if index < 2 else GOOD
            draw.text((index * (size + 12) + 2, 4), f"{'before' if index < 2 else 'after'}"
                      f"{' — exposed marked' if label == 'marked' else ''}", fill=colour, font=font(15))
        draw.text((2, size + 34), f"{outfit_name}   {counts}", fill=INK, font=font(16))
        draw.text((2, size + 54), note, fill=GOLD, font=font(13))
        tiles.append(tile)

    width = tiles[0].width + 36
    sheet = Image.new("RGBA", (width, 118 + len(tiles) * (tiles[0].height + 16)), PAPER)
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 16), "Undergarment showing through the outfits", fill=INK, font=font(30))
    draw.text((18, 56), "The base wears a neutral tank so the mannequin is never nude. Outfits 006-010 were registered "
                        "after the original coverage pass and were never checked against it.", fill=DIM, font=font(16))
    draw.text((18, 80), "RED = fit gap, garment failed to meet the arm — now repainted.    "
                        "AMBER = neckline the outfit means to leave open — left alone.", fill=GOLD, font=font(16))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, (18, 118 + index * (tile.height + 16)))
    sheet.convert("RGB").save(out)
    print(f"Wrote {out} {sheet.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
