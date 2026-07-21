#!/usr/bin/env python3
"""Verify registered Demigods production assets against manifest provenance."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    from scripts import validate_assets
except ImportError:  # Direct execution from scripts/.
    import validate_assets  # type: ignore[no-redef]


REGISTERED_STATUS = "production_ready"
SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")


@dataclass
class RegisteredAssetResult:
    id: str | None
    category: str | None
    path: str | None
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    declared_sha256: str | None = None
    actual_sha256: str | None = None
    declared_dimensions: list[int] | None = None
    actual_dimensions: list[int] | None = None


@dataclass
class ManifestConsistencyResult:
    manifest: str
    passed: bool
    checked: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    assets: list[RegisteredAssetResult] = field(default_factory=list)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError(f"manifest top-level value must be an object: {path}")
    return value


def locked_canvas(manifest: dict[str, Any], errors: list[str]) -> tuple[int, int] | None:
    canvas = manifest.get("master_canvas")
    if not isinstance(canvas, dict):
        errors.append("manifest master_canvas must be an object")
        return None

    width = canvas.get("width")
    height = canvas.get("height")
    if not isinstance(width, int) or not isinstance(height, int):
        errors.append("manifest master_canvas dimensions must be integers")
        return None

    if (width, height) != validate_assets.CANVAS_SIZE:
        errors.append(
            "manifest master_canvas must remain locked at "
            f"{validate_assets.CANVAS_SIZE[0]} × {validate_assets.CANVAS_SIZE[1]}"
        )
        return None
    return width, height


def is_safe_repository_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_registered_asset(
    entry: Any,
    *,
    repository_root: Path,
    expected_dimensions: tuple[int, int],
    seen_ids: set[str],
    seen_paths: set[str],
) -> RegisteredAssetResult:
    if not isinstance(entry, dict):
        return RegisteredAssetResult(
            id=None,
            category=None,
            path=None,
            passed=False,
            errors=["registered_production_assets entries must be objects"],
        )

    asset_id = entry.get("id")
    category = entry.get("category")
    asset_path = entry.get("path")
    result = RegisteredAssetResult(
        id=asset_id if isinstance(asset_id, str) else None,
        category=category if isinstance(category, str) else None,
        path=asset_path if isinstance(asset_path, str) else None,
        passed=False,
    )
    errors = result.errors

    if not isinstance(asset_id, str) or not asset_id.strip():
        errors.append("registered asset is missing a non-empty string id")
    elif asset_id in seen_ids:
        errors.append(f"duplicate registered asset id: {asset_id}")
    else:
        seen_ids.add(asset_id)

    if category not in validate_assets.PRODUCTION_CATEGORIES:
        errors.append(f"registered asset category is not recognized: {category!r}")

    if not isinstance(asset_path, str) or not asset_path:
        errors.append("registered asset is missing a non-empty string path")
        resolved_path: Path | None = None
    elif not is_safe_repository_path(asset_path):
        errors.append(f"registered asset path must be repository-relative without traversal: {asset_path}")
        resolved_path = None
    else:
        normalized_path = Path(asset_path).as_posix()
        if normalized_path in seen_paths:
            errors.append(f"duplicate registered asset path: {normalized_path}")
        else:
            seen_paths.add(normalized_path)

        if not normalized_path.endswith(".png"):
            errors.append("registered production asset path must end in .png")
        if isinstance(category, str) and category in validate_assets.PRODUCTION_CATEGORIES:
            expected_prefix = f"assets/{category}/"
            if not normalized_path.startswith(expected_prefix):
                errors.append(
                    f"registered asset path must be under {expected_prefix}: {normalized_path}"
                )
        resolved_path = repository_root / Path(asset_path)

    status = entry.get("status")
    if status != REGISTERED_STATUS:
        errors.append(
            f"registered asset status must be {REGISTERED_STATUS!r}; found {status!r}"
        )

    declared_sha256 = entry.get("sha256")
    result.declared_sha256 = declared_sha256 if isinstance(declared_sha256, str) else None
    if not isinstance(declared_sha256, str) or not SHA256_PATTERN.fullmatch(declared_sha256):
        errors.append("registered asset sha256 must be a lowercase 64-character hexadecimal digest")

    declared_dimensions = entry.get("dimensions")
    if (
        not isinstance(declared_dimensions, list)
        or len(declared_dimensions) != 2
        or not all(isinstance(value, int) for value in declared_dimensions)
    ):
        errors.append("registered asset dimensions must be a two-integer array")
    else:
        result.declared_dimensions = declared_dimensions
        if tuple(declared_dimensions) != expected_dimensions:
            errors.append(
                f"registered asset dimensions must equal {list(expected_dimensions)}; "
                f"found {declared_dimensions}"
            )

    if resolved_path is None or not resolved_path.is_file():
        if isinstance(asset_path, str):
            errors.append(f"registered production asset does not exist: {asset_path}")
        result.passed = not errors
        return result

    result.actual_sha256 = validate_assets.sha256_file(resolved_path)
    if isinstance(declared_sha256, str) and result.actual_sha256 != declared_sha256:
        errors.append("registered asset SHA-256 does not match manifest")

    if isinstance(category, str) and category in validate_assets.PRODUCTION_CATEGORIES:
        file_result = validate_assets.validate_file(
            resolved_path,
            *expected_dimensions,
            category=category,
        )
        result.actual_dimensions = file_result.dimensions
        if file_result.dimensions != list(expected_dimensions):
            errors.append(
                f"registered asset dimensions are {file_result.dimensions}; "
                f"expected {list(expected_dimensions)}"
            )
        errors.extend(f"asset QA: {error}" for error in file_result.errors)
        result.warnings.extend(f"asset QA: {warning}" for warning in file_result.warnings)

    result.passed = not errors
    return result


def validate_manifest_consistency(
    manifest_path: Path,
    repository_root: Path,
) -> ManifestConsistencyResult:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = load_json(manifest_path)
    except ValueError as exc:
        return ManifestConsistencyResult(
            manifest=str(manifest_path),
            passed=False,
            checked=0,
            errors=[str(exc)],
        )

    expected_dimensions = locked_canvas(manifest, errors)
    registered = manifest.get("registered_production_assets")
    if not isinstance(registered, list):
        errors.append("manifest registered_production_assets must be an array")
        registered = []

    assets: list[RegisteredAssetResult] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    if expected_dimensions is not None:
        for entry in registered:
            asset_result = validate_registered_asset(
                entry,
                repository_root=repository_root,
                expected_dimensions=expected_dimensions,
                seen_ids=seen_ids,
                seen_paths=seen_paths,
            )
            assets.append(asset_result)
            errors.extend(
                f"{asset_result.id or asset_result.path or 'unnamed asset'}: {error}"
                for error in asset_result.errors
            )
            warnings.extend(
                f"{asset_result.id or asset_result.path or 'unnamed asset'}: {warning}"
                for warning in asset_result.warnings
            )

    return ManifestConsistencyResult(
        manifest=str(manifest_path),
        passed=not errors,
        checked=len(assets),
        errors=errors,
        warnings=warnings,
        assets=assets,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("assets/asset_manifest.json"))
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args(argv)

    result = validate_manifest_consistency(args.manifest, args.repository_root)
    print(f"{'PASS' if result.passed else 'FAIL'} registered production asset manifest")
    for error in result.errors:
        print(f"  - ERROR: {error}")
    for warning in result.warnings:
        print(f"  - WARNING: {warning}")
    print(f"Checked {result.checked} registered production asset(s).")

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.json_report}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
