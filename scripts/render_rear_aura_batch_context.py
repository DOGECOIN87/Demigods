#!/usr/bin/env python3
"""Render deterministic full-context QA composites for the first remaining rear-aura batch."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/qa/composites"
SHEET_PATH = ROOT / "docs/qa/rear_auras_003_005_011_013_full_context_sheet.png"
AURA_DIR = ROOT / "incoming/rear_auras_003_005_011_013"
BASE = ROOT / "assets/base_bodies/base_body_001_neutral_master.png"
HAIR_BACK = ROOT / "assets/hair_back/hair_back_008_red_long_wavy.png"
HAIR_FRONT = ROOT / "assets/hair_front/hair_front_008_red_short_bangs.png"
OUTFIT = ROOT / "assets/outfits/outfit_009_navy_high_collar_coat.png"
AURAS = [
    "aura_rear_003_blue_crystalline_burst.png",
    "aura_rear_005_lavender_lightning.png",
    "aura_rear_011_fire_ring.png",
    "aura_rear_012_lightning_ring.png",
    "aura_rear_013_violet_flame_ring.png",
]
BACKGROUNDS = [
    "background_001_celestial_throne_hall.png",
    "background_008_violet_void_portal.png",
]


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def render(background_name: str, aura_name: str) -> Image.Image:
    canvas = rgba(ROOT / "assets/backgrounds" / background_name)
    canvas.alpha_composite(rgba(AURA_DIR / aura_name))
    canvas.alpha_composite(rgba(HAIR_BACK))
    canvas.alpha_composite(rgba(BASE))
    canvas.alpha_composite(rgba(OUTFIT))
    canvas.alpha_composite(rgba(HAIR_FRONT))
    return canvas


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    thumb, label_h = 250, 34
    sheet = Image.new("RGB", (thumb * len(AURAS), (thumb + label_h) * len(BACKGROUNDS)), (25, 25, 30))
    draw = ImageDraw.Draw(sheet)
    for row, background_name in enumerate(BACKGROUNDS):
        background_stem = Path(background_name).stem
        for col, aura_name in enumerate(AURAS):
            aura_stem = Path(aura_name).stem
            composite = render(background_name, aura_name)
            output = OUT_DIR / f"{aura_stem}_with_red_hair_navy_coat_over_{background_stem}.png"
            composite.save(output)
            preview = composite.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS)
            x = col * thumb
            y = row * (thumb + label_h)
            sheet.paste(preview, (x, y))
            draw.text((x + 8, y + thumb + 10), aura_stem.replace("aura_rear_", ""), fill=(235, 235, 235))
    sheet.save(SHEET_PATH)
    print(f"Rendered {len(AURAS) * len(BACKGROUNDS)} rear-aura context composites")
    print(SHEET_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
