#!/usr/bin/env python3
"""Record the cowl opening cut into `outfit_006` in the asset manifest.

The black hooded robe's cowl was painted shut: a flat near-black shape, values
around (17,18,21) with no modelling in it at all, arched up to y475. The rig's
chin is 476.5, so the fill met the jaw and covered the neck completely, and the
head read as sitting on a black dome.

`docs/qa/outfit_necklines_2026-09-10.md` had declined this one, on the grounds
that a high cowl closing at the jaw is a garment rather than a defect. Rendered
over the base and enlarged it is neither: there is no neck, and no fold, seam or
shading anywhere in the shape that would make it read as one. It is the same
sealed interior `outfit_010`'s stand collar had, in a hood.

The cut is `scripts/open_collar.py` with the cowl's own rim traced from the art:

    rim_centre 510  rim_rise 20  half 30

The rim's ends land on the neck's own silhouette where it flares into the
trapezius, at about y490, so the opening closes on drawn anatomy instead of
ending mid-shoulder. Ending it on a wider arc left a soft notch at each side of
the neck's base, where the cut's wall crossed the flare with nothing to meet.

    python scripts/update_hood_opening_manifest.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
ASSET_ID = "outfit_006"
METHOD = "open_collar_crisp_rim_c510_r20_h30"
QA_REPORT = "docs/qa/outfit_refit_2026-09-10.md"
NOTE = (
    "The cowl's interior was painted opaque as a flat near-black shape whose top "
    "arc reached y475, one row above the rig's chin at 476.5, so it covered the "
    "whole neck and the head read as sitting on a black dome. Cut above the rim "
    "arc traced from the art, bounded by the base body's own neck alpha, so the "
    "opening's walls close on the neck's silhouette where it flares at about "
    "y490. 1768 px cleared; no other pixel of the garment is touched."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    entry = next((e for e in manifest["registered_production_assets"]
                  if e["id"] == ASSET_ID), None)
    if entry is None:
        raise SystemExit(f"{ASSET_ID} is not registered")

    path = ROOT / entry["path"]
    digest = sha256_file(path)
    if digest == entry["sha256"]:
        print(f"{ASSET_ID}: manifest already matches the file")
        return 0

    provenance = entry.setdefault("provenance", {})
    steps = provenance.setdefault("postprocessing", [])
    if METHOD not in steps:
        steps.append(METHOD)
    scripts = provenance.get("postprocessing_script", "")
    if "open_collar" not in scripts:
        provenance["postprocessing_script"] = (
            f"{scripts}; scripts/open_collar.py" if scripts else "scripts/open_collar.py"
        )
    provenance["pre_hood_opening_sha256"] = entry["sha256"]
    provenance["post_hood_opening_sha256"] = digest
    provenance["collar_note"] = NOTE
    entry["sha256"] = digest
    entry["qa_report"] = QA_REPORT

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"{ASSET_ID}: sha256 -> {digest[:12]}, recorded {METHOD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
