#!/usr/bin/env python3
"""Validate Demigods production assets against locked canvas and alpha rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.png$")
TRANSPARENT_PREFIXES = (
    "base_body_",
    "base_pose_",
    "hair_back_",
    "hair_front_",
    "eyes_",
    "eyebrows_",
    "mouth_",
    "expression_mark_",
    "outfit_",
    "neck_accessory_",
    "head_accessory_",
    "hand_object_",
    "back_accessory_",
    "aura_rear_",
    "aura_front_",
    "global_finish_",
)
BACKGROUND_PREFIX = "background_"
PRODUCTION_IMAGE_EXTENSIONS = {".png"}
REFERENCE_IMAGE_EXTENSIONS = {".webp", ".jpg", ".jpeg"}


@dataclass
class ValidationResult:
    path: str
    passed: bool
    errors: list[str]
    warnings: list[str]
    dimensions: list[int] | None = None
    mode: str | None = None
    format: str | None = None
    alpha_extrema: list[int] | None = None
    visible_bbox: list[int] | None = None


def classify_asset(filename: str) -> str | None:
    if filename.startswith(BACKGROUND_PREFIX):
        return "background"
    if filename.startswith(TRANSPARENT_PREFIXES):
        return "transparent"
    return None


def validate_file(path: Path, width: int, height: int) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    dimensions: list[int] | None = None
    mode: str | None = None
    decoded_format: str | None = None
    alpha_extrema: list[int] | None = None
    visible_bbox: list[int] | None = None

    if path.suffix.lower() not in PRODUCTION_IMAGE_EXTENSIONS:
        errors.append("production assets must use the .png extension")
    if not NAME_PATTERN.fullmatch(path.name):
        errors.append("filename must be lowercase snake_case and end in .png")

    category = classify_asset(path.name)
    if category is None:
        errors.append("filename does not match a recognized production asset prefix")

    try:
        with Image.open(path) as image:
            image.load()
            dimensions = list(image.size)
            mode = image.mode
            decoded_format = image.format

            if image.format != "PNG":
                errors.append(f"decoded format is {image.format}, expected PNG")
            if image.size != (width, height):
                errors.append(f"size is {image.size}, expected {(width, height)}")

            if category == "transparent":
                if image.mode != "RGBA":
                    errors.append(f"mode is {image.mode}, expected RGBA")
                if "A" not in image.getbands():
                    errors.append("missing alpha channel")
                else:
                    alpha = image.getchannel("A")
                    extrema = alpha.getextrema()
                    bbox = alpha.getbbox()
                    alpha_extrema = list(extrema)
                    visible_bbox = list(bbox) if bbox else None

                    if extrema == (255, 255):
                        errors.append("alpha channel is fully opaque")
                    if bbox is None:
                        errors.append("asset is fully transparent")
                    elif bbox[0] == 0 or bbox[1] == 0 or bbox[2] == width or bbox[3] == height:
                        errors.append(f"visible pixels touch a canvas edge: bbox={bbox}")

                    if extrema[1] < 255:
                        warnings.append("no fully opaque pixels detected; inspect unintended global transparency")

            elif category == "background":
                if image.mode not in {"RGB", "RGBA"}:
                    errors.append(f"background mode is {image.mode}, expected RGB or RGBA")
                if "A" in image.getbands():
                    alpha = image.getchannel("A")
                    extrema = alpha.getextrema()
                    alpha_extrema = list(extrema)
                    if extrema != (255, 255):
                        errors.append("background contains transparent pixels")

            if not image.info.get("icc_profile"):
                warnings.append("no embedded ICC profile; confirm sRGB interpretation")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"could not fully decode image: {exc}")

    return ValidationResult(
        path=str(path),
        passed=not errors,
        errors=errors,
        warnings=warnings,
        dimensions=dimensions,
        mode=mode,
        format=decoded_format,
        alpha_extrema=alpha_extrema,
        visible_bbox=visible_bbox,
    )


def discover_files(directory: Path, include_references: bool) -> list[Path]:
    extensions = set(PRODUCTION_IMAGE_EXTENSIONS)
    if include_references:
        extensions.update(REFERENCE_IMAGE_EXTENSIONS)
    return sorted(path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in extensions)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--width", type=int, default=2048)
    parser.add_argument("--height", type=int, default=2048)
    parser.add_argument("--json-report", type=Path)
    parser.add_argument(
        "--include-references",
        action="store_true",
        help="Also inspect WebP/JPEG files; these will fail production-format checks.",
    )
    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"ERROR: directory does not exist: {args.directory}", file=sys.stderr)
        return 2

    files = discover_files(args.directory, args.include_references)
    results = [validate_file(path, args.width, args.height) for path in files]

    for result in results:
        print(f"{'PASS' if result.passed else 'FAIL'} {result.path}")
        for error in result.errors:
            print(f"  - ERROR: {error}")
        for warning in result.warnings:
            print(f"  - WARNING: {warning}")

    failed = sum(not result.passed for result in results)
    warned = sum(bool(result.warnings) for result in results)
    summary = {
        "directory": str(args.directory),
        "expected_dimensions": [args.width, args.height],
        "checked": len(results),
        "failed": failed,
        "passed": len(results) - failed,
        "with_warnings": warned,
        "results": [asdict(result) for result in results],
    }

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.json_report}")

    print(f"\nChecked {len(results)} file(s); {failed} failed; {warned} with warnings.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
