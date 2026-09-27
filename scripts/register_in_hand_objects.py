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

Round 1 (1024 x 1024 WebP): of seven renders, only the arcane staff and the
violet orb were registered. The owner rejected the dark wand, silver sword and
gold staff with blue gem, whose painted hands were so large that fitting them
shrank the item by about a third; the star spellbook shows a cut-off wrist stump
above the book; and the gold lantern's hand is so large the lantern ends up
tiny. Their sources are kept for reference.

Round 2 (1920 x 1920 PNG, all twelve items): the gold lantern, gold staff with
blue gem, blue crescent staff and brown tome were registered; each was fitted and
then reviewed again independently (docs/qa/hand_objects_in_hand_2026-09-26.md).
These renders carry faint speckle across the canvas and never reach full alpha,
so before fitting, alpha below 16 is dropped along with specks smaller than 0.2%
of the largest piece, and after fitting alpha of 250 or more is set to 255. Their
scale and offset were chosen by comparing candidate fits on the bare and dressed
bodies (the hand has to cover the body's own hand, the item has to stay close to
its old size), so they are recorded directly rather than derived from a width.

2026-09-27 (docs/qa/hand_objects_in_hand_2026-09-27.md): two of the owner's six
candidates, the dark wand and the star spellbook, were registered from
images/trait_candidates/hand_objects/in_hand_2026-09-27/. The round-1 arcane staff and
violet orb, and the round-2 gold staff with blue gem, were fitted again from the same
renders, because their painted hands left an edge of the body's own hand showing. Their
offsets were found with the fit tool's cover command rather than by centring the painted hand.

To register a new batch, add an entry to BATCHES (its source folder, decision date, QA
note and item table) and run the script again. Batches are applied in order, so a later
batch's render for the same item replaces an earlier one. Every source listed here is
re-read on each run, so each must stay committed.

    python scripts/register_in_hand_objects.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
SOURCES = ROOT / "images" / "trait_candidates" / "hand_objects" / "in_hand_2026-09-26"
ROUND2 = SOURCES / "round2"
CANDIDATES_0927 = ROOT / "images" / "trait_candidates" / "hand_objects" / "in_hand_2026-09-27"
ALPHA_FLOOR = 16
SPECK_FRACTION = 0.002
OPAQUE_FROM = 250
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

# Round 1. asset id -> (source render, pose, painted-hand centre, painted-hand width)
ITEMS = {
    "hand_object_001": ("001_arcane_staff_source.webp", 2, (494, 638), 85),
    "hand_object_002": ("002_violet_crystal_orb_source.webp", 4, (490, 718), 200),
}

# Round 2. asset id -> (source render, pose, painted-hand centre and width in the source, scale, offset)
# The scale may be 1 (placement only) for a render already drawn at the body's size, never above.
ROUND2_ITEMS = {
    "hand_object_006": ("006_gold_lantern.png", 2, (945.8, 351.3), 312, 0.251, (210, 680)),
    "hand_object_007": ("007_gold_staff_with_blue_gem.png", 2, (906, 1140), 177, 0.4, (85, 312)),
    "hand_object_008": ("008_blue_crescent_staff.png", 2, (906, 1012), 165, 0.435, (53, 328)),
    "hand_object_012": ("012_brown_tome.png", 4, (1118.5, 1019.9), 587, 0.186, (238, 549)),
}

# 2026-09-27, same fields as ROUND2_ITEMS. Two of the owner's 2026-09-26 candidates.
ITEMS_0927 = {
    "hand_object_003": ("003_dark_wand.png", 2, (465.5, 757.2), 87, 0.95, (4, 49)),
    "hand_object_005": ("005_star_spellbook.png", 4, (437.0, 895.7), 186, 0.6, (178, 219)),
}
# 2026-09-27: the round-1 renders fitted again so the painted hand covers the body's own hand.
ROUND1_REFIT_0927 = {
    "hand_object_001": ("001_arcane_staff_source.webp", 2, (491.4, 634.9), 88, 0.93, (-11, 184)),
    "hand_object_002": ("002_violet_crystal_orb_source.webp", 4, (407.0, 715.8), 363, 0.49, (217, 384)),
}
# 2026-09-27: the round-2 gold staff fitted again, 7.5% larger, so its painted fist covers the body's.
ROUND2_REFIT_0927 = {
    "hand_object_007": ("007_gold_staff_with_blue_gem.png", 2, (906, 1140), 177, 0.43, (58, 276)),
}
QA_0927 = {"decided_on": "2026-09-27", "qa_report": "docs/qa/hand_objects_in_hand_2026-09-27.md",
           "qa_composite": "docs/qa/hand_objects_in_hand_2026-09-27.png"}
QA_PASS_0927 = {
    "decided_on": "2026-09-27",
    "qa_report": "docs/qa/hand_objects_in_hand_2026-09-27-passing.md",
    "qa_composite": "docs/qa/hand_objects_in_hand_2026-09-27-passing.png",
    "prompt": "prompts/hand_objects_in_hand_pack_2026-09-27.md",
    "items": {
        "hand_object_004": ("004_silver_sword.png", 2, (629.3, 958.2), 100, 0.79, (-53, 12)),
        "hand_object_008": ("008_blue_crescent_staff.png", 2, (906, 1012), 165, 0.46, (31, 303)),
        "hand_object_010": ("010_horned_skull_scepter.png", 2, (623.6, 863.6), 98, 0.76, (-34, 116)),
    },
}

# Batches fitted with scripts/fit_in_hand_render.py, applied in order after round 1.
BATCHES = [
    {"folder": ROUND2, "decided_on": DECIDED_ON,
     "qa_report": "docs/qa/hand_objects_in_hand_2026-09-26.md",
     "qa_composite": "docs/qa/hand_objects_in_hand_2026-09-26.png",
     "items": ROUND2_ITEMS},
    {"folder": CANDIDATES_0927, **QA_0927, "items": ITEMS_0927},
    {"folder": SOURCES, **QA_0927, "items": ROUND1_REFIT_0927},
    {"folder": ROUND2, **QA_0927, "items": ROUND2_REFIT_0927},
    {"folder": ROOT / "images" / "trait_candidates" / "hand_objects" / "in_hand_2026-09-27-pass", **QA_PASS_0927},
]


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


def clean_render(source: Path) -> Image.Image:
    """Drop the faint speckle round-2 renders carry: low alpha, then tiny detached pieces."""
    with Image.open(source) as opened:
        pixels = np.asarray(opened.convert("RGBA")).copy()
    alpha = pixels[..., 3]
    alpha[alpha < ALPHA_FLOOR] = 0
    labels, count = ndimage.label(alpha > 0)
    if count > 1:
        sizes = ndimage.sum(alpha > 0, labels, range(1, count + 1))
        keep = np.isin(labels, [i + 1 for i, size in enumerate(sizes) if size >= SPECK_FRACTION * sizes.max()])
        alpha[~keep] = 0
    return Image.fromarray(pixels, "RGBA")


def fit_round2(source: Path, scale: float, offset: tuple[int, int]) -> tuple[Image.Image, dict]:
    if not 0 < scale <= 1:
        raise ValueError(f"{source.name}: scale {scale:.3f} would enlarge the render")
    render = clean_render(source)
    size = (round(render.width * scale), round(render.height * scale))
    reduced = render.resize(size, Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    layer.paste(reduced, offset, reduced)
    pixels = np.asarray(layer).copy()
    pixels[..., 3][pixels[..., 3] >= OPAQUE_FROM] = 255
    layer = Image.fromarray(pixels, "RGBA")
    bounds = layer.getchannel("A").getbbox()
    if bounds is None or bounds[0] == 0 or bounds[1] == 0 or bounds[2] == CANVAS[0] or bounds[3] == CANVAS[1]:
        raise ValueError(f"{source.name}: fitted layer touches the canvas edge: {bounds}")
    return layer, {
        "scale": scale,
        "offset": list(offset),
        "output_bounds": [bounds[0], bounds[1], bounds[2] - 1, bounds[3] - 1],
        "cleanup": {"alpha_floor": ALPHA_FLOOR, "speck_fraction": SPECK_FRACTION, "opaque_from": OPAQUE_FROM},
    }


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in manifest["registered_production_assets"]}
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    requires = {rule["trait"]: rule for rule in compatibility["requires"]}
    in_hand = compatibility.setdefault("in_hand", [])
    in_hand_traits = {rule["trait"] for rule in in_hand}

    round1 = {"decided_on": DECIDED_ON, "qa_report": "docs/qa/hand_objects_in_hand_2026-09-26.md",
              "qa_composite": "docs/qa/hand_objects_in_hand_2026-09-26.png"}
    jobs = [(asset_id, SOURCES / name, pose, centre, width, None, None, round1)
            for asset_id, (name, pose, centre, width) in ITEMS.items()]
    for batch in BATCHES:
        jobs += [(asset_id, batch["folder"] / name, pose, centre, width, scale, offset, batch)
                 for asset_id, (name, pose, centre, width, scale, offset) in batch["items"].items()]
    for asset_id, source, pose, centre, width, scale, offset, batch in jobs:
        entry = entries[asset_id]
        asset = ROOT / entry["path"]
        if scale is None:
            layer, transform = fit(source, pose, centre, width)
            method = "reduce_to_base_hand_width_then_translate_hand_centre"
        else:
            layer, transform = fit_round2(source, scale, offset)
            method = "clean_speckle_then_reduce_and_place_by_reviewed_fit"
        layer.save(asset, "PNG", optimize=True)
        base = BASE_HANDS[pose]
        with Image.open(source) as opened:
            source_size = list(opened.size)
        entry["sha256"] = sha256(asset)
        entry["approved_on"] = batch["decided_on"]
        entry["qa_report"] = batch["qa_report"]
        entry["qa_composite"] = batch["qa_composite"]
        previous_provenance = entry.get("provenance", {})
        prior_source_hash = previous_provenance.get("source_sha256")
        current_source_hash = sha256(source)
        if "superseded_provenance" in previous_provenance:
            inherited_provenance = previous_provenance["superseded_provenance"]
        elif prior_source_hash != current_source_hash:
            inherited_provenance = previous_provenance
        else:
            inherited_provenance = None
        provenance = {
            "origin": "generator_render_painted_in_hand",
            "trait": entry["provenance"].get("trait"),
            "prompt": batch.get("prompt", PROMPTS),
            "reference_path": base["path"],
            "source_path": source.relative_to(ROOT).as_posix(),
            "source_sha256": current_source_hash,
            "source_dimensions": source_size,
            "pose": pose,
            "contact_feature": f"painted hand over the base's {base['feature']}",
            "painted_hand": {"centre": list(centre), "width": width},
            "base_hand": {"centre": list(base["centre"]), "width": base["width"]},
            "transform": {"method": method, "resample": "lanczos", **transform},
            "intake_script": "scripts/register_in_hand_objects.py",
            "native_dimensions": list(CANVAS),
        }
        if inherited_provenance:
            provenance["superseded_provenance"] = inherited_provenance
        entry["provenance"] = provenance
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
