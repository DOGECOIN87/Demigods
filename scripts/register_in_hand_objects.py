#!/usr/bin/env python3
"""Register hand objects painted together with the hand that holds them (2026-09-26).

The owner asked for every held item to be drawn with the hand already gripping
it, so no separate hand overlay is needed. The renders were made from
``prompts/hand_objects_in_hand_pack_2026-09-26.md`` and are preserved unedited
under images/trait_candidates/hand_objects/in_hand_2026-09-26/.

Each render is a 1024 x 1024 RGBA image whose painted hand is larger than the
body's. This reduces it (scale < 1, Lanczos) so the painted hand matches the
width of the base's own hand, and places it so the painted hand's centre lands
on the base hand's centre. The hand centres and widths below were measured on
each render by eye; the base values are the skin extent of the base pose's hand.

The result replaces the registered asset of the same name, so every requires and
excludes rule keeps applying. An ``in_hand`` rule in config/compatibility.json
makes the renderer draw it over the body (scripts/generate_777.py).

Of the seven renders received, the star spellbook (a cut-off wrist stump shows
above the book) and the gold lantern (the hand is so large the lantern ends up
tiny) were not registered; their sources are kept for reference.

    python scripts/register_in_hand_objects.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
SOURCES = ROOT / "images" / "trait_candidates" / "hand_objects" / "in_hand_2026-09-26"
PROMPTS = "prompts/hand_objects_in_hand_pack_2026-09-26.md"
DECIDED_ON = "2026-09-26"
CANVAS = (1254, 1254)

# Base hand: centre and width of the skin, measured on the base pose.
BASE_HANDS = {
    2: {"path": "assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png",
        "centre": (448, 758), "width": 72, "feature": "closed fist"},
    4: {"path": "assets/base_bodies/base_pose_004_viewer_left_palm_up.png",
        "centre": (447, 730), "width": 98, "feature": "open palm"},
}

# asset id -> (source render, pose, painted-hand centre, painted-hand width)
ITEMS = {
    "hand_object_001": ("001_arcane_staff_source.webp", 2, (494, 638), 85),
    "hand_object_002": ("002_violet_crystal_orb_source.webp", 4, (490, 718), 200),
    "hand_object_003": ("003_dark_wand_source.webp", 2, (463, 757), 133),
    "hand_object_004": ("004_silver_sword_source.webp", 2, (523, 801), 123),
    "hand_object_007": ("007_gold_staff_with_blue_gem_source.webp", 2, (437, 665), 134),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit(source: Path, pose: int, centre: tuple[int, int], width: int) -> tuple[Image.Image, dict]:
    base = BASE_HANDS[pose]
    scale = base["width"] / width
    if not 0 < scale < 1:
        raise ValueError(f"{source.name}: scale {scale:.3f} is not a reduction")
    with Image.open(source) as opened:
        render = opened.convert("RGBA")
    size = (round(render.width * scale), round(render.height * scale))
    reduced = render.resize(size, Image.Resampling.LANCZOS)
    offset = (round(base["centre"][0] - centre[0] * scale), round(base["centre"][1] - centre[1] * scale))
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    layer.paste(reduced, offset, reduced)
    bounds = layer.getchannel("A").getbbox()
    if bounds is None or bounds[0] == 0 or bounds[1] == 0 or bounds[2] == CANVAS[0] or bounds[3] == CANVAS[1]:
        raise ValueError(f"{source.name}: fitted layer touches the canvas edge: {bounds}")
    return layer, {
        "scale": round(scale, 4),
        "offset": list(offset),
        "output_bounds": [bounds[0], bounds[1], bounds[2] - 1, bounds[3] - 1],
    }


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in manifest["registered_production_assets"]}
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    requires = {rule["trait"]: rule for rule in compatibility["requires"]}
    in_hand = compatibility.setdefault("in_hand", [])
    in_hand_traits = {rule["trait"] for rule in in_hand}

    for asset_id, (source_name, pose, centre, width) in ITEMS.items():
        entry = entries[asset_id]
        source = SOURCES / source_name
        asset = ROOT / entry["path"]
        layer, transform = fit(source, pose, centre, width)
        layer.save(asset, "PNG", optimize=True)
        base = BASE_HANDS[pose]
        with Image.open(source) as opened:
            source_size = list(opened.size)
        entry["sha256"] = sha256(asset)
        entry["approved_on"] = DECIDED_ON
        entry["qa_report"] = "docs/qa/hand_objects_in_hand_2026-09-26.md"
        entry["qa_composite"] = "docs/qa/hand_objects_in_hand_2026-09-26.png"
        entry["provenance"] = {
            "origin": "generator_render_painted_in_hand",
            "trait": entry["provenance"].get("trait"),
            "prompt": PROMPTS,
            "reference_path": base["path"],
            "source_path": source.relative_to(ROOT).as_posix(),
            "source_sha256": sha256(source),
            "source_dimensions": source_size,
            "pose": pose,
            "contact_feature": f"painted hand over the base's {base['feature']}",
            "painted_hand": {"centre": list(centre), "width": width},
            "base_hand": {"centre": list(base["centre"]), "width": base["width"]},
            "transform": {"method": "reduce_to_base_hand_width_then_translate_hand_centre",
                          "resample": "lanczos", **transform},
            "intake_script": "scripts/register_in_hand_objects.py",
            "native_dimensions": list(CANVAS),
        }
        name = Path(entry["path"]).name
        rule = requires[name]
        rule["reason"] = (
            f"Painted holding the item in the pose {pose:03d} hand; the painted hand is fitted "
            f"over the base's {base['feature']}."
        )
        if name not in in_hand_traits:
            in_hand.append({
                "trait": name,
                "reason": "Painted with the hand that holds it; drawn over the body so that hand shows.",
            })
        print(f"{asset_id}: scale {transform['scale']} offset {transform['offset']} bounds {transform['output_bounds']}")

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
