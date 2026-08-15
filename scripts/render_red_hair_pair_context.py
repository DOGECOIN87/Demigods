#!/usr/bin/env python3
"""Render deterministic full-context QA composites for the DG-036/DG-122 red hair pair."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SIZE = (1254, 1254)

BACK = ROOT / "incoming/red_hair_pair/hair_back_008_red_long_wavy.png"
FRONT = ROOT / "incoming/red_hair_pair/hair_front_008_red_short_bangs.png"
BASE = ROOT / "assets/base_bodies/base_body_001_neutral_master.png"
OUTFIT = ROOT / "assets/outfits/outfit_001_celestial_scholar_pose_001.png"
BACKGROUND_NAMES = [
    "background_001_celestial_throne_hall.png",
    "background_008_violet_void_portal.png",
]
OUT_DIR = ROOT / "docs/qa/composites"
SHEET_PATH = ROOT / "docs/qa/red_hair_pair_full_context_sheet.png"


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def render_context(background_name: str) -> Image.Image:
    canvas = rgba(ROOT / "assets/backgrounds" / background_name)
    canvas.alpha_composite(rgba(BACK))
    canvas.alpha_composite(rgba(BASE))
    canvas.alpha_composite(rgba(OUTFIT))
    canvas.alpha_composite(rgba(FRONT))
    return canvas


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panels = []
    for background_name in BACKGROUND_NAMES:
        composite = render_context(background_name)
        stem = Path(background_name).stem
        path = OUT_DIR / f"red_hair_pair_over_{stem}.png"
        composite.save(path)
        panels.append((stem, composite))

    thumb = 500
    sheet = Image.new("RGB", (thumb * len(panels), thumb + 54), (25, 25, 30))
    draw = ImageDraw.Draw(sheet)
    for index, (label, composite) in enumerate(panels):
        preview = composite.convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS)
        x = index * thumb
        sheet.paste(preview, (x, 0))
        draw.text((x + 14, thumb + 16), label, fill=(235, 235, 235))
    sheet.save(SHEET_PATH)
    print(f"Rendered {len(panels)} full-context composites")
    print(SHEET_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
