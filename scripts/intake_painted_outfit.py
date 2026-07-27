#!/usr/bin/env python3
"""Turn a flat studio render of a garment into a rig-fitted outfit candidate.

The painted robe references arrive as native 1254 x 1254 **RGB** files: what
looks like a transparency checker in a viewer is painted into the pixels, and
the alpha channel is absent. They are also drawn at full humanoid proportions,
roughly 1100 px from collar to hem, against a rig whose whole body below the
chin is 606 px. Both have to be fixed before the file is an outfit layer.

## Background

The background is found by flood fill from the canvas border through near-white,
near-neutral pixels, rather than by thresholding brightness. Thresholding would
eat the white-and-gold robes, whose fabric is as bright as the backdrop; the
fill stops at their grey shading and gold linework instead. The tolerance has
real headroom -- 235 and 225 give the same result to within 1%, while 242 leaks
through the garment and takes the whole canvas.

Edge alpha comes from softening that mask, and edge colour is then un-premultiplied
against the backdrop white. Skipping the second step leaves a pale rim that is
invisible on a light page and obvious the moment the character stands against a
dark background, which is where these are actually used.

## Fit

The garment is scaled about the locked centre axis so its collar and hem land on
the rig, using `refit_trait_layer.refit`. Repository rules on rescaling were
waived for this intake by the collection owner; the operation is still recorded
in `postprocessing` so it stays visible.

## What this cannot fix

An outfit layer composites *over* the base body, so its sleeves replace whatever
the arms were doing, and these are painted with one arm position. Run
`--pose-report` to measure that against every registered base pose before
registering: it prints how much of each pose's distinguishing silhouette the
garment hides.
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from refit_trait_layer import CANVAS, MAX_BOUNDS, refit, visible_box  # noqa: E402

# Flood-fill acceptance. A background pixel is bright and neutral; the robes'
# white fabric carries enough grey and gold that it never qualifies.
BACKGROUND_LEVEL = 235
BACKGROUND_NEUTRALITY = 8
BACKDROP = (253, 253, 253)

# Edge softening, and the coverage floor for the colour solve. Un-premultiplying
# divides by coverage, so without a floor the 1 px rim fills with noise.
EDGE_FEATHER = 0.8
COLOUR_COVERAGE_FLOOR = 0.35
ALPHA_FLOOR = 8

# Rig targets. The hem matches the registered procedural coats at 1108. The
# collar seat was found by sweeping scale and offset for the placement that
# leaves zero bare skin in the shoulder band while keeping that hem: seating the
# collar at the more obvious 480 left a rim of shoulder showing outside the
# pauldrons on every robe and every pose.
COLLAR_TOP_Y = 442
HEM_Y = 1108

# Body rows the garment must cover completely. Bare skin here reads as a hole.
SHOULDER_BAND = (535, 660)

BASE_BODIES = [
    "base_body_001_neutral_master",
    "base_pose_002_viewer_left_vertical_grip",
    "base_pose_003_viewer_right_vertical_grip",
    "base_pose_004_viewer_left_palm_up",
    "base_pose_005_centered_two_hand_grip",
]

ARM_BAND = (640, 860)
POSE_BAND = (560, 1000)


def background_mask(image: Image.Image) -> Image.Image:
    """Flood fill the backdrop from the canvas border."""
    width, height = image.size
    pixels = image.convert("RGB").load()

    def is_backdrop(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return (min(red, green, blue) > BACKGROUND_LEVEL
                and max(red, green, blue) - min(red, green, blue) < BACKGROUND_NEUTRALITY)

    seen = [[False] * height for _ in range(width)]
    queue: deque[tuple[int, int]] = deque()

    def seed(x: int, y: int) -> None:
        if not seen[x][y] and is_backdrop(x, y):
            seen[x][y] = True
            queue.append((x, y))

    for x in range(width):
        seed(x, 0)
        seed(x, height - 1)
    for y in range(height):
        seed(0, y)
        seed(width - 1, y)

    while queue:
        cx, cy = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not seen[nx][ny] and is_backdrop(nx, ny):
                seen[nx][ny] = True
                queue.append((nx, ny))

    mask = Image.new("L", (width, height), 0)
    paint = mask.load()
    for x in range(width):
        for y in range(height):
            if not seen[x][y]:
                paint[x, y] = 255
    return mask


def cutout(image: Image.Image) -> Image.Image:
    """Alpha from the softened mask; colour un-premultiplied against the backdrop."""
    source = image.convert("RGB")
    coverage = background_mask(source).filter(ImageFilter.GaussianBlur(EDGE_FEATHER))

    width, height = source.size
    read = source.load()
    alpha_read = coverage.load()
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    write = result.load()

    for y in range(height):
        for x in range(width):
            alpha = alpha_read[x, y]
            if alpha < ALPHA_FLOOR:
                continue
            fraction = alpha / 255.0
            solve = max(fraction, COLOUR_COVERAGE_FLOOR)
            channels = []
            for value, backdrop in zip(read[x, y], BACKDROP):
                recovered = backdrop + (value - backdrop) / solve
                channels.append(min(255, max(0, round(recovered))))
            write[x, y] = (channels[0], channels[1], channels[2], alpha)
    return result


def fit_to_rig(layer: Image.Image) -> tuple[Image.Image, float]:
    left, top, right, bottom = visible_box(layer)
    scale = (HEM_Y - COLLAR_TOP_Y) / (bottom - top)
    return refit(layer, scale=scale, top_y=COLLAR_TOP_Y), scale


def shoulder_gap(layer: Image.Image, body_path: Path) -> int:
    """Body pixels in the shoulder band the garment fails to cover."""
    body = Image.open(body_path).convert("RGBA").getchannel("A").load()
    outfit = layer.getchannel("A").load()
    return sum(1 for y in range(*SHOULDER_BAND) for x in range(CANVAS)
               if body[x, y] > 128 and outfit[x, y] <= 128)


def pose_report(layer: Image.Image, assets: Path) -> list[dict]:
    """How each registered base pose fares under this garment.

    `hidden` is the share of the pose's own silhouette difference from the
    neutral master that the outfit covers. A pose differs from the master only
    in its arms and hands, so a high number means the outfit has erased the one
    thing that makes that pose a distinct asset.
    """
    outfit = layer.getchannel("A").load()
    reference = Image.open(assets / f"{BASE_BODIES[0]}.png").convert("RGBA")
    ref_alpha = reference.getchannel("A").load()

    rows = []
    for name in BASE_BODIES:
        body = Image.open(assets / f"{name}.png").convert("RGBA")
        alpha = body.getchannel("A").load()

        bare = sum(1 for y in range(*ARM_BAND) for x in range(CANVAS)
                   if alpha[x, y] > 128 and outfit[x, y] <= 128)
        unique = [(x, y) for y in range(*POSE_BAND) for x in range(CANVAS)
                  if (alpha[x, y] > 128) != (ref_alpha[x, y] > 128)]
        hidden = sum(1 for x, y in unique if outfit[x, y] > 128)
        rows.append({
            "pose": name,
            "bare_arm_pixels": bare,
            "pose_unique": len(unique),
            "hidden": hidden,
            "hidden_share": (hidden / len(unique)) if unique else 0.0,
        })
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--assets", type=Path, default=Path("assets/base_bodies"))
    parser.add_argument("--pose-report", action="store_true")
    args = parser.parse_args(argv)

    if args.out.resolve().is_relative_to(Path("assets").resolve()):
        raise SystemExit("refusing to write candidates under assets/")

    image = Image.open(args.source)
    if image.size != (CANVAS, CANVAS):
        raise SystemExit(f"source must be natively {CANVAS} x {CANVAS}; got {image.size}")

    layer = cutout(image)
    fitted, scale = fit_to_rig(layer)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fitted.save(args.out)

    left, top, right, bottom = visible_box(fitted)
    within = (left >= MAX_BOUNDS[0] and top >= MAX_BOUNDS[1]
              and right <= MAX_BOUNDS[2] and bottom <= MAX_BOUNDS[3])
    print(f"{args.source.name}")
    print(f"  cut out, scaled {scale:.3f} -> {args.out}")
    print(f"  bounds [{left},{top},{right},{bottom}] within {list(MAX_BOUNDS)}: {within}")

    bare_shoulder = shoulder_gap(fitted, args.assets / f"{BASE_BODIES[0]}.png")
    print(f"  bare shoulder pixels: {bare_shoulder}")

    if args.pose_report:
        print(f"  {'pose':44s} {'bare arm px':>12s} {'pose detail hidden':>20s}")
        for row in pose_report(fitted, args.assets):
            print(f"  {row['pose']:44s} {row['bare_arm_pixels']:12d} "
                  f"{row['hidden']:9d} ({row['hidden_share'] * 100:5.1f}%)")

    return 0 if within else 1


if __name__ == "__main__":
    raise SystemExit(main())
