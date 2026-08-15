"""Render pose-specific QA composites for DG-143–DG-144.

Evidence-only renderer. It composites each unregistered review candidate above the
approved palm-up base pose and does not alter assets, manifest, backlog, or ledger.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "qa"
COMPOSITES = OUT / "composites"
BASE = ROOT / "assets" / "base_bodies" / "base_pose_004_viewer_left_palm_up.png"
ITEMS = [
    ("DG-143", ROOT / "incoming" / "hand_objects" / "hand_object_011_round_talisman_pose_004_left.png", "hand_object_011_over_pose_004.png"),
    ("DG-144", ROOT / "incoming" / "hand_objects" / "hand_object_012_brown_tome_pose_004_left.png", "hand_object_012_over_pose_004.png"),
]

def composite(trait_path, out_path):
    base = Image.open(BASE).convert("RGBA")
    trait = Image.open(trait_path).convert("RGBA")
    if base.size != (1254, 1254) or trait.size != (1254, 1254):
        raise ValueError("expected 1254x1254 inputs")
    canvas = Image.new("RGBA", base.size, (255, 255, 255, 255))
    canvas.alpha_composite(base)
    canvas.alpha_composite(trait)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path)
    return out_path

def main():
    results = [(bid, composite(candidate, COMPOSITES / filename)) for bid, candidate, filename in ITEMS]
    cell, pad, label_h = 420, 16, 44
    sheet = Image.new("RGB", (len(results) * (cell + pad) + pad, cell + label_h + 64), (24, 24, 28))
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, 12), "Demigods hand-object pose review — DG-143–DG-144", fill=(240, 240, 240))
    for index, (bid, path) in enumerate(results):
        x, y = pad + index * (cell + pad), 44
        image = Image.open(path).convert("RGB")
        image.thumbnail((cell, cell))
        sheet.paste(image, (x + (cell - image.width) // 2, y))
        draw.text((x + 4, y + cell + 6), f"{bid}  POSE CONTEXT", fill=(120, 230, 140))
        draw.text((x + 4, y + cell + 21), path.name, fill=(180, 180, 190))
    out = OUT / "hand_objects_011-012_pose_review_sheet.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"Rendered {len(results)} pose composites")
    print(f"Review sheet: {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
