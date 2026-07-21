#!/usr/bin/env python3
"""Validate an intact approved Demigods master-avatar source before registration."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

EXPECTED_SIZE = (2048, 2048)
EXPECTED_MODE = "RGBA"
DEFAULT_OUTPUT = Path("assets/base_body/base_body_001_neutral_master.png")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_source(path: Path) -> dict[str, object]:
    report: dict[str, object] = {
        "source": str(path),
        "exists": path.is_file(),
        "errors": [],
        "warnings": [],
    }
    errors = report["errors"]
    warnings = report["warnings"]
    assert isinstance(errors, list)
    assert isinstance(warnings, list)

    if not path.is_file():
        errors.append("source file does not exist")
        return report

    if path.suffix.lower() != ".png":
        errors.append("approved production source must be a PNG")

    report["size_bytes"] = path.stat().st_size
    report["sha256"] = sha256(path)

    try:
        with Image.open(path) as image:
            image.load()
            report["format"] = image.format
            report["mode"] = image.mode
            report["dimensions"] = list(image.size)
            report["bands"] = list(image.getbands())

            if image.format != "PNG":
                errors.append(f"decoded format is {image.format}, expected PNG")
            if image.size != EXPECTED_SIZE:
                errors.append(f"dimensions are {image.size}, expected {EXPECTED_SIZE}")
            if image.mode != EXPECTED_MODE:
                errors.append(f"mode is {image.mode}, expected {EXPECTED_MODE}")
            if "A" not in image.getbands():
                errors.append("missing alpha channel")
            else:
                alpha = image.getchannel("A")
                extrema = alpha.getextrema()
                bbox = alpha.getbbox()
                report["alpha_extrema"] = list(extrema)
                report["visible_bbox"] = list(bbox) if bbox else None

                if extrema == (255, 255):
                    errors.append("alpha channel is fully opaque")
                if bbox is None:
                    errors.append("image is fully transparent")
                elif bbox[0] == 0 or bbox[1] == 0 or bbox[2] == EXPECTED_SIZE[0] or bbox[3] == EXPECTED_SIZE[1]:
                    errors.append(f"visible pixels touch a canvas edge: bbox={bbox}")

                if extrema[1] < 255:
                    warnings.append("no fully opaque pixels were detected; inspect edge and opacity quality")

            if image.info.get("icc_profile"):
                report["icc_profile_present"] = True
            else:
                warnings.append("no embedded ICC profile detected; confirm sRGB interpretation")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"could not fully decode image: {exc}")

    report["passed_binary_qa"] = not errors
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and optionally register the exact approved 2048x2048 RGBA PNG."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--report", type=Path, default=Path("base_source_intake_report.json"))
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = inspect_source(args.source)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if not report.get("passed_binary_qa"):
        print(json.dumps(report, indent=2))
        print(f"FAIL: report written to {args.report}", file=sys.stderr)
        return 1

    if args.register:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            print(f"REFUSED: output already exists: {args.output}", file=sys.stderr)
            return 2
        shutil.copy2(args.source, args.output)
        print(f"REGISTERED: {args.output}")
        print(f"SHA-256: {report['sha256']}")
    else:
        print("PASS: binary requirements satisfied")
        print("Manual visual QA is still required for exact pose, anchors, outfit, lighting, and anatomy.")

    print(f"Report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
