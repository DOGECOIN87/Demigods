#!/usr/bin/env python3
"""Independently verify generated Demigods images, metadata, and provenance."""

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

try:
    from scripts.generate_777 import LAYER_ORDER
except ImportError:  # Direct execution from scripts/.
    from generate_777 import LAYER_ORDER  # type: ignore[no-redef]

SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")
METADATA_KEYS = {
    "name",
    "description",
    "image",
    "token_id",
    "attributes",
    "trait_signature",
    "image_sha256",
}
ATTRIBUTE_KEYS = {"trait_type", "value", "source_file"}


@dataclass
class OutputValidationResult:
    output: str
    passed: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    expected_supply: int = 777
    metadata_files: int = 0
    image_files: int = 0
    unique_trait_signatures: int = 0
    unique_image_hashes: int = 0
    dry_run: bool = False
    trait_provenance_hash: str | None = None
    image_provenance_hash: str | None = None


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def provenance_hash(values: list[str]) -> str:
    return hashlib.sha256("".join(values).encode("utf-8")).hexdigest()


def expected_labels(supply: int, padding: int) -> list[str]:
    return [f"{token_id:0{padding}d}" for token_id in range(1, supply + 1)]


def validate_sha256(value: Any, label: str, errors: list[str], *, allow_none: bool = False) -> str | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
        errors.append(f"{label} must be a lowercase 64-character SHA-256 hex string")
        return None
    return value


def validate_attributes(
    attributes: Any,
    token_label: str,
    errors: list[str],
) -> tuple[list[str], str | None]:
    prefix = f"metadata/{token_label}.json attributes"
    if not isinstance(attributes, list):
        errors.append(f"{prefix} must be an array")
        return [], None
    if len(attributes) < 2:
        errors.append(f"{prefix} must contain at least background and base_bodies")

    trait_types: list[str] = []
    raw_parts: list[str] = []
    seen: set[str] = set()

    for index, attribute in enumerate(attributes):
        label = f"{prefix}[{index}]"
        if not isinstance(attribute, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = sorted(ATTRIBUTE_KEYS - set(attribute))
        extras = sorted(set(attribute) - ATTRIBUTE_KEYS)
        if missing:
            errors.append(f"{label} is missing keys: {', '.join(missing)}")
        if extras:
            errors.append(f"{label} has unexpected keys: {', '.join(extras)}")

        trait_type = attribute.get("trait_type")
        value = attribute.get("value")
        source_file = attribute.get("source_file")

        if not isinstance(trait_type, str) or trait_type not in LAYER_ORDER:
            errors.append(f"{label}.trait_type is not a recognized layer: {trait_type!r}")
            continue
        if trait_type in seen:
            errors.append(f"{prefix} contains duplicate trait_type: {trait_type}")
        seen.add(trait_type)
        trait_types.append(trait_type)

        if not isinstance(value, str) or not value:
            errors.append(f"{label}.value must be a non-empty string")
        if not isinstance(source_file, str):
            errors.append(f"{label}.source_file must be a string")
            continue

        source_path = Path(source_file)
        if source_path.is_absolute() or len(source_path.parts) != 2:
            errors.append(
                f"{label}.source_file must be category/filename.png, got {source_file!r}"
            )
            continue
        if source_path.parts[0] != trait_type:
            errors.append(
                f"{label}.source_file category {source_path.parts[0]!r} "
                f"does not match trait_type {trait_type!r}"
            )
        if source_path.suffix != ".png":
            errors.append(f"{label}.source_file must reference a PNG")
        if isinstance(value, str) and source_path.stem != value:
            errors.append(
                f"{label}.value {value!r} does not match source stem {source_path.stem!r}"
            )
        raw_parts.append(f"{trait_type}:{source_path.name}")

    ordered = sorted(trait_types, key=LAYER_ORDER.index) if trait_types else []
    if trait_types != ordered:
        errors.append(f"{prefix} are not in canonical layer order")
    if "backgrounds" not in seen:
        errors.append(f"{prefix} is missing required backgrounds layer")
    if "base_bodies" not in seen:
        errors.append(f"{prefix} is missing required base_bodies layer")

    raw_signature = "|".join(raw_parts) if raw_parts else None
    return trait_types, raw_signature


def validate_rendered_image(
    image_path: Path,
    label: str,
    expected_size: tuple[int, int],
    errors: list[str],
) -> str | None:
    try:
        digest = sha256_file(image_path)
        with Image.open(image_path) as probe:
            probe.verify()
        with Image.open(image_path) as image:
            image.load()
            if image.format != "PNG":
                errors.append(f"images/{label}.png decoded format is {image.format}, expected PNG")
            if image.size != expected_size:
                errors.append(
                    f"images/{label}.png size is {image.size}, expected {expected_size}"
                )
            if image.mode != "RGBA":
                errors.append(f"images/{label}.png mode is {image.mode}, expected RGBA")
            if "A" not in image.getbands():
                errors.append(f"images/{label}.png is missing alpha channel")
            else:
                extrema = image.getchannel("A").getextrema()
                if extrema != (255, 255):
                    errors.append(
                        f"images/{label}.png contains transparency {extrema}; "
                        "final composites must be opaque because backgrounds fill the canvas"
                    )
        return digest
    except Exception as exc:  # noqa: BLE001
        errors.append(f"images/{label}.png could not be fully decoded: {exc}")
        return None


def validate_output(
    output: Path,
    *,
    expected_supply: int = 777,
    expected_size: tuple[int, int] = (1254, 1254),
    token_padding: int = 4,
    allow_dry_run: bool = False,
) -> OutputValidationResult:
    result = OutputValidationResult(output=str(output), expected_supply=expected_supply)
    errors = result.errors
    warnings = result.warnings

    manifest_path = output / "manifest.json"
    try:
        manifest = load_json(manifest_path)
    except ValueError as exc:
        errors.append(str(exc))
        return result

    supply = manifest.get("supply")
    if supply != expected_supply:
        errors.append(f"manifest supply is {supply!r}; expected {expected_supply}")

    collection = manifest.get("collection")
    if not isinstance(collection, str) or not collection:
        errors.append("manifest collection must be a non-empty string")
        collection = "Demigods"

    dry_run = manifest.get("dry_run")
    if not isinstance(dry_run, bool):
        errors.append("manifest dry_run must be a boolean")
        dry_run = False
    result.dry_run = dry_run
    if dry_run and not allow_dry_run:
        errors.append("dry-run output is not a final collection; pass --allow-dry-run to audit it")

    canvas = manifest.get("canvas")
    if not isinstance(canvas, dict):
        errors.append("manifest canvas must be an object")
    else:
        actual_size = (canvas.get("width"), canvas.get("height"))
        if actual_size != expected_size:
            errors.append(f"manifest canvas is {actual_size}; expected {expected_size}")

    if manifest.get("layer_order") != LAYER_ORDER:
        errors.append("manifest layer_order does not match the canonical generator layer order")

    category_counts = manifest.get("category_counts")
    if not isinstance(category_counts, dict):
        errors.append("manifest category_counts must be an object")
    else:
        missing_categories = sorted(set(LAYER_ORDER) - set(category_counts))
        extra_categories = sorted(set(category_counts) - set(LAYER_ORDER))
        if missing_categories:
            errors.append(
                f"manifest category_counts is missing: {', '.join(missing_categories)}"
            )
        if extra_categories:
            errors.append(
                f"manifest category_counts has unexpected keys: {', '.join(extra_categories)}"
            )
        for category, count in category_counts.items():
            if not isinstance(count, int) or count < 0:
                errors.append(f"manifest category_counts.{category} must be a non-negative integer")
        if category_counts.get("backgrounds", 0) < 1:
            errors.append("manifest category_counts.backgrounds must be at least 1")
        if category_counts.get("base_bodies", 0) < 1:
            errors.append("manifest category_counts.base_bodies must be at least 1")

    theoretical_space = manifest.get("theoretical_combination_space")
    if not isinstance(theoretical_space, int) or theoretical_space < expected_supply:
        errors.append(
            "manifest theoretical_combination_space must be an integer at least equal to supply"
        )

    for key in ("config_sha256", "compatibility_sha256"):
        validate_sha256(manifest.get(key), f"manifest {key}", errors, allow_none=False)

    labels = expected_labels(expected_supply, token_padding)
    expected_metadata_names = {f"{label}.json" for label in labels}
    expected_image_names = {f"{label}.png" for label in labels}
    metadata_dir = output / "metadata"
    images_dir = output / "images"

    actual_metadata_names = (
        {path.name for path in metadata_dir.iterdir() if path.is_file()}
        if metadata_dir.is_dir()
        else set()
    )
    actual_image_names = (
        {path.name for path in images_dir.iterdir() if path.is_file()}
        if images_dir.is_dir()
        else set()
    )
    result.metadata_files = len(actual_metadata_names)
    result.image_files = len(actual_image_names)

    missing_metadata = sorted(expected_metadata_names - actual_metadata_names)
    extra_metadata = sorted(actual_metadata_names - expected_metadata_names)
    if missing_metadata:
        errors.append(f"missing metadata files: {', '.join(missing_metadata[:10])}")
    if extra_metadata:
        errors.append(f"unexpected metadata files: {', '.join(extra_metadata[:10])}")

    if dry_run:
        if actual_image_names:
            errors.append("dry-run output must not contain rendered image files")
    else:
        missing_images = sorted(expected_image_names - actual_image_names)
        extra_images = sorted(actual_image_names - expected_image_names)
        if missing_images:
            errors.append(f"missing image files: {', '.join(missing_images[:10])}")
        if extra_images:
            errors.append(f"unexpected image files: {', '.join(extra_images[:10])}")

    manifest_trait_signatures = manifest.get("trait_signatures")
    manifest_image_hashes = manifest.get("image_hashes")
    if not isinstance(manifest_trait_signatures, list):
        errors.append("manifest trait_signatures must be an array")
        manifest_trait_signatures = []
    if not isinstance(manifest_image_hashes, list):
        errors.append("manifest image_hashes must be an array")
        manifest_image_hashes = []

    metadata_trait_signatures: list[str] = []
    metadata_image_hashes: list[str] = []

    for token_id, label in enumerate(labels, start=1):
        metadata_path = metadata_dir / f"{label}.json"
        if not metadata_path.is_file():
            continue
        try:
            record = load_json(metadata_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        missing_keys = sorted(METADATA_KEYS - set(record))
        extra_keys = sorted(set(record) - METADATA_KEYS)
        if missing_keys:
            errors.append(f"metadata/{label}.json is missing keys: {', '.join(missing_keys)}")
        if extra_keys:
            errors.append(f"metadata/{label}.json has unexpected keys: {', '.join(extra_keys)}")

        expected_name = f"{collection} #{label}"
        if record.get("name") != expected_name:
            errors.append(
                f"metadata/{label}.json name is {record.get('name')!r}; expected {expected_name!r}"
            )
        if not isinstance(record.get("description"), str) or not record["description"].strip():
            errors.append(f"metadata/{label}.json description must be non-empty")
        if record.get("token_id") != token_id:
            errors.append(
                f"metadata/{label}.json token_id is {record.get('token_id')!r}; expected {token_id}"
            )
        expected_image_ref = f"images/{label}.png"
        if record.get("image") != expected_image_ref:
            errors.append(
                f"metadata/{label}.json image is {record.get('image')!r}; "
                f"expected {expected_image_ref!r}"
            )

        _, raw_signature = validate_attributes(record.get("attributes"), label, errors)
        signature = validate_sha256(
            record.get("trait_signature"),
            f"metadata/{label}.json trait_signature",
            errors,
        )
        if signature:
            metadata_trait_signatures.append(signature)
            if raw_signature and hashlib.sha256(raw_signature.encode("utf-8")).hexdigest() != signature:
                errors.append(
                    f"metadata/{label}.json trait_signature does not match its attributes"
                )

        image_hash = validate_sha256(
            record.get("image_sha256"),
            f"metadata/{label}.json image_sha256",
            errors,
            allow_none=dry_run,
        )

        if dry_run:
            if image_hash is not None:
                errors.append(f"metadata/{label}.json image_sha256 must be null in a dry run")
            continue

        image_path = images_dir / f"{label}.png"
        if not image_path.is_file():
            continue
        actual_hash = validate_rendered_image(image_path, label, expected_size, errors)
        if actual_hash:
            metadata_image_hashes.append(actual_hash)
            if image_hash != actual_hash:
                errors.append(
                    f"metadata/{label}.json image_sha256 does not match images/{label}.png"
                )

    if len(metadata_trait_signatures) != expected_supply:
        errors.append(
            f"validated {len(metadata_trait_signatures)} trait signatures; expected {expected_supply}"
        )
    result.unique_trait_signatures = len(set(metadata_trait_signatures))
    if result.unique_trait_signatures != expected_supply:
        errors.append(
            f"unique trait signatures total {result.unique_trait_signatures}; expected {expected_supply}"
        )

    if manifest_trait_signatures != metadata_trait_signatures:
        errors.append("manifest trait_signatures do not exactly match metadata token order")

    calculated_trait_provenance = (
        provenance_hash(metadata_trait_signatures) if metadata_trait_signatures else None
    )
    result.trait_provenance_hash = calculated_trait_provenance
    declared_trait_provenance = validate_sha256(
        manifest.get("trait_provenance_hash"),
        "manifest trait_provenance_hash",
        errors,
    )
    if calculated_trait_provenance and declared_trait_provenance != calculated_trait_provenance:
        errors.append("manifest trait_provenance_hash does not match metadata signatures")

    if dry_run:
        if manifest_image_hashes:
            errors.append("dry-run manifest image_hashes must be empty")
        if manifest.get("image_provenance_hash") is not None:
            errors.append("dry-run manifest image_provenance_hash must be null")
    else:
        if len(metadata_image_hashes) != expected_supply:
            errors.append(
                f"validated {len(metadata_image_hashes)} image hashes; expected {expected_supply}"
            )
        result.unique_image_hashes = len(set(metadata_image_hashes))
        if manifest_image_hashes != metadata_image_hashes:
            errors.append("manifest image_hashes do not exactly match rendered token order")
        calculated_image_provenance = (
            provenance_hash(metadata_image_hashes) if metadata_image_hashes else None
        )
        result.image_provenance_hash = calculated_image_provenance
        declared_image_provenance = validate_sha256(
            manifest.get("image_provenance_hash"),
            "manifest image_provenance_hash",
            errors,
        )
        if calculated_image_provenance and declared_image_provenance != calculated_image_provenance:
            errors.append("manifest image_provenance_hash does not match rendered images")
        if result.unique_image_hashes < 1:
            errors.append("no valid rendered image hashes were found")
        elif result.unique_image_hashes < expected_supply:
            warnings.append(
                f"only {result.unique_image_hashes} unique image hashes exist for "
                f"{expected_supply} unique trait signatures; inspect visually identical combinations"
            )

    result.passed = not errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--supply", type=int, default=777)
    parser.add_argument("--width", type=int, default=1254)
    parser.add_argument("--height", type=int, default=1254)
    parser.add_argument("--token-padding", type=int, default=4)
    parser.add_argument("--allow-dry-run", action="store_true")
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args(argv)

    result = validate_output(
        args.output,
        expected_supply=args.supply,
        expected_size=(args.width, args.height),
        token_padding=args.token_padding,
        allow_dry_run=args.allow_dry_run,
    )

    print(f"{'PASS' if result.passed else 'FAIL'} generated collection output")
    for error in result.errors:
        print(f"  - ERROR: {error}")
    for warning in result.warnings:
        print(f"  - WARNING: {warning}")
    print(
        f"Metadata: {result.metadata_files}/{result.expected_supply}; "
        f"images: {result.image_files}/{result.expected_supply}; "
        f"unique signatures: {result.unique_trait_signatures}."
    )

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.json_report}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
