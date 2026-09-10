#!/usr/bin/env python3
"""Withdraw the three outfits that are drawn narrower than the body they cover.

The base bodies wear a cream tank and shorts so a base reads as dressed on its
own. `outfit_005`, `outfit_009` and `outfit_010` are each drawn inside that
body: a band of tank runs from the armpit past the hip on both sides, and the
shoulder is bare above a sleeve that clearly means to reach it. Closing that
needs the garment redrawn at the body's width. Warping the edge outward was
built and reverted - it drags a lapel, a sash or a hem trim out with the edge -
and the strip cannot be filled without the garment's own contour ending up in
the middle of the fabric.

Rather than ship a garment whose sash moved in order to close a strip, the three
are withdrawn from the trait set.

`base_pose_005_centered_two_hand_grip` goes with them. Outfits are not an
optional category and `outfit_005` was the only outfit bound to that pose, so
with the outfit gone no valid token could be built on it.

Nothing is deleted. The art moves to `incoming/`, the manifest entries move to
`blocked_assets` with the SHA-256 they were retired at, and the backlog rows are
marked `QA-failed`.

    python scripts/retire_narrow_outfits.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
RETIRED = ROOT / "incoming" / "outfits_retired_2026-09-10"
QA_REPORT = "docs/qa/outfit_refit_2026-09-10.md"
WITHDRAWN_ON = "2026-09-10"

NARROW = (
    "Drawn narrower than the base body it covers. The cream tank showed as a "
    "band from the armpit past the hip on both sides, and the shoulder was bare "
    "above a sleeve drawn to reach it. Closing that needs the garment redrawn at "
    "the body's measured width: warping the edge outward drags the trim behind "
    "it, and filling the strip leaves the garment's own contour line in the "
    "middle of the fabric."
)

# id -> (why this one, what a replacement has to do)
RETIRE = {
    "outfit_005": (
        f"{NARROW} On the sun temple tunic the strip was 12-16 px down both "
        "flanks and both tank straps showed above the shoulder line.",
        "A replacement must reach the base body's own silhouette at the flank "
        "and cover the shoulder to the deltoid, measured against "
        "base_pose_005_centered_two_hand_grip before it is registered.",
    ),
    "outfit_009": (
        f"{NARROW} On the navy coat the tank ran 14-22 px wide between the "
        "coat's body and its own sleeve, from the armpit to below the hip.",
        "A replacement must close the side seam between body and sleeve and "
        "cover the shoulder cap, measured against base_body_001_neutral_master "
        "before it is registered.",
    ),
    "outfit_010": (
        f"{NARROW} On the celestial robe the same band ran beside the sash, "
        "which is why the edge could not be moved without moving the sash.",
        "A replacement must close the side seam between body and sleeve and "
        "cover the shoulder cap, measured against base_body_001_neutral_master "
        "before it is registered.",
    ),
    "base_pose_005": (
        "Withdrawn with outfit_005, which was the only outfit bound to this "
        "pose. Outfits are not an optional category, so with that binding gone "
        "the generator can build no valid token on this pose. Nothing is wrong "
        "with the pose itself.",
        "Bring this pose back together with an outfit drawn for its clasped "
        "two-hand grip. The outfits bound to base_body_001 are drawn for "
        "hanging arms and their sleeves miss these hands.",
    ),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retire_manifest(manifest: dict) -> list[dict]:
    entries = [e for e in manifest["registered_production_assets"] if e["id"] in RETIRE]
    if not entries:
        return []
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
        reason, requirement = RETIRE[entry["id"]]
        retired.append({
            "id": entry["id"],
            "backlog_id": entry.get("backlog_id"),
            "intended_path": entry["path"],
            "status": "retired",
            "sha256": digest,
            "retained_at": str((RETIRED / path.name).relative_to(ROOT)),
            "withdrawn_on": WITHDRAWN_ON,
            "reason": reason,
            "requirement": requirement,
            "qa_report": QA_REPORT,
        })
    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if e["id"] not in RETIRE
    ]
    blocked = [b for b in manifest.get("blocked_assets", []) if b.get("id") not in RETIRE]
    manifest["blocked_assets"] = blocked + retired
    pending = list(manifest.get("pending_categories", []))
    for category in ("outfits", "base_bodies"):
        if category not in pending:
            pending.append(category)
    manifest["pending_categories"] = pending
    return retired


def mark_backlog(paths: set[str]) -> int:
    """Flip the backlog rows for these asset paths to QA-failed.

    Rows are matched by asset path rather than by `DG-` id on purpose: two of the
    four assets retired here carry no `backlog_id` in the manifest, and an
    id-based update would skip them and leave the ledger claiming they are still
    registered.
    """
    lines = BACKLOG.read_text().splitlines(keepends=True)
    changed = 0
    for index, line in enumerate(lines):
        if not line.startswith("| DG-"):
            continue
        cells = line.rstrip("\n").split("|")
        if len(cells) < 10:
            continue
        if cells[6].strip().strip("`") not in paths:
            continue
        cells[8] = " QA-failed "
        lines[index] = "|".join(cells) + "\n"
        changed += 1
    BACKLOG.write_text("".join(lines), encoding="utf-8")
    return changed


def drop_compatibility(ids: set[str]) -> int:
    rules = json.loads(COMPATIBILITY.read_text())
    before = len(rules["requires"])
    rules["requires"] = [
        r for r in rules["requires"]
        if not any(r.get("trait", "").startswith(i) for i in ids)
    ]
    COMPATIBILITY.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    return before - len(rules["requires"])


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    retired = retire_manifest(manifest)
    if not retired:
        print("those outfits are already retired")
        return 0
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    paths = {item["intended_path"] for item in retired}
    changed = mark_backlog(paths)
    if changed != len(retired):
        raise SystemExit(f"updated {changed} backlog rows, expected {len(retired)}")

    dropped = drop_compatibility(set(RETIRE))

    print(f"retired {len(retired)} assets to {RETIRED.relative_to(ROOT)}")
    for item in retired:
        print(f"  {item['id']:16s} {item['sha256'][:12]}  backlog_id={item['backlog_id']}")
    print(f"backlog rows marked QA-failed: {changed}")
    print(f"compatibility rules dropped: {dropped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
