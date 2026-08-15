"""Render pose-specific QA composites for DG-138–DG-142.

Evidence-only renderer. It composites each unregistered review candidate above the
approved base pose and does not alter assets, manifest, backlog, or ledger state.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "qa"
COMPOSITES = OUT / "composites"
BASE = ROOT / "assets" / "base_bodies" / "base_pose_002_viewer_left_vertical_grip.png"

ITEMS = [
    ("DG-138", ROOT / "incoming" / "hand_objects" / "hand_object_006_gold_lantern_pose_002_left.png", "hand_object_006_over_pose_002.png"),
    ("DG-139", ROOT / "incoming" / "hand_objects" / "hand_object_007_gold_blue_gem_staff_pose_002_left.png", "hand_object_007_over_pose_002.png"),
    ("DG-140", ROOT / "incoming" / "hand_objects" / "hand_object_008_blue_crescent_staff_pose_002_left.png", "hand_object_008_over_pose_002.png"),
    ("DG-141", ROOT / "incoming" / "hand_objects" / "hand_object_009_violet_blade_pose_002_left.png", "hand_object_009_over_pose_002.png"),
    ("DG-142", ROOT / "incoming" / "hand_objects" / "hand_object_010_horned_skull_scepter_pose_002_left.png", "hand_object_010_over_pose_002.png"),
]

def composite(trait_path: Path, out_path: Path) -> Path:
    base = Image.open(BASE).convert("RGBA")
    trait = Image.open(trait_path).convert("RGBA")
    if base.size != (1254, 1254) or trait.size != (1254, 1254):
        raise ValueError(f"expected 1254x1254 inputs: {BASE.name}, {trait_path.name}")
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
    draw.text((pad, 12), "Demigods hand-object pose review — DG-138–DG-142", fill=(240, 240, 240))
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
    results = []
    for backlog_id, candidate, filename in ITEMS:
        results.append((backlog_id, composite(candidate, COMPOSITES / filename)))
    sheet = render_sheet(results, OUT / "hand_objects_006-010_pose_review_sheet.png")
    print(f"Rendered {len(results)} pose composites")
    print(f"Review sheet: {sheet.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
