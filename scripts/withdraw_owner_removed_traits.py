#!/usr/bin/env python3
"""Record the owner's 2026-09-26 decision: trim the modular trait library.

Removed by decision, not for failing QA:

- **Outfits without all five poses: 001-005 and 010.** Each is one garment layer
  drawn for a single pose, so a token could only wear it in that pose. The four
  dressed-body families (006-009) exist in every pose and stay; they are now the
  whole outfit category.
- **Head accessories, rear auras, front auras and hand objects.** Whole categories.

Each registered file moves out of `assets/` to `incoming/owner_removed_2026-09-26/`.
`incoming/.gitignore` keeps it out of the tree, and git history keeps the bytes at
the recorded hash. Each manifest entry becomes a `withdrawn` record. Every backlog
row in a removed category closes as `withdrawn`, and compatibility rules naming a
removed trait go. The categories stay in the layer order so a redesigned set
could return, but their optional-category probabilities go: an empty category
has nothing to be optional about.

    python scripts/withdraw_owner_removed_traits.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
COLLECTION = ROOT / "config" / "collection.json"
RETIRED = ROOT / "incoming" / "owner_removed_2026-09-26"
DECIDED_ON = "2026-09-26"
QA_REPORT = "docs/qa/owner_trait_removal_2026-09-26.md"

REMOVED_CATEGORIES = ("head_accessories", "rear_auras", "front_auras", "hand_objects")
POSES_PER_OUTFIT = 5
# The families the pose count must find; a mismatch means the library changed
# since the decision was taken, so stop rather than remove something else.
EXPECTED_SHORT_OUTFITS = {"outfit_001", "outfit_002", "outfit_003", "outfit_004", "outfit_005", "outfit_010"}

CATEGORY_DECISION = (
    "The owner removed this category from the collection on 2026-09-26. It stays "
    "in the layer order so a redesigned set could return, but none is planned."
)
OUTFIT_DECISION = (
    "The owner removed every outfit that does not exist in all five poses on 2026-09-26. "
    "This one was drawn for a single pose, so it could only ever appear in that pose."
)
OUTFIT_REQUIREMENT = (
    "Return only as a dressed-body family rendered in all five poses, like outfits 006-009."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def outfit_family(path: str) -> str:
    return re.sub(r"_pose_\d{3}$", "", Path(path).stem)


def set_status(backlog: str, backlog_id: str, status: str) -> str:
    pattern = re.compile(
        rf"^(\| {re.escape(backlog_id)} \|.*\| )(\**[A-Za-z-]+\**)( \|)$", re.MULTILINE
    )
    updated, count = pattern.subn(rf"\g<1>{status}\g<3>", backlog)
    if count != 1:
        raise SystemExit(f"{backlog_id}: matched {count} backlog rows")
    return updated


def backlog_rows(backlog: str) -> dict[str, str]:
    """Map each backlog row's intended production path to its ID."""
    rows: dict[str, str] = {}
    for line in backlog.splitlines():
        if not line.startswith("| DG-"):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        match = re.search(r"`(assets/[^`]+)`", cells[6])
        if match:
            rows[match.group(1)] = cells[1]
    return rows


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    collection = json.loads(COLLECTION.read_text(encoding="utf-8"))
    registered = manifest["registered_production_assets"]

    families: dict[str, list[dict]] = defaultdict(list)
    for entry in registered:
        if entry["category"] == "outfits":
            families[outfit_family(entry["path"])].append(entry)
    short = {name: entries for name, entries in families.items() if len(entries) < POSES_PER_OUTFIT}
    short_ids = {name[: len("outfit_000")] for name in short}
    if short_ids and short_ids != EXPECTED_SHORT_OUTFITS:
        raise SystemExit(f"outfits short of {POSES_PER_OUTFIT} poses are {sorted(short_ids)}, "
                         f"expected {sorted(EXPECTED_SHORT_OUTFITS)}")

    removing = [e for e in registered if e["category"] in REMOVED_CATEGORIES]
    removing += [e for entries in short.values() for e in entries]
    if not removing:
        print("already withdrawn")
        return 0

    rows = backlog_rows(backlog)
    withdrawn = []
    for entry in sorted(removing, key=lambda e: e["path"]):
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        destination = RETIRED / entry["category"] / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), destination)
        outfit = entry["category"] == "outfits"
        record = {
            "id": entry["id"],
            "backlog_id": rows.get(entry["path"]),
            "intended_path": entry["path"],
            "status": "withdrawn",
            "sha256": digest,
            "retained_at": str(destination.relative_to(ROOT)),
            "withdrawn_on": DECIDED_ON,
            "reason": OUTFIT_DECISION if outfit else CATEGORY_DECISION,
            "qa_report": QA_REPORT,
        }
        if outfit:
            record["requirement"] = OUTFIT_REQUIREMENT
        withdrawn.append(record)

    removed_paths = {e["path"] for e in removing}
    removed_files = {Path(p).name for p in removed_paths}
    manifest["registered_production_assets"] = [e for e in registered if e["path"] not in removed_paths]

    # Assets in these categories that were already out of assets/ (QA failures)
    # carry the decision too, so no record reads as work still to redo.
    for item in manifest.get("blocked_assets", []):
        if any(f"assets/{c}/" in str(item.get("intended_path", "")) for c in REMOVED_CATEGORIES):
            item["owner_decision"] = CATEGORY_DECISION
    manifest["blocked_assets"] = manifest.get("blocked_assets", []) + withdrawn
    manifest["pending_categories"] = [
        c for c in manifest.get("pending_categories", []) if c not in REMOVED_CATEGORIES
    ]

    # Close every backlog row in a removed category, whatever its state, and the
    # rows of the removed outfits.
    closing = [
        backlog_id for path, backlog_id in rows.items()
        if path in removed_paths or any(path.startswith(f"assets/{c}/") for c in REMOVED_CATEGORIES)
    ]
    for backlog_id in sorted(closing):
        backlog = set_status(backlog, backlog_id, "withdrawn")

    compatibility["requires"] = [
        r for r in compatibility["requires"]
        if r.get("trait") not in removed_files and r.get("requires") not in removed_files
    ]
    kept_excludes = []
    for rule in compatibility.get("excludes", []):
        if rule.get("trait") in removed_files:
            continue
        excluded = rule.get("excludes", [])
        excluded = [excluded] if isinstance(excluded, str) else list(excluded)
        remaining = [name for name in excluded if name not in removed_files]
        if remaining:
            kept_excludes.append({**rule, "excludes": remaining})
    compatibility["excludes"] = kept_excludes
    compatibility["hides"] = [r for r in compatibility.get("hides", []) if r.get("trait") not in removed_files]

    optional = collection.get("optional_categories") or {}
    collection["optional_categories"] = {c: p for c, p in optional.items() if c not in REMOVED_CATEGORIES}

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    COLLECTION.write_text(json.dumps(collection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for category in REMOVED_CATEGORIES:
        live = ROOT / "assets" / category
        if live.exists() and not any(live.iterdir()):
            live.rmdir()

    by_category: dict[str, int] = defaultdict(int)
    for item in withdrawn:
        by_category[item["intended_path"].split("/")[1]] += 1
    print(f"withdrew {len(withdrawn)} registered assets to {RETIRED.relative_to(ROOT)}: "
          + ", ".join(f"{n} {c}" for c, n in sorted(by_category.items())))
    print(f"closed {len(closing)} backlog rows; {len(manifest['registered_production_assets'])} assets remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
