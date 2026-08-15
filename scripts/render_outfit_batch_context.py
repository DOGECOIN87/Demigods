#!/usr/bin/env python3
"""Render deterministic full-context QA composites for a neutral-pose outfit batch."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/qa/composites"
SHEET_PATH = ROOT / "docs/qa/outfits_006_010_full_context_sheet.png"
BASE = ROOT / "assets/base_bodies/base_body_001_neutral_master.png"
HAIR_BACK = ROOT / "assets/hair_back/hair_back_008_red_long_wavy.png"
HAIR_FRONT = ROOT / "assets/hair_front/hair_front_008_red_short_bangs.png"
OUTFITS = [
    "outfit_006_black_layered_hooded_robe.png",
    "outfit_007_brown_leather_long_coat.png",
    "outfit_008_olive_ragged_cloak.png",
    "outfit_009_navy_high_collar_coat.png",
    "outfit_010_celestial_robe_white_gold.png",
]
BACKGROUNDS = [
    "background_001_celestial_throne_hall.png",
    "background_008_violet_void_portal.png",
]


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def render(background_name: str, outfit_name: str) -> Image.Image:
    canvas = rgba(ROOT / "assets/backgrounds" / background_name)
    canvas.alpha_composite(rgba(HAIR_BACK))
    canvas.alpha_composite(rgba(BASE))
    canvas.alpha_composite(rgba(ROOT / "incoming/outfits_006_010" / outfit_name))
    canvas.alpha_composite(rgba(HAIR_FRONT))
    return canvas


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    thumb = 250
    label_h = 34
    sheet = Image.new("RGB", (thumb * len(OUTFITS), (thumb + label_h) * len(BACKGROUNDS)), (25, 25, 30))
    draw = ImageDraw.Draw(sheet)
    for row, background_name in enumerate(BACKGROUNDS):
        background_stem = Path(background_name).stem
        for col, outfit_name in enumerate(OUTFITS):
            outfit_stem = Path(outfit_name).stem
            composite = render(background_name, outfit_name)
            output = OUT_DIR / f"{outfit_stem}_with_red_hair_over_{background_stem}.png"
            composite.save(output)
            preview = composite.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS)
            x = col * thumb
            y = row * (thumb + label_h)
            sheet.paste(preview, (x, y))
            draw.text((x + 8, y + thumb + 10), outfit_stem.replace("outfit_", ""), fill=(235, 235, 235))
    sheet.save(SHEET_PATH)
    print(f"Rendered {len(OUTFITS) * len(BACKGROUNDS)} outfit-context composites")
    print(SHEET_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
