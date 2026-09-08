#!/usr/bin/env python3
"""Render the before/after approval sheets for the realigned pending candidates.

Two sheets are produced:

* `head_accessories_approval.png` - each of the ten head accessories at its old
  uniform 520 px / top_y 129 placement beside its re-seated version, over the
  base master with the silver hair pair and an outfit.
* `hand_objects_approval.png` - each of the five hand objects at the retired
  shared X 404 anchor beside its version realigned to the measured grip contact,
  in its own approved pose, plus finished characters built from the result.

Nothing here registers an asset. The sheets exist so a human can approve or
reject each backlog row by ID.

    python scripts/render_alignment_approval_sheet.py \
      --aligned incoming/aligned_2026-09-07 \
      --out-dir docs/qa/aligned_candidates_2026-09-07
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

INK = (238, 240, 246)
DIM = (150, 156, 172)
GOLD = (255, 214, 120)
BAD = (255, 138, 138)
GOOD = (140, 232, 168)
PANEL = (22, 23, 28)
PAPER = (13, 14, 18)

HEAD_ROWS = [
    ("DG-123", "head_accessory_001_gold_pointed_crown", "520 -> 330 wide; lowest ink Y408 -> Y356"),
    ("DG-124", "head_accessory_002_large_gold_halo", "520 circle -> 400x115 ellipse; Y655 -> Y243"),
    ("DG-125", "head_accessory_003_green_laurel", "520 -> 310 wide; Y571 -> Y392"),
    ("DG-126", "head_accessory_004_black_curved_horns", "500 -> 200 wide; Y580 -> Y308, bases clear of the eyes"),
    ("DG-127", "head_accessory_005_silver_winged_circlet", "520 -> 350 wide; Y407 -> Y315"),
    ("DG-128", "head_accessory_006_silver_ornate_tiara", "520 -> 370 wide; Y444 -> Y352"),
    ("DG-129", "head_accessory_007_silver_drop_circlet", "520 -> 370 wide, seat 129 -> 180; Y313 -> Y310"),
    ("DG-130", "head_accessory_008_translucent_white_veil", "480 -> 420 wide; Y511 -> Y462"),
    ("DG-131", "head_accessory_009_pale_blue_spiked_tiara", "520 -> 390 wide; Y339 -> Y285"),
    ("DG-132", "head_accessory_010_gold_low_circlet", "520 -> 360 wide, seat 129 -> 200; Y279 -> Y303"),
]

HAND_ROWS = [
    ("DG-133", "hand_object_001_arcane_staff_pose_002_left", 2, "x404 -> grip 438,772 + 12 deg lean"),
    ("DG-134", "hand_object_002_violet_orb_pose_004_left", 4, "x404 -> palm 438,748, raised 30 px"),
    ("DG-135", "hand_object_003_dark_wand_pose_002_left", 2, "x404 -> grip 438,772 + 12 deg lean"),
    ("DG-136", "hand_object_004_silver_sword_pose_002_left", 2, "x404 -> grip 438,772 + 12 deg lean"),
    ("DG-137", "hand_object_005_star_spellbook_pose_004_left", 4, "x404 -> palm 438,748, raised 25 px"),
]

POSE_STACK = {
    2: ("assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png",
        "assets/outfits/outfit_002_storm_guardian_pose_002.png"),
    4: ("assets/base_bodies/base_pose_004_viewer_left_palm_up.png",
        "assets/outfits/outfit_004_lunar_oracle_pose_004.png"),
}

HEAD_STACK = [
    "assets/backgrounds/background_006_moonlit_marble_balcony.png",
    "assets/hair_back/hair_back_003_silver_long_wavy.png",
    "assets/base_bodies/base_body_001_neutral_master.png",
    "assets/outfits/outfit_001_celestial_scholar_pose_001.png",
    "assets/hair_front/hair_front_003_silver_straight_bangs.png",
]

_font_cache: dict[int, ImageFont.FreeTypeFont] = {}


def font(size: int):
    if size not in _font_cache:
        for path in FONT_CANDIDATES:
            if Path(path).exists():
                _font_cache[size] = ImageFont.truetype(path, size)
                break
        else:
            _font_cache[size] = ImageFont.load_default()
    return _font_cache[size]


_layer_cache: dict[str, Image.Image] = {}


def layer(path: Path | str) -> Image.Image:
    key = str(path)
    if key not in _layer_cache:
        with Image.open(key) as handle:
            _layer_cache[key] = handle.convert("RGBA")
    return _layer_cache[key]


def composite(paths) -> Image.Image:
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    for item in paths:
        canvas.alpha_composite(layer(item))
    return canvas


def brow_line(image: Image.Image) -> Image.Image:
    """Mark the eyebrow line a head-worn band has to clear."""
    marked = image.copy()
    ImageDraw.Draw(marked).line([(350, 308), (910, 308)], fill=(255, 70, 70, 140), width=3)
    return marked


def pair_row(before: Image.Image, after: Image.Image, crop, size, dg, name, change):
    width = size * 2 + 30
    tile = Image.new("RGBA", (width, size + 64), PANEL)
    tile.paste(before.crop(crop).resize((size, size), Image.LANCZOS), (0, 26))
    tile.paste(after.crop(crop).resize((size, size), Image.LANCZOS), (size + 30, 26))
    draw = ImageDraw.Draw(tile)
    draw.text((2, 4), "before", fill=BAD, font=font(15))
    draw.text((size + 32, 4), "after", fill=GOOD, font=font(15))
    draw.text((2, size + 32), f"{dg}  {name}", fill=INK, font=font(15))
    draw.text((2, size + 50), change, fill=GOLD, font=font(13))
    return tile


def build_head_sheet(old_dir: Path, new_dir: Path, size: int = 300) -> Image.Image:
    crop = (300, 80, 960, 740)
    tiles = []
    for dg, name, change in HEAD_ROWS:
        before = brow_line(composite(HEAD_STACK + [old_dir / f"{name}.png"]))
        after = brow_line(composite(HEAD_STACK + [new_dir / f"{name}.png"]))
        tiles.append(pair_row(before, after, crop, size, dg, name, change))
    cols, tile_w, tile_h = 2, tiles[0].width, tiles[0].height
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * (tile_w + 18) + 18, 96 + rows * (tile_h + 18)), PAPER)
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 18), "Head accessories DG-123 … DG-132 — resize and reseat", fill=INK, font=font(30))
    draw.text((18, 58), "Every row was normalized at 520 px wide with its top at Y 129, so bands crossed the face. Each now "
                        "sits on the skull dome and clears the eyebrow line at Y 308-323 (marked red).", fill=DIM, font=font(16))
    for index, tile in enumerate(tiles):
        x = 18 + (index % cols) * (tile_w + 18)
        y = 96 + (index // cols) * (tile_h + 18)
        sheet.paste(tile, (x, y))
    return sheet


def build_hand_sheet(old_dir: Path, new_dir: Path, head_dir: Path, size: int = 330) -> Image.Image:
    crop = (150, 380, 850, 1080)
    tiles = []
    for dg, name, pose, change in HAND_ROWS:
        body, outfit = POSE_STACK[pose]
        stack = ["assets/backgrounds/background_003_arcane_library.png",
                 "assets/hair_back/hair_back_002_black_long_wavy.png", body, outfit,
                 "assets/hair_front/hair_front_002_black_side_swept.png"]
        before = composite(stack + [old_dir / f"{name}.png"])
        after = composite(stack + [new_dir / f"{name}.png"])
        tiles.append(pair_row(before, after, crop, size, dg, f"{name}  (pose {pose:03d})", change))

    finals = []
    recipes = [
        ("DG-133 + DG-126", ["assets/backgrounds/background_003_arcane_library.png",
                             "assets/rear_auras/aura_rear_013_violet_flame_ring.png",
                             "assets/back_accessories/back_accessory_005_black_violet_ragged_cloak.png",
                             "assets/hair_back/hair_back_004_violet_long_wavy.png",
                             POSE_STACK[2][0], POSE_STACK[2][1],
                             "assets/neck_accessories/neck_accessory_004_silver_dark_round_pendant.png",
                             "assets/hair_front/hair_front_004_violet_parted_bangs.png",
                             head_dir / "head_accessory_004_black_curved_horns.png",
                             new_dir / "hand_object_001_arcane_staff_pose_002_left.png"]),
        ("DG-134 + DG-130", ["assets/backgrounds/background_001_celestial_throne_hall.png",
                             "assets/rear_auras/aura_rear_008_gold_neon_ring.png",
                             "assets/back_accessories/back_accessory_001_silver_feathered_wings.png",
                             "assets/hair_back/hair_back_003_silver_long_wavy.png",
                             POSE_STACK[4][0], POSE_STACK[4][1],
                             "assets/neck_accessories/neck_accessory_006_silver_pale_circle_charm.png",
                             "assets/hair_front/hair_front_003_silver_straight_bangs.png",
                             head_dir / "head_accessory_008_translucent_white_veil.png",
                             new_dir / "hand_object_002_violet_orb_pose_004_left.png"]),
        ("DG-136 + DG-124", ["assets/backgrounds/background_005_solar_sky_temple.png",
                             "assets/rear_auras/aura_rear_011_fire_ring.png",
                             "assets/back_accessories/back_accessory_007_gold_luminous_wings.png",
                             "assets/hair_back/hair_back_001_gold_long_wavy.png",
                             POSE_STACK[2][0], POSE_STACK[2][1],
                             "assets/neck_accessories/neck_accessory_007_gold_teardrop_pendant.png",
                             "assets/hair_front/hair_front_001_gold_parted_bangs.png",
                             head_dir / "head_accessory_002_large_gold_halo.png",
                             new_dir / "hand_object_004_silver_sword_pose_002_left.png"]),
        ("DG-137 + DG-123", ["assets/backgrounds/background_008_violet_void_portal.png",
                             "assets/rear_auras/aura_rear_016_cosmic_sparkle_ring.png",
                             "assets/back_accessories/back_accessory_002_black_violet_bat_wings.png",
                             "assets/hair_back/hair_back_002_black_long_wavy.png",
                             POSE_STACK[4][0], POSE_STACK[4][1],
                             "assets/neck_accessories/neck_accessory_003_black_ribbon_bow.png",
                             "assets/hair_front/hair_front_002_black_side_swept.png",
                             head_dir / "head_accessory_001_gold_pointed_crown.png",
                             new_dir / "hand_object_005_star_spellbook_pose_004_left.png"]),
    ]
    for label, stack in recipes:
        card = Image.new("RGBA", (size + 30, size + 64), PANEL)
        card.paste(composite(stack).resize((size, size), Image.LANCZOS), (0, 26))
        draw = ImageDraw.Draw(card)
        draw.text((2, 4), "finished token", fill=GOOD, font=font(15))
        draw.text((2, size + 32), label, fill=INK, font=font(15))
        draw.text((2, size + 50), "aligned candidates in a full stack", fill=GOLD, font=font(13))
        finals.append(card)

    tile_w, tile_h = tiles[0].width, tiles[0].height
    head_h = 96
    body_h = 3 * (tile_h + 18)
    finals_h = 46 + finals[0].height + 18
    sheet = Image.new("RGBA", (2 * (tile_w + 18) + 18, head_h + body_h + finals_h), PAPER)
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 18), "Hand objects DG-133 … DG-137 — realign to the measured grip contact", fill=INK, font=font(30))
    draw.text((18, 58), "All five sat on the retired shared anchor X 404, which lands at the wrist. They now use the "
                        "same contacts and lean as the registered objects.", fill=DIM, font=font(16))
    for index, tile in enumerate(tiles):
        sheet.paste(tile, (18 + (index % 2) * (tile_w + 18), head_h + (index // 2) * (tile_h + 18)))
    y = head_h + body_h
    draw.text((18, y + 10), "Finished tokens built from the realigned candidates", fill=GOLD, font=font(22))
    for index, card in enumerate(finals):
        sheet.paste(card, (18 + index * (card.width + 14), y + 46))
    return sheet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--aligned", type=Path, default=Path("incoming/aligned_2026-09-07"))
    parser.add_argument("--previous", type=Path, default=Path("incoming"))
    parser.add_argument("--out-dir", type=Path, default=Path("docs/qa/aligned_candidates_2026-09-07"))
    args = parser.parse_args(argv)

    aligned = args.aligned if args.aligned.is_absolute() else ROOT / args.aligned
    previous = args.previous if args.previous.is_absolute() else ROOT / args.previous
    out_dir = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    head = build_head_sheet(previous / "head_accessories", aligned / "head_accessories")
    head.convert("RGB").save(out_dir / "head_accessories_approval.png")
    hand = build_hand_sheet(previous / "hand_objects", aligned / "hand_objects", aligned / "head_accessories")
    hand.convert("RGB").save(out_dir / "hand_objects_approval.png")
    print(f"Wrote {out_dir / 'head_accessories_approval.png'} {head.size}")
    print(f"Wrote {out_dir / 'hand_objects_approval.png'} {hand.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
