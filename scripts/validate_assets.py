#!/usr/bin/env python3
"""Validate Demigods production assets and manifest references.

The validator distinguishes canonical production folders from source-reference
folders. It performs binary decoding, format, dimensions, alpha, naming, and
manifest consistency checks without treating low-resolution reference images as
production assets.
"""

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
NUMBERED_NAME = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*_\d{3}_[a-z0-9]+(?:_[a-z0-9]+)*\.png$")


@dataclass
class AssetResult:
    path: str
    category: str
    sha256: str | None = None
    size: tuple[int, int] | None = None
    mode: str | None = None
    alpha_extrema: tuple[int, int] | None = None
    visible_bbox: tuple[int, int, int, int] | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


@dataclass
class ManifestResult:
    path: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_name(category: str, name: str) -> list[str]:
    errors: list[str] = []
    config = PRODUCTION_CATEGORIES[category]
    if not SNAKE_CASE_PNG.fullmatch(name):
        errors.append("filename must be lowercase snake_case PNG")
    if not any(name.startswith(prefix) for prefix in config["prefixes"]):
        allowed = ", ".join(config["prefixes"])
        errors.append(f"filename prefix does not match category; expected one of: {allowed}")
    if not NUMBERED_NAME.fullmatch(name):
        errors.append("filename must include a sequential three-digit number and description")
    return errors


def validate_asset(path: Path, root: Path, width: int, height: int) -> AssetResult:
    relative = path.relative_to(root)
    category = relative.parts[0] if relative.parts else ""
    result = AssetResult(path=relative.as_posix(), category=category)

    if category not in PRODUCTION_CATEGORIES:
        result.errors.append("file is not inside a canonical production category")
        return result

    if len(relative.parts) != 2:
        result.errors.append("production assets must be stored directly inside their category folder")

    if path.suffix.lower() != ".png":
        result.errors.append("production assets must use PNG format")
    result.errors.extend(expected_name(category, path.name))

    try:
        result.sha256 = sha256_file(path)

        with Image.open(path) as probe:
            probe.verify()
        with Image.open(path) as image:
            image.load()
            result.size = image.size
            result.mode = image.mode

            if image.format != "PNG":
                result.errors.append(f"decoded format is {image.format!r}; expected PNG")
            if image.size != (width, height):
                result.errors.append(f"size is {image.size}; expected {(width, height)}")

            config = PRODUCTION_CATEGORIES[category]
            has_alpha = "A" in image.getbands()
            if config["requires_alpha"] and not has_alpha:
                result.errors.append("missing alpha channel")
            if config["requires_opaque_canvas"] and image.mode not in {"RGB", "RGBA"}:
                result.errors.append(f"background mode is {image.mode}; expected RGB or RGBA")

            if has_alpha:
                alpha = image.getchannel("A")
                result.alpha_extrema = alpha.getextrema()
                result.visible_bbox = alpha.getbbox()

                if config["requires_alpha"]:
                    if result.alpha_extrema == (255, 255):
                        result.errors.append("alpha channel is fully opaque; genuine transparency is required")
                    if result.visible_bbox is None:
                        result.errors.append("asset is fully transparent")
                    elif not config["allow_edge_touch"]:
                        left, top, right, bottom = result.visible_bbox
                        if left == 0 or top == 0 or right == width or bottom == height:
                            result.errors.append(
                                f"visible pixels touch a canvas edge: bbox={result.visible_bbox}"
                            )
                elif config["requires_opaque_canvas"] and result.alpha_extrema != (255, 255):
                    result.errors.append(
                        f"background alpha is {result.alpha_extrema}; backgrounds must fill the canvas"
                    )
            elif config["requires_opaque_canvas"]:
                result.visible_bbox = (0, 0, width, height)

            if image.info.get("icc_profile") is None:
                result.warnings.append("no embedded ICC profile; confirm the file was authored/exported as sRGB")
    except Exception as exc:  # noqa: BLE001
        result.errors.append(f"binary decode failed: {exc}")

    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def validate_manifest(manifest_path: Path, repository_root: Path) -> ManifestResult:
    result = ManifestResult(path=manifest_path.as_posix())
    try:
        manifest = load_json(manifest_path)
    except (FileNotFoundError, ValueError) as exc:
        result.errors.append(str(exc))
        return result

    if manifest.get("target_supply") != 777:
        result.errors.append("target_supply must equal exactly 777")

    canvas = manifest.get("master_canvas", {})
    if canvas.get("width") != 2048 or canvas.get("height") != 2048:
        result.errors.append("manifest master_canvas must be 2048 × 2048")

    declared_dirs = manifest.get("production_directories", {})
    if not isinstance(declared_dirs, dict):
        result.errors.append("production_directories must be an object")
        declared_dirs = {}

    for category in PRODUCTION_CATEGORIES:
        expected = f"assets/{category}"
        declared = declared_dirs.get(category)
        if declared != expected:
            result.errors.append(
                f"production_directories.{category} is {declared!r}; expected {expected!r}"
            )

    reference_items = manifest.get("approved_visual_references", [])
    if not isinstance(reference_items, list):
        result.errors.append("approved_visual_references must be an array")
        reference_items = []

    for item in reference_items:
        if not isinstance(item, dict):
            result.errors.append("approved_visual_references entries must be objects")
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            result.errors.append("approved visual reference is missing a string path")
            continue
        target = repository_root / raw_path
        if not target.is_file():
            result.errors.append(f"approved visual reference does not exist: {raw_path}")
        if item.get("production_ready") is False:
            result.warnings.append(f"visual reference is intentionally not production-ready: {raw_path}")

    items = manifest.get("blocked_assets", [])
    if not isinstance(items, list):
        result.errors.append("blocked_assets must be an array")
        items = []
    for item in items:
        if not isinstance(item, dict):
            result.errors.append("blocked_assets entries must be objects")
            continue
        intended = item.get("intended_path")
        if isinstance(intended, str):
            parts = Path(intended).parts
            if len(parts) < 3 or parts[0] != "assets" or parts[1] not in PRODUCTION_CATEGORIES:
                result.errors.append(f"blocked asset has noncanonical intended_path: {intended}")
            if (repository_root / intended).exists():
                result.warnings.append(
                    f"blocked asset path already exists and requires status review: {intended}"
                )

    ledger = manifest.get("status_ledger")
    if not isinstance(ledger, str) or not (repository_root / ledger).is_file():
        result.errors.append("status_ledger must reference an existing repository file")

    return result


def discover_production_files(root: Path) -> tuple[list[Path], list[Path]]:
    production: list[Path] = []
    ignored: list[Path] = []
    if not root.exists():
        return production, ignored

    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root)
        category = relative.parts[0] if relative.parts else ""
        if category in PRODUCTION_CATEGORIES:
            production.append(path)
        elif path.suffix.lower() in {".png", ".webp", ".jpg", ".jpeg"}:
            ignored.append(path)
    return production, ignored


def print_asset_result(result: AssetResult) -> None:
    label = "PASS" if result.passed else "FAIL"
    print(f"{label} {result.path}")
    for error in result.errors:
        print(f"  ERROR: {error}")
    for warning in result.warnings:
        print(f"  WARN:  {warning}")


def build_report(
    asset_results: list[AssetResult],
    manifest_result: ManifestResult | None,
    ignored: list[Path],
    root: Path,
) -> dict[str, Any]:
    failures = sum(not item.passed for item in asset_results)
    warnings = sum(len(item.warnings) for item in asset_results)
    if manifest_result:
        failures += 0 if manifest_result.passed else 1
        warnings += len(manifest_result.warnings)
    return {
        "root": root.as_posix(),
        "summary": {
            "production_files": len(asset_results),
            "failed_assets": sum(not item.passed for item in asset_results),
            "manifest_failed": bool(manifest_result and not manifest_result.passed),
            "warnings": warnings,
            "overall_failures": failures,
            "ignored_reference_images": len(ignored),
        },
        "assets": [asdict(item) | {"passed": item.passed} for item in asset_results],
        "manifest": (
            asdict(manifest_result) | {"passed": manifest_result.passed}
            if manifest_result
            else None
        ),
        "ignored_reference_images": [path.relative_to(root).as_posix() for path in ignored],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("assets"))
    parser.add_argument("--width", type=int, default=CANVAS_SIZE[0])
    parser.add_argument("--height", type=int, default=CANVAS_SIZE[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--allow-empty", action="store_true")
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args(argv)

    production_files, ignored = discover_production_files(args.directory)
    asset_results = [
        validate_asset(path, args.directory, args.width, args.height)
        for path in production_files
    ]

    for result in asset_results:
        print_asset_result(result)

    if ignored:
        print(f"\nIgnored {len(ignored)} non-production reference image(s).")

    manifest_result: ManifestResult | None = None
    if args.manifest:
        manifest_result = validate_manifest(args.manifest, args.repository_root)
        label = "PASS" if manifest_result.passed else "FAIL"
        print(f"\n{label} manifest {manifest_result.path}")
        for error in manifest_result.errors:
            print(f"  ERROR: {error}")
        for warning in manifest_result.warnings:
            print(f"  WARN:  {warning}")

    no_files_error = not production_files and not args.allow_empty
    if no_files_error:
        print("\nFAIL no production assets were found; use --allow-empty only during preproduction")

    report = build_report(asset_results, manifest_result, ignored, args.directory)
    if no_files_error:
        report["summary"]["overall_failures"] += 1
        report["summary"]["empty_library_failure"] = True

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    failed_assets = sum(not result.passed for result in asset_results)
    manifest_failed = bool(manifest_result and not manifest_result.passed)
    print(
        f"\nChecked {len(asset_results)} production asset(s); "
        f"{failed_assets} asset failure(s); "
        f"manifest {'failed' if manifest_failed else 'passed or not requested'}."
    )
    return 1 if failed_assets or manifest_failed or no_files_error else 0


if __name__ == "__main__":
    sys.exit(main())
