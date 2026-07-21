#!/usr/bin/env python3
"""Validate Demigods production assets and manifest references."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image

CANVAS_SIZE = (2048, 2048)
PRODUCTION_CATEGORIES: dict[str, dict[str, Any]] = {
    "backgrounds": {
        "prefixes": ("background_",),
        "requires_alpha": False,
        "requires_opaque_canvas": True,
        "allow_edge_touch": True,
    },
    "rear_auras": {
        "prefixes": ("aura_rear_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": True,
    },
    "back_accessories": {
        "prefixes": ("back_accessory_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "hair_back": {
        "prefixes": ("hair_back_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "base_bodies": {
        "prefixes": ("base_body_", "base_pose_"),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "outfits": {
        "prefixes": ("outfit_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "neck_accessories": {
        "prefixes": ("neck_accessory_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "eyes": {
        "prefixes": ("eyes_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "eyebrows": {
        "prefixes": ("eyebrows_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "mouths": {
        "prefixes": ("mouth_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "expression_marks": {
        "prefixes": ("expression_mark_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "hair_front": {
        "prefixes": ("hair_front_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "head_accessories": {
        "prefixes": ("head_accessory_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "hand_objects": {
        "prefixes": ("hand_object_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": False,
    },
    "front_auras": {
        "prefixes": ("aura_front_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": True,
    },
    "global_finish": {
        "prefixes": ("global_finish_",),
        "requires_alpha": True,
        "requires_opaque_canvas": False,
        "allow_edge_touch": True,
    },
}

SNAKE_CASE_PNG = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.png$")
NUMBERED_NAME = re.compile(
    r"^[a-z0-9]+(?:_[a-z0-9]+)*_\d{3}_[a-z0-9]+(?:_[a-z0-9]+)*\.png$"
)
REFERENCE_EXTENSIONS = {".webp", ".jpg", ".jpeg"}


@dataclass
class ValidationResult:
    path: str
    category: str | None
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    sha256: str | None = None
    dimensions: list[int] | None = None
    mode: str | None = None
    format: str | None = None
    alpha_extrema: list[int] | None = None
    visible_bbox: list[int] | None = None


@dataclass
class ManifestValidationResult:
    path: str
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_filename(filename: str) -> str | None:
    matches = [
        category
        for category, config in PRODUCTION_CATEGORIES.items()
        if any(filename.startswith(prefix) for prefix in config["prefixes"])
    ]
    return matches[0] if len(matches) == 1 else None


def filename_errors(filename: str, category: str | None) -> list[str]:
    errors: list[str] = []
    if not SNAKE_CASE_PNG.fullmatch(filename):
        errors.append("filename must be lowercase snake_case and end in .png")
    if not NUMBERED_NAME.fullmatch(filename):
        errors.append("filename must include a sequential three-digit number and description")
    if category is None:
        errors.append("filename does not match a recognized production asset prefix")
    return errors


def validate_file(
    path: Path,
    width: int,
    height: int,
    *,
    category: str | None = None,
) -> ValidationResult:
    inferred_category = classify_filename(path.name)
    effective_category = category or inferred_category
    errors = filename_errors(path.name, inferred_category)
    warnings: list[str] = []

    if path.suffix.lower() != ".png":
        errors.append("production assets must use PNG format")
    if category is not None and inferred_category != category:
        errors.append(
            f"filename category is {inferred_category!r}; file is stored under {category!r}"
        )

    result = ValidationResult(
        path=str(path),
        category=effective_category,
        passed=False,
        errors=errors,
        warnings=warnings,
    )

    try:
        result.sha256 = sha256_file(path)
        with Image.open(path) as probe:
            probe.verify()
        with Image.open(path) as image:
            image.load()
            result.dimensions = list(image.size)
            result.mode = image.mode
            result.format = image.format

            if image.format != "PNG":
                errors.append(f"decoded format is {image.format}, expected PNG")
            if image.size != (width, height):
                errors.append(f"size is {image.size}, expected {(width, height)}")

            if effective_category is None:
                result.passed = not errors
                return result

            config = PRODUCTION_CATEGORIES[effective_category]
            has_alpha = "A" in image.getbands()

            if config["requires_alpha"]:
                if image.mode != "RGBA":
                    errors.append(f"mode is {image.mode}, expected RGBA")
                if not has_alpha:
                    errors.append("missing alpha channel")
                else:
                    alpha = image.getchannel("A")
                    extrema = alpha.getextrema()
                    bbox = alpha.getbbox()
                    result.alpha_extrema = list(extrema)
                    result.visible_bbox = list(bbox) if bbox else None

                    if extrema == (255, 255):
                        errors.append("alpha channel is fully opaque")
                    if bbox is None:
                        errors.append("asset is fully transparent")
                    elif not config["allow_edge_touch"]:
                        if (
                            bbox[0] == 0
                            or bbox[1] == 0
                            or bbox[2] == width
                            or bbox[3] == height
                        ):
                            errors.append(f"visible pixels touch a canvas edge: bbox={bbox}")
                    if extrema[1] < 255:
                        warnings.append(
                            "no fully opaque pixels detected; inspect unintended global transparency"
                        )

            if config["requires_opaque_canvas"]:
                if image.mode not in {"RGB", "RGBA"}:
                    errors.append(f"background mode is {image.mode}, expected RGB or RGBA")
                if has_alpha:
                    alpha = image.getchannel("A")
                    extrema = alpha.getextrema()
                    result.alpha_extrema = list(extrema)
                    if extrema != (255, 255):
                        errors.append("background contains transparent pixels")

            if not image.info.get("icc_profile"):
                warnings.append("no embedded ICC profile; confirm sRGB interpretation")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"could not fully decode image: {exc}")

    result.passed = not errors
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def validate_manifest(path: Path, repository_root: Path) -> ManifestValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = load_json(path)
    except ValueError as exc:
        return ManifestValidationResult(str(path), False, [str(exc)], warnings)

    if manifest.get("target_supply") != 777:
        errors.append("target_supply must equal exactly 777")

    canvas = manifest.get("master_canvas", {})
    if canvas.get("width") != 2048 or canvas.get("height") != 2048:
        errors.append("master_canvas must be 2048 × 2048")

    directories = manifest.get("production_directories")
    if not isinstance(directories, dict):
        errors.append("production_directories must be an object")
        directories = {}
    for category in PRODUCTION_CATEGORIES:
        expected = f"assets/{category}"
        if directories.get(category) != expected:
            errors.append(
                f"production_directories.{category} must equal {expected!r}"
            )

    ledger = manifest.get("status_ledger")
    if not isinstance(ledger, str) or not (repository_root / ledger).is_file():
        errors.append("status_ledger must reference an existing repository file")

    references = manifest.get("approved_visual_references", [])
    if not isinstance(references, list):
        errors.append("approved_visual_references must be an array")
        references = []
    for item in references:
        if not isinstance(item, dict):
            errors.append("approved_visual_references entries must be objects")
            continue
        reference_path = item.get("path")
        if not isinstance(reference_path, str):
            errors.append("approved visual reference is missing a string path")
            continue
        if not (repository_root / reference_path).is_file():
            errors.append(f"approved visual reference does not exist: {reference_path}")
        if item.get("production_ready") is False:
            warnings.append(
                f"visual reference is intentionally not production-ready: {reference_path}"
            )

    blocked = manifest.get("blocked_assets", [])
    if not isinstance(blocked, list):
        errors.append("blocked_assets must be an array")
        blocked = []
    for item in blocked:
        if not isinstance(item, dict):
            errors.append("blocked_assets entries must be objects")
            continue
        intended = item.get("intended_path")
        if not isinstance(intended, str):
            errors.append("blocked asset is missing intended_path")
            continue
        parts = Path(intended).parts
        if len(parts) < 3 or parts[0] != "assets" or parts[1] not in PRODUCTION_CATEGORIES:
            errors.append(f"blocked asset has noncanonical intended_path: {intended}")
        if (repository_root / intended).exists():
            warnings.append(f"blocked asset path exists and requires status review: {intended}")

    return ManifestValidationResult(str(path), not errors, errors, warnings)


def discover_production_files(root: Path) -> tuple[list[tuple[Path, str]], list[Path]]:
    production: list[tuple[Path, str]] = []
    ignored: list[Path] = []

    if root.name in PRODUCTION_CATEGORIES:
        category = root.name
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if path.suffix.lower() == ".png":
                production.append((path, category))
            elif path.suffix.lower() in REFERENCE_EXTENSIONS:
                ignored.append(path)
        return production, ignored

    for category in PRODUCTION_CATEGORIES:
        folder = root / category
        if not folder.is_dir():
            continue
        for path in sorted(p for p in folder.rglob("*") if p.is_file()):
            if path.suffix.lower() == ".png":
                production.append((path, category))
            elif path.suffix.lower() in REFERENCE_EXTENSIONS:
                ignored.append(path)

    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root)
        top = relative.parts[0] if relative.parts else ""
        if top not in PRODUCTION_CATEGORIES and path.suffix.lower() in {
            ".png",
            *REFERENCE_EXTENSIONS,
        }:
            ignored.append(path)

    return production, sorted(set(ignored))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--width", type=int, default=CANVAS_SIZE[0])
    parser.add_argument("--height", type=int, default=CANVAS_SIZE[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--allow-empty", action="store_true")
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args(argv)

    if not args.directory.is_dir():
        print(f"ERROR: directory does not exist: {args.directory}", file=sys.stderr)
        return 2

    files, ignored = discover_production_files(args.directory)
    results = [
        validate_file(path, args.width, args.height, category=category)
        for path, category in files
    ]

    for result in results:
        print(f"{'PASS' if result.passed else 'FAIL'} {result.path}")
        for error in result.errors:
            print(f"  - ERROR: {error}")
        for warning in result.warnings:
            print(f"  - WARNING: {warning}")

    if ignored:
        print(f"Ignored {len(ignored)} non-production reference image(s).")

    manifest_result: ManifestValidationResult | None = None
    if args.manifest:
        manifest_result = validate_manifest(args.manifest, args.repository_root)
        print(f"{'PASS' if manifest_result.passed else 'FAIL'} manifest {manifest_result.path}")
        for error in manifest_result.errors:
            print(f"  - ERROR: {error}")
        for warning in manifest_result.warnings:
            print(f"  - WARNING: {warning}")

    no_files_failure = not results and not args.allow_empty
    if no_files_failure:
        print("FAIL no production PNGs found; use --allow-empty only during preproduction")

    failed = sum(not result.passed for result in results)
    warned = sum(bool(result.warnings) for result in results)
    manifest_failed = bool(manifest_result and not manifest_result.passed)
    summary = {
        "directory": str(args.directory),
        "expected_dimensions": [args.width, args.height],
        "checked": len(results),
        "failed": failed,
        "passed": len(results) - failed,
        "with_warnings": warned,
        "empty_library_failure": no_files_failure,
        "ignored_reference_images": [str(path) for path in ignored],
        "manifest": asdict(manifest_result) if manifest_result else None,
        "results": [asdict(result) for result in results],
    }

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.json_report}")

    print(
        f"Checked {len(results)} production file(s); {failed} failed; "
        f"{warned} with warnings."
    )
    return 1 if failed or manifest_failed or no_files_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
