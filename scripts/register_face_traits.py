#!/usr/bin/env python3
"""Register the 60 facial traits and the rebuilt front aura.

Copies the built bytes into `assets/<category>/`, writes a manifest entry per
asset, flips the backlog rows to `registered`, clears the five categories that
were still pending, and makes expression marks optional.

Two naming corrections are made here, and both are deliberate.

The backlog's intended paths for the facial families cite cells of a `FACE`
reference sheet - `eyes_001_sheet_r1c1_dark_neutral.png` and so on. That sheet
exists in this repository only as a 128x96 browsing preview, from which a 1254 px
eye pair cannot be reconstructed, so the families are built from the approved
master's own painted face instead. Keeping `sheet_r1c1` in the filename would
claim a provenance the asset does not have, so the cell reference is dropped from
the names and the reason is recorded in each entry.

`aura_front_001` was deregistered on 2026-09-09 as a flat-shaded placeholder. Its
replacement is a rendered flame field, so the blocked-asset record is retired
rather than left standing beside a registered asset of the same id.

    python scripts/register_face_traits.py --built incoming/face_traits_2026-09-09
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
APPROVED_ON = "2026-09-09"
QA_REPORT = "docs/qa/face_traits_2026-09-09/README.md"
AURA_QA_REPORT = "docs/qa/front_aura_001_rebuilt_2026-09-09.md"

# Expression marks are an accent, not a feature: most faces carry none.
OPTIONAL_RATES = {"expression_marks": 0.3}

NAME_NOTE = (
    "The backlog cites cells of a FACE reference sheet for this family. That sheet is "
    "present only as images/reference_sheets/anime_character_creation_asset_sheet.webp at "
    "128x96 px - a browsing preview, per its own index - so a 1254 px facial trait cannot be "
    "reconstructed from it. The family is built from the approved base master's own painted "
    "face instead, and the sheet-cell reference is dropped from the filenames rather than "
    "claiming a source the asset does not have."
)

FAMILY_NOTES = {
    "eyes": (
        "The master's eye pair, separated from the skin it is painted on, with the iris "
        "remapped through a three-stop ramp. Lash line, sclera and the shared upper-left "
        "catchlight are the master's own, so the pair stays on-model and on-rig; only the "
        "iris body changes colour, and the ramp keeps the pupil dark and the rim light where "
        "the painting put them. A feathered skin patch beneath the art covers the baked eyes "
        "across every registered base."
    ),
    "eyebrows": (
        "The master's brow pair, remapped per column: how high it sits, how far the inner end "
        "lifts or falls, how much of the painted arch is kept and how heavy the line is. The "
        "transform runs on the brow's difference from the skin behind it, not on its separated "
        "alpha and colour, which is what keeps a moved brow from carrying a halo. A feathered "
        "skin patch beneath the art covers the baked brows across every registered base."
    ),
    "mouths": (
        "Drawn with soft round brushes in the master's own mouth-line colour, calibrated to the "
        "painted mouth: X 605-650, dropping 7 px from end to centre. mouth_001 is that painted "
        "mouth itself rather than a redrawing of it. A feathered skin patch beneath the art "
        "covers the baked mouth across every registered base."
    ),
    "expression_marks": (
        "Drawn accents on the cheeks. They carry no skin patch, being additive overlays on skin "
        "that is already there. They sit below the eye line because the face narrows fast under "
        "the eyes, and off the forehead because hair_front renders above them."
    ),
}

EYES = [
    ("DG-055", "eyes_001_dark_neutral", "Dark neutral iris"),
    ("DG-056", "eyes_002_dark_umber", "Dark umber iris"),
    ("DG-057", "eyes_003_dark_slate", "Dark slate iris"),
    ("DG-058", "eyes_004_deep_olive", "Deep olive iris"),
    ("DG-059", "eyes_005_deep_blue", "Deep blue iris"),
    ("DG-060", "eyes_006_violet", "Violet iris"),
    ("DG-061", "eyes_007_near_black", "Near-black iris"),
    ("DG-062", "eyes_008_dark_brown", "Dark brown iris"),
    ("DG-063", "eyes_009_gold", "Gold iris"),
    ("DG-064", "eyes_010_yellow_green", "Yellow-green iris"),
    ("DG-065", "eyes_011_cyan", "Cyan iris"),
    ("DG-066", "eyes_012_emerald", "Emerald iris"),
    ("DG-067", "eyes_013_crimson", "Crimson iris"),
    ("DG-068", "eyes_014_magenta", "Magenta iris"),
    ("DG-069", "eyes_015_charcoal", "Charcoal iris"),
    ("DG-070", "eyes_016_black", "Black iris"),
    ("DG-071", "eyes_017_warm_neutral", "Warm neutral iris"),
    ("DG-072", "eyes_018_gray", "Gray iris"),
    ("DG-073", "eyes_019_rose", "Rose iris"),
    ("DG-074", "eyes_020_pink", "Pink iris"),
    ("DG-075", "eyes_021_amber", "Amber iris"),
    ("DG-076", "eyes_022_orange_gold", "Orange-gold iris"),
    ("DG-077", "eyes_023_cool_charcoal", "Cool charcoal iris"),
    ("DG-078", "eyes_024_blue_black", "Blue-black iris"),
]

EYEBROWS = [
    ("DG-079", "eyebrows_001_neutral", "Neutral brow pair, as painted"),
    ("DG-080", "eyebrows_002_raised", "Raised brow pair"),
    ("DG-081", "eyebrows_003_lowered", "Lowered brow pair"),
    ("DG-082", "eyebrows_004_angry", "Angry brow pair, inner ends down"),
    ("DG-083", "eyebrows_005_furious", "Furious brow pair, driven down and in"),
    ("DG-084", "eyebrows_006_worried", "Worried brow pair, inner ends up"),
    ("DG-085", "eyebrows_007_pleading", "Pleading brow pair, inner ends high"),
    ("DG-086", "eyebrows_008_arched", "Arched brow pair"),
    ("DG-087", "eyebrows_009_flat", "Flat brow pair"),
    ("DG-088", "eyebrows_010_thin", "Thin brow pair"),
    ("DG-089", "eyebrows_011_thick", "Thick brow pair"),
    ("DG-090", "eyebrows_012_bold_raised", "Bold raised brow pair"),
    ("DG-091", "eyebrows_013_fine_arched", "Fine arched brow pair"),
    ("DG-092", "eyebrows_014_wide_set", "Wide-set brow pair"),
    ("DG-093", "eyebrows_015_close_set", "Close-set brow pair"),
    ("DG-094", "eyebrows_016_quizzical", "Quizzical brow pair, one raised"),
]

MOUTHS = [
    ("DG-095", "mouth_001_closed_neutral", "Fine closed neutral mouth, the master's own"),
    ("DG-096", "mouth_002_small_open_smile", "Small open smile with tongue"),
    ("DG-097", "mouth_003_small_dark_open", "Small dark open mouth with upper teeth"),
    ("DG-098", "mouth_004_wide_open_smile", "Wide open smile"),
    ("DG-099", "mouth_005_short_line", "Fine short mouth line"),
    ("DG-100", "mouth_006_soft_curve", "Small soft curved smile"),
    ("DG-101", "mouth_007_flat_line", "Fine flat line"),
    ("DG-102", "mouth_008_small_downturned", "Small downturned open mouth"),
    ("DG-103", "mouth_009_tiny_neutral", "Tiny neutral mark"),
    ("DG-104", "mouth_010_tiny_curve", "Tiny curved mark"),
    ("DG-105", "mouth_011_pink_open_pout", "Open pout with tongue"),
    ("DG-106", "mouth_012_tiny_round", "Tiny dark round mouth"),
]

MARKS = [
    ("DG-107", "expression_mark_001_pink_blush_strokes", "Pink blush strokes on both cheeks"),
    ("DG-108", "expression_mark_002_yellow_stress_marks", "Yellow stress marks"),
    ("DG-109", "expression_mark_003_dark_gloom_lines", "Dark gloom lines under both eyes"),
    ("DG-110", "expression_mark_004_gold_sparkle", "Gold sparkle cluster"),
    ("DG-111", "expression_mark_005_cyan_sweat_drop", "Cyan sweat drop"),
    ("DG-112", "expression_mark_006_pink_anger_cross", "Pink anger vein mark"),
    ("DG-113", "expression_mark_007_yellow_green_emphasis", "Yellow-green square emphasis mark"),
    ("DG-114", "expression_mark_008_pink_curved_mark", "Pink curved surprise mark"),
]

FAMILIES = [
    ("eyes", EYES, "prompts/06_eyes_eyebrows_mouths.md"),
    ("eyebrows", EYEBROWS, "prompts/06_eyes_eyebrows_mouths.md"),
    ("mouths", MOUTHS, "prompts/06_eyes_eyebrows_mouths.md"),
    ("expression_marks", MARKS, "prompts/07_expression_marks.md"),
]

AURA = ("DG-145", "aura_front_001_orange_rising_flame", "Orange rising foreground flame")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_facts(path: Path) -> tuple[list[int], str, str, list[int]]:
    with Image.open(path) as image:
        image.load()
        box = image.convert("RGBA").getchannel("A").getbbox()
        return list(image.size), image.mode, image.format or "PNG", [box[0], box[1], box[2] - 1, box[3] - 1]


def face_entry(category: str, backlog_id: str, name: str, trait: str, path: Path) -> dict[str, Any]:
    dimensions, mode, fmt, bounds = image_facts(path)
    return {
        "id": "_".join(name.split("_")[:2]) if category != "expression_marks"
              else "_".join(name.split("_")[:3]),
        "category": category,
        "path": f"assets/{category}/{name}.png",
        "status": "production_ready",
        "sha256": sha256_file(path),
        "dimensions": dimensions,
        "format": fmt,
        "mode": mode,
        "backlog_id": backlog_id,
        "provenance": {
            "origin": "approved_master_face_derivation",
            "reference_path": "assets/base_bodies/base_body_001_neutral_master.png",
            "trait": trait,
            "native_dimensions": [1254, 1254],
            "build_script": "scripts/build_face_traits.py",
            "separation_script": "scripts/extract_face_features.py",
            "output_bounds": bounds,
            "family_method": FAMILY_NOTES[category],
            "naming_note": NAME_NOTE,
        },
        "approved_on": APPROVED_ON,
        "qa_report": QA_REPORT,
    }


def aura_entry(path: Path) -> dict[str, Any]:
    dimensions, mode, fmt, bounds = image_facts(path)
    backlog_id, name, trait = AURA
    return {
        "id": "aura_front_001",
        "category": "front_auras",
        "path": f"assets/front_auras/{name}.png",
        "status": "production_ready",
        "sha256": sha256_file(path),
        "dimensions": dimensions,
        "format": fmt,
        "mode": mode,
        "backlog_id": backlog_id,
        "provenance": {
            "origin": "procedural_effect_render",
            "reference_path": "assets/base_bodies/base_body_001_neutral_master.png",
            "trait": trait,
            "native_dimensions": [1254, 1254],
            "build_script": "scripts/build_front_aura_flame.py",
            "output_bounds": bounds,
            "replaces": "the flat-shaded aura_front_001 placeholder deregistered on 2026-09-09",
            "method": (
                "Four octaves of fractal value noise, advected upward and used both to modulate "
                "six tongue envelopes and to carve them into separate licks by a threshold that "
                "rises with height. Intensity is compressed rather than clipped, so no lick's "
                "core lands on a single flat value, and colour is compressed on a longer scale "
                "than opacity so the body reads orange and only the hottest cores reach pale "
                "gold. Nothing is drawn above Y 582, below the shoulder line, so the flame never "
                "crosses the face."
            ),
            "flatness_measurements": {
                "note": (
                    "Calibrated against the two front auras the collection already had. The "
                    "accepted aura_front_002 measures 83 alpha levels, a 0.067 top-value share "
                    "and a 0.219 flat-neighbourhood share; the rejected placeholder measures 28, "
                    "0.334 and 0.883."
                ),
            },
        },
        "approved_on": APPROVED_ON,
        "qa_report": AURA_QA_REPORT,
    }


def register(built: Path, aura: Path) -> list[dict[str, Any]]:
    entries = []
    for category, rows, _prompt in FAMILIES:
        destination_dir = ROOT / "assets" / category
        destination_dir.mkdir(parents=True, exist_ok=True)
        for backlog_id, name, trait in rows:
            source = built / category / f"{name}.png"
            if not source.exists():
                raise SystemExit(f"missing built asset: {source}")
            destination = destination_dir / f"{name}.png"
            shutil.copyfile(source, destination)
            if sha256_file(destination) != sha256_file(source):
                raise SystemExit(f"copy mismatch: {name}")
            entries.append(face_entry(category, backlog_id, name, trait, destination))

    destination = ROOT / "assets" / "front_auras" / f"{AURA[1]}.png"
    shutil.copyfile(aura, destination)
    entries.append(aura_entry(destination))
    return entries


def update_manifest(entries: list[dict[str, Any]]) -> None:
    path = ROOT / "assets" / "asset_manifest.json"
    manifest = json.loads(path.read_text())
    known = {entry["path"] for entry in manifest["registered_production_assets"]}
    for entry in entries:
        if entry["path"] in known:
            raise SystemExit(f"already registered: {entry['path']}")
    manifest["registered_production_assets"].extend(entries)
    manifest["pending_categories"] = [
        category for category in manifest.get("pending_categories", [])
        if category not in {"eyes", "eyebrows", "mouths", "expression_marks", "front_auras"}
    ]
    manifest["blocked_assets"] = [
        blocked for blocked in manifest.get("blocked_assets", [])
        if blocked.get("id") != "aura_front_001"
    ]
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_collection() -> None:
    path = ROOT / "config" / "collection.json"
    collection = json.loads(path.read_text())
    collection.setdefault("optional_categories", {}).update(OPTIONAL_RATES)
    path.write_text(json.dumps(collection, indent=2) + "\n", encoding="utf-8")


def update_backlog() -> None:
    """Rewrite each facial row's description, path and status in place."""
    path = ROOT / "docs" / "trait-production-backlog.md"
    rows: dict[str, tuple[str, str, str]] = {}
    for category, family, prompt in FAMILIES:
        for backlog_id, name, trait in family:
            rows[backlog_id] = (trait, f"`assets/{category}/{name}.png`", f"`{prompt}`")
    rows[AURA[0]] = (AURA[2], f"`assets/front_auras/{AURA[1]}.png`",
                     "procedural — `scripts/build_front_aura_flame.py`")

    lines = path.read_text().splitlines(keepends=True)
    changed = 0
    for index, line in enumerate(lines):
        if not line.startswith("| DG-"):
            continue
        cells = line.rstrip("\n").split("|")
        backlog_id = cells[1].strip()
        if backlog_id not in rows:
            continue
        trait, asset_path, prompt = rows[backlog_id]
        cells[3] = f" {trait} "
        cells[6] = f" {asset_path} "
        cells[7] = f" {prompt} "
        cells[8] = " registered "
        lines[index] = "|".join(cells) + "\n"
        changed += 1
    if changed != len(rows):
        raise SystemExit(f"updated {changed} backlog rows, expected {len(rows)}")
    path.write_text("".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--built", type=Path, default=Path("incoming/face_traits_2026-09-09"))
    parser.add_argument("--aura", type=Path,
                        default=Path("incoming/front_auras/aura_front_001_orange_rising_flame.png"))
    args = parser.parse_args(argv)
    built = args.built if args.built.is_absolute() else ROOT / args.built
    aura = args.aura if args.aura.is_absolute() else ROOT / args.aura

    entries = register(built, aura)
    update_manifest(entries)
    update_collection()
    update_backlog()
    print(f"registered {len(entries)} assets")
    for entry in entries:
        print(f"  {entry['id']:32s} {entry['sha256'][:12]}  {entry['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
