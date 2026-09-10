#!/usr/bin/env python3
"""Retire the head accessories that repeat a silhouette already in the set.

Ten head accessories is too many for a 770-token collection: each lands on about
42 tokens, and five of the ten are the same shape - a band across the forehead -
so a holder cannot tell most of them apart at token size. What varies between
them is filigree, which is invisible at the scale these are seen.

Four bands are retired and six shapes kept, each of which reads differently in
silhouette: a pointed crown, a floating ring, a wreath, horns, a crystal-spiked
crown, and a drape. That takes each remaining accessory from about 42 tokens to
about 71 without touching any other category.

The retired art is kept, not deleted, so a later pass can bring one back if a
distinct design is wanted in its place.

    python scripts/retire_duplicate_head_accessories.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
LIVE = ROOT / "assets" / "head_accessories"
RETIRED = ROOT / "incoming" / "head_accessories_retired_2026-09-10"
QA_REPORT = "docs/qa/head_accessory_count_2026-09-10.md"

# id -> why this one and not another
RETIRE = {
    "head_accessory_005": "silver band across the forehead; the wings read as filigree at token size",
    "head_accessory_006": "silver band across the forehead, the most ornate of four alike",
    "head_accessory_007": "silver band across the forehead with a drop",
    "head_accessory_010": "gold band across the forehead",
}

KEEP_REASON = {
    "head_accessory_001": "pointed crown - tall silhouette",
    "head_accessory_002": "halo - a ring clear of the head",
    "head_accessory_003": "laurel wreath - open at the top",
    "head_accessory_004": "curved horns - reads from the outline alone",
    "head_accessory_008": "veil - a drape down both sides",
    "head_accessory_009": "spiked tiara - crystal points, the one band with a shape of its own",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    entries = [e for e in manifest["registered_production_assets"] if e["id"] in RETIRE]
    if not entries:
        print("those head accessories are already retired")
        return 0

    RETIRED.mkdir(parents=True, exist_ok=True)
    retired = []
    for entry in sorted(entries, key=lambda e: e["id"]):
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = sha256_file(path)
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
                f"Retired to thin the category: {RETIRE[entry['id']]}. Ten head accessories on "
                "770 tokens is about 42 tokens each, and five of the ten were the same band "
                "silhouette, distinguished only by filigree that is invisible at token size. Six "
                "shapes are kept, each of which reads differently in outline, at about 71 tokens "
                "each. Nothing is wrong with this asset; there were too many like it."
            ),
            "requirement": (
                "Bring this back only as part of a set whose silhouettes differ. A replacement "
                "should read as a distinct shape at 418 px, not as another forehead band."
            ),
            "qa_report": QA_REPORT,
        })

    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if e["id"] not in RETIRE
    ]
    blocked = [b for b in manifest.get("blocked_assets", []) if b.get("id") not in RETIRE]
    manifest["blocked_assets"] = blocked + retired
    # The category has rows that are no longer registered, so the ledger counts
    # it as unfinished. It is the same bookkeeping the neck accessories got.
    pending = list(manifest.get("pending_categories", []))
    if "head_accessories" not in pending:
        pending.append("head_accessories")
    manifest["pending_categories"] = pending
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    backlog = ROOT / "docs" / "trait-production-backlog.md"
    lines = backlog.read_text().splitlines(keepends=True)
    ids = {r["backlog_id"] for r in retired if r["backlog_id"]}
    changed = 0
    for index, line in enumerate(lines):
        if not line.startswith("| DG-"):
            continue
        cells = line.rstrip("\n").split("|")
        if cells[1].strip() not in ids:
            continue
        cells[8] = " QA-failed "
        lines[index] = "|".join(cells) + "\n"
        changed += 1
    if changed != len(ids):
        raise SystemExit(f"updated {changed} backlog rows, expected {len(ids)}")
    backlog.write_text("".join(lines), encoding="utf-8")

    print(f"retired {len(retired)} head accessories to {RETIRED.relative_to(ROOT)}")
    for item in retired:
        print(f"  {item['id']:22s} {item['sha256'][:12]}")
    print(f"{len(KEEP_REASON)} kept:")
    for key, why in KEEP_REASON.items():
        print(f"  {key:22s} {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
