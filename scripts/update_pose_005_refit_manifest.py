#!/usr/bin/env python3
"""Record the pose 005 proportion correction in the manifest.

`scripts/refit_pose_005_proportions.py` rewrites two registered assets in place.
This records what it replaced, so the provenance chain stays unbroken: the
pre-refit bytes are kept under `incoming/pose_005_refit_2026-09-09/originals/`
and their hashes must still match what the manifest claims before anything is
changed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
ORIGINALS = ROOT / "incoming" / "pose_005_refit_2026-09-09" / "originals"
QA_REPORT = "docs/qa/pose_005_proportions_2026-09-09.md"
METHOD = "pose_005_proportion_refit_2026-09-09"

ASSETS = {
    "base_pose_005": "assets/base_bodies/base_pose_005_centered_two_hand_grip.png",
    "outfit_005": "assets/outfits/outfit_005_sun_temple_pose_005.png",
}

NOTE = (
    "Four of the five base bodies place the eye line at Y 368.5-371.8, the chin at "
    "Y 475-477 and the shoulder junction at Y 495-497. Pose 005 sat at Y 350.8, 452 "
    "and 472 - a smaller head on a longer body, off the collection's proportions by "
    "20-24 px. The silhouette rig gate could not see it: canvas, top of head, foot "
    "baseline, centre X and maximum bounds are all measured at the outline's extremes "
    "and pose 005 met every one. It blocked the facial system, because eyes, eyebrows "
    "and mouths are one shared layer placed by rig anchor, and no single seat fits both "
    "pose 005 and the other four. Corrected by a monotone piecewise-linear remap of the "
    "Y axis through the measured landmarks (141 -> 141, 350.8 -> 370.3, 452 -> 476.5, "
    "472 -> 496.3, 1139 -> 1139), holding both locked rows fixed and leaving X untouched: "
    "the head stretches 9.3% vertically and the body below the shoulder compresses 3.6%. "
    "Pose 005's head was already the collection's width, so only its height needed to "
    "move. outfit_005 is drawn to this base and bound to it by a compatibility rule, so "
    "it takes the identical map and their fit is preserved exactly. Resampling is linear "
    "on premultiplied alpha along Y only. The pre-refit bytes are kept at "
    "incoming/pose_005_refit_2026-09-09/originals/ for local verification; that tree is "
    "ignored by incoming/.gitignore like every other candidate drop, so the durable record "
    "of what was replaced is pre_pose_005_refit_sha256, which is the hash this manifest "
    "carried in the preceding commit."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    updated = 0
    for entry in manifest["registered_production_assets"]:
        path = ASSETS.get(entry.get("id"))
        if path is None:
            continue
        current = ROOT / path
        original = ORIGINALS / current.name
        if not original.exists():
            raise SystemExit(f"missing pre-refit original: {original}")
        before, after = sha256_file(original), sha256_file(current)
        if entry["sha256"] not in (before, after):
            raise SystemExit(f"{entry['id']}: manifest hash matches neither the original nor the current file")
        entry["sha256"] = after
        provenance = entry.setdefault("provenance", {})
        steps = list(provenance.get("postprocessing", []))
        if METHOD not in steps:
            steps.append(METHOD)
        provenance["postprocessing"] = steps
        provenance["pose_005_refit_script"] = "scripts/refit_pose_005_proportions.py"
        provenance["pre_pose_005_refit_sha256"] = before
        provenance["post_pose_005_refit_sha256"] = after
        provenance["pre_pose_005_refit_path"] = str(original.relative_to(ROOT))
        provenance["pose_005_refit_note"] = NOTE
        entry["qa_report"] = QA_REPORT
        updated += 1

    if updated != len(ASSETS):
        raise SystemExit(f"updated {updated} entries, expected {len(ASSETS)}")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated {updated} manifest entries for {METHOD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
