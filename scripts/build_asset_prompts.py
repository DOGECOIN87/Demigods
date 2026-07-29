#!/usr/bin/env python3
"""Emit one fully-resolved generation prompt per pending backlog asset.

`build_trait_prompts.py` produces one template per layer category with
`[SPECIFY ...]` slots the operator fills in by hand. That is the right shape for
exploring a category, but it makes a 20-asset batch 20 rounds of prompt
authoring before any image exists.

This script closes that gap: it reads `docs/trait-production-backlog.md`, pulls
each asset's own visual description, source reference cell, and canonical output
filename, and substitutes them into the category template. The result is a
copy-paste-ready prompt per backlog ID with nothing left to fill in.

Usage:
    python scripts/build_asset_prompts.py --batch hair-first
    python scripts/build_asset_prompts.py --ids DG-029 DG-030
    python scripts/build_asset_prompts.py --category "hair back"
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:  # imported as `scripts.build_asset_prompts` by the tests
    from scripts.build_trait_prompts import AVOID, CATS, GATES, header
except ImportError:  # run directly as a script
    from build_trait_prompts import AVOID, CATS, GATES, header  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"

# Backlog category label -> canonical layer number in the locked stack.
CATEGORY_LAYER = {
    "rear aura": 2,
    "back accessory": 3,
    "hair back": 4,
    "outfit": 6,
    "neck accessory": 7,
    "eyes": 8,
    "eyebrows": 9,
    "mouth": 10,
    "expression mark": 11,
    "hair front": 12,
    "head accessory": 13,
    "hand object": 14,
    "front aura": 15,
}

# Named batches. "hair-first" is the minimum set that removes the two visually
# obvious gaps in the current library: bald tokens and a single repeated outfit.
BATCHES = {
    "hair-first": ["hair back", "hair front", "outfit"],
    "faces": ["eyes", "eyebrows", "mouth", "expression mark"],
    "accessories": ["neck accessory", "head accessory", "hand object"],
    "effects": ["rear aura", "front aura", "back accessory"],
}

# Categories whose members are distinct designs per reference cell rather than
# one design in several colours. Recolouring a registered sibling is rejected.
NO_RECOLOUR = {
    "hair back": (
        "The eight upper-row HAIR cells are DISTINCT CUTS, not one design in eight colours "
        "(measured ink heights span 20-27 px across the row, a 29% spread). Render THIS cell's "
        "own silhouette, length, layering, and volume. Do not recolour a sibling hair asset."
    ),
    "hair front": (
        "The eight lower-row HAIR cells are DISTINCT bang shapes, not one design recoloured. "
        "Render THIS cell's own parting, bang edge, and strand layout."
    ),
    "outfit": (
        "Each OUTFIT cell is a distinct cut. Recolours of one cut do not count as new outfits "
        "(prompts/08_outfits.md). Render THIS cell's own garment construction."
    ),
}


def parse_source_keys(text: str) -> dict[str, str]:
    """Read the backlog's `Source keys` table into {key: repository path}."""
    keys: dict[str, str] = {}
    in_table = False
    for line in text.splitlines():
        if line.startswith("| Key |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
            if len(cells) >= 2 and not set(cells[0]) <= set("- "):
                keys[cells[0]] = cells[1]
    return keys


def parse_backlog(text: str) -> list[dict[str, str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("| DG-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        rows.append({
            "id": cells[0],
            "category": cells[1],
            "description": cells[2],
            "reference": cells[3],
            "dependency": cells[4],
            "path": cells[5].strip("`"),
            "prompt": cells[6].strip("`"),
            "status": cells[7].replace("*", "").strip(),
        })
    return rows


def gate_flags(row: dict[str, str]) -> str:
    """The runnable rig-gate flags for one asset.

    `GATES` is written for the per-category templates, where layer 02 carries
    prose — "--floor-aura for ground-plane rings; --trait for body-centred
    glows" — because the correct mode genuinely differs per asset. A ground-plane
    ring is seated on the foot baseline so the character stands inside it, which
    puts its near arc below Y 1139 and fails `--trait` by design; a body-centred
    glow has no such exemption. A per-asset prompt has to print one runnable
    command, so resolve that choice from the asset's own description.
    """
    layer = CATEGORY_LAYER[row["category"]]
    if layer == 2:
        return "--floor-aura" if "ring" in row["description"].lower() else "--trait"
    flags, _ = GATES[layer]
    return flags


def resolve_reference(reference: str, keys: dict[str, str]) -> tuple[str, str]:
    """Split a backlog reference cell into (sheet path, cell locator)."""
    match = re.match(r"`([A-Z]+)`,?\s*(.*)", reference)
    if not match:
        return ("", reference)
    key, cell = match.groups()
    return (keys.get(key, key), cell.strip())


def build_prompt(row: dict[str, str], keys: dict[str, str]) -> str:
    layer = CATEGORY_LAYER[row["category"]]
    spec = next(c for c in CATS if c[0] == layer)
    _, title, attach, _target, bullets, exclude, _fname = spec
    _, proportion = GATES[layer]
    gate_cmd = gate_flags(row)
    sheet, cell = resolve_reference(row["reference"], keys)
    filename = Path(row["path"]).name

    # Drop the template's own [SPECIFY]/[COLOR] placeholder bullets; this
    # asset's description and reference cell supply that detail concretely.
    concrete = [b for b in bullets if "[SPECIFY" not in b and "[COLOR]" not in b]

    body = header(title, attach)
    # header() already embeds the base ATTACH line; append the reference sheet.
    if sheet:
        body = body.replace(
            f"ATTACH: {attach}",
            f"ATTACH: {attach}\nATTACH ALSO: {sheet}\n\nDESIGN REFERENCE CELL: {cell}\n"
            "Use that cell ONLY as a design reference for shape, cut, and palette. Render a fresh "
            "native 1254 x 1254 asset from it. Never enlarge, upscale, crop, or trace the compressed "
            "cell pixels into the output.",
        )

    parts = [
        body,
        f"\n\nTARGET:\n{row['description']}.",
        "\n".join(f"- {b}" for b in concrete),
    ]
    if row["category"] in NO_RECOLOUR:
        parts.append(f"\nDISTINCT DESIGN: {NO_RECOLOUR[row['category']]}")
    parts += [
        f"\nPROPORTION: {proportion}.",
        f"\nISOLATION: the final asset contains ONLY the {title}; exclude {exclude}.",
        f"\nOUTPUT: one transparent 1254 x 1254 PNG. filename: {filename}",
        f"\nAVOID:\n{AVOID}.",
        "\nReturn one transparent PNG only. No text or alternate versions.",
    ]
    prompt = "\n".join(parts)

    return (
        f"### {row['id']} — {row['description']}\n\n"
        f"- Category: `{row['category']}` (layer {layer:02d})\n"
        f"- Output path: `{row['path']}`\n"
        f"- Reference: `{sheet}` — {cell}\n"
        f"- Gate: `python scripts/rig_gate_report.py {gate_cmd} {row['path']}`\n\n"
        f"```\n{prompt}\n```\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--batch", choices=sorted(BATCHES))
    group.add_argument("--ids", nargs="+")
    group.add_argument("--category", action="append")
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--include-registered",
        action="store_true",
        help="also emit prompts for assets already registered (default: pending only)",
    )
    args = parser.parse_args(argv)

    text = BACKLOG.read_text()
    keys = parse_source_keys(text)
    rows = parse_backlog(text)

    if args.batch:
        wanted_categories = BATCHES[args.batch]
        selected = [r for r in rows if r["category"] in wanted_categories]
        label = args.batch
    elif args.category:
        selected = [r for r in rows if r["category"] in args.category]
        label = "-".join(args.category).replace(" ", "_")
    else:
        wanted = {i.upper() for i in args.ids}
        selected = [r for r in rows if r["id"] in wanted]
        label = "selected"
        missing = wanted - {r["id"] for r in selected}
        if missing:
            print(f"error: unknown backlog IDs: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1

    if not args.include_registered:
        selected = [r for r in selected if r["status"] == "pending"]

    unsupported = [r for r in selected if r["category"] not in CATEGORY_LAYER]
    if unsupported:
        print(
            "error: no category template for: "
            + ", ".join(sorted({r["category"] for r in unsupported})),
            file=sys.stderr,
        )
        return 1

    if not selected:
        print("No pending assets matched the selection; nothing to write.", file=sys.stderr)
        return 1

    out_path = args.out or ROOT / "prompts" / f"batch_{label}.md"
    lines = [
        f"# DEMIGODS — resolved generation prompts ({label})",
        "",
        f"{len(selected)} fully-resolved prompts, one per pending backlog asset, in registration "
        "order. Nothing is left to fill in: each prompt carries its own visual description, source "
        "reference cell, and canonical output filename.",
        "",
        "Generated by `python scripts/build_asset_prompts.py`. Do not edit by hand — regenerate.",
        "",
        "## Operator loop",
        "",
        "1. Paste one prompt into the image model with the listed attachments.",
        "2. Save the returned PNG into `incoming/` under its canonical filename.",
        "3. When the batch is done, run `python scripts/bulk_intake.py incoming/` to QA everything "
        "and render a single review sheet.",
        "4. Approve on the sheet, then register with "
        "`python scripts/bulk_intake.py incoming/ --register-approved <ids>`.",
        "",
        "## Progress",
        "",
    ]
    lines += [f"- [ ] {r['id']} — {r['description']}" for r in selected]
    lines += ["", "---", ""]
    lines += [build_prompt(r, keys) for r in selected]

    out_path.write_text("\n".join(lines))
    print(f"Wrote {out_path.relative_to(ROOT)} with {len(selected)} resolved prompt(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
