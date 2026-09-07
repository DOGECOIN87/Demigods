#!/usr/bin/env python3
"""Re-seat the pending head-accessory and hand-object candidates onto the rig.

Both batches passed binary and rig gates already, and both were nonetheless
misplaced, for the same reason: they were normalized against a single fixed
anchor instead of the anchor the design actually needs.

* Every head accessory was normalized at 520 px wide with its top at Y 129, the
  top of the locked character bounds. That is right for a crown and wrong for a
  circlet: a forehead band seated at the top of the canvas floats above the
  skull, and 520 px is wider than the head (329 px) and the hair (419-529 px).
  Each row here carries the width and seat Y its own design needs, measured
  against the base master's skull curve, so the head-contact band lands on the
  hairline just above the eyebrow line at Y 308-323.

* Hand objects 001-005 were normalized against the retired shared hand anchor
  X 404, which `docs/qa/hand_object_recalibration_findings_2026-08-15.md` showed
  sits at the wrist rather than through the hand. The registered objects were
  recalibrated to the measured grip contacts - pose 002 (438, 772) and pose 004
  (438, 748) - and the pose-002 items also carry a 12 degree outward lean so a
  held shaft does not read as an upright prop. These five never received that
  pass; this applies it.

The head accessories are re-derived from their immutable generator sources in a
single reduction, so nothing is resampled twice. The hand objects keep their
already-normalized bytes and receive only the same integer translation and lean
the registered family received.

    python scripts/align_pending_candidates.py --out-dir incoming/aligned_2026-09-07
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
MAX_BOUNDS = (233, 129, 1021, 1139)

# pose -> measured grip/palm contact point, and the lean a held item carries
POSE_CONTACT = {2: (438, 772), 4: (438, 748)}
POSE_LEAN_DEGREES = {2: 12.0, 4: 0.0}

# backlog id -> (production name, immutable source, alpha threshold, width, seat Y, height)
# height is None for a proportional reduction.
HEAD_ACCESSORIES: list[dict[str, Any]] = [
    dict(id="DG-123", name="head_accessory_001_gold_pointed_crown",
         source="head_accessory_001_gold_pointed_crown_regen1.png", alpha=32,
         width=400, top_y=132, height=None,
         seat="crown of the skull, band on the hairline"),
    dict(id="DG-124", name="head_accessory_002_large_gold_halo",
         source="head_accessory_002_large_gold_halo_regen2.png", alpha=32,
         width=430, top_y=132, height=130,
         seat="foreshortened ring hovering above the crown"),
    dict(id="DG-125", name="head_accessory_003_green_laurel",
         source="head_accessory_003_green_laurel_regen1.png", alpha=64,
         width=450, top_y=132, height=None,
         seat="wreath framing the skull above the brow"),
    dict(id="DG-126", name="head_accessory_004_black_curved_horns",
         source="head_accessory_004_black_curved_horns_regen1.png", alpha=64,
         width=440, top_y=129, height=None,
         seat="horn bases on the upper skull"),
    dict(id="DG-127", name="head_accessory_005_silver_winged_circlet",
         source="head_accessory_005_silver_winged_circlet_regen1.png", alpha=80,
         width=420, top_y=129, height=None,
         seat="band on the hairline, wings at the temples"),
    dict(id="DG-128", name="head_accessory_006_silver_ornate_tiara",
         source="head_accessory_006_silver_ornate_tiara_source2.png", alpha=64,
         width=450, top_y=129, height=None,
         seat="band on the hairline, side arcs past the ears"),
    dict(id="DG-129", name="head_accessory_007_silver_drop_circlet",
         source="head_accessory_007_silver_drop_circlet_source2.png", alpha=64,
         width=440, top_y=215, height=None,
         seat="forehead band with the drop centred above the eye line"),
    dict(id="DG-130", name="head_accessory_008_translucent_white_veil",
         source="head_accessory_008_translucent_white_veil_source3.png", alpha=32,
         width=480, top_y=129, height=None,
         seat="draped from the crown, face window preserved"),
    dict(id="DG-131", name="head_accessory_009_pale_blue_spiked_tiara",
         source="head_accessory_009_pale_blue_spiked_tiara_source3.png", alpha=32,
         width=470, top_y=129, height=None,
         seat="band on the hairline, points clear of the brow"),
    dict(id="DG-132", name="head_accessory_010_gold_low_circlet",
         source="head_accessory_010_gold_low_circlet_source2.png", alpha=32,
         width=430, top_y=240, height=None,
         seat="low headband seated on the hairline"),
]

# backlog id -> (production name, pose, translation applied to the normalized layer)
HAND_OBJECTS: list[dict[str, Any]] = [
    dict(id="DG-133", name="hand_object_001_arcane_staff_pose_002_left", pose=2, dx=34, dy=0,
         contact="shaft centre through the closed grip"),
    dict(id="DG-134", name="hand_object_002_violet_orb_pose_004_left", pose=4, dx=34, dy=-30,
         contact="cradle base seated on the open palm, fingers visible below"),
    dict(id="DG-135", name="hand_object_003_dark_wand_pose_002_left", pose=2, dx=34, dy=0,
         contact="shaft centre through the closed grip"),
    dict(id="DG-136", name="hand_object_004_silver_sword_pose_002_left", pose=2, dx=34, dy=0,
         contact="wrapped grip through the closed fist"),
    dict(id="DG-137", name="hand_object_005_star_spellbook_pose_004_left", pose=4, dx=34, dy=-25,
         contact="lower cover resting across the palm, fingers visible below"),
]

HEAD_SOURCE_DIR = "images/trait_candidates/head_accessories"
HAND_CANDIDATE_DIR = "incoming/hand_objects"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_bounds(image: Image.Image) -> list[int]:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise ValueError("layer is fully transparent")
    return [box[0], box[1], box[2] - 1, box[3] - 1]


def check_bounds(bounds: list[int], name: str) -> None:
    left, top, right, bottom = bounds
    if left < MAX_BOUNDS[0] or top < MAX_BOUNDS[1] or right > MAX_BOUNDS[2] or bottom > MAX_BOUNDS[3]:
        raise ValueError(f"{name}: bounds {bounds} escape the locked trait bounds {list(MAX_BOUNDS)}")


def build_head_accessory(row: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    source = ROOT / HEAD_SOURCE_DIR / row["source"]
    out = out_dir / f"{row['name']}.png"
    report = out.with_suffix(".png.provenance.json")
    command = [
        sys.executable, str(ROOT / "scripts/normalize_generator_source.py"), str(source),
        "--out", str(out),
        "--target-width", str(row["width"]),
        "--top-y", str(row["top_y"]),
        "--alpha-threshold", str(row["alpha"]),
        "--report", str(report),
    ]
    if row["height"] is not None:
        command += ["--target-height", str(row["height"])]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{row['name']}: normalization failed\n{result.stderr}")

    with Image.open(out) as image:
        bounds = visible_bounds(image.convert("RGBA"))
    check_bounds(bounds, row["name"])

    record = json.loads(report.read_text())
    record["backlog_id"] = row["id"]
    record["alignment"] = {
        "reason": "re-seated from the retired uniform 520 px / top_y 129 placement",
        "seat": row["seat"],
        "target_width": row["width"],
        "top_y": row["top_y"],
        "target_height": row["height"],
    }
    record["output_bounds"] = bounds
    record["output_sha256"] = sha256_file(out)
    report.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return dict(id=row["id"], name=row["name"], path=out, bounds=bounds, sha256=record["output_sha256"])


def build_hand_object(row: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    source = ROOT / HAND_CANDIDATE_DIR / f"{row['name']}.png"
    out = out_dir / f"{row['name']}.png"
    contact = POSE_CONTACT[row["pose"]]
    lean = POSE_LEAN_DEGREES[row["pose"]]

    with Image.open(source) as handle:
        layer = handle.convert("RGBA")
    if layer.size != (CANVAS, CANVAS):
        raise ValueError(f"{row['name']}: expected a {CANVAS} x {CANVAS} layer; got {layer.size}")
    source_sha = sha256_file(source)
    source_bounds = visible_bounds(layer)

    moved = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    moved.paste(layer, (row["dx"], row["dy"]), layer)
    if lean:
        moved = moved.rotate(lean, resample=Image.BICUBIC, center=contact, expand=False)

    bounds = visible_bounds(moved)
    check_bounds(bounds, row["name"])
    moved.save(out)

    record = {
        "origin": "hand_object_contact_realignment",
        "backlog_id": row["id"],
        "source_path": (ROOT / HAND_CANDIDATE_DIR / f"{row['name']}.png").relative_to(ROOT).as_posix(),
        "source_sha256": source_sha,
        "source_bounds": source_bounds,
        "pose": row["pose"],
        "contact_point": list(contact),
        "contact_feature": row["contact"],
        "transform": {
            "method": "integer_translation_then_lean_about_contact_point",
            "dx": row["dx"],
            "dy": row["dy"],
            "lean_degrees": lean,
            "resample": "bicubic" if lean else "none",
        },
        "reason": "retired shared hand anchor X 404 replaced by the measured grip contact",
        "final_dimensions": [CANVAS, CANVAS],
        "output_path": out.relative_to(ROOT).as_posix() if out.is_absolute() else out.as_posix(),
        "output_bounds": bounds,
    }
    record["output_sha256"] = sha256_file(out)
    report = out.with_suffix(".png.provenance.json")
    report.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return dict(id=row["id"], name=row["name"], path=out, bounds=bounds, sha256=record["output_sha256"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=Path("incoming/aligned_candidates"))
    args = parser.parse_args(argv)

    out_dir = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir
    (out_dir / "head_accessories").mkdir(parents=True, exist_ok=True)
    (out_dir / "hand_objects").mkdir(parents=True, exist_ok=True)

    results = []
    for row in HEAD_ACCESSORIES:
        results.append(build_head_accessory(row, out_dir / "head_accessories"))
    for row in HAND_OBJECTS:
        results.append(build_hand_object(row, out_dir / "hand_objects"))

    for item in results:
        print(f"{item['id']}  {item['name']:52s} bounds {item['bounds']}  {item['sha256'][:12]}")
    print(f"\n{len(results)} aligned candidates written to {out_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
