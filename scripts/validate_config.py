#!/usr/bin/env python3
"""Validate locked collection configuration and compatibility-rule integrity."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    from scripts import validate_assets
except ImportError:  # Direct execution from scripts/.
    import validate_assets  # type: ignore[no-redef]

LOCKED_COLLECTION: dict[str, Any] = {
    "name": "Demigods",
    "symbol": "DEMIGODS",
    "supply": 777,
    "token_id_start": 1,
    "token_id_padding": 4,
    "canvas": {
        "width": 1254,
        "height": 1254,
        "color_space": "sRGB",
    },
    "master_rig": {
        "canvas_center_x": 627,
        "top_of_head_y": 141,
        "head_center": [627, 343],
        "eye_line_y": 367,
        "mouth_center": [627, 441],
        "shoulder_line_y": 569,
        "waist_center": [627, 808],
        "viewer_left_hand_anchor": [404, 772],
        "viewer_right_hand_anchor": [850, 772],
        "foot_baseline_y": 1139,
        "maximum_character_bounds": [233, 129, 1021, 1139],
    },
    "lighting": {
        "key_direction": "upper-left",
        "shadow_direction": "lower-right",
        "rim_light": "subtle cool right rim",
        "ambient_fill": "soft neutral",
    },
}


@dataclass
class ConfigValidationResult:
    collection_path: str
    compatibility_path: str
    passed: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    available_traits: int = 0
    requires_rules: int = 0
    excludes_rules: int = 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value must be an object: {path}")
    return value


def compare_locked_value(
    actual: Any,
    expected: Any,
    path: str,
    errors: list[str],
) -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            errors.append(f"{path} must be an object")
            return
        for key, expected_value in expected.items():
            compare_locked_value(
                actual.get(key),
                expected_value,
                f"{path}.{key}" if path else key,
                errors,
            )
        return

    if actual != expected:
        errors.append(f"{path} is {actual!r}; locked value is {expected!r}")


def validate_collection(collection: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    compare_locked_value(collection, LOCKED_COLLECTION, "", errors)

    description = collection.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description must be a non-empty string")

    allowed_top_level = {
        "name",
        "symbol",
        "description",
        "supply",
        "token_id_start",
        "token_id_padding",
        "canvas",
        "master_rig",
        "lighting",
    }
    extras = sorted(set(collection) - allowed_top_level)
    if extras:
        warnings.append(f"unrecognized collection keys: {', '.join(extras)}")

    return errors, warnings


def discover_trait_inventory(assets_root: Path) -> dict[str, str]:
    inventory: dict[str, str] = {}
    for category in validate_assets.PRODUCTION_CATEGORIES:
        folder = assets_root / category
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if path.is_file() and path.suffix == ".png":
                inventory[path.name] = category
    return inventory


def normalize_targets(value: Any, label: str, errors: list[str]) -> list[str]:
    if isinstance(value, str):
        targets = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        targets = list(value)
    else:
        errors.append(f"{label} must be a filename string or an array of filename strings")
        return []

    if not targets:
        errors.append(f"{label} must not be empty")
    if len(targets) != len(set(targets)):
        errors.append(f"{label} contains duplicate filenames")
    return targets


def validate_trait_name(
    name: Any,
    label: str,
    inventory: dict[str, str],
    errors: list[str],
) -> str | None:
    if not isinstance(name, str):
        errors.append(f"{label} must be a filename string")
        return None
    if not validate_assets.SNAKE_CASE_PNG.fullmatch(name):
        errors.append(f"{label} must be a lowercase snake_case PNG filename: {name!r}")
    if not validate_assets.NUMBERED_NAME.fullmatch(name):
        errors.append(f"{label} must include a three-digit sequence and description: {name!r}")
    if validate_assets.classify_filename(name) is None:
        errors.append(f"{label} has an unrecognized asset prefix: {name!r}")
    if name not in inventory:
        errors.append(f"{label} references a missing production trait: {name}")
    return name


def validate_compatibility(
    compatibility: dict[str, Any],
    inventory: dict[str, str],
) -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    warnings: list[str] = []

    version = compatibility.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append("compatibility version must be an integer greater than or equal to 1")

    notes = compatibility.get("notes", [])
    if not isinstance(notes, list) or not all(isinstance(note, str) for note in notes):
        errors.append("compatibility notes must be an array of strings")

    requires = compatibility.get("requires")
    excludes = compatibility.get("excludes")
    if not isinstance(requires, list):
        errors.append("requires must be an array")
        requires = []
    if not isinstance(excludes, list):
        errors.append("excludes must be an array")
        excludes = []

    required_pairs: set[tuple[str, str]] = set()
    excluded_pairs: set[frozenset[str]] = set()

    for index, rule in enumerate(requires):
        label = f"requires[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{label} must be an object")
            continue
        extra_keys = sorted(set(rule) - {"trait", "requires", "reason"})
        if extra_keys:
            warnings.append(f"{label} has unrecognized keys: {', '.join(extra_keys)}")
        trait = validate_trait_name(rule.get("trait"), f"{label}.trait", inventory, errors)
        targets = normalize_targets(rule.get("requires"), f"{label}.requires", errors)
        for target_value in targets:
            target = validate_trait_name(
                target_value,
                f"{label}.requires",
                inventory,
                errors,
            )
            if trait is None or target is None:
                continue
            if trait == target:
                errors.append(f"{label} cannot require itself: {trait}")
                continue
            pair = (trait, target)
            if pair in required_pairs:
                errors.append(f"duplicate requires relationship: {trait} -> {target}")
            required_pairs.add(pair)
            if inventory.get(trait) == inventory.get(target):
                errors.append(
                    f"impossible same-category requirement: {trait} -> {target} "
                    f"({inventory.get(trait)})"
                )

    for index, rule in enumerate(excludes):
        label = f"excludes[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{label} must be an object")
            continue
        extra_keys = sorted(set(rule) - {"trait", "excludes", "reason"})
        if extra_keys:
            warnings.append(f"{label} has unrecognized keys: {', '.join(extra_keys)}")
        trait = validate_trait_name(rule.get("trait"), f"{label}.trait", inventory, errors)
        targets = normalize_targets(rule.get("excludes"), f"{label}.excludes", errors)
        for target_value in targets:
            target = validate_trait_name(
                target_value,
                f"{label}.excludes",
                inventory,
                errors,
            )
            if trait is None or target is None:
                continue
            if trait == target:
                errors.append(f"{label} cannot exclude itself: {trait}")
                continue
            pair = frozenset((trait, target))
            if pair in excluded_pairs:
                errors.append(f"duplicate exclusion relationship: {trait} x {target}")
            excluded_pairs.add(pair)
            if inventory.get(trait) == inventory.get(target):
                warnings.append(
                    f"redundant same-category exclusion: {trait} x {target} "
                    f"({inventory.get(trait)})"
                )

    for trait, required in sorted(required_pairs):
        if frozenset((trait, required)) in excluded_pairs:
            errors.append(
                f"contradictory compatibility rules: {trait} requires and excludes {required}"
            )

    reverse_requirements = {(target, trait) for trait, target in required_pairs}
    circular = sorted(required_pairs.intersection(reverse_requirements))
    for trait, required in circular:
        if trait < required:
            warnings.append(f"mutual requirement detected: {trait} <-> {required}")

    allowed_top_level = {"version", "requires", "excludes", "notes"}
    extras = sorted(set(compatibility) - allowed_top_level)
    if extras:
        warnings.append(f"unrecognized compatibility keys: {', '.join(extras)}")

    return errors, warnings, len(requires), len(excludes)


def validate_configuration(
    collection_path: Path,
    compatibility_path: Path,
    assets_root: Path,
) -> ConfigValidationResult:
    result = ConfigValidationResult(
        collection_path=str(collection_path),
        compatibility_path=str(compatibility_path),
    )
    try:
        collection = load_json(collection_path)
        compatibility = load_json(compatibility_path)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result

    collection_errors, collection_warnings = validate_collection(collection)
    inventory = discover_trait_inventory(assets_root)
    compatibility_errors, compatibility_warnings, requires_count, excludes_count = (
        validate_compatibility(compatibility, inventory)
    )

    result.errors.extend(collection_errors)
    result.errors.extend(compatibility_errors)
    result.warnings.extend(collection_warnings)
    result.warnings.extend(compatibility_warnings)
    result.available_traits = len(inventory)
    result.requires_rules = requires_count
    result.excludes_rules = excludes_count
    result.passed = not result.errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", type=Path, default=Path("config/collection.json"))
    parser.add_argument(
        "--compatibility",
        type=Path,
        default=Path("config/compatibility.json"),
    )
    parser.add_argument("--assets", type=Path, default=Path("assets"))
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args(argv)

    result = validate_configuration(args.collection, args.compatibility, args.assets)
    print(f"{'PASS' if result.passed else 'FAIL'} collection and compatibility configuration")
    for error in result.errors:
        print(f"  - ERROR: {error}")
    for warning in result.warnings:
        print(f"  - WARNING: {warning}")
    print(
        f"Available traits: {result.available_traits}; "
        f"requires rules: {result.requires_rules}; excludes rules: {result.excludes_rules}."
    )

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.json_report}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
