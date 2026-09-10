#!/usr/bin/env python3
"""Withdraw the neck accessory category.

Rendered at full size over an outfit, none of the eight pieces is neckwear. The
chokers are chest-wide bands lying across the collarbones and over the garment's
own collar; the two bows cover the whole upper chest; the four pendants hang from
points outside the neck entirely, resting on the shoulders. They are ornaments at
roughly twice the scale the anatomy takes.

This is the third pass over the category. The first found it seated at Y 545-555,
mid-chest, and moved it to the throat. The second found the pieces were 150-175 px
wide against a 61 px neck, so the chain ends hung in open air, and re-seated each
one at the row where its own topmost ink lands inside the silhouette. Both passes
were fixing where the pieces sit. The remaining fault is what they are: at this
scale nothing can be seated onto a neck, because they are not built to a neck's
proportions. That needs the eight designs re-drawn, not re-placed.

So the category is withdrawn rather than adjusted again. The assets move out of
`assets/`, the manifest records why, and the backlog rows go back to pending with
the size requirement written down.

    python scripts/deregister_neck_accessories.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
LIVE = ROOT / "assets" / "neck_accessories"
RETIRED = ROOT / "incoming" / "neck_accessories_withdrawn_2026-09-10"
QA_REPORT = "docs/qa/neck_accessories_withdrawn_2026-09-10.md"

REASON = (
    "Not neckwear at this scale. Rendered over an outfit the chokers are chest-wide bands "
    "lying across the collarbones and over the garment's own collar, the bows cover the whole "
    "upper chest, and the pendants hang from points outside the neck, resting on the shoulders. "
    "Two earlier passes corrected where the pieces sit - out of mid-chest to the throat, then to "
    "the row where each one's topmost ink lands inside the silhouette - and both were fixing the "
    "wrong thing. A 150-175 px ornament cannot be seated on a 61 px neck; the designs have to be "
    "redrawn to the neck's proportions. Retained as candidate evidence."
)

REQUIREMENT = (
    "Redraw to the neck: the base body's neck is 61 px across at Y 482 and spans Y 476-496 from "
    "chin to shoulder junction. A choker is a band no wider than the neck plus a few pixels of "
    "wrap; a pendant's chain must start inside the neck silhouette and its drop hang on the "
    "chest below Y 520, clear of an outfit's collar."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    entries = [e for e in manifest["registered_production_assets"] if e["category"] == "neck_accessories"]
    if not entries:
        print("neck accessories are already withdrawn")
        return 0

    RETIRED.mkdir(parents=True, exist_ok=True)
    withdrawn = []
    for entry in sorted(entries, key=lambda e: e["id"]):
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        shutil.move(str(path), RETIRED / path.name)
        withdrawn.append({
            "id": entry["id"],
            "backlog_id": entry.get("backlog_id"),
            "intended_path": entry["path"],
            "status": "withdrawn",
            "sha256": digest,
            "retained_at": str((RETIRED / path.name).relative_to(ROOT)),
            "withdrawn_on": "2026-09-10",
            "reason": REASON,
            "requirement": REQUIREMENT,
            "qa_report": QA_REPORT,
        })

    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if e["category"] != "neck_accessories"
    ]
    blocked = [b for b in manifest.get("blocked_assets", []) if not str(b.get("id", "")).startswith("neck_accessory")]
    manifest["blocked_assets"] = blocked + withdrawn
    pending = list(manifest.get("pending_categories", []))
    if "neck_accessories" not in pending:
        pending.append("neck_accessories")
    manifest["pending_categories"] = pending
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if LIVE.exists() and not any(LIVE.iterdir()):
        LIVE.rmdir()

    backlog = ROOT / "docs" / "trait-production-backlog.md"
    lines = backlog.read_text().splitlines(keepends=True)
    ids = {w["backlog_id"] for w in withdrawn if w["backlog_id"]}
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

    print(f"withdrew {len(withdrawn)} neck accessories to {RETIRED.relative_to(ROOT)}")
    for item in withdrawn:
        print(f"  {item['id']:22s} {item['sha256'][:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
