#!/usr/bin/env python3
"""Withdraw registered outfits from the collection by recorded decision.

    python scripts/withdraw_outfits.py outfit_005_sun_temple_pose_005.png \\
        --reason "Removed by the owner on 2026-09-25: ..." --qa-report docs/qa/<note>.md

For each named outfit this retires the bytes to ``incoming/outfits_withdrawn_<date>/``,
moves its manifest entry to ``blocked_assets`` with its SHA-256 and the reason,
closes its backlog row as ``withdrawn``, and removes every compatibility rule that
names it - its pose binding, its ``hides`` rule and any exclusion. A dressed-body
render is also marked withdrawn in its ``sources.json`` review, so a later
``intake_dressed_bodies.py --register`` cannot put it back. The ledger is
regenerated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
DRESSED_SOURCES = ROOT / "images" / "trait_candidates" / "outfits_dressed" / "sources.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def names(value: object) -> list[str]:
    return [value] if isinstance(value, str) else list(value or [])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("outfits", nargs="+", help="registered outfit filenames")
    parser.add_argument("--reason", required=True, help="why the outfits leave the collection")
    parser.add_argument("--qa-report", required=True, help="repository path of the note recording the decision")
    args = parser.parse_args(argv)

    today = date.today().isoformat()
    retired_dir = ROOT / "incoming" / f"outfits_withdrawn_{today}"
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    rules = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    targets = set(args.outfits)

    entries = {Path(e["path"]).name: e for e in manifest["registered_production_assets"]
               if e["category"] == "outfits"}
    missing = sorted(targets - set(entries))
    if missing:
        print(f"error: not registered outfits: {', '.join(missing)}", file=sys.stderr)
        return 1

    records = []
    for name in sorted(targets):
        entry = entries[name]
        path = ROOT / entry["path"]
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            print(f"error: {name} does not match its manifest hash", file=sys.stderr)
            return 1
        retired_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), retired_dir / name)
        # Match the backlog row by asset path, not by the manifest's backlog_id:
        # some older entries carry none, and an id-based update skips them silently.
        row = re.compile(rf"^(\| (DG-\d{{3}}) \|[^\n]*`{re.escape(entry['path'])}`[^\n]*\| )([A-Za-z-]+)( \|)$",
                         re.MULTILINE)
        found = row.search(backlog)
        if found is None:
            print(f"error: no backlog row claims {entry['path']}", file=sys.stderr)
            return 1
        backlog = row.sub(r"\g<1>withdrawn\g<4>", backlog, count=1)
        records.append({
            "id": entry["id"],
            "backlog_id": entry.get("backlog_id") or found.group(2),
            "intended_path": entry["path"],
            "status": "withdrawn",
            "sha256": digest,
            "retained_at": str((retired_dir / name).relative_to(ROOT)),
            "withdrawn_on": today,
            "reason": args.reason,
            "requirement": "Return only as a new render that passes the collection's gates, by the owner's decision.",
            "owner_decision": args.reason,
            "qa_report": args.qa_report,
        })

    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if Path(e["path"]).name not in targets
    ]
    manifest["blocked_assets"] = manifest.get("blocked_assets", []) + records

    rules["requires"] = [r for r in rules.get("requires", []) if r.get("trait") not in targets]
    rules["hides"] = [r for r in rules.get("hides", []) if r.get("trait") not in targets]
    kept_excludes = []
    for rule in rules.get("excludes", []):
        if rule.get("trait") in targets:
            continue
        remaining = [n for n in names(rule.get("excludes")) if n not in targets]
        if remaining:
            rule["excludes"] = remaining
            kept_excludes.append(rule)
    rules["excludes"] = kept_excludes

    if DRESSED_SOURCES.exists():
        sources = json.loads(DRESSED_SOURCES.read_text(encoding="utf-8"))
        for render in sources.get("renders", []):
            if render.get("target") in targets:
                render.setdefault("review", {})
                render["review"]["decision"] = "withdrawn"
                render["review"]["withdrawn_on"] = today
                render["review"]["withdrawn_reason"] = args.reason
        DRESSED_SOURCES.write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for record in records:
        print(f"withdrew {record['backlog_id']} {Path(record['intended_path']).name}")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "report_production_status.py"), "--write"],
                   check=True, cwd=ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
