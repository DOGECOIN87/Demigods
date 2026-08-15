#!/usr/bin/env python3
"""Normalize a generator-native trait source into a Demigods review candidate.

This tool implements docs/workflows/generator_source_transform.md. It never edits
its source. It clears only negligible alpha haze, crops transparent margin,
downscales the isolated trait, and places it on the locked 1254 × 1254 canvas.
The final PNG remains only a review candidate until the usual intake, rig, and
human composite gates pass.

Example:
    python scripts/normalize_generator_source.py \
      images/trait_candidates/hair_front/source.png \
      --out incoming/hair_front_003_silver_straight_bangs.png \
      --target-width 520 --top-y 132
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
CENTER_X = 627
MAX_BOUNDS = (233, 129, 1021, 1139)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_alpha(path: Path) -> tuple[bool, str, tuple[int, int]]:
    with Image.open(path) as image:
        image.load()
        return "A" in image.getbands(), image.mode, image.size


def clear_alpha_haze(image: Image.Image, threshold: int) -> Image.Image:
    """Remove only negligible-alpha presentation haze and clear hidden RGB."""
    if not 0 <= threshold <= 192:
        raise ValueError("alpha threshold must be between 0 and 192")
    result = image.convert("RGBA")
    pixels = np.array(result, dtype=np.uint8)
    alpha = pixels[:, :, 3]
    pixels[alpha <= threshold] = 0
    return Image.fromarray(pixels, "RGBA")


def visible_box(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("source has no visible pixels after alpha cleanup")
    return bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1


def resize_premultiplied(image: Image.Image, width: int, height: int) -> Image.Image:
    """Downsample RGBA without pulling hidden matte colours into alpha edges."""
    source = np.asarray(image.convert("RGBA"), dtype=np.float32)
    alpha = source[:, :, 3:4] / 255.0
    premultiplied = source[:, :, :3] * alpha

    rgb_images = [
        Image.fromarray(np.clip(premultiplied[:, :, channel], 0, 255).astype(np.uint8), "L")
        .resize((width, height), Image.Resampling.LANCZOS)
        for channel in range(3)
    ]
    alpha_image = Image.fromarray(source[:, :, 3].astype(np.uint8), "L").resize(
        (width, height), Image.Resampling.LANCZOS
    )

    rgb = np.stack([np.asarray(channel, dtype=np.float32) for channel in rgb_images], axis=-1)
    out_alpha = np.asarray(alpha_image, dtype=np.float32)
    divisor = np.maximum(out_alpha[:, :, None] / 255.0, 1e-6)
    restored = np.clip(rgb / divisor, 0, 255)
    restored[out_alpha <= 0] = 0
    output = np.dstack([restored, out_alpha]).astype(np.uint8)
    return Image.fromarray(output, "RGBA")


def normalize(
    source_path: Path,
    *,
    target_width: int,
    top_y: int,
    alpha_threshold: int = 8,
    center_x: int = CENTER_X,
) -> tuple[Image.Image, dict[str, Any]]:
    has_source_alpha, source_mode, source_size = has_alpha(source_path)
    if not has_source_alpha:
        raise ValueError(
            "source must carry a real alpha channel; opaque checkerboard or matte images "
            "require a separately approved alpha-recovery workflow"
        )
    if source_size[0] < CANVAS or source_size[1] < CANVAS:
        raise ValueError(
            f"source must be at least {CANVAS} × {CANVAS} before reduction-only normalization; got {source_size}"
        )
    if target_width <= 0:
        raise ValueError("target width must be positive")

    cleaned = clear_alpha_haze(Image.open(source_path), alpha_threshold)
    left, top, right, bottom = visible_box(cleaned)
    if left == 0 or top == 0 or right == source_size[0] - 1 or bottom == source_size[1] - 1:
        raise ValueError(
            "visible source pixels touch a source-canvas edge after alpha cleanup; "
            "the asset is not safely isolated for automatic normalization"
        )

    content = cleaned.crop((left, top, right + 1, bottom + 1))
    scale = target_width / content.width
    if scale >= 1.0:
        raise ValueError(
            f"normalization allows reduction only; requested scale {scale:.4f} would not reduce source content"
        )
    target_height = max(1, round(content.height * scale))
    scaled = resize_premultiplied(content, target_width, target_height)

    out_left = round(center_x - target_width / 2)
    out_top = top_y
    out_right = out_left + target_width - 1
    out_bottom = out_top + target_height - 1
    if out_left < MAX_BOUNDS[0] or out_top < MAX_BOUNDS[1] or out_right > MAX_BOUNDS[2] or out_bottom > MAX_BOUNDS[3]:
        raise ValueError(
            "normalized bounds "
            f"[{out_left},{out_top},{out_right},{out_bottom}] exceed locked trait bounds {list(MAX_BOUNDS)}"
        )

    output = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    output.alpha_composite(scaled, (out_left, out_top))
    report: dict[str, Any] = {
        "origin": "generator_source_transform",
        "source_path": source_path.relative_to(ROOT).as_posix(),
        "source_sha256": sha256_file(source_path),
        "source_dimensions": list(source_size),
        "source_mode": source_mode,
        "alpha_cleanup": {"method": "clear_negligible_alpha_haze", "threshold": alpha_threshold},
        "transform": {
            "method": "crop_transparent_margin_then_premultiplied_lanczos_reduction",
            "source_visible_bounds": [left, top, right, bottom],
            "crop_dimensions": [content.width, content.height],
            "scale": round(scale, 8),
            "target_dimensions": [target_width, target_height],
            "placement": {"center_x": center_x, "top_y": top_y, "bounds": [out_left, out_top, out_right, out_bottom]},
        },
        "final_dimensions": [CANVAS, CANVAS],
        "normalization_script": "scripts/normalize_generator_source.py",
    }
    return output, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="immutable RGBA generator-source PNG")
    parser.add_argument("--out", type=Path, required=True, help="normalized review-candidate PNG")
    parser.add_argument("--target-width", type=int, required=True, help="final trait width in pixels; must downscale source content")
    parser.add_argument("--top-y", type=int, required=True, help="locked-canvas top coordinate for normalized content")
    parser.add_argument("--center-x", type=int, default=CENTER_X)
    parser.add_argument(
        "--alpha-threshold", type=int, default=8,
        help="remove alpha at or below this value; use values above 32 only for a documented low-opacity generator presentation matte",
    )
    parser.add_argument("--report", type=Path, help="JSON provenance sidecar; defaults beside --out")
    args = parser.parse_args(argv)

    output, report = normalize(
        args.source,
        target_width=args.target_width,
        top_y=args.top_y,
        alpha_threshold=args.alpha_threshold,
        center_x=args.center_x,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.out)
    report["output_path"] = args.out.relative_to(ROOT).as_posix() if args.out.is_absolute() else args.out.as_posix()
    report["output_sha256"] = sha256_file(args.out)
    report_path = args.report or args.out.with_suffix(args.out.suffix + ".provenance.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    print(f"Provenance: {report_path}")
    print(f"Source: {report['source_dimensions'][0]}x{report['source_dimensions'][1]} {report['source_mode']} -> "
          f"{CANVAS}x{CANVAS} RGBA at scale {report['transform']['scale']:.4f}")
    print(f"Bounds: {report['transform']['placement']['bounds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
