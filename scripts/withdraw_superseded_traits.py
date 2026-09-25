#!/usr/bin/env python3
"""Record the owner's 2026-09-25 decisions: neckwear omitted, four outfits superseded.

Two sets of assets leave the collection by decision rather than by failing QA,
so their backlog rows close as ``withdrawn`` instead of staying open as work:

- **Neck accessories, DG-047-DG-054.** Out of assets/ since 2026-09-10 because
  none was drawn to the neck it sat on (docs/qa/neck_accessories_withdrawn_2026-09-10.md).
  On 2026-09-25 the owner omitted neckwear from the collection. The eight
  withdrawal records keep their hashes and reasons; this adds the decision.
- **Outfits 006-009, DG-042-DG-045.** Each was one garment layer fitted to the
  neutral pose only, over a base it did not fully cover. The owner supplied each
  family again as five dressed-body renders, one per pose
  (images/trait_candidates/outfits_dressed/), which replace them. The
  single-pose layers are retired, not deleted, and their requires rules go.

    python scripts/withdraw_superseded_traits.py
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
COMPATIBILITY = ROOT / "config" / "compatibility.json"
RETIRED = ROOT / "incoming" / "outfits_superseded_2026-09-25"
DECIDED_ON = "2026-09-25"
QA_REPORT = "docs/qa/dressed_bodies_2026-09-25.md"

SUPERSEDED = {
    "outfit_006": "outfit_006_black_layered_hooded_robe",
    "outfit_007": "outfit_007_brown_leather_long_coat",
    "outfit_008": "outfit_008_olive_ragged_cloak",
    "outfit_009": "outfit_009_navy_high_collar_coat",
}
NECKWEAR_ROWS = [f"DG-{n:03d}" for n in range(47, 55)]
NECKWEAR_DECISION = (
    "Omitted from the collection by the owner on 2026-09-25. The category stays "
    "defined so a redrawn set could return, but no neckwear is planned."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_status(backlog: str, backlog_id: str, status: str) -> str:
    pattern = re.compile(rf"^(\| {re.escape(backlog_id)} \|.*\| )([A-Za-z-]+)( \|)$", re.MULTILINE)
    updated, count = pattern.subn(rf"\g<1>{status}\g<3>", backlog)
    if count != 1:
        raise SystemExit(f"{backlog_id}: matched {count} backlog rows")
    return updated


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))

    retiring = [e for e in manifest["registered_production_assets"] if e["id"] in SUPERSEDED]
    RETIRED.mkdir(parents=True, exist_ok=True)
    retired = []
    for entry in sorted(retiring, key=lambda e: e["id"]):
        path = ROOT / entry["path"]
        if not path.exists():
            raise SystemExit(f"missing registered asset: {entry['path']}")
        digest = sha256_file(path)
        if digest != entry["sha256"]:
            raise SystemExit(f"{entry['id']}: file does not match the manifest hash")
        shutil.move(str(path), RETIRED / path.name)
        family = SUPERSEDED[entry["id"]]
        retired.append({
            "id": entry["id"],
            "backlog_id": entry.get("backlog_id"),
            "intended_path": entry["path"],
            "status": "retired",
            "sha256": digest,
            "retained_at": str((RETIRED / path.name).relative_to(ROOT)),
            "withdrawn_on": DECIDED_ON,
            "reason": (
                "Superseded by the owner's dressed-body renders of the same family, "
                f"assets/outfits/{family}_pose_001.png to _pose_005.png. This layer was fitted "
                "to the neutral pose only, so the family appeared in one pose of five, and it "
                "was drawn narrower than the base it covered; the dressed renders are painted "
                "with the body, in every pose. Nothing replaces it in pose 001 but its own "
                "dressed render."
            ),
            "requirement": (
                "Do not bring back alongside the dressed family: two versions of one outfit in "
                "the same pose would be a duplicate trait."
            ),
            "qa_report": QA_REPORT,
        })
        backlog = set_status(backlog, entry["backlog_id"], "withdrawn")
    manifest["registered_production_assets"] = [
        e for e in manifest["registered_production_assets"] if e["id"] not in SUPERSEDED
    ]
    manifest["blocked_assets"] = [
        b for b in manifest.get("blocked_assets", []) if b.get("id") not in SUPERSEDED
    ] + retired

    for item in manifest["blocked_assets"]:
        if item.get("backlog_id") in NECKWEAR_ROWS:
            item["owner_decision"] = NECKWEAR_DECISION
    for backlog_id in NECKWEAR_ROWS:
        backlog = set_status(backlog, backlog_id, "withdrawn")
    manifest["pending_categories"] = [
        c for c in manifest.get("pending_categories", []) if c != "neck_accessories"
    ]

    superseded_files = {f"{name}.png" for name in SUPERSEDED.values()}
    compatibility["requires"] = [
        r for r in compatibility["requires"] if r.get("trait") not in superseded_files
    ]

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"retired {len(retired)} superseded outfits to {RETIRED.relative_to(ROOT)}")
    for item in retired:
        print(f"  {item['id']:12s} {item['backlog_id']}  {item['sha256'][:12]}")
    print(f"withdrew neckwear rows {NECKWEAR_ROWS[0]}-{NECKWEAR_ROWS[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
