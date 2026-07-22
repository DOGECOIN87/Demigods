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

EXPECTED_SIZE = (1254, 1254)
EXPECTED_MODE = "RGBA"
DEFAULT_OUTPUT = Path("assets/base_bodies/base_body_001_neutral_master.png")
CANVAS_CENTER_X = 627
TOP_OF_HEAD_Y = 141
FOOT_BASELINE_Y = 1139
MAXIMUM_CHARACTER_BOUNDS = (233, 129, 1021, 1139)
CENTER_TOLERANCE_PX = 1.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rig_geometry_errors(
    bbox: tuple[int, int, int, int],
    *,
    require_silhouette_center: bool = True,
) -> list[str]:
    """Validate PIL's exclusive-right/bottom alpha bbox against the locked rig."""
    left, top, right_exclusive, bottom_exclusive = bbox
    right = right_exclusive - 1
    bottom = bottom_exclusive - 1
    max_left, max_top, max_right, max_bottom = MAXIMUM_CHARACTER_BOUNDS
    errors: list[str] = []

    if left < max_left or top < max_top or right > max_right or bottom > max_bottom:
        errors.append(
            "visible pixels exceed locked maximum character bounds: "
            f"observed={[left, top, right, bottom]}, "
            f"allowed={list(MAXIMUM_CHARACTER_BOUNDS)}"
        )
    if top != TOP_OF_HEAD_Y:
        errors.append(
            f"top of visible head is Y {top}, expected locked Y {TOP_OF_HEAD_Y}"
        )
    if bottom != FOOT_BASELINE_Y:
        errors.append(
            f"foot baseline is Y {bottom}, expected locked Y {FOOT_BASELINE_Y}"
        )

    visible_center_x = (left + right) / 2
    if (
        require_silhouette_center
        and abs(visible_center_x - CANVAS_CENTER_X) > CENTER_TOLERANCE_PX
    ):
        errors.append(
            "visible silhouette is not centered on the locked axis: "
            f"observed X {visible_center_x:g}, expected X {CANVAS_CENTER_X} "
            f"within {CENTER_TOLERANCE_PX:g} px"
        )
    return errors


def inspect_source(path: Path) -> dict[str, object]:
    report: dict[str, object] = {
        "source": str(path),
        "intended_output": str(DEFAULT_OUTPUT),
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
        report["passed_binary_qa"] = False
        return report

    if path.suffix.lower() != ".png":
        errors.append("approved production source must be a PNG")

    report["size_bytes"] = path.stat().st_size
    report["sha256"] = sha256(path)

    try:
        with Image.open(path) as probe:
            probe.verify()
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
                elif (
                    bbox[0] == 0
                    or bbox[1] == 0
                    or bbox[2] == EXPECTED_SIZE[0]
                    or bbox[3] == EXPECTED_SIZE[1]
                ):
                    errors.append(f"visible pixels touch a canvas edge: bbox={bbox}")
                else:
                    locked_bbox = [
                        bbox[0],
                        bbox[1],
                        bbox[2] - 1,
                        bbox[3] - 1,
                    ]
                    geometry_errors = rig_geometry_errors(bbox)
                    report["rig_geometry"] = {
                        "observed_visible_bounds_inclusive": locked_bbox,
                        "expected_top_of_head_y": TOP_OF_HEAD_Y,
                        "expected_foot_baseline_y": FOOT_BASELINE_Y,
                        "expected_center_x": CANVAS_CENTER_X,
                        "maximum_character_bounds_inclusive": list(
                            MAXIMUM_CHARACTER_BOUNDS
                        ),
                        "center_tolerance_px": CENTER_TOLERANCE_PX,
                        "passed": not geometry_errors,
                    }
                    errors.extend(geometry_errors)

                if extrema[1] < 255:
                    warnings.append(
                        "no fully opaque pixels were detected; inspect edge and opacity quality"
                    )

            if image.info.get("icc_profile"):
                report["icc_profile_present"] = True
            else:
                report["icc_profile_present"] = False
                warnings.append("no embedded ICC profile detected; confirm sRGB interpretation")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"could not fully decode image: {exc}")

    report["passed_binary_qa"] = not errors
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and optionally register the exact approved 1254x1254 RGBA PNG."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--report", type=Path, default=Path("base_source_intake_report.json"))
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = inspect_source(args.source)
    report["intended_output"] = str(args.output)
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
        print("PASS: binary and locked visible-geometry requirements satisfied")
        print("Manual visual QA is still required for exact pose, anchors, outfit, lighting, and anatomy.")

    print(f"Report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
