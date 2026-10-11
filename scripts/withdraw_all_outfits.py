#!/usr/bin/env python3
"""Withdraw every outfit: the owner removed all clothing on 2026-10-11.

After the 77 rare 1-of-1s were finished, the owner judged that none of the
registered garments suited the collection's art. Every outfit leaves the
generator so the category can be redrawn from the 1-of-1s
(docs/qa/outfits_withdrawn_2026-10-11.md). The base bodies render undressed
until new outfits are registered; the outfits category is optional, so the
generator keeps working with it empty.

As in scripts/withdraw_traits.py, each file moves to
incoming/outfits_withdrawn_2026-10-11/outfits/ (untracked; history keeps the
bytes at the recorded hash), its manifest entry becomes a withdrawn record, its
backlog row closes as withdrawn, and every compatibility rule naming it goes.

    python scripts/withdraw_all_outfits.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

try:
    from scripts.withdraw_headwear_and_auras import (
        BACKLOG, COMPATIBILITY, MANIFEST, ROOT, backlog_rows, drop_rules_naming, set_status, sha256_file,
    )
except ImportError:  # Direct execution from scripts/.
    from withdraw_headwear_and_auras import (  # type: ignore[no-redef]
        BACKLOG, COMPATIBILITY, MANIFEST, ROOT, backlog_rows, drop_rules_naming, set_status, sha256_file,
    )

RETIRED = ROOT / "incoming" / "outfits_withdrawn_2026-10-11"
DECIDED_ON = "2026-10-11"
QA_REPORT = "docs/qa/outfits_withdrawn_2026-10-11.md"
REASON = (
    "The owner removed all clothing from the generator on 2026-10-11: the registered outfits "
    "did not suit the finished 1-of-1 artwork. New outfits will be drawn per pose from the "
    "1-of-1 study in docs/pose_anatomy_2026-10-11.md."
)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    registered = manifest["registered_production_assets"]

    removing = [e for e in registered if e["category"] == "outfits"]
    if not removing:
        print("already withdrawn")
        return 0

    rows = backlog_rows(backlog)
    records = []
    for entry in sorted(removing, key=lambda e: e["path"]):
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        destination = RETIRED / "outfits" / path.name
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
            "reason": REASON,
            "qa_report": QA_REPORT,
        })
        if entry["path"] in rows:
            backlog = set_status(backlog, rows[entry["path"]], "withdrawn")

    manifest["registered_production_assets"] = [e for e in registered if e["category"] != "outfits"]
    manifest["blocked_assets"] = manifest.get("blocked_assets", []) + records
    drop_rules_naming(compatibility, {Path(e["path"]).name for e in removing})

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"withdrew {len(records)} outfits to {RETIRED.relative_to(ROOT).as_posix()}; "
          f"{len(manifest['registered_production_assets'])} assets remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
