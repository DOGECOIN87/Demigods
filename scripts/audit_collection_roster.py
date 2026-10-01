#!/usr/bin/env python3
"""Inventory one-of-one art and validate an explicitly selected 700/77 roster.

This does not promote review art or change the live 770/7 generator config.
Selection and token IDs must be supplied by the owner in a roster JSON file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SIZE = (1254, 1254)
TOTAL = 777
GENERATIVE = 700
ONE_OF_ONE = 77


def inventory(root: Path = ROOT) -> dict[str, list[str]]:
    return {
        "current_variations": sorted(str(p.relative_to(root)) for p in (root / "images/variations/complete_72").glob("*.png")),
        "registered_legendary": sorted(str(p.relative_to(root)) for p in (root / "assets/legendary").glob("*.png")),
        "other_one_of_ones": sorted(str(p.relative_to(root)) for p in (root / "images/one_of_ones").glob("*.png")),
        "historical_webps": sorted(str(p.relative_to(root)) for p in (root / "images/variations/nature").glob("*.webp")),
        "references": sorted(str(p.relative_to(root)) for p in (root / "images/variations/references").glob("*.jpg")),
    }


def validate_roster(roster: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if roster.get("generative_count") != GENERATIVE:
        errors.append(f"generative_count must be {GENERATIVE}")
    entries = roster.get("one_of_ones")
    if not isinstance(entries, list) or len(entries) != ONE_OF_ONE:
        return errors + [f"one_of_ones must contain exactly {ONE_OF_ONE} selections"]
    ids: set[int] = set()
    sources: set[str] = set()
    digests: set[str] = set()
    for n, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"entry {n}: expected an object")
            continue
        token_id, source = entry.get("token_id"), entry.get("source")
        if type(token_id) is not int or not 1 <= token_id <= TOTAL or token_id in ids:
            errors.append(f"entry {n}: token_id must be a unique integer in 1..{TOTAL}")
        else:
            ids.add(token_id)
        if not isinstance(source, str) or not source.endswith(".png"):
            errors.append(f"entry {n}: source must be a repository PNG path")
            continue
        path = (root / source).resolve()
        if root.resolve() not in path.parents or not path.is_file():
            errors.append(f"entry {n}: source is missing or outside the repository: {source}")
            continue
        if source in sources:
            errors.append(f"entry {n}: repeated source: {source}")
        sources.add(source)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in digests:
            errors.append(f"entry {n}: duplicate artwork bytes: {source}")
        digests.add(digest)
        try:
            with Image.open(path) as image:
                image.load()
                if image.format != "PNG" or image.size != SIZE:
                    errors.append(f"entry {n}: expected fully decoded native 1254x1254 PNG: {source}")
        except Exception as exc:  # noqa: BLE001 - report corrupt uploads
            errors.append(f"entry {n}: cannot decode {source}: {exc}")
    if len(ids) == ONE_OF_ONE and TOTAL - len(ids) != GENERATIVE:
        errors.append("reserved IDs do not leave 700 generative IDs")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", type=Path, help="JSON with generative_count and 77 {token_id, source} entries")
    args = parser.parse_args()
    counts = {name: len(paths) for name, paths in inventory().items()}
    print(json.dumps({"target": {"generative": GENERATIVE, "one_of_ones": ONE_OF_ONE}, "inventory": counts}, indent=2))
    if not args.roster:
        print("No final one-of-one selection supplied; live generator remains 770/7.")
        return 0
    errors = validate_roster(json.loads(args.roster.read_text()))
    for error in errors:
        print(f"FAIL {error}")
    if not errors:
        print("PASS: 77 distinct native PNGs and token IDs; 700 IDs remain for generation.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
