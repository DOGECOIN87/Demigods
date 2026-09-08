#!/usr/bin/env python3
"""Register the approved, realigned head-accessory and hand-object candidates.

Copies the exact approved bytes into `assets/<category>/`, writes a manifest
entry per asset carrying the alignment provenance, flips the backlog rows to
`registered`, binds each hand object to the pose it was fitted for, and drops
the two now-complete categories out of `pending_categories`.

Head accessories and hand objects both become optional: a token wearing no
crown and holding nothing is a normal token, and forcing one of each would
make every character a monarch with a prop.

    python scripts/register_aligned_candidates.py --aligned incoming/aligned_2026-09-07
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
APPROVED_ON = "2026-09-07"
QA_REPORT = "docs/qa/aligned_candidates_2026-09-07/README.md"

HEAD_ACCESSORIES = [
    ("DG-123", "head_accessory_001_gold_pointed_crown", "Gold pointed crown"),
    ("DG-124", "head_accessory_002_large_gold_halo", "Large gold halo ring"),
    ("DG-125", "head_accessory_003_green_laurel", "Green laurel wreath"),
    ("DG-126", "head_accessory_004_black_curved_horns", "Balanced black curved horn set"),
    ("DG-127", "head_accessory_005_silver_winged_circlet", "Silver winged circlet"),
    ("DG-128", "head_accessory_006_silver_ornate_tiara", "Silver ornate tiara"),
    ("DG-129", "head_accessory_007_silver_drop_circlet", "Silver forehead circlet with central drop"),
    ("DG-130", "head_accessory_008_translucent_white_veil", "Translucent white veil"),
    ("DG-131", "head_accessory_009_pale_blue_spiked_tiara", "Pale-blue spiked crown/tiara"),
    ("DG-132", "head_accessory_010_gold_low_circlet", "Gold low-profile circlet"),
]

HAND_OBJECTS = [
    ("DG-133", "hand_object_001_arcane_staff_pose_002_left",
     "Gnarled wood staff with blue flame/crystal", "base_pose_002_viewer_left_vertical_grip.png"),
    ("DG-134", "hand_object_002_violet_orb_pose_004_left",
     "Purple crystal orb", "base_pose_004_viewer_left_palm_up.png"),
    ("DG-135", "hand_object_003_dark_wand_pose_002_left",
     "Slender dark wand", "base_pose_002_viewer_left_vertical_grip.png"),
    ("DG-136", "hand_object_004_silver_sword_pose_002_left",
     "Silver straight sword", "base_pose_002_viewer_left_vertical_grip.png"),
    ("DG-137", "hand_object_005_star_spellbook_pose_004_left",
     "Dark spellbook with gold star emblem", "base_pose_004_viewer_left_palm_up.png"),
]

# A trait in a category the generator treats as optional appears on this share
# of tokens. Head accessories and hand objects are decorative, not structural.
OPTIONAL_RATES = {"head_accessories": 0.55, "hand_objects": 0.60}

POSE_REASON = {
    "base_pose_002_viewer_left_vertical_grip.png":
        "Fitted to the viewer-left closed grip at the measured contact (438, 772), with the "
        "12 degree outward lean the registered pose-002 objects carry.",
    "base_pose_004_viewer_left_palm_up.png":
        "Fitted to the viewer-left open palm at the measured contact (438, 748).",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_entry(name: str, category: str, backlog_id: str, trait: str,
                provenance_sidecar: dict[str, Any], path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        dimensions, mode, fmt = list(image.size), image.mode, image.format
    transform = provenance_sidecar.get("transform", {})
    origin = provenance_sidecar.get("origin", "generator_source_transform")

    provenance: dict[str, Any] = {
        "origin": origin,
        "reference_path": "assets/base_bodies/base_body_001_neutral_master.png",
        "trait": trait,
        "native_dimensions": [1254, 1254],
        "intake_script": "scripts/align_pending_candidates.py",
        "alignment_pass": "aligned_candidates_2026-09-07",
        "output_bounds": provenance_sidecar.get("output_bounds"),
    }
    if origin == "generator_source_transform":
        provenance.update({
            "source_path": provenance_sidecar["source_path"],
            "source_sha256": provenance_sidecar["source_sha256"],
            "source_dimensions": provenance_sidecar["source_dimensions"],
            "alpha_cleanup": provenance_sidecar["alpha_cleanup"],
            "transform": transform,
            "normalization_script": "scripts/normalize_generator_source.py",
            "postprocessing": ["reduction_only_head_reseat_2026-09-07"],
            "alignment": provenance_sidecar.get("alignment"),
        })
    else:
        provenance.update({
            "source_path": provenance_sidecar["source_path"],
            "source_sha256": provenance_sidecar["source_sha256"],
            "source_bounds": provenance_sidecar["source_bounds"],
            "pose": provenance_sidecar["pose"],
            "contact_point": provenance_sidecar["contact_point"],
            "contact_feature": provenance_sidecar["contact_feature"],
            "transform": transform,
            "postprocessing": ["hand_object_contact_realignment_2026-09-07"],
            "realignment_reason": provenance_sidecar.get("reason"),
        })

    return {
        # head_accessory_001_gold_pointed_crown -> head_accessory_001
        "id": "_".join(name.split("_")[:3]),
        "category": category,
        "path": f"assets/{category}/{name}.png",
        "status": "production_ready",
        "sha256": sha256_file(path),
        "dimensions": dimensions,
        "format": fmt or "PNG",
        "mode": mode,
        "backlog_id": backlog_id,
        "provenance": provenance,
        "approved_on": APPROVED_ON,
        "qa_report": QA_REPORT,
    }


def register(aligned: Path) -> list[dict[str, Any]]:
    entries = []
    for backlog_id, name, trait in HEAD_ACCESSORIES:
        source = aligned / "head_accessories" / f"{name}.png"
        sidecar = json.loads(source.with_suffix(".png.provenance.json").read_text())
        destination = ROOT / "assets" / "head_accessories" / f"{name}.png"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        assert sha256_file(destination) == sha256_file(source), name
        entries.append(build_entry(name, "head_accessories", backlog_id, trait, sidecar, destination))

    for backlog_id, name, trait, _pose in HAND_OBJECTS:
        source = aligned / "hand_objects" / f"{name}.png"
        sidecar = json.loads(source.with_suffix(".png.provenance.json").read_text())
        destination = ROOT / "assets" / "hand_objects" / f"{name}.png"
        shutil.copyfile(source, destination)
        assert sha256_file(destination) == sha256_file(source), name
        entries.append(build_entry(name, "hand_objects", backlog_id, trait, sidecar, destination))
    return entries


def update_manifest(entries: list[dict[str, Any]]) -> None:
    path = ROOT / "assets" / "asset_manifest.json"
    manifest = json.loads(path.read_text())
    known = {entry["path"] for entry in manifest["registered_production_assets"]}
    for entry in entries:
        if entry["path"] in known:
            raise SystemExit(f"already registered: {entry['path']}")
    manifest["registered_production_assets"].extend(entries)
    manifest["pending_categories"] = [
        category for category in manifest.get("pending_categories", [])
        if category not in {"head_accessories", "hand_objects"}
    ]
    path.write_text(json.dumps(manifest, indent=2) + "\n")


def update_compatibility() -> None:
    path = ROOT / "config" / "compatibility.json"
    rules = json.loads(path.read_text())
    existing = {(rule["trait"], rule["requires"]) for rule in rules["requires"]}
    for _backlog_id, name, _trait, pose in HAND_OBJECTS:
        key = (f"{name}.png", pose)
        if key in existing:
            continue
        rules["requires"].append({
            "trait": f"{name}.png",
            "requires": pose,
            "reason": POSE_REASON[pose],
        })
    path.write_text(json.dumps(rules, indent=2) + "\n")


def update_collection() -> None:
    path = ROOT / "config" / "collection.json"
    collection = json.loads(path.read_text())
    collection.setdefault("optional_categories", {}).update(OPTIONAL_RATES)
    path.write_text(json.dumps(collection, indent=2) + "\n")


def update_backlog() -> None:
    path = ROOT / "docs" / "trait-production-backlog.md"
    text = path.read_text()
    ids = [row[0] for row in HEAD_ACCESSORIES] + [row[0] for row in HAND_OBJECTS]
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not line.startswith("| DG-"):
            continue
        backlog_id = line.split("|")[1].strip()
        if backlog_id in ids and line.rstrip().endswith("| pending |"):
            lines[index] = line.rstrip()[: -len("| pending |")] + "| registered |\n"
    path.write_text("".join(lines))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--aligned", type=Path, default=Path("incoming/aligned_2026-09-07"))
    args = parser.parse_args(argv)
    aligned = args.aligned if args.aligned.is_absolute() else ROOT / args.aligned

    entries = register(aligned)
    update_manifest(entries)
    update_compatibility()
    update_collection()
    update_backlog()
    for entry in entries:
        print(f"registered {entry['backlog_id']}  {entry['path']}  {entry['sha256'][:12]}")
    print(f"\n{len(entries)} assets registered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
