#!/usr/bin/env python3
"""Retire the rear auras and wings that repeat a shape already in the set.

Eighteen rear auras on 770 tokens is about 43 tokens each, and eleven of the
eighteen are the same object: a flat ellipse on the floor under the feet,
recoloured. Green, gold, pink, white, orange, blue, violet, pale blue, cyan -
at the size a token is seen they read as one trait with a colour picker on it,
not as eleven things. The wings have the same problem once: the gold pair and
the silver pair are one silhouette in two metals.

## Where the line is

A hard-edged shape is read by its outline, so recolouring it does not make a
new trait: the eleven floor rings collapse to one, and the two feathered wings
to one. A full-figure glow has no outline to read, so its colour is the whole
of it - the violet halo and the gold radiance stay, because a token wearing
one does not look like a token wearing the other.

Kept auras: a floor ring, a soft violet halo, a warm gold radiance, a
crystalline burst, a void flame, a lightning arc, an upright sparkle ring, and
a raised flame ring. Eight shapes, about 96 tokens each.

The art is kept, not deleted, so a later pass can bring one back.

    python scripts/thin_duplicate_effects.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
RETIRED = ROOT / "incoming" / "effects_retired_2026-09-10"
QA_REPORT = "docs/qa/effect_trait_count_2026-09-10.md"

RETIRE = {
    "aura_rear_001": "blue floor ring; the same ellipse as ten others",
    "aura_rear_007": "green floor ring, recoloured",
    "aura_rear_008": "gold floor ring, recoloured",
    "aura_rear_009": "pink floor ring, recoloured",
    "aura_rear_011": "orange floor ring; flame texture on the same ellipse, and the raised flame ring keeps that idea",
    "aura_rear_012": "blue floor ring with an arc texture",
    "aura_rear_013": "violet floor ring with a flame texture",
    "aura_rear_014": "pale blue floor ring with a crystal texture",
    "aura_rear_015": "violet floor ring with a smoke texture",
    "aura_rear_017": "cyan floor ring with a splash texture",
    "back_accessory_007": "gold feathered wings; the same silhouette as the silver pair",
}

KEEP_REASON = {
    "aura_rear_002": "violet radial glow - a halo with no outline, so its colour is the trait",
    "aura_rear_003": "crystalline burst - shards standing behind the figure",
    "aura_rear_004": "void flame - flame climbing the body, not a ring",
    "aura_rear_005": "lightning - arcs around the whole figure",
    "aura_rear_006": "gold radiance - the warm counterpart to the violet halo",
    "aura_rear_010": "white neon ring - the one floor ring, in the colour that sits under any palette",
    "aura_rear_016": "cosmic sparkle ring - upright behind the torso, with rays",
    "aura_rear_018": "blue flame ring - raised off the floor and burning, a different object",
    "back_accessory_001": "silver feathered wings",
    "back_accessory_002": "black and violet bat wings",
    "back_accessory_003": "cyan fairy wings",
    "back_accessory_004": "navy formal cape",
    "back_accessory_005": "black and violet ragged cloak",
    "back_accessory_006": "pale blue crystal wings - shards, not feathers",
    "back_accessory_008": "olive and silver spiked wings - plated, not feathers",
}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    entries = [e for e in manifest["registered_production_assets"] if e["id"] in RETIRE]
    if not entries:
        print("those traits are already retired")
        return 0

    RETIRED.mkdir(parents=True, exist_ok=True)
    retired = []
    for entry in sorted(entries, key=lambda e: e["id"]):
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        shutil.move(str(path), RETIRED / path.name)
        retired.append({
            "id": entry["id"],
            "backlog_id": entry.get("backlog_id"),
            "intended_path": entry["path"],
            "status": "retired",
            "sha256": digest,
            "retained_at": str((RETIRED / path.name).relative_to(ROOT)),
            "withdrawn_on": "2026-09-10",
            "reason": (
                f"Retired to thin the category: {RETIRE[entry['id']]}. A hard-edged shape is "
                "read by its outline at token size, so a recolour of it is not a second trait. "
                "Nothing is wrong with this asset; there were too many like it."
            ),
            "requirement": (
                "Bring this back only as a shape that is not already in the set. A colour "
                "variant of a ring or a wing already registered will be rejected again."
            ),
            "qa_report": QA_REPORT,
        })

    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if e["id"] not in RETIRE
    ]
    blocked = [b for b in manifest.get("blocked_assets", []) if b.get("id") not in RETIRE]
    manifest["blocked_assets"] = blocked + retired
    pending = list(manifest.get("pending_categories", []))
    for category in ("rear_auras", "back_accessories"):
        if category not in pending:
            pending.append(category)
    manifest["pending_categories"] = pending
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Match on the asset path, not the backlog id: four of the rings predate the
    # manifest carrying a backlog_id and would be missed by id alone, leaving
    # the ledger claiming they are still registered.
    paths = {r["intended_path"] for r in retired}
    lines = BACKLOG.read_text().splitlines(keepends=True)
    changed = 0
    for index, line in enumerate(lines):
        if not line.startswith("| DG-"):
            continue
        cells = line.rstrip("\n").split("|")
        if cells[6].strip().strip("`") not in paths:
            continue
        cells[8] = " QA-failed "
        lines[index] = "|".join(cells) + "\n"
        changed += 1
    if changed != len(paths):
        raise SystemExit(f"updated {changed} backlog rows, expected {len(paths)}")
    BACKLOG.write_text("".join(lines), encoding="utf-8")

    print(f"retired {len(retired)} traits to {RETIRED.relative_to(ROOT)}")
    for item in retired:
        print(f"  {item['id']:22s} {item['sha256'][:12]}")
    print(f"{len(KEEP_REASON)} kept:")
    for key, why in KEEP_REASON.items():
        print(f"  {key:22s} {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
