#!/usr/bin/env python3
"""Render pose-specific QA composites for a Demigods hand-object review batch.

This renderer is evidence-only. It composites each unregistered review candidate
above its approved base pose in canonical layer order; it does not alter assets,
manifest, backlog, or ledger state.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "qa"
COMPOSITES = OUT / "composites"

ITEMS = [
    (
        "DG-133",
        ROOT / "assets" / "base_bodies" / "base_pose_002_viewer_left_vertical_grip.png",
        ROOT / "incoming" / "hand_objects" / "hand_object_001_arcane_staff_pose_002_left.png",
        "hand_object_001_over_pose_002.png",
    ),
    (
        "DG-134",
        ROOT / "assets" / "base_bodies" / "base_pose_004_viewer_left_palm_up.png",
        ROOT / "incoming" / "hand_objects" / "hand_object_002_violet_orb_pose_004_left.png",
        "hand_object_002_over_pose_004.png",
    ),
    (
        "DG-135",
        ROOT / "assets" / "base_bodies" / "base_pose_002_viewer_left_vertical_grip.png",
        ROOT / "incoming" / "hand_objects" / "hand_object_003_dark_wand_pose_002_left.png",
        "hand_object_003_over_pose_002.png",
    ),
    (
        "DG-136",
        ROOT / "assets" / "base_bodies" / "base_pose_002_viewer_left_vertical_grip.png",
        ROOT / "incoming" / "hand_objects" / "hand_object_004_silver_sword_pose_002_left.png",
        "hand_object_004_over_pose_002.png",
    ),
    (
        "DG-137",
        ROOT / "assets" / "base_bodies" / "base_pose_004_viewer_left_palm_up.png",
        ROOT / "incoming" / "hand_objects" / "hand_object_005_star_spellbook_pose_004_left.png",
        "hand_object_005_over_pose_004.png",
    ),
]


def composite(base_path: Path, trait_path: Path, out_path: Path) -> Path:
    base = Image.open(base_path).convert("RGBA")
    trait = Image.open(trait_path).convert("RGBA")
    if base.size != (1254, 1254) or trait.size != (1254, 1254):
        raise ValueError(f"expected 1254x1254 inputs: {base_path.name}, {trait_path.name}")
    canvas = Image.new("RGBA", base.size, (255, 255, 255, 255))
    canvas.alpha_composite(base)
    canvas.alpha_composite(trait)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path)
    return out_path


def render_sheet(results: list[tuple[str, Path]], out_path: Path) -> Path:
    cell, pad, label_h = 300, 12, 44
    width = len(results) * (cell + pad) + pad
    height = cell + label_h + 64
    sheet = Image.new("RGB", (width, height), (24, 24, 28))
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, 12), "Demigods hand-object pose review — 5 candidates", fill=(240, 240, 240))
    for index, (backlog_id, image_path) in enumerate(results):
        x = pad + index * (cell + pad)
        y = 44
        image = Image.open(image_path).convert("RGB")
        image.thumbnail((cell, cell))
        sheet.paste(image, (x + (cell - image.width) // 2, y))
        draw.text((x + 4, y + cell + 6), f"{backlog_id}  POSE CONTEXT", fill=(120, 230, 140))
        draw.text((x + 4, y + cell + 21), image_path.name[:37], fill=(180, 180, 190))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)
    return out_path


def main() -> int:
    results: list[tuple[str, Path]] = []
    for backlog_id, base, candidate, filename in ITEMS:
        result = composite(base, candidate, COMPOSITES / filename)
        results.append((backlog_id, result))
    sheet = render_sheet(results, OUT / "hand_objects_001-005_pose_review_sheet.png")
    print(f"Rendered {len(results)} pose composites")
    print(f"Review sheet: {sheet.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
