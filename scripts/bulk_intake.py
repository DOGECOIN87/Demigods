#!/usr/bin/env python3
"""QA a whole batch of generated trait candidates in one pass.

Registering an asset today means running the rig gate by hand, building a
composite by hand, eyeballing it, then hand-editing the manifest and the
backlog. That is fine for one representative test and far too slow for a
twenty-asset batch.

This script does the mechanical part for a whole drop folder at once:

    python scripts/bulk_intake.py incoming/

  - matches each PNG to its backlog row by canonical filename
  - runs binary QA (native size, RGBA, genuine alpha, full decode)
  - runs the category's rig gate in --trait mode with its width ceiling
  - composites each candidate over the base master in correct layer order
  - renders ONE review sheet so approval is a single visual pass
  - writes a JSON report

Nothing is registered by this step. After looking at the review sheet:

    python scripts/bulk_intake.py incoming/ --register-approved DG-029 DG-030

which copies the exact approved bytes to their canonical paths, writes manifest
entries, flips backlog status to `registered`, and regenerates the ledger.
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

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:  # imported as `scripts.bulk_intake` by the tests
    from scripts.build_asset_prompts import (
        CATEGORY_LAYER, PROCEDURAL_GATE_FLAGS, gate_flags, parse_backlog,
    )
    from scripts.build_trait_prompts import GATES
    from scripts.rig_gate_report import analyze, load_rig
except ImportError:  # run directly as a script
    from build_asset_prompts import (  # type: ignore[no-redef]
        CATEGORY_LAYER, PROCEDURAL_GATE_FLAGS, gate_flags, parse_backlog,
    )
    from build_trait_prompts import GATES  # type: ignore[no-redef]
    from rig_gate_report import analyze, load_rig  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
MANIFEST = ROOT / "assets" / "asset_manifest.json"
CONFIG = ROOT / "config" / "collection.json"
BASE_MASTER = ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png"
COMPOSITE_DIR = ROOT / "docs" / "qa" / "composites"

LAYER_ORDER = [
    "backgrounds", "rear_auras", "back_accessories", "hair_back",
    "base_bodies", "outfits", "neck_accessories", "eyes", "eyebrows",
    "mouths", "expression_marks", "hair_front", "head_accessories",
    "hand_objects", "front_auras", "global_finish",
]
BASE_INDEX = LAYER_ORDER.index("base_bodies")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_category(production_path: str) -> str:
    """assets/<category>/<file>.png -> <category>."""
    return Path(production_path).parent.name


def asset_id(production_path: str) -> str:
    """hair_back_003_silver_long_wavy.png -> hair_back_003."""
    stem = Path(production_path).stem
    match = re.match(r"^(.*?_\d{3})", stem)
    return match.group(1) if match else stem


def max_width_ratio_for(category: str) -> float | None:
    """Pull the category's width ceiling out of the shared gate table."""
    layer = CATEGORY_LAYER.get(category)
    if layer is None:
        return None
    gate_cmd, _ = GATES[layer]
    match = re.search(r"--max-width-ratio\s+([\d.]+)", gate_cmd)
    return float(match.group(1)) if match else None


def load_transform_provenance(candidate: Path) -> tuple[dict | None, list[str]]:
    """Load and verify an optional generator-source transformation sidecar.

    Direct native candidates retain the existing no-sidecar path. A normalized
    candidate must prove that its immutable source still exists and that neither
    the source nor the output changed after the transform report was written.
    """
    sidecar = candidate.with_suffix(candidate.suffix + ".provenance.json")
    if not sidecar.exists():
        return None, []
    try:
        value = json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"transform provenance unreadable: {type(exc).__name__}: {exc}"]
    if not isinstance(value, dict):
        return None, ["transform provenance must be a JSON object"]

    errors: list[str] = []
    if value.get("origin") != "generator_source_transform":
        errors.append("transform provenance origin must be generator_source_transform")
    source_value = value.get("source_path")
    source = ROOT / source_value if isinstance(source_value, str) else None
    if not isinstance(source_value, str) or Path(source_value).is_absolute() or ".." in Path(source_value).parts:
        errors.append("transform provenance source_path must be a safe repository-relative path")
    elif source is None or not source.is_file():
        errors.append(f"transform provenance source does not exist: {source_value}")
    elif value.get("source_sha256") != sha256(source):
        errors.append("transform provenance source SHA-256 does not match immutable source")

    if value.get("output_sha256") != sha256(candidate):
        errors.append("transform provenance output SHA-256 does not match normalized candidate")
    if value.get("final_dimensions") != [1254, 1254]:
        errors.append("transform provenance final_dimensions must be [1254, 1254]")
    transform = value.get("transform")
    if not isinstance(transform, dict) or transform.get("method") != "crop_transparent_margin_then_premultiplied_lanczos_reduction":
        errors.append("transform provenance must record the approved reduction-only method")
    elif not isinstance(transform.get("scale"), (float, int)) or not 0 < transform["scale"] < 1:
        errors.append("transform provenance scale must prove a reduction-only operation")
    return value, errors


def binary_qa(path: Path) -> list[tuple[str, bool, str]]:
    """Decode fully and confirm the properties a modular layer must have."""
    checks: list[tuple[str, bool, str]] = []
    try:
        with Image.open(path) as im:
            im.load()  # full decode; a truncated file raises here
            size, mode, fmt = im.size, im.mode, im.format
            alpha_extrema = im.convert("RGBA").getchannel("A").getextrema()
    except Exception as exc:  # noqa: BLE001 - report any decode failure verbatim
        return [("decode", False, f"{type(exc).__name__}: {exc}")]

    checks.append(("decode", True, "full decode ok"))
    checks.append(("format", fmt == "PNG", f"{fmt}"))
    checks.append(("dimensions", size == (1254, 1254), f"{size[0]}x{size[1]}"))
    checks.append(("mode", mode == "RGBA", mode))
    checks.append(("genuine_alpha", alpha_extrema[0] == 0, f"alpha_min={alpha_extrema[0]}"))
    checks.append(("visible_pixels", alpha_extrema[1] > 0, f"alpha_max={alpha_extrema[1]}"))
    return checks


def build_composite(candidate: Path, category: str, out_path: Path) -> Path:
    """Composite the candidate over the base master in correct layer order."""
    base = Image.open(BASE_MASTER).convert("RGBA")
    trait = Image.open(candidate).convert("RGBA")
    canvas = Image.new("RGBA", base.size, (255, 255, 255, 255))

    behind = LAYER_ORDER.index(category) < BASE_INDEX if category in LAYER_ORDER else False
    if behind:
        canvas.alpha_composite(trait)
        canvas.alpha_composite(base)
    else:
        canvas.alpha_composite(base)
        canvas.alpha_composite(trait)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path)
    return out_path


def render_review_sheet(results: list[dict], out_path: Path, columns: int = 5) -> Path:
    """One sheet with every composite and its verdict, for a single approval pass."""
    cell, pad, label_h = 300, 12, 46
    rows = (len(results) + columns - 1) // columns
    width = columns * (cell + pad) + pad
    height = rows * (cell + label_h + pad) + pad + 40
    sheet = Image.new("RGB", (width, height), (24, 24, 28))
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, pad), f"Demigods batch review — {len(results)} candidate(s)", fill=(240, 240, 240))

    for index, result in enumerate(results):
        col, row = index % columns, index // columns
        x = pad + col * (cell + pad)
        y = 40 + pad + row * (cell + label_h + pad)
        composite = result.get("composite")
        if composite and Path(composite).exists():
            thumb = Image.open(composite).convert("RGB")
            thumb.thumbnail((cell, cell))
            sheet.paste(thumb, (x + (cell - thumb.width) // 2, y))
        else:
            draw.rectangle([x, y, x + cell, y + cell], outline=(120, 60, 60))
            draw.text((x + 8, y + cell // 2), "no composite", fill=(200, 120, 120))

        passed = result["passed"]
        colour = (120, 230, 140) if passed else (240, 120, 120)
        draw.text((x + 4, y + cell + 6), f"{result['id']}  {'PASS' if passed else 'FAIL'}", fill=colour)
        draw.text((x + 4, y + cell + 20), result["filename"][:40], fill=(180, 180, 190))
        if not passed:
            draw.text((x + 4, y + cell + 32), result["failures"][0][:40], fill=(220, 150, 150))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)
    return out_path


def inspect(drop_dir: Path, rows: list[dict]) -> list[dict]:
    by_filename = {Path(r["path"]).name: r for r in rows}
    loaded = load_rig(CONFIG)
    rig, canvas = loaded["rig"], loaded["canvas"]

    results = []
    for candidate in sorted(drop_dir.glob("*.png")):
        row = by_filename.get(candidate.name)
        result: dict = {
            "filename": candidate.name,
            "source": str(candidate),
            "sha256": sha256(candidate),
            "passed": False,
            "failures": [],
        }
        if row is None:
            result["id"] = "UNMATCHED"
            result["failures"].append("filename matches no backlog production path")
            results.append(result)
            continue

        category = manifest_category(row["path"])
        result.update({
            "id": row["id"],
            "backlog_status": row["status"],
            "category": category,
            "production_path": row["path"],
            "description": row["description"],
        })

        provenance, provenance_errors = load_transform_provenance(candidate)
        if provenance is not None:
            result["provenance"] = provenance
        result["failures"] += [f"provenance:{error}" for error in provenance_errors]

        checks = binary_qa(candidate)
        result["binary_qa"] = [{"check": c, "passed": p, "value": v} for c, p, v in checks]
        result["failures"] += [f"binary:{c}={v}" for c, p, v in checks if not p]

        if not result["failures"]:
            # A ground-plane ring is seated on the foot baseline so the character
            # stands inside it, putting its near arc below Y 1139. Gating every
            # candidate as a partial layer would fail that whole family on
            # max_bounds for doing exactly what it is designed to do.
            flags = gate_flags(row)
            result["gate_mode"] = flags
            gate = analyze(
                candidate, rig, canvas, tolerance=1,
                trait="--trait" in flags,
                floor_aura="--floor-aura" in flags,
                global_finish="--global-finish" in flags,
                max_width_ratio=max_width_ratio_for(row["category"]),
            )
            result["rig_gate"] = {
                "passed": gate["passed"],
                "checks": [
                    {"check": c, "passed": p, "value": str(v), "expected": str(e)}
                    for c, p, v, e, _ in gate["checks"]
                ],
            }
            result["failures"] += [
                f"gate:{c}={v}" for c, p, v, e, _ in gate["checks"] if not p
            ]
            composite = COMPOSITE_DIR / f"{asset_id(row['path'])}_over_base.png"
            result["composite"] = str(build_composite(candidate, category, composite).relative_to(ROOT))

        if row["status"] == "registered":
            result["failures"].append("backlog row is already registered")

        result["passed"] = not result["failures"]
        results.append(result)
    return results


def pair_hair_rule(production_path: str, manifest: dict) -> dict | None:
    """Bind a front-hair layer to the rear-hair layer of the same colour.

    `hair_front_004` and `hair_back_004` are the same colour by construction —
    the two HAIR reference rows are index-aligned. Without a rule the generator
    will happily put violet bangs on gold rear hair, and put bangs on a token
    whose rear hair rolled absent, which reads as floating hair on a bald head.

    The config validator rejects rules that name a file not yet on disk, so the
    rule can only be written at the moment the front layer is registered.
    """
    name = Path(production_path).name
    match = re.match(r"^hair_front_(\d{3})", name)
    if not match:
        return None
    index = match.group(1)
    counterpart = next(
        (
            e["path"]
            for e in manifest["registered_production_assets"]
            if Path(e["path"]).name.startswith(f"hair_back_{index}")
        ),
        None,
    )
    if counterpart is None:
        return None
    return {
        "trait": name,
        "requires": Path(counterpart).name,
        "reason": (
            "Front bangs must match the rear hair colour, and must not appear on a token "
            "whose rear hair is absent."
        ),
    }


def clear_finished_categories(manifest: dict, backlog_text: str) -> list[str]:
    """Drop categories from `pending_categories` once every row is registered.

    The ledger cross-check fails when the manifest still calls a category pending
    after its last asset lands, so this has to happen in the same write as the
    registration rather than being left to a follow-up edit.

    Mutates `manifest` and returns the categories cleared.
    """
    rows = parse_backlog(backlog_text)
    finished = []
    for category in list(manifest.get("pending_categories", [])):
        category_rows = [r for r in rows if manifest_category(r["path"]) == category]
        if category_rows and all(r["status"] == "registered" for r in category_rows):
            manifest["pending_categories"].remove(category)
            finished.append(category)
    return finished


def register(results: list[dict], approved: set[str], batch_note: str) -> int:
    manifest = json.loads(MANIFEST.read_text())
    backlog_text = BACKLOG.read_text()
    compatibility_path = ROOT / "config" / "compatibility.json"
    compatibility = json.loads(compatibility_path.read_text())
    by_id = {r["id"]: r for r in results}

    unknown = approved - set(by_id)
    if unknown:
        print(f"error: not in this batch: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1

    blocked = [i for i in approved if not by_id[i]["passed"]]
    if blocked:
        print(
            "error: refusing to register candidates that failed QA: "
            + ", ".join(sorted(blocked)),
            file=sys.stderr,
        )
        return 1

    today = date.today().isoformat()
    registered = []
    pending_copies: list[tuple[Path, Path]] = []
    for backlog_id in sorted(approved):
        result = by_id[backlog_id]

        entry = {
            "id": asset_id(result["production_path"]),
            "category": result["category"],
            "path": result["production_path"],
            "status": "production_ready",
            "sha256": result["sha256"],
            "dimensions": [1254, 1254],
            "format": "PNG",
            "mode": "RGBA",
            "backlog_id": backlog_id,
            "qa_composite": result["composite"],
            "provenance": result.get("provenance") or {
                "origin": "native_image_generation",
                "reference_path": "assets/base_bodies/base_body_001_neutral_master.png",
                "trait": result["description"],
                "native_dimensions": [1254, 1254],
                "intake_script": "scripts/bulk_intake.py",
            },
            "approved_on": today,
            "qa_report": batch_note,
        }
        manifest["registered_production_assets"].append(entry)

        # Any pre-registration status is registerable: `pending` for an asset
        # that was never produced, `candidate` for one whose art is in hand
        # awaiting review, `approved` for one already signed off. `registered`
        # is excluded so a re-run cannot silently double-register.
        pattern = re.compile(
            rf"^(\| {re.escape(backlog_id)} \|.*\| )(pending|candidate|approved)( \|?\s*)$",
            re.MULTILINE,
        )
        backlog_text, count = pattern.subn(r"\1registered\3", backlog_text)
        if count != 1:
            print(
                f"error: could not flip backlog status for {backlog_id} "
                f"(matched {count} rows); nothing written",
                file=sys.stderr,
            )
            return 1
        # Deferred until every validation has passed. Copying inside this loop
        # left an unregistered PNG under assets/<category>/ when a later step
        # failed, and the generator discovers assets by scanning those folders —
        # so a partial failure would have put unapproved art into the collection.
        pending_copies.append((Path(result["source"]), ROOT / result["production_path"]))
        registered.append(backlog_id)

    # Pairing rules are appended after every asset in the batch is in the
    # manifest, so a front layer can bind to a rear layer registered in the same
    # run regardless of the order the two were approved in.
    existing = {(r["trait"], r["requires"]) for r in compatibility["requires"]}
    added_rules = []
    for backlog_id in sorted(approved):
        rule = pair_hair_rule(by_id[backlog_id]["production_path"], manifest)
        if rule and (rule["trait"], rule["requires"]) not in existing:
            compatibility["requires"].append(rule)
            existing.add((rule["trait"], rule["requires"]))
            added_rules.append(f"{rule['trait']} -> {rule['requires']}")

    finished = clear_finished_categories(manifest, backlog_text)
    if finished:
        print(f"Category complete, cleared from pending: {', '.join(finished)}")

    # Everything validated; now commit the side effects.
    for source, destination in pending_copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)  # exact approved bytes

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    BACKLOG.write_text(backlog_text)
    if added_rules:
        compatibility_path.write_text(json.dumps(compatibility, indent=2) + "\n")
        print(f"Added {len(added_rules)} hair pairing rule(s): {'; '.join(added_rules)}")
    print(f"Registered {len(registered)}: {', '.join(registered)}")

    ledger = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "report_production_status.py"), "--write"],
        capture_output=True, text=True,
    )
    print(ledger.stdout.strip().splitlines()[0] if ledger.stdout else ledger.stderr.strip())
    return ledger.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drop_dir", type=Path, help="folder of generated candidate PNGs")
    parser.add_argument("--register-approved", nargs="*", metavar="DG-ID")
    parser.add_argument("--sheet", type=Path, default=ROOT / "docs" / "qa" / "batch_review_sheet.png")
    parser.add_argument("--report", type=Path, default=ROOT / "docs" / "qa" / "batch_intake_report.json")
    parser.add_argument("--qa-note", default="docs/qa/batch_intake_report.json")
    args = parser.parse_args(argv)

    if not args.drop_dir.is_dir():
        print(f"error: {args.drop_dir} is not a directory", file=sys.stderr)
        return 1

    rows = parse_backlog(BACKLOG.read_text())
    results = inspect(args.drop_dir, rows)
    if not results:
        print(f"No PNGs found in {args.drop_dir}.", file=sys.stderr)
        return 1

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(results, indent=2) + "\n")

    passed = [r for r in results if r["passed"]]
    print(f"{len(passed)}/{len(results)} candidate(s) passed automated QA.\n")
    for result in results:
        mark = "PASS" if result["passed"] else "FAIL"
        print(f"  [{mark}] {result['id']:<8} {result['filename']}")
        for failure in result["failures"]:
            print(f"           - {failure}")

    if any(r.get("composite") for r in results):
        sheet = render_review_sheet(results, args.sheet)
        print(f"\nReview sheet: {sheet.relative_to(ROOT)}")
        print(f"Report:       {args.report.relative_to(ROOT)}")

    if args.register_approved is not None:
        if not args.register_approved:
            print("error: --register-approved needs at least one backlog ID", file=sys.stderr)
            return 1
        return register(results, set(args.register_approved), args.qa_note)

    print("\nNothing registered. Review the sheet, then re-run with "
          "--register-approved <DG-IDs>.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
