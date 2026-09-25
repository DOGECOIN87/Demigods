#!/usr/bin/env python3
"""Record the owner's 2026-09-25 trait reductions.

The owner asked for fewer traits. Withdrawn by that decision:

- **Head accessories**, all of them. The six registered pieces go; the four
  retired on 2026-09-10 close with them.
- **Front auras**, both. They were mandatory, so every token wore flames or
  light pillars across the legs, over whatever outfit it had.
- **Global finish**, all three. A whole-image colour wash on 75% of tokens,
  listed in the metadata as though it were a trait.
- **Ten of the sixteen eyebrows.** On average 74% of a brow's line sits under
  the front hair - all of it under the teal open-centre bangs - and the
  withdrawn ten are near-copies of the six kept: pleading of worried, bold
  raised of raised, furious of angry, fine arched and arched of the
  collection's own neutral arch, and thin, thick, wide-set, close-set and
  lowered of neutral. See docs/qa/trait_reduction_2026-09-25.md.

Registered bytes are retired, not deleted, and every backlog row closes as
``withdrawn`` with the decision on the record.

    python scripts/withdraw_trait_reductions.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
COLLECTION = ROOT / "config" / "collection.json"
RETIRED = ROOT / "incoming" / "trait_reduction_2026-09-25"
DECIDED_ON = "2026-09-25"
QA_REPORT = "docs/qa/trait_reduction_2026-09-25.md"

WHOLE_CATEGORIES = {
    "head_accessories": "The owner removed head accessories from the collection on 2026-09-25 to reduce the trait count.",
    "front_auras": "The owner removed front auras on 2026-09-25. They were mandatory, so every token wore flames or light pillars across the legs.",
    "global_finish": "The owner removed the global finish on 2026-09-25: a whole-image colour wash listed as a trait.",
}
EYEBROWS_KEPT = {
    "eyebrows_001_neutral.png", "eyebrows_002_raised.png", "eyebrows_004_angry.png",
    "eyebrows_006_worried.png", "eyebrows_009_flat.png", "eyebrows_016_quizzical.png",
}
EYEBROW_REASON = (
    "Withdrawn when the owner cut the eyebrows from sixteen to six on 2026-09-25. On average 74% of a "
    "brow's line sits under the front hair, and this one is a near-copy of a brow kept "
    "(neutral, raised, angry, worried, flat or quizzical)."
)
REQUIREMENT = "Return only by the owner's decision, restored from the retained bytes and re-registered."


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_status(backlog: str, backlog_id: str, status: str) -> str:
    pattern = re.compile(rf"^(\| {re.escape(backlog_id)} \|.*\| )([A-Za-z-]+)( \|)$", re.MULTILINE)
    updated, count = pattern.subn(rf"\g<1>{status}\g<3>", backlog)
    if count != 1:
        raise SystemExit(f"{backlog_id}: matched {count} backlog rows")
    return updated


def withdrawn(entry: dict) -> bool:
    if entry["category"] in WHOLE_CATEGORIES:
        return True
    return entry["category"] == "eyebrows" and Path(entry["path"]).name not in EYEBROWS_KEPT


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    collection = json.loads(COLLECTION.read_text(encoding="utf-8"))

    leaving = [e for e in manifest["registered_production_assets"] if withdrawn(e)]
    records = []
    for entry in sorted(leaving, key=lambda e: e["path"]):
        path = ROOT / entry["path"]
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        destination = RETIRED / entry["category"] / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), destination)
        reason = WHOLE_CATEGORIES.get(entry["category"], EYEBROW_REASON)
        records.append({
            "id": entry["id"],
            "backlog_id": entry.get("backlog_id"),
            "intended_path": entry["path"],
            "status": "withdrawn",
            "sha256": digest,
            "retained_at": str(destination.relative_to(ROOT)),
            "withdrawn_on": DECIDED_ON,
            "reason": reason + " Nothing is wrong with this asset.",
            "requirement": REQUIREMENT,
            "owner_decision": reason,
            "qa_report": QA_REPORT,
        })
        if entry.get("backlog_id"):
            backlog = set_status(backlog, entry["backlog_id"], "withdrawn")

    leaving_ids = {e["id"] for e in leaving}
    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if e["id"] not in leaving_ids
    ]
    # The four head accessories retired on 2026-09-10 close with their category.
    for item in manifest.get("blocked_assets", []):
        if str(item.get("intended_path", "")).startswith("assets/head_accessories/"):
            item["owner_decision"] = WHOLE_CATEGORIES["head_accessories"]
            if item.get("backlog_id"):
                backlog = set_status(backlog, item["backlog_id"], "withdrawn")
    manifest["blocked_assets"] = manifest.get("blocked_assets", []) + records
    manifest["pending_categories"] = [
        c for c in manifest.get("pending_categories", []) if c not in WHOLE_CATEGORIES
    ]

    optional = collection.get("optional_categories", {})
    for category in WHOLE_CATEGORIES:
        optional.pop(category, None)

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COLLECTION.write_text(json.dumps(collection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"withdrew {len(records)} registered assets to {RETIRED.relative_to(ROOT)}")
    for record in records:
        print(f"  {record['backlog_id']}  {Path(record['intended_path']).name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
