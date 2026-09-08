#!/usr/bin/env python3
"""Re-seat the registered neck and back accessories onto the anatomy they wear on.

Both categories carry the defect the head accessories carried, from the same
cause: a whole batch normalized at one fixed width and seat instead of the seat
each design needs. The automated gates cannot see it, because canvas size, alpha
behaviour, maximum bounds and width ratio are all satisfied by a layer sitting in
the wrong place.

**Neck accessories** were all refit to `top_y` 545–555 at a uniform 0.45 scale.
The base body's neck spans Y 470–505; 550 is the middle of the chest, so every
choker read as a chest strap and every pendant chain began below the collarbone
with nothing holding it up.

A first correction moved them all to the throat at Y 482 and traded one error for
another. These pieces are 150–175 px wide and the neck at Y 482 is 61 px, so the
chain ends and band tips hung in open air either side of it. A necklace has to
*touch* where it attaches. Each row is now seated at the row where its own topmost
ink lands inside the body silhouette — Y 496–504, the neck-to-shoulder junction —
so the chain disappears behind the neck instead of ending in space.

**Back accessories** were all normalized at 590 px wide with `top_y` 420. That is
1.33× the body width, which for a wing pair is barely wider than the character —
and seated at the jaw, so the upper half hid behind the head and hair, leaving
small fins at the shoulders. The six wing designs now span 760 px, seated so the
pair's vertical centre sits at the upper back. The two capes keep their existing
seat: they already hang from the shoulder to the hem, and widening them would
push the hem past the locked foot baseline.

Each asset is re-derived from its immutable generator source in a single
reduction, so nothing is resampled twice.

    python scripts/reseat_registered_accessories.py --out-dir incoming/reseat_2026-09-07
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

# Measured on the registered base master.
NECK_SPAN = (470, 505)      # chin to shoulder line; only 61 px wide at Y 482
SHOULDER_LINE = 569
FOOT_BASELINE = 1139

NECK_ACCESSORIES: list[dict[str, Any]] = [
    dict(id="neck_accessory_001", name="neck_accessory_001_black_choker",
         source="dg047_black_choker_source.png", alpha=32, width=170, top_y=498,
         seat="band meeting the neck at the shoulder junction"),
    dict(id="neck_accessory_002", name="neck_accessory_002_gold_blue_drop_choker",
         source="dg048_gold_blue_drop_choker_source.png", alpha=32, width=175, top_y=496,
         seat="band meeting the neck, drop on the upper chest"),
    dict(id="neck_accessory_003", name="neck_accessory_003_black_ribbon_bow",
         source="dg049_black_ribbon_bow_source.png", alpha=32, width=170, top_y=504,
         seat="bow tied at the base of the neck"),
    dict(id="neck_accessory_004", name="neck_accessory_004_silver_dark_round_pendant",
         source="dg050_silver_dark_pendant_source.png", alpha=32, width=150, top_y=500,
         seat="chain ends meeting the neck, pendant on the chest"),
    dict(id="neck_accessory_005", name="neck_accessory_005_silver_navy_long_pendant",
         source="dg051_silver_navy_pendant_source.png", alpha=32, width=150, top_y=500,
         seat="chain ends meeting the neck, long pendant down the chest"),
    dict(id="neck_accessory_006", name="neck_accessory_006_silver_pale_circle_charm",
         source="dg052_silver_pale_circle_charm_source.png", alpha=32, width=150, top_y=500,
         seat="chain ends meeting the neck, charm on the chest"),
    dict(id="neck_accessory_007", name="neck_accessory_007_gold_teardrop_pendant",
         source="dg053_gold_teardrop_pendant_source.png", alpha=32, width=150, top_y=500,
         seat="chain ends meeting the neck, teardrop on the chest"),
    dict(id="neck_accessory_008", name="neck_accessory_008_violet_ribbon_bow",
         source="dg054_violet_ribbon_bow_source.png", alpha=32, width=170, top_y=500,
         seat="bow tied at the base of the neck"),
]

# Wing pairs meet at their centre, so top_y is chosen to put that meeting point at
# the upper back rather than to hang the layer from a fixed line.
BACK_ACCESSORIES: list[dict[str, Any]] = [
    dict(id="back_accessory_001", name="back_accessory_001_silver_feathered_wings",
         source="dg021_silver_feathered_wings_source.png", alpha=32, width=760, top_y=374,
         seat="wing pair spread from the upper back"),
    dict(id="back_accessory_002", name="back_accessory_002_black_violet_bat_wings",
         source="dg022_black_violet_bat_wings_source.png", alpha=32, width=760, top_y=362,
         seat="wing pair spread from the upper back"),
    dict(id="back_accessory_003", name="back_accessory_003_cyan_fairy_wings",
         source="dg023_cyan_fairy_wings_source.png", alpha=32, width=760, top_y=300,
         seat="wing pair spread from the upper back"),
    dict(id="back_accessory_004", name="back_accessory_004_navy_formal_cape",
         source="dg024_navy_formal_cape_source.png", alpha=32, width=590, top_y=500,
         seat="collar at the shoulders, hem above the foot baseline — unchanged"),
    dict(id="back_accessory_005", name="back_accessory_005_black_violet_ragged_cloak",
         source="dg025_black_violet_ragged_cloak_source.png", alpha=32, width=590, top_y=440,
         seat="hood behind the head, hem above the foot baseline — unchanged"),
    dict(id="back_accessory_006", name="back_accessory_006_pale_blue_crystal_wings",
         source="dg026_pale_blue_crystal_wings_source_retry.png", alpha=32, width=760, top_y=300,
         seat="wing pair spread from the upper back"),
    dict(id="back_accessory_007", name="back_accessory_007_gold_luminous_wings",
         source="dg027_gold_luminous_wings_source_retry.png", alpha=32, width=760, top_y=345,
         seat="wing pair spread from the upper back"),
    dict(id="back_accessory_008", name="back_accessory_008_olive_silver_spiked_wings",
         source="dg028_olive_silver_spiked_wings_source_retry.png", alpha=32, width=760, top_y=372,
         seat="wing pair spread from the upper back"),
]

CATEGORIES = {
    "neck_accessories": (NECK_ACCESSORIES, "images/trait_candidates/neck_accessories"),
    "back_accessories": (BACK_ACCESSORIES, "images/trait_candidates/back_accessories"),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_bounds(image: Image.Image) -> list[int]:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise ValueError("layer is fully transparent")
    return [box[0], box[1], box[2] - 1, box[3] - 1]


def build(row: dict[str, Any], source_dir: str, out_dir: Path) -> dict[str, Any]:
    source = ROOT / source_dir / row["source"]
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
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{row['name']}: normalization failed\n{result.stderr}")

    with Image.open(out) as image:
        bounds = visible_bounds(image.convert("RGBA"))
    left, top, right, bottom = bounds
    if left < MAX_BOUNDS[0] or top < MAX_BOUNDS[1] or right > MAX_BOUNDS[2] or bottom > MAX_BOUNDS[3]:
        raise ValueError(f"{row['name']}: bounds {bounds} escape {list(MAX_BOUNDS)}")

    record = json.loads(report.read_text())
    record["asset_id"] = row["id"]
    record["alignment"] = {
        "reason": "re-seated from a batch-wide fixed width and seat",
        "seat": row["seat"],
        "target_width": row["width"],
        "top_y": row["top_y"],
    }
    record["output_bounds"] = bounds
    record["output_sha256"] = sha256_file(out)
    report.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return dict(id=row["id"], name=row["name"], path=out, bounds=bounds, sha256=record["output_sha256"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=Path("incoming/reseat_accessories"))
    args = parser.parse_args(argv)
    out_root = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir

    results = []
    for category, (rows, source_dir) in CATEGORIES.items():
        directory = out_root / category
        directory.mkdir(parents=True, exist_ok=True)
        for row in rows:
            results.append(build(row, source_dir, directory))

    for item in results:
        print(f"{item['id']:22s} bounds {str(item['bounds']):26s} {item['sha256'][:12]}")
    print(f"\n{len(results)} accessories re-seated into {out_root.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
