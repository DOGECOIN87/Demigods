#!/usr/bin/env python3
"""Deterministically compose exactly 777 unique Demigods tokens."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

try:
    from scripts import validate_assets
except ImportError:  # Direct execution from scripts/.
    import validate_assets  # type: ignore[no-redef]

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
REQUIRED_CATEGORIES = {"backgrounds", "base_bodies"}
PRODUCTION_SUPPLY = 777


@dataclass(frozen=True)
class GeneratedToken:
    token_id: int
    token_label: str
    raw_signature: str
    trait_signature: str
    selection: dict[str, Path]


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"required JSON file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value must be an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_assets(root: Path) -> dict[str, list[Path]]:
    assets: dict[str, list[Path]] = {}
    for category in LAYER_ORDER:
        folder = root / category
        files = (
            sorted(path for path in folder.iterdir() if path.is_file() and path.suffix == ".png")
            if folder.is_dir()
            else []
        )
        assets[category] = files
    return assets


def category_counts(assets: dict[str, list[Path]]) -> dict[str, int]:
    return {category: len(assets.get(category, [])) for category in LAYER_ORDER}


def theoretical_space(assets: dict[str, list[Path]]) -> int:
    counts = [len(files) for files in assets.values() if files]
    return math.prod(counts) if counts else 0


def raw_signature(selection: dict[str, Path]) -> str:
    return "|".join(
        f"{category}:{selection[category].name}"
        for category in LAYER_ORDER
        if category in selection
    )


def signature_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def selected_names(selection: dict[str, Path]) -> set[str]:
    return {path.name for path in selection.values()}


def violates_rules(selection: dict[str, Path], rules: dict[str, Any]) -> bool:
    names = selected_names(selection)

    for rule in rules.get("requires", []):
        if not isinstance(rule, dict):
            continue
        trait = rule.get("trait")
        required = rule.get("requires")
        if trait not in names:
            continue
        required_names = {required} if isinstance(required, str) else set(required or [])
        if required_names and not required_names.issubset(names):
            return True

    for rule in rules.get("excludes", []):
        if not isinstance(rule, dict):
            continue
        trait = rule.get("trait")
        excluded = rule.get("excludes", [])
        excluded_names = {excluded} if isinstance(excluded, str) else set(excluded)
        if trait in names and names.intersection(excluded_names):
            return True

    return False


def choose_selection(rng: random.Random, assets: dict[str, list[Path]]) -> dict[str, Path]:
    return {
        category: rng.choice(assets[category])
        for category in LAYER_ORDER
        if assets.get(category)
    }


def generate_tokens(
    *,
    rng: random.Random,
    assets: dict[str, list[Path]],
    rules: dict[str, Any],
    supply: int,
    max_attempts: int,
) -> tuple[list[GeneratedToken], int]:
    seen: set[str] = set()
    tokens: list[GeneratedToken] = []
    attempts = 0

    while len(tokens) < supply and attempts < max_attempts:
        attempts += 1
        selection = choose_selection(rng, assets)
        if violates_rules(selection, rules):
            continue

        raw = raw_signature(selection)
        digest = signature_digest(raw)
        if digest in seen:
            continue
        seen.add(digest)

        token_id = len(tokens) + 1
        tokens.append(
            GeneratedToken(
                token_id=token_id,
                token_label=f"{token_id:04d}",
                raw_signature=raw,
                trait_signature=digest,
                selection=selection,
            )
        )

    return tokens, attempts


def validate_library(
    assets_root: Path,
    assets: dict[str, list[Path]],
    size: tuple[int, int],
) -> list[str]:
    errors: list[str] = []
    missing = sorted(category for category in REQUIRED_CATEGORIES if not assets.get(category))
    if missing:
        errors.append(f"missing required categories: {', '.join(missing)}")

    for category in LAYER_ORDER:
        folder = assets_root / category
        if not folder.exists():
            continue
        for path in sorted(p for p in folder.iterdir() if p.is_file()):
            if path.suffix != ".png":
                errors.append(f"non-PNG production file: {path.as_posix()}")

    for category, files in assets.items():
        for path in files:
            result = validate_assets.validate_file(path, *size, category=category)
            errors.extend(f"{result.path}: {message}" for message in result.errors)

    return errors


def prepare_output(output: Path, overwrite: bool) -> tuple[Path, Path]:
    if output.exists() and any(output.iterdir()):
        if not overwrite:
            raise ValueError(
                f"output directory is not empty: {output}; use --overwrite to replace generated files"
            )
        shutil.rmtree(output)

    images_dir = output / "images"
    metadata_dir = output / "metadata"
    images_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    return images_dir, metadata_dir


def render(selection: dict[str, Path], output_path: Path, size: tuple[int, int]) -> str:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    for category in LAYER_ORDER:
        path = selection.get(category)
        if path is None:
            continue
        with Image.open(path) as source:
            source.load()
            layer = source.convert("RGBA")
            if layer.size != size:
                raise ValueError(f"{path} is {layer.size}; expected {size}")
            canvas = Image.alpha_composite(canvas, layer)
    canvas.save(output_path, "PNG", optimize=True)
    return sha256_file(output_path)


def metadata_record(
    token: GeneratedToken,
    collection: dict[str, Any],
    assets_root: Path,
    image_sha256: str | None,
) -> dict[str, Any]:
    attributes = [
        {
            "trait_type": category,
            "value": token.selection[category].stem,
            "source_file": token.selection[category].relative_to(assets_root).as_posix(),
        }
        for category in LAYER_ORDER
        if category in token.selection
    ]
    return {
        "name": f"{collection.get('name', 'Demigods')} #{token.token_label}",
        "description": collection.get(
            "description", "A 777-piece modular chibi-fantasy generative collection."
        ),
        "image": f"images/{token.token_label}.png",
        "token_id": token.token_id,
        "attributes": attributes,
        "trait_signature": token.trait_signature,
        "image_sha256": image_sha256,
    }


def collection_provenance(values: list[str]) -> str:
    return hashlib.sha256("".join(values).encode("utf-8")).hexdigest()


def generate_collection(
    *,
    assets_root: Path,
    output: Path,
    collection: dict[str, Any],
    compatibility: dict[str, Any],
    seed: str,
    supply: int,
    max_attempts: int,
    dry_run: bool,
    overwrite: bool,
    config_path: Path | None = None,
    compatibility_path: Path | None = None,
) -> dict[str, Any]:
    width = int(collection.get("canvas", {}).get("width", 1254))
    height = int(collection.get("canvas", {}).get("height", 1254))
    size = (width, height)

    assets = discover_assets(assets_root)
    preflight_errors = validate_library(assets_root, assets, size)
    if preflight_errors:
        raise ValueError("preflight failed:\n- " + "\n- ".join(preflight_errors))

    space = theoretical_space(assets)
    if space < supply:
        raise ValueError(
            f"theoretical combination space is only {space}; at least {supply} are required"
        )

    tokens, attempts = generate_tokens(
        rng=random.Random(seed),
        assets=assets,
        rules=compatibility,
        supply=supply,
        max_attempts=max_attempts,
    )
    if len(tokens) != supply:
        raise ValueError(
            f"generated only {len(tokens)} unique valid signatures after {attempts} attempts; "
            "add traits or revise compatibility rules"
        )

    images_dir, metadata_dir = prepare_output(output, overwrite)
    image_hashes: list[str] = []

    for token in tokens:
        image_hash: str | None = None
        if not dry_run:
            image_hash = render(token.selection, images_dir / f"{token.token_label}.png", size)
            image_hashes.append(image_hash)

        record = metadata_record(token, collection, assets_root, image_hash)
        (metadata_dir / f"{token.token_label}.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8"
        )
        action = "Prepared" if dry_run else "Rendered"
        print(f"{action} {token.token_label}/{supply}")

    trait_signatures = [token.trait_signature for token in tokens]
    manifest = {
        "collection": collection.get("name", "Demigods"),
        "supply": supply,
        "seed": seed,
        "attempts": attempts,
        "max_attempts": max_attempts,
        "dry_run": dry_run,
        "canvas": {"width": width, "height": height},
        "layer_order": LAYER_ORDER,
        "category_counts": category_counts(assets),
        "theoretical_combination_space": space,
        "trait_provenance_hash": collection_provenance(trait_signatures),
        "image_provenance_hash": collection_provenance(image_hashes) if image_hashes else None,
        "config_sha256": sha256_file(config_path) if config_path and config_path.is_file() else None,
        "compatibility_sha256": (
            sha256_file(compatibility_path)
            if compatibility_path and compatibility_path.is_file()
            else None
        ),
        "trait_signatures": trait_signatures,
        "image_hashes": image_hashes,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    metadata_files = sorted(metadata_dir.glob("*.json"))
    image_files = sorted(images_dir.glob("*.png"))
    if len(metadata_files) != supply:
        raise RuntimeError(f"metadata count is {len(metadata_files)}; expected {supply}")
    if not dry_run and len(image_files) != supply:
        raise RuntimeError(f"image count is {len(image_files)}; expected {supply}")
    if len(set(trait_signatures)) != supply:
        raise RuntimeError("duplicate trait signatures detected after generation")

    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=Path("assets"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--config", type=Path, default=Path("config/collection.json"))
    parser.add_argument("--compatibility", type=Path, default=Path("config/compatibility.json"))
    parser.add_argument("--seed", default="demigods-production-seed")
    parser.add_argument("--supply", type=int)
    parser.add_argument("--max-attempts", type=int, default=1_000_000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--allow-nonstandard-supply", action="store_true")
    args = parser.parse_args(argv)

    try:
        collection = load_json(args.config)
        compatibility = load_json(args.compatibility)
        configured_supply = int(collection.get("supply", PRODUCTION_SUPPLY))
        supply = args.supply if args.supply is not None else configured_supply
        if supply != PRODUCTION_SUPPLY and not args.allow_nonstandard_supply:
            raise ValueError(
                f"production supply must equal exactly {PRODUCTION_SUPPLY}; "
                "--allow-nonstandard-supply is reserved for tests"
            )

        width = int(collection.get("canvas", {}).get("width", 1254))
        height = int(collection.get("canvas", {}).get("height", 1254))
        assets = discover_assets(args.assets)
        errors = validate_library(args.assets, assets, (width, height))
        if errors:
            raise ValueError("preflight failed:\n- " + "\n- ".join(errors))
        space = theoretical_space(assets)
        if space < supply:
            raise ValueError(
                f"theoretical combination space is only {space}; at least {supply} are required"
            )
        print(f"Preflight passed. Theoretical combination space: {space}.")
        if args.preflight_only:
            return 0

        manifest = generate_collection(
            assets_root=args.assets,
            output=args.output,
            collection=collection,
            compatibility=compatibility,
            seed=args.seed,
            supply=supply,
            max_attempts=args.max_attempts,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
            config_path=args.config,
            compatibility_path=args.compatibility,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        f"Complete: {manifest['supply']} unique tokens. "
        f"Trait provenance: {manifest['trait_provenance_hash']}"
    )
    if manifest["image_provenance_hash"]:
        print(f"Image provenance: {manifest['image_provenance_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
