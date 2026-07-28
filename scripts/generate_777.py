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


def resolve_optional(
    collection: dict[str, Any],
    override: dict[str, float] | None = None,
) -> dict[str, float]:
    """Return the {category: present-probability} map for optional categories.

    A category listed here is included in a token only with the given probability;
    otherwise it is omitted entirely (the "None" trait real collections rely on).
    The two required categories can never be optional, and probabilities must sit
    strictly between 0 and 1 so both the present and absent branches can occur.
    """
    raw = override if override is not None else collection.get("optional_categories") or {}
    if not isinstance(raw, dict):
        raise ValueError("optional_categories must be an object of {category: probability}")
    resolved: dict[str, float] = {}
    for category, probability in raw.items():
        if category not in LAYER_ORDER:
            raise ValueError(f"optional category is not a known layer: {category!r}")
        if category in REQUIRED_CATEGORIES:
            raise ValueError(f"required category cannot be optional: {category}")
        if not isinstance(probability, (int, float)) or not (0.0 < float(probability) < 1.0):
            raise ValueError(
                f"optional_categories.{category} must be a probability strictly between 0 and 1"
            )
        resolved[category] = float(probability)
    return resolved


def theoretical_space(
    assets: dict[str, list[Path]],
    optional: dict[str, float] | None = None,
) -> int:
    """Distinct-combination ceiling.

    An optional category contributes an extra "absent" branch, so its factor is
    (count + 1) rather than count. Mandatory categories keep their raw count.
    """
    optional = optional or {}
    counts = [
        len(files) + (1 if category in optional else 0)
        for category, files in assets.items()
        if files
    ]
    return math.prod(counts) if counts else 0


def estimate_valid_space(
    assets: dict[str, list[Path]],
    optional: dict[str, float] | None,
    rules: dict[str, Any],
    samples: int = 20000,
    seed: int = 0,
) -> tuple[int, float]:
    """Estimate the combination space that actually survives the rules.

    `theoretical_space` is only a ceiling: it multiplies category counts and
    ignores `requires`/`excludes` completely. That gap is not academic. A single
    "this outfit requires exactly that base pose" rule collapses an
    outfit x pose factor from N*M down to N, so a library of five pose-locked
    outfits and five poses has 5 valid pairs, not 25 — and the ceiling overstates
    the real space fivefold.

    Sampling rather than enumerating keeps this usable: a full trait library runs
    to billions of combinations, which is not enumerable, while the valid
    *fraction* converges quickly.

    Returns (estimated valid combinations, valid fraction).
    """
    optional = optional or {}
    ceiling = theoretical_space(assets, optional)
    if ceiling == 0:
        return (0, 0.0)
    if not rules.get("requires") and not rules.get("excludes"):
        return (ceiling, 1.0)

    rng = random.Random(seed)
    populated = {c: f for c, f in assets.items() if f}
    valid = 0
    for _ in range(samples):
        selection: dict[str, Path] = {}
        for category, files in populated.items():
            if category in optional and rng.random() >= optional[category]:
                continue
            selection[category] = rng.choice(files)
        if not violates_rules(selection, rules):
            valid += 1

    fraction = valid / samples
    return (int(round(ceiling * fraction)), fraction)


def saturation_report(supply: int, valid_space: int, fraction: float, ceiling: int) -> str:
    """Human-readable line about how much of the valid space the supply consumes.

    Minting a supply that approaches the valid space means near-exhaustive
    output: almost every possible character exists, so rarity carries no
    information and tokens differ only in whichever categories still vary.
    """
    lines = [
        f"Theoretical combination space: {ceiling} (ceiling, ignores compatibility rules).",
        f"Rule-valid combination space:  {valid_space} "
        f"({fraction:.1%} of the ceiling survives the rules).",
    ]
    if valid_space > 0:
        saturation = supply / valid_space
        lines.append(f"Supply saturation: {supply}/{valid_space} = {saturation:.1%} of the valid space.")
        if saturation > 0.90:
            lines.append(
                "WARNING: above 90% saturation the collection is effectively exhaustive — "
                "nearly every legal combination is minted, so rarity is meaningless. "
                "Add traits to the constrained categories before minting."
            )
        elif saturation > 0.50:
            lines.append(
                "WARNING: above 50% saturation, rare combinations stop being rare. "
                "Consider adding traits to the most constrained categories."
            )
    return "\n".join(lines)


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


def choose_selection(
    rng: random.Random,
    assets: dict[str, list[Path]],
    optional: dict[str, float] | None = None,
) -> dict[str, Path]:
    """Pick one asset per non-empty category; skip optional categories by probability.

    The rng.random() gate is drawn for every optional category in layer order,
    before the rng.choice, so the sequence stays deterministic for a fixed seed.
    """
    optional = optional or {}
    selection: dict[str, Path] = {}
    for category in LAYER_ORDER:
        files = assets.get(category)
        if not files:
            continue
        probability = optional.get(category)
        if probability is not None and rng.random() >= probability:
            continue
        selection[category] = rng.choice(files)
    return selection


def generate_tokens(
    *,
    rng: random.Random,
    assets: dict[str, list[Path]],
    rules: dict[str, Any],
    supply: int,
    max_attempts: int,
    optional: dict[str, float] | None = None,
) -> tuple[list[GeneratedToken], int]:
    seen: set[str] = set()
    tokens: list[GeneratedToken] = []
    attempts = 0

    while len(tokens) < supply and attempts < max_attempts:
        attempts += 1
        selection = choose_selection(rng, assets, optional)
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
    optional_categories: dict[str, float] | None = None,
) -> dict[str, Any]:
    width = int(collection.get("canvas", {}).get("width", 1254))
    height = int(collection.get("canvas", {}).get("height", 1254))
    size = (width, height)

    optional = resolve_optional(collection, optional_categories)

    assets = discover_assets(assets_root)
    preflight_errors = validate_library(assets_root, assets, size)
    if preflight_errors:
        raise ValueError("preflight failed:\n- " + "\n- ".join(preflight_errors))

    space = theoretical_space(assets, optional)
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
        optional=optional,
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
        "optional_categories": optional,
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
        optional = resolve_optional(collection)
        assets = discover_assets(args.assets)
        errors = validate_library(args.assets, assets, (width, height))
        if errors:
            raise ValueError("preflight failed:\n- " + "\n- ".join(errors))
        space = theoretical_space(assets, optional)
        if space < supply:
            raise ValueError(
                f"theoretical combination space is only {space}; at least {supply} are required"
            )
        optional_note = (
            "Optional: " + ", ".join(f"{c}={p:g}" for c, p in optional.items())
            if optional
            else ""
        )
        valid_space, fraction = estimate_valid_space(assets, optional, compatibility)
        if valid_space < supply:
            raise ValueError(
                f"only about {valid_space} combinations survive the compatibility rules "
                f"(ceiling {space}); at least {supply} are required. Add traits to the "
                "constrained categories or relax a rule."
            )
        print("Preflight passed.")
        print(saturation_report(supply, valid_space, fraction, space))
        if optional_note:
            print(optional_note)
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
