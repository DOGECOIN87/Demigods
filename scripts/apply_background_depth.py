#!/usr/bin/env python3
"""Apply a deterministic depth treatment (slight blur + corner vignette) to backgrounds.

A background sits behind a sharp character. Softening it slightly and darkening
the corners pushes it back in depth and keeps attention on the figure.

This is done as a recorded post-process rather than in the generation prompt on
purpose: an image generator will not apply a *consistent* blur and vignette
across eight separate backgrounds, and a 777-piece collection needs the set to
match. The same input always produces the same bytes, so the result is auditable.

Never writes into assets/. Registered backgrounds are pinned by SHA-256, so a
treated file is a new candidate that needs fresh human approval and
re-registration with `postprocessing` recorded in the manifest.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

CANVAS = (1254, 1254)

BLUR_RADIUS = 3.0      # px; "slight" — detail stays legible, edges soften
VIGNETTE_STRENGTH = 0.3   # fraction of brightness removed at the corners
VIGNETTE_POWER = 2.4   # higher = darkening stays further out toward the corners

# Colour harmonisation. The registered backgrounds arrived from separate renders
# with independent palettes; a shared split-tone is what makes them read as one
# collection. Shadows go deep navy-violet, midtones violet-blue, highlights warm
# gold — the palette the approved four already share.
GRADE_SHADOW = (26, 28, 58)
GRADE_MID = (96, 92, 148)
GRADE_HIGHLIGHT = (247, 228, 182)
GRADE_STRENGTH = 0.34   # blend toward the split-tone; 1.0 would be a full duotone
DESATURATE = 0.22       # pull saturation out of the scene, not the character
DARKEN = 0.93           # background sits back so the lit foreground separates


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_tone_lut() -> tuple[list[int], list[int], list[int]]:
    """256-entry per-channel LUT mapping luminance through shadow/mid/highlight."""
    channels: list[list[int]] = [[], [], []]
    for level in range(256):
        t = level / 255.0
        for index in range(3):
            if t < 0.5:
                local = t / 0.5
                value = GRADE_SHADOW[index] + (GRADE_MID[index] - GRADE_SHADOW[index]) * local
            else:
                local = (t - 0.5) / 0.5
                value = GRADE_MID[index] + (GRADE_HIGHLIGHT[index] - GRADE_MID[index]) * local
            channels[index].append(max(0, min(255, round(value))))
    return channels[0], channels[1], channels[2]


def harmonise(image: Image.Image, *, grade: float, desaturate: float, darken: float) -> Image.Image:
    """Pull a background toward the shared collection palette and push it back."""
    result = image
    if desaturate > 0:
        result = ImageEnhance.Color(result).enhance(1.0 - desaturate)
    if grade > 0:
        luminance = result.convert("L")
        red, green, blue = split_tone_lut()
        toned = Image.merge(
            "RGB",
            (luminance.point(red), luminance.point(green), luminance.point(blue)),
        )
        result = Image.blend(result, toned, grade)
    if darken != 1.0:
        result = ImageEnhance.Brightness(result).enhance(darken)
    return result


def vignette_mask(size: tuple[int, int], power: float) -> Image.Image:
    """Smooth radial mask: black at centre, white toward the corners."""
    # radial_gradient is 256x256 and circular; resizing keeps it smooth and is
    # far cheaper than evaluating the falloff per pixel.
    mask = Image.radial_gradient("L").resize(size, Image.BICUBIC)
    return mask.point(lambda v: int(255 * ((v / 255.0) ** power)))


def apply_depth(
    image: Image.Image,
    *,
    blur_radius: float,
    vignette_strength: float,
    vignette_power: float,
    grade: float = GRADE_STRENGTH,
    desaturate: float = DESATURATE,
    darken: float = DARKEN,
) -> Image.Image:
    if image.size != CANVAS:
        raise ValueError(f"background must be {CANVAS[0]} x {CANVAS[1]}; got {image.size}")

    result = image.convert("RGB")
    if blur_radius > 0:
        result = result.filter(ImageFilter.GaussianBlur(blur_radius))

    result = harmonise(result, grade=grade, desaturate=desaturate, darken=darken)

    if vignette_strength > 0:
        darkened = ImageEnhance.Brightness(result).enhance(1.0 - vignette_strength)
        result = Image.composite(darkened, result, vignette_mask(CANVAS, vignette_power))

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path, help="background PNG(s) to treat")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("images/background_candidates/depth_treated"),
        help="candidate output directory; never assets/",
    )
    parser.add_argument("--blur", type=float, default=BLUR_RADIUS)
    parser.add_argument("--vignette", type=float, default=VIGNETTE_STRENGTH)
    parser.add_argument("--vignette-power", type=float, default=VIGNETTE_POWER)
    parser.add_argument("--grade", type=float, default=GRADE_STRENGTH,
                        help="blend toward the shared split-tone palette (0 disables)")
    parser.add_argument("--desaturate", type=float, default=DESATURATE,
                        help="saturation removed from the background scene")
    parser.add_argument("--darken", type=float, default=DARKEN,
                        help="brightness multiplier; below 1 pushes the scene back")
    args = parser.parse_args(argv)

    if "assets" in args.out_dir.parts:
        print("refusing to write into assets/: treated files are candidates, not registered assets")
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for source in args.sources:
        if not source.is_file():
            print(f"  MISSING {source}")
            failures += 1
            continue
        try:
            treated = apply_depth(
                Image.open(source),
                blur_radius=args.blur,
                vignette_strength=args.vignette,
                vignette_power=args.vignette_power,
                grade=args.grade,
                desaturate=args.desaturate,
                darken=args.darken,
            )
        except ValueError as exc:
            print(f"  FAIL {source.name}: {exc}")
            failures += 1
            continue

        destination = args.out_dir / f"{source.stem}_depth.png"
        treated.save(destination)
        print(f"  {source.name}")
        print(f"    source  sha256 {sha256_file(source)}")
        print(f"    treated sha256 {sha256_file(destination)} -> {destination}")

    print(
        f"\nblur {args.blur} px, vignette {args.vignette} at power {args.vignette_power}. "
        "Treated files are candidates: they need human approval and re-registration "
        "with postprocessing recorded before use."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
