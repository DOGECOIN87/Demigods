#!/usr/bin/env python3
"""Deterministically compose exactly 777 unique Demigods tokens."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

from PIL import Image

LAYER_ORDER = [
    "backgrounds",
    "rear_auras",
    "back_accessories",
    "hair_back",
    "base_bodies",
    "outfits",
    "neck_accessories",
    "eyes",
    "eyebrows",
    "mouths",
    "expression_marks",
    "hair_front",
    "head_accessories",
    "hand_objects",
    "front_auras",
    "global_finish",
]
IMAGE_SUFFIXES = {".png", ".webp", ".jpg", ".jpeg"}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def discover_assets(root: Path) -> dict[str, list[Path]]:
    assets: dict[str, list[Path]] = {}
    for category in LAYER_ORDER:
        folder = root / category
        files = sorted(
            p for p in folder.glob("*")
            if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
        ) if folder.exists() else []
        assets[category] = files
    return assets


def signature(selection: dict[str, Path]) -> str:
    ordered = [f"{category}:{selection[category].name}" for category in LAYER_ORDER if category in selection]
    return "|".join(ordered)


def violates_rules(selection: dict[str, Path], rules: dict[str, Any]) -> bool:
    names = {path.name for path in selection.values()}
    for rule in rules.get("requires", []):
        if rule.get("trait") in names and rule.get("requires") not in names:
            return True
    for rule in rules.get("excludes", []):
        if rule.get("trait") in names and any(item in names for item in rule.get("excludes", [])):
            return True
    return False


def choose_selection(rng: random.Random, assets: dict[str, list[Path]]) -> dict[str, Path]:
    selection: dict[str, Path] = {}
    for category in LAYER_ORDER:
        choices = assets[category]
        if choices:
            selection[category] = rng.choice(choices)
    return selection


def render(selection: dict[str, Path], output_path: Path, size: tuple[int, int]) -> None:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    for category in LAYER_ORDER:
        path = selection.get(category)
        if path is None:
            continue
        with Image.open(path) as source:
            layer = source.convert("RGBA")
            if layer.size != size:
                raise ValueError(f"{path} is {layer.size}; expected {size}")
            canvas = Image.alpha_composite(canvas, layer)
    canvas.save(output_path, "PNG", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets", type=Path, default=Path("assets"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--config", type=Path, default=Path("config/collection.json"))
    parser.add_argument("--compatibility", type=Path, default=Path("config/compatibility.json"))
    parser.add_argument("--seed", default="demigods-production-seed")
    parser.add_argument("--supply", type=int, default=777)
    parser.add_argument("--max-attempts", type=int, default=1_000_000)
    args = parser.parse_args()

    collection = load_json(args.config)
    rules = load_json(args.compatibility)
    width = int(collection.get("canvas", {}).get("width", 2048))
    height = int(collection.get("canvas", {}).get("height", 2048))
    size = (width, height)

    assets = discover_assets(args.assets)
    missing = [category for category, files in assets.items() if not files and category in {"backgrounds", "base_bodies"}]
    if missing:
        print(f"Missing required categories: {', '.join(missing)}", file=sys.stderr)
        return 2

    rng = random.Random(args.seed)
    args.output.mkdir(parents=True, exist_ok=True)
    images_dir = args.output / "images"
    metadata_dir = args.output / "metadata"
    images_dir.mkdir(exist_ok=True)
    metadata_dir.mkdir(exist_ok=True)

    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    attempts = 0

    while len(records) < args.supply and attempts < args.max_attempts:
        attempts += 1
        selection = choose_selection(rng, assets)
        if violates_rules(selection, rules):
            continue
        raw_signature = signature(selection)
        digest = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)

        token_id = len(records) + 1
        token_label = f"{token_id:04d}"
        image_name = f"{token_label}.png"
        render(selection, images_dir / image_name, size)

        attributes = [
            {
                "trait_type": category,
                "value": path.stem,
                "source_file": path.as_posix(),
            }
            for category, path in selection.items()
        ]
        record = {
            "name": f"Demigods #{token_label}",
            "description": collection.get("description", "Demigods 777 generative collection."),
            "image": image_name,
            "token_id": token_id,
            "attributes": attributes,
            "trait_signature": digest,
        }
        (metadata_dir / f"{token_label}.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8"
        )
        records.append(record)
        print(f"Rendered {token_label}/{args.supply}")

    if len(records) != args.supply:
        print(
            f"Generated only {len(records)} unique valid tokens after {attempts} attempts. "
            "Add more traits or relax compatibility rules.",
            file=sys.stderr,
        )
        return 1

    provenance_input = "".join(record["trait_signature"] for record in records)
    provenance_hash = hashlib.sha256(provenance_input.encode("utf-8")).hexdigest()
    manifest = {
        "collection": collection.get("name", "Demigods"),
        "supply": args.supply,
        "seed": args.seed,
        "attempts": attempts,
        "provenance_hash": provenance_hash,
        "trait_signatures": [record["trait_signature"] for record in records],
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Complete: {args.supply} unique tokens. Provenance: {provenance_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
