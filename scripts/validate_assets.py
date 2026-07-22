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

CANVAS_SIZE = (1254, 1254)
BACKGROUND_CANDIDATE_COUNT = 8
BACKGROUND_CANDIDATE_DIRECTORY = Path("images/background_candidates")
BACKGROUND_CANDIDATE_SIZE = (1024, 1024)
BACKGROUND_CANDIDATE_STATUS = "reference_only_requires_native_1254_png"
SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
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


def is_safe_repository_path(value: str) -> bool:
    candidate = Path(value)
    return not candidate.is_absolute() and ".." not in candidate.parts


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
    if (
        canvas.get("width") != CANVAS_SIZE[0]
        or canvas.get("height") != CANVAS_SIZE[1]
    ):
        errors.append(
            f"master_canvas must be {CANVAS_SIZE[0]} × {CANVAS_SIZE[1]}"
        )

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

    background_candidates = manifest.get("background_candidates")
    if not isinstance(background_candidates, list):
        errors.append("background_candidates must be an array")
        background_candidates = []
    if len(background_candidates) != BACKGROUND_CANDIDATE_COUNT:
        errors.append(
            "background_candidates must contain exactly "
            f"{BACKGROUND_CANDIDATE_COUNT} entries"
        )

    seen_candidate_ids: set[str] = set()
    seen_candidate_paths: set[str] = set()
    seen_candidate_hashes: set[str] = set()
    seen_production_paths: set[str] = set()

    for index, item in enumerate(background_candidates, start=1):
        label = f"background_candidates[{index - 1}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue

        expected_id = f"background_{index:03d}"
        candidate_id = item.get("id")
        if candidate_id != expected_id:
            errors.append(f"{label}.id must equal {expected_id!r}")
        if isinstance(candidate_id, str):
            if candidate_id in seen_candidate_ids:
                errors.append(f"duplicate background candidate id: {candidate_id}")
            seen_candidate_ids.add(candidate_id)

        candidate_path = item.get("path")
        resolved: Path | None = None
        if not isinstance(candidate_path, str) or not candidate_path:
            errors.append(f"{label}.path must be a non-empty string")
        elif not is_safe_repository_path(candidate_path):
            errors.append(f"{label}.path must be a safe repository-relative path")
        else:
            normalized_path = Path(candidate_path).as_posix()
            path_value = Path(normalized_path)
            if path_value.parent != BACKGROUND_CANDIDATE_DIRECTORY:
                errors.append(
                    f"{label}.path must be directly under "
                    f"{BACKGROUND_CANDIDATE_DIRECTORY.as_posix()}/"
                )
            if path_value.suffix.lower() not in {".jpg", ".jpeg"}:
                errors.append(f"{label}.path must reference a JPEG")
            if not path_value.name.startswith(f"{expected_id}_"):
                errors.append(f"{label}.path filename must start with {expected_id}_")
            if normalized_path in seen_candidate_paths:
                errors.append(f"duplicate background candidate path: {normalized_path}")
            seen_candidate_paths.add(normalized_path)
            resolved = repository_root / path_value
            if not resolved.is_file():
                errors.append(f"background candidate does not exist: {candidate_path}")

        if item.get("status") != BACKGROUND_CANDIDATE_STATUS:
            errors.append(
                f"{label}.status must equal {BACKGROUND_CANDIDATE_STATUS!r}"
            )
        if item.get("production_ready") is not False:
            errors.append(f"{label}.production_ready must be false")
        if item.get("source_format") != "JPEG":
            errors.append(f"{label}.source_format must equal 'JPEG'")
        if item.get("source_mode") != "RGB":
            errors.append(f"{label}.source_mode must equal 'RGB'")
        if item.get("source_dimensions") != list(BACKGROUND_CANDIDATE_SIZE):
            errors.append(
                f"{label}.source_dimensions must equal "
                f"{list(BACKGROUND_CANDIDATE_SIZE)}"
            )
        declared_size_bytes = item.get("source_size_bytes")
        if not isinstance(declared_size_bytes, int) or declared_size_bytes <= 0:
            errors.append(f"{label}.source_size_bytes must be a positive integer")

        expected_sha = item.get("sha256")
        if not isinstance(expected_sha, str) or not SHA256_PATTERN.fullmatch(expected_sha):
            errors.append(f"{label}.sha256 must be a lowercase 64-character digest")
        elif expected_sha in seen_candidate_hashes:
            errors.append(f"duplicate background candidate SHA-256: {expected_sha}")
        else:
            seen_candidate_hashes.add(expected_sha)

        provenance = item.get("provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{label}.provenance must be an object")
        else:
            if provenance.get("origin") != "user_attachment":
                errors.append(f"{label}.provenance.origin must equal 'user_attachment'")
            source_filename = provenance.get("source_filename")
            if (
                not isinstance(source_filename, str)
                or not source_filename
                or Path(source_filename).name != source_filename
                or Path(source_filename).suffix.lower() not in {".jpg", ".jpeg"}
            ):
                errors.append(
                    f"{label}.provenance.source_filename must be a JPEG basename"
                )
            received_on = provenance.get("received_on")
            if not isinstance(received_on, str) or not DATE_PATTERN.fullmatch(received_on):
                errors.append(
                    f"{label}.provenance.received_on must use YYYY-MM-DD"
                )
            if provenance.get("preservation") != "byte_for_byte":
                errors.append(
                    f"{label}.provenance.preservation must equal 'byte_for_byte'"
                )
            if provenance.get("modifications") != []:
                errors.append(f"{label}.provenance.modifications must be an empty array")

        if resolved is not None and resolved.is_file():
            actual_sha = sha256_file(resolved)
            if isinstance(expected_sha, str) and expected_sha != actual_sha:
                errors.append(f"background candidate SHA-256 mismatch: {candidate_path}")
            actual_size_bytes = resolved.stat().st_size
            if declared_size_bytes != actual_size_bytes:
                errors.append(
                    f"background candidate byte size is {actual_size_bytes}, "
                    f"manifest declares {declared_size_bytes}: {candidate_path}"
                )

            try:
                with Image.open(resolved) as probe:
                    probe.verify()
                with Image.open(resolved) as image:
                    image.load()
                    if image.size != BACKGROUND_CANDIDATE_SIZE:
                        errors.append(
                            f"background candidate dimensions are {list(image.size)}, "
                            f"expected {list(BACKGROUND_CANDIDATE_SIZE)}: {candidate_path}"
                        )
                    if image.format != "JPEG":
                        errors.append(
                            f"background candidate format is {image.format}, "
                            f"expected JPEG: {candidate_path}"
                        )
                    if image.mode != "RGB":
                        errors.append(
                            f"background candidate mode is {image.mode}, "
                            f"expected RGB: {candidate_path}"
                        )
            except Exception as exc:  # noqa: BLE001
                errors.append(
                    f"could not fully decode background candidate {candidate_path}: {exc}"
                )

        intended = item.get("intended_production_path")
        intended_parts = Path(intended).parts if isinstance(intended, str) else ()
        if (
            len(intended_parts) < 3
            or intended_parts[0] != "assets"
            or intended_parts[1] != "backgrounds"
            or Path(intended).suffix != ".png"
            or not is_safe_repository_path(intended)
            or not Path(intended).name.startswith(f"{expected_id}_")
        ):
            errors.append(
                f"background candidate has noncanonical intended production path: {intended!r}"
            )
        elif intended in seen_production_paths:
            errors.append(f"duplicate intended production path: {intended}")
        else:
            seen_production_paths.add(intended)

        if isinstance(candidate_path, str):
            warnings.append(f"background candidate is reference-only: {candidate_path}")

    candidate_directory = repository_root / BACKGROUND_CANDIDATE_DIRECTORY
    on_disk_candidates = (
        {
            path.relative_to(repository_root).as_posix()
            for path in candidate_directory.iterdir()
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
        }
        if candidate_directory.is_dir()
        else set()
    )
    if on_disk_candidates != seen_candidate_paths:
        missing = sorted(seen_candidate_paths - on_disk_candidates)
        undeclared = sorted(on_disk_candidates - seen_candidate_paths)
        if missing:
            errors.append(
                "manifest-declared background candidates missing from disk: "
                + ", ".join(missing)
            )
        if undeclared:
            errors.append(
                "undeclared background candidate JPEGs found on disk: "
                + ", ".join(undeclared)
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
