#!/usr/bin/env python3
"""Withdraw single hand objects the owner removed from the collection.

2026-09-27: the violet blade (hand_object_009). It still had its old art, drawn
behind the body's fist, and no render with the hand painted holding it had
passed; the owner removed it rather than wait for one. The rest of the
category stays.

As for the headwear and auras (scripts/withdraw_headwear_and_auras.py), each file
moves to incoming/owner_removed_2026-09-27/hand_objects/, which git ignores (history
keeps the bytes at the recorded hash). Its manifest entry becomes a withdrawn
record, its backlog row closes as withdrawn, and the compatibility rules naming it
go. To remove another, add its asset id and the reason to WITHDRAWN.

    python scripts/withdraw_hand_objects.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

try:
    from scripts.withdraw_headwear_and_auras import (
        BACKLOG, COMPATIBILITY, DECIDED_ON, MANIFEST, RETIRED, ROOT,
        backlog_rows, drop_rules_naming, set_status, sha256_file,
    )
except ImportError:  # Direct execution from scripts/.
    from withdraw_headwear_and_auras import (  # type: ignore[no-redef]
        BACKLOG, COMPATIBILITY, DECIDED_ON, MANIFEST, RETIRED, ROOT,
        backlog_rows, drop_rules_naming, set_status, sha256_file,
    )

QA_REPORT = "docs/qa/hand_objects_in_hand_2026-09-27.md"
WITHDRAWN = {
    "hand_object_009": (
        "The owner removed the violet blade from the collection on 2026-09-27. It still had "
        "its old art, drawn behind the body's fist, and no render with the hand painted "
        "holding it had passed review."
    ),
}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    registered = manifest["registered_production_assets"]

    removing = [e for e in registered if e["id"] in WITHDRAWN]
    if not removing:
        print("already withdrawn")
        return 0

    rows = backlog_rows(backlog)
    records = []
    for entry in sorted(removing, key=lambda e: e["path"]):
        if entry["category"] != "hand_objects":
            raise SystemExit(f"{entry['id']} is not a hand object")
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        destination = RETIRED / "hand_objects" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), destination)
        records.append({
            "id": entry["id"],
            "backlog_id": rows.get(entry["path"]),
            "intended_path": entry["path"],
            "status": "withdrawn",
            "sha256": digest,
            "retained_at": destination.relative_to(ROOT).as_posix(),
            "withdrawn_on": DECIDED_ON,
            "reason": WITHDRAWN[entry["id"]],
            "qa_report": QA_REPORT,
        })
        backlog = set_status(backlog, rows[entry["path"]], "withdrawn")

    manifest["registered_production_assets"] = [e for e in registered if e["id"] not in WITHDRAWN]
    manifest["blocked_assets"] = manifest.get("blocked_assets", []) + records
    drop_rules_naming(compatibility, {Path(e["path"]).name for e in removing})

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"withdrew {', '.join(r['id'] for r in records)} to {RETIRED.relative_to(ROOT).as_posix()}/hand_objects; "
          f"{len(manifest['registered_production_assets'])} assets remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
