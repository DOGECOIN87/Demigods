#!/usr/bin/env python3
"""Record the owner's 2026-09-27 decision: remove headwear and auras from the collection.

Removed by decision, not for failing QA: the head accessory (headwear), rear aura
and front aura categories, whole. Hand objects and outfits are not touched.

It follows the neckwear precedent (scripts/deregister_neck_accessories.py):

- Each registered file moves out of `assets/` to
  `incoming/owner_removed_2026-09-27/<category>/`. `incoming/.gitignore` keeps it
  out of the tree, and git history keeps the bytes at the recorded hash.
- Each manifest entry becomes a `withdrawn` record in `blocked_assets`. The records
  these categories already had, for assets QA retired, carry the decision too.
- Every backlog row in the three categories closes as `withdrawn`.
- Compatibility rules naming a removed trait go, and so do the categories'
  optional-category probabilities and their `pending_categories` entries.

The categories stay in the layer order, as neckwear did, so a redesigned set
could return.

    python scripts/withdraw_headwear_and_auras.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
COLLECTION = ROOT / "config" / "collection.json"
RETIRED = ROOT / "incoming" / "owner_removed_2026-09-27"
DECIDED_ON = "2026-09-27"
QA_REPORT = "docs/qa/headwear_aura_removal_2026-09-27.md"

REMOVED_CATEGORIES = ("head_accessories", "rear_auras", "front_auras")

DECISION = (
    "The owner removed this category from the collection on 2026-09-27. It stays "
    "in the layer order so a redesigned set could return, but none is planned."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def in_removed_category(path: str) -> bool:
    return any(path.startswith(f"assets/{category}/") for category in REMOVED_CATEGORIES)


def set_status(backlog: str, backlog_id: str, status: str) -> str:
    pattern = re.compile(
        rf"^(\| {re.escape(backlog_id)} \|.*\| )(\**[A-Za-z-]+\**)( \|)$", re.MULTILINE
    )
    updated, count = pattern.subn(rf"\g<1>{status}\g<3>", backlog)
    if count != 1:
        raise SystemExit(f"{backlog_id}: matched {count} backlog rows")
    return updated


def drop_rules_naming(compatibility: dict, removed_files: set[str]) -> None:
    """Remove every compatibility rule for a removed trait, and removed traits from exclude lists."""
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
    for kind in ("hides", "in_hand"):
        if kind in compatibility:
            compatibility[kind] = [r for r in compatibility[kind] if r.get("trait") not in removed_files]


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

    removing = [e for e in registered if e["category"] in REMOVED_CATEGORIES]
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
        withdrawn.append({
            "id": entry["id"],
            "backlog_id": rows.get(entry["path"]),
            "intended_path": entry["path"],
            "status": "withdrawn",
            "sha256": digest,
            "retained_at": destination.relative_to(ROOT).as_posix(),
            "withdrawn_on": DECIDED_ON,
            "reason": DECISION,
            "qa_report": QA_REPORT,
        })

    removed_paths = {e["path"] for e in removing}
    removed_files = {Path(p).name for p in removed_paths}
    manifest["registered_production_assets"] = [e for e in registered if e["path"] not in removed_paths]

    # Assets in these categories that QA had already moved out of assets/ carry the
    # decision too, so no record reads as work still to redo.
    for item in manifest.get("blocked_assets", []):
        if in_removed_category(str(item.get("intended_path", ""))):
            item["owner_decision"] = DECISION
    manifest["blocked_assets"] = manifest.get("blocked_assets", []) + withdrawn
    manifest["pending_categories"] = [
        c for c in manifest.get("pending_categories", []) if c not in REMOVED_CATEGORIES
    ]

    # Close every backlog row in a removed category, whatever its state.
    closing = sorted(backlog_id for path, backlog_id in rows.items() if in_removed_category(path))
    for backlog_id in closing:
        backlog = set_status(backlog, backlog_id, "withdrawn")

    drop_rules_naming(compatibility, removed_files)

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

    by_category = Counter(item["intended_path"].split("/")[1] for item in withdrawn)
    print(f"withdrew {len(withdrawn)} registered assets to {RETIRED.relative_to(ROOT).as_posix()}: "
          + ", ".join(f"{n} {c}" for c, n in sorted(by_category.items())))
    print(f"closed {len(closing)} backlog rows; {len(manifest['registered_production_assets'])} assets remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
