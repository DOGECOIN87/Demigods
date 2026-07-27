#!/usr/bin/env python3
"""Remove the baked eyes, eyebrows and mouth from a registered base body.

The layer stack composites `eyes` (08), `eyebrows` (09) and `mouths` (10) over
`base_bodies` (05), but every registered base carries a painted face, so any
trait layer in those categories either stacks on top of the baked feature or has
to occlude it with skin padding. See docs/qa/face_layer_conflict_2026-07-27.md.

This resolves that the same way the scalp was already resolved: the base becomes
faceless. It keeps the nose, ears, blush, jaw line and neck shading, and erases
only the three features the trait categories are responsible for.

Method. Baked ink is found as connected dark components inside the face window
and classified by geometry, so nothing is hard-coded to one pose's coordinates
and the ears -- which are as dark as the lashes and sit within 8 px of the eye
bounding box -- are never touched. The mouth is a soft 30-90 px curve that no
threshold separates from the jaw arc by darkness alone, so it is found in a
window keyed to the eye baseline and identified as the one component that does
not touch a window border; the jaw arc always does.

The component pixels are dilated to swallow the antialiased fringe, then filled
by push-pull pyramid interpolation. Repeated blurring does not work here: an eye
socket is ~90 px across, and Jacobi-style relaxation needs on the order of 90^2
passes to carry skin to the centre, so a practical pass count leaves the ink as
a grey smudge. The pyramid instead averages known pixels into a coarse level
where the hole is a couple of pixels wide, then bilinearly pushes that estimate
back down, keeping every known pixel at every level. Skin flows all the way in,
and the fill inherits the face's own gradient rather than a flat swatch, so the
upper-left key light survives.

Outputs are candidates. They are written outside `assets/` and are not
production assets until reviewed and registered.
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

SOURCES = [
    "base_body_001_neutral_master",
    "base_pose_002_viewer_left_vertical_grip",
    "base_pose_003_viewer_right_vertical_grip",
    "base_pose_004_viewer_left_palm_up",
    "base_pose_005_centered_two_hand_grip",
]

# Face search window in locked canvas coordinates. Stops above the neck so the
# collar shading and the jaw arc are never candidates.
FACE_WINDOW = (450, 280, 810, 470)

# Luminance below this is ink rather than skin. Face skin measures 200-220 in
# the lit areas and does not fall below 190 outside the painted features.
INK_LEVEL = 185
MIN_COMPONENT = 100

# Geometry filters, in pixels, that separate the three features from the ears.
EYE_WIDTH = (70, 115)
EYE_HEIGHT = (45, 85)
BROW_MAX_HEIGHT = 30
BROW_WIDTH = (50, 100)

# Mouth search window, relative to the eye baseline and the eye midpoint. Wide
# enough that the jaw arc enters it, which is how the arc is recognised.
MOUTH_BAND = (20, 45)
MOUTH_HALF_WIDTH = 90
MOUTH_INK_LEVEL = 200
MOUTH_MIN_COMPONENT = 12

# Face skin measures 214 and up around the brows and mouth, so growing a
# component through anything below this captures the soft painted tails that a
# threshold tuned for the ink core leaves behind, without leaking into skin.
RELAXED_INK = 208
GROW_PAD = 16

# The brow is painted in two passes: a dark core and a soft under-brow shadow
# separated from it by a few rows of clean skin, so growth cannot reach the
# shadow. The whole band from above the brow down to the eyelid is cleared
# instead. It contains nothing but brow and skin.
BROW_BAND_PAD_X = 8
BROW_BAND_PAD_TOP = 10
BROW_BAND_GAP_TO_EYE = 3

# Fringe swallowed around each component before filling.
DILATE_RADIUS = 6
FEATHER = 1.5

# Relaxation after the pyramid fill, to erase bilinear interpolation seams.
POLISH_PASSES = 24
POLISH_RADIUS = 3.0


def components(mask: list[list[bool]], width: int, height: int,
               minimum: int = MIN_COMPONENT) -> list[dict]:
    seen = [[False] * height for _ in range(width)]
    found = []
    for x in range(width):
        for y in range(height):
            if not mask[x][y] or seen[x][y]:
                continue
            queue = deque([(x, y)])
            seen[x][y] = True
            pixels = []
            while queue:
                cx, cy = queue.popleft()
                pixels.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height and mask[nx][ny] and not seen[nx][ny]:
                        seen[nx][ny] = True
                        queue.append((nx, ny))
            if len(pixels) >= minimum:
                xs = [p[0] for p in pixels]
                ys = [p[1] for p in pixels]
                found.append({
                    "pixels": pixels,
                    "box": (min(xs), min(ys), max(xs), max(ys)),
                    "count": len(pixels),
                })
    return found


def in_range(value: int, bounds: tuple[int, int]) -> bool:
    return bounds[0] <= value <= bounds[1]


def measure(comp: dict, offset_x: int, offset_y: int) -> dict:
    x0, y0, x1, y1 = comp["box"]
    comp["width"] = x1 - x0 + 1
    comp["height"] = y1 - y0 + 1
    comp["center_x"] = offset_x + (x0 + x1) / 2
    comp["top"] = offset_y + y0
    comp["bottom"] = offset_y + y1
    return comp


def find_eyes_and_brows(found: list[dict]) -> tuple[list[dict], list[dict]]:
    eyes = [c for c in found
            if in_range(c["width"], EYE_WIDTH) and in_range(c["height"], EYE_HEIGHT)]
    eyes.sort(key=lambda c: c["count"], reverse=True)
    eyes = sorted(eyes[:2], key=lambda c: c["center_x"])
    if len(eyes) != 2:
        raise SystemExit(f"expected two eye components, found {len(eyes)}")

    eye_top = min(c["top"] for c in eyes)
    brows = [c for c in found
             if c is not eyes[0] and c is not eyes[1]
             and c["height"] <= BROW_MAX_HEIGHT
             and in_range(c["width"], BROW_WIDTH)
             and c["bottom"] < eye_top]
    return eyes, brows


def find_mouth(image: Image.Image, eyes: list[dict]) -> list[dict]:
    """The mouth is the only ink in its window that clears every window border.

    The jaw arc is darker than the mouth in places and cannot be separated by
    threshold, but it always crosses the window; the mouth never does.
    """
    midpoint = round(sum(c["center_x"] for c in eyes) / 2)
    eye_bottom = max(c["bottom"] for c in eyes)
    window = (midpoint - MOUTH_HALF_WIDTH, eye_bottom + MOUTH_BAND[0],
              midpoint + MOUTH_HALF_WIDTH, eye_bottom + MOUTH_BAND[1])

    crop = image.crop(window)
    width, height = crop.size
    luminance = crop.convert("L").load()
    alpha = crop.getchannel("A").load()
    ink = [[luminance[x, y] < MOUTH_INK_LEVEL and alpha[x, y] > 128
            for y in range(height)] for x in range(width)]

    inside = []
    for comp in components(ink, width, height, MOUTH_MIN_COMPONENT):
        x0, y0, x1, y1 = comp["box"]
        if x0 == 0 or y0 == 0 or x1 == width - 1 or y1 == height - 1:
            continue
        comp["pixels"] = [(x + window[0], y + window[1]) for x, y in comp["pixels"]]
        comp["box"] = (x0 + window[0], y0 + window[1], x1 + window[0], y1 + window[1])
        inside.append(measure(comp, 0, 0))
    return inside, window


def span_fill(pixels: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Close a ring of ink into a solid region, row by row.

    An eye component is the lashes, outline and iris; the sclera between them is
    bright, so it survives a darkness threshold and then bleeds outward during
    the fill as a pale ghost. Filling each row between its own extremes takes
    the whole eye instead. Ears are separate components and are unaffected.
    """
    rows: dict[int, list[int]] = {}
    for x, y in pixels:
        rows.setdefault(y, []).append(x)
    filled = []
    for y, xs in rows.items():
        for x in range(min(xs), max(xs) + 1):
            filled.append((x, y))
    return filled


def grow(image: Image.Image, pixels: list[tuple[int, int]], bounds: tuple[int, int, int, int],
         threshold: int = RELAXED_INK) -> list[tuple[int, int]]:
    """Flood outward from an ink core through anything still darker than skin."""
    luminance = image.convert("L").load()
    alpha = image.getchannel("A").load()
    x0, y0, x1, y1 = bounds
    seen = set(pixels)
    queue = deque(pixels)
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if not (x0 <= nx <= x1 and y0 <= ny <= y1) or (nx, ny) in seen:
                continue
            if alpha[nx, ny] > 128 and luminance[nx, ny] < threshold:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return list(seen)


def paint(size: tuple[int, int], origin: tuple[int, int],
          pixel_sets: list[list[tuple[int, int]]]) -> Image.Image:
    mask = Image.new("L", size, 0)
    pixels = mask.load()
    for group in pixel_sets:
        for x, y in group:
            px, py = x - origin[0], y - origin[1]
            if 0 <= px < size[0] and 0 <= py < size[1]:
                pixels[px, py] = 255
    return mask


def build_mask(groups: dict[str, list[dict]], protect: list[list[tuple[int, int]]],
               size: tuple[int, int],
               origin: tuple[int, int]) -> tuple[Image.Image, Image.Image]:
    """Return the hard hole to fill and the feathered mask used to blend it.

    The eye bounding boxes overlap the ears by a few pixels, so anything the
    classifier decided to keep is subtracted from the hole; an ear is as dark as
    a lash and would otherwise be partly erased by the dilation.
    """
    mask = paint(size, origin, [c["pixels"] for comps in groups.values() for c in comps])
    hard = mask.filter(ImageFilter.MaxFilter(DILATE_RADIUS * 2 + 1))
    keep = paint(size, origin, protect).filter(ImageFilter.MaxFilter(3))
    hard = Image.composite(Image.new("L", size, 0), hard, keep)
    return hard, hard.filter(ImageFilter.GaussianBlur(FEATHER))


def _downsample(colour: list[tuple[float, float, float]], weight: list[float],
                width: int, height: int):
    new_w, new_h = max(1, (width + 1) // 2), max(1, (height + 1) // 2)
    out_colour = [(0.0, 0.0, 0.0)] * (new_w * new_h)
    out_weight = [0.0] * (new_w * new_h)
    for y in range(new_h):
        for x in range(new_w):
            acc_r = acc_g = acc_b = acc_w = 0.0
            for dy in (0, 1):
                sy = 2 * y + dy
                if sy >= height:
                    continue
                for dx in (0, 1):
                    sx = 2 * x + dx
                    if sx >= width:
                        continue
                    w = weight[sy * width + sx]
                    if w <= 0.0:
                        continue
                    r, g, b = colour[sy * width + sx]
                    acc_r += r * w
                    acc_g += g * w
                    acc_b += b * w
                    acc_w += w
            index = y * new_w + x
            if acc_w > 0.0:
                out_colour[index] = (acc_r / acc_w, acc_g / acc_w, acc_b / acc_w)
                out_weight[index] = min(1.0, acc_w)
    return out_colour, out_weight, new_w, new_h


def _sample(colour: list[tuple[float, float, float]], width: int, height: int,
            fx: float, fy: float) -> tuple[float, float, float]:
    fx = min(max(fx, 0.0), width - 1.0)
    fy = min(max(fy, 0.0), height - 1.0)
    x0, y0 = int(fx), int(fy)
    x1, y1 = min(x0 + 1, width - 1), min(y0 + 1, height - 1)
    tx, ty = fx - x0, fy - y0
    out = []
    for channel in range(3):
        top = (colour[y0 * width + x0][channel] * (1 - tx)
               + colour[y0 * width + x1][channel] * tx)
        bottom = (colour[y1 * width + x0][channel] * (1 - tx)
                  + colour[y1 * width + x1][channel] * tx)
        out.append(top * (1 - ty) + bottom * ty)
    return out[0], out[1], out[2]


def push_pull(crop: Image.Image, hole: Image.Image) -> Image.Image:
    """Fill `hole` by pyramid interpolation of the surrounding known pixels.

    Transparent pixels count as unknown. Their RGB is (0,0,0) in every one of
    these renders, so treating them as known let black outside the silhouette
    bleed into any hole near the head edge -- which is exactly where the eyebrow
    band sits on the pose-005 master.
    """
    rgb = crop.convert("RGB")
    width, height = rgb.size
    source = rgb.load()
    hole_data = hole.load()
    alpha_data = crop.getchannel("A").load()

    colour = [(0.0, 0.0, 0.0)] * (width * height)
    weight = [0.0] * (width * height)
    for y in range(height):
        for x in range(width):
            index = y * width + x
            r, g, b = source[x, y]
            colour[index] = (float(r), float(g), float(b))
            if hole_data[x, y] == 0 and alpha_data[x, y] >= 200:
                weight[index] = 1.0

    pyramid = [(colour, weight, width, height)]
    while pyramid[-1][2] > 2 or pyramid[-1][3] > 2:
        c, w, cw, ch = pyramid[-1]
        pyramid.append(_downsample(c, w, cw, ch))

    for level in range(len(pyramid) - 2, -1, -1):
        fine_c, fine_w, fw, fh = pyramid[level]
        coarse_c, _, cw, ch = pyramid[level + 1]
        for y in range(fh):
            for x in range(fw):
                index = y * fw + x
                w = fine_w[index]
                if w >= 1.0:
                    continue
                estimate = _sample(coarse_c, cw, ch, x / 2.0 - 0.25, y / 2.0 - 0.25)
                if w <= 0.0:
                    fine_c[index] = estimate
                else:
                    have = fine_c[index]
                    fine_c[index] = tuple(have[i] * w + estimate[i] * (1 - w)
                                          for i in range(3))
                fine_w[index] = 1.0

    filled = Image.new("RGB", (width, height))
    target = filled.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pyramid[0][0][y * width + x]
            target[x, y] = (min(255, max(0, round(r))),
                            min(255, max(0, round(g))),
                            min(255, max(0, round(b))))
    return filled


def process(path: Path, out_dir: Path) -> dict:
    image = Image.open(path).convert("RGBA")
    x0, y0, _, _ = FACE_WINDOW
    crop = image.crop(FACE_WINDOW)
    width, height = crop.size

    luminance = crop.convert("L").load()
    alpha = crop.getchannel("A").load()
    ink = [[luminance[x, y] < INK_LEVEL and alpha[x, y] > 128
            for y in range(height)] for x in range(width)]

    # Detection runs on the crop; everything after it works in canvas
    # coordinates, so pixels and boxes are rebased together. Rebasing only the
    # pixels once put the eyebrow band in the corner of the canvas.
    found = [measure(c, x0, y0) for c in components(ink, width, height)]
    for comp in found:
        comp["pixels"] = [(x + x0, y + y0) for x, y in comp["pixels"]]
        bx0, by0, bx1, by1 = comp["box"]
        comp["box"] = (bx0 + x0, by0 + y0, bx1 + x0, by1 + y0)
    eyes, brows = find_eyes_and_brows(found)
    mouths, mouth_window = find_mouth(image, eyes)
    if not mouths:
        raise SystemExit(f"{path.name}: no mouth component found")

    eye_top = min(c["box"][1] for c in eyes)
    for comp in eyes:
        comp["pixels"] = span_fill(comp["pixels"])
    for comp in brows:
        bx0, by0, bx1, by1 = comp["box"]
        band_bottom = max(by1, eye_top - BROW_BAND_GAP_TO_EYE)
        comp["pixels"] = [
            (x, y)
            for x in range(bx0 - BROW_BAND_PAD_X, bx1 + BROW_BAND_PAD_X + 1)
            for y in range(by0 - BROW_BAND_PAD_TOP, band_bottom + 1)
        ]
    for comp in mouths:
        comp["pixels"] = grow(image, comp["pixels"],
                              (mouth_window[0], mouth_window[1],
                               mouth_window[2] - 1, mouth_window[3] - 1))

    groups = {"eyes": eyes, "eyebrows": brows, "mouths": mouths}
    for comps in groups.values():
        for comp in comps:
            xs = [p[0] for p in comp["pixels"]]
            ys = [p[1] for p in comp["pixels"]]
            comp["box"] = (min(xs), min(ys), max(xs), max(ys))

    classified = {id(c) for comps in groups.values() for c in comps}
    protect = [c["pixels"] for c in found if id(c) not in classified]
    hard, blend = build_mask(groups, protect, crop.size, (x0, y0))
    filled = push_pull(crop, hard)
    # The pyramid estimate is close but bilinear, so a short relaxation pass
    # removes the interpolation seams. It converges now that the hole already
    # holds skin-valued pixels.
    known = crop.convert("RGB")
    opaque = crop.getchannel("A").point(lambda v: 255 if v >= 200 else 0)
    # Restore against a plate whose transparent regions hold extrapolated skin,
    # so the polish blur has no black to pull in either.
    plate = Image.composite(known, filled, opaque)
    for _ in range(POLISH_PASSES):
        filled = Image.composite(filled.filter(ImageFilter.GaussianBlur(POLISH_RADIUS)),
                                 plate, hard)

    result = image.copy()
    patch = Image.composite(filled, known, blend).convert("RGBA")
    patch.putalpha(crop.getchannel("A"))
    result.paste(patch, (x0, y0))

    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / f"{path.stem}_faceless.png"
    result.save(destination)

    return {
        "destination": destination,
        "groups": {k: [c["box"] for c in v] for k, v in groups.items()},
        "alpha_unchanged": result.getchannel("A").tobytes() == image.getchannel("A").tobytes(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=Path("assets/base_bodies"))
    parser.add_argument("--out-dir", type=Path,
                        default=Path("images/trait_candidates/base_bodies"))
    parser.add_argument("--source", action="append",
                        help="stem to process; default processes all five bases")
    args = parser.parse_args(argv)

    if args.out_dir.resolve().is_relative_to(Path("assets").resolve()):
        raise SystemExit("refusing to write candidates under assets/")

    for stem in (args.source or SOURCES):
        report = process(args.assets / f"{stem}.png", args.out_dir)
        counts = {k: len(v) for k, v in report["groups"].items()}
        print(f"{stem}")
        print(f"  removed {counts['eyes']} eyes, {counts['eyebrows']} eyebrows, "
              f"{counts['mouths']} mouth(s); alpha unchanged: {report['alpha_unchanged']}")
        for name, boxes in report["groups"].items():
            for box in boxes:
                print(f"    {name:11s} {box}")
        print(f"  -> {report['destination']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
