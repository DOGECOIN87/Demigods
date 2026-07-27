#!/usr/bin/env python3
"""Recover the base master's painted face as isolated eyes, eyebrows and mouth.

The features erased by `build_faceless_base.py` are the collection's approved
face art. Rather than draw replacements, they are lifted back out of the
pre-removal master as trait layers, which guarantees they register with the rig
exactly and keeps the approved design.

Method: difference matting against the faceless render. The faceless base is a
measured reconstruction of the skin that sat *behind* each feature, so for every
pixel the original is the feature composited over that skin. Solving that
composite for coverage and colour recovers a real matte, with genuine soft edges
where the artist feathered the lashes -- not a luminance key, which is what
would happen if the feature were cut against black and is what the repository's
matte-contamination check exists to catch.

    alpha = clamp(distance(original, skin) / FULL_COVER)
    colour = skin + (original - skin) / alpha

Compositing the result back over the faceless base reproduces the original; the
script reports the worst-case error so that claim is checked rather than
asserted.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_faceless_base as faceless  # noqa: E402

# Channel distance at which a pixel counts as fully the feature rather than
# skin. The painted ink sits 60-180 away from skin, so this only softens the
# outermost antialiased ring.
FULL_COVER = 42.0

# Alpha below this is dropped to zero. Without it the matte carries a wide veil
# of one- and two-level dust, which fails the visible-bounds gate by putting
# nonzero alpha far outside the artwork.
ALPHA_FLOOR = 10

# Un-premultiplying divides by coverage, so at 4% coverage a one-level rounding
# difference becomes a 25-level colour swing and the layer edge fills with
# saturated confetti. Invisible while the layer stays brown, vivid the moment it
# is recoloured. Colour is solved at no less than this coverage; alpha still
# carries the true value, so the edge stays as soft as it was painted.
COLOUR_COVERAGE_FLOOR = 0.30

# Numbers 001-024 (eyes), 001-016 (eyebrows) and 001-012 (mouths) are reserved
# for the painted `FACE` sheet cells in the backlog. These recovered layers are
# a different asset and take their own numbers.
CATEGORY_PATHS = {
    "eyes": "eyes_025_base_master_brown.png",
    "eyebrows": "eyebrows_017_base_master_brown.png",
    "mouths": "mouth_013_base_master_closed_smile.png",
}


def feature_masks(original: Image.Image) -> dict[str, Image.Image]:
    """Re-run the removal tool's detection so the masks match what it erased."""
    x0, y0, _, _ = faceless.FACE_WINDOW
    crop = original.crop(faceless.FACE_WINDOW)
    width, height = crop.size

    luminance = crop.convert("L").load()
    alpha = crop.getchannel("A").load()
    ink = [[luminance[x, y] < faceless.INK_LEVEL and alpha[x, y] > 128
            for y in range(height)] for x in range(width)]

    found = [faceless.measure(c, x0, y0) for c in faceless.components(ink, width, height)]
    for comp in found:
        comp["pixels"] = [(x + x0, y + y0) for x, y in comp["pixels"]]
        bx0, by0, bx1, by1 = comp["box"]
        comp["box"] = (bx0 + x0, by0 + y0, bx1 + x0, by1 + y0)

    eyes, brows = faceless.find_eyes_and_brows(found)
    mouths, mouth_window = faceless.find_mouth(original, eyes)

    eye_top = min(c["box"][1] for c in eyes)
    for comp in eyes:
        comp["pixels"] = faceless.span_fill(comp["pixels"])
    for comp in brows:
        bx0, by0, bx1, by1 = comp["box"]
        band_bottom = max(by1, eye_top - faceless.BROW_BAND_GAP_TO_EYE)
        comp["pixels"] = [
            (x, y)
            for x in range(bx0 - faceless.BROW_BAND_PAD_X, bx1 + faceless.BROW_BAND_PAD_X + 1)
            for y in range(by0 - faceless.BROW_BAND_PAD_TOP, band_bottom + 1)
        ]
    for comp in mouths:
        comp["pixels"] = faceless.grow(original, comp["pixels"],
                                       (mouth_window[0], mouth_window[1],
                                        mouth_window[2] - 1, mouth_window[3] - 1))

    groups = {"eyes": eyes, "eyebrows": brows, "mouths": mouths}
    classified = {id(c) for comps in groups.values() for c in comps}
    protect = faceless.paint(original.size, (0, 0),
                             [c["pixels"] for c in found if id(c) not in classified])
    protect = protect.filter(ImageFilter.MaxFilter(3))

    # The dilated eye and eyebrow masks overlap by a few rows of skin between
    # the lash line and the brow. Left overlapping, both layers would extract
    # the same pixels and compositing them would apply the difference twice, so
    # the masks are made mutually exclusive in category order.
    empty = Image.new("L", original.size, 0)
    masks: dict[str, Image.Image] = {}
    taken = empty.copy()
    for name in ("eyes", "eyebrows", "mouths"):
        mask = faceless.paint(original.size, (0, 0), [c["pixels"] for c in groups[name]])
        mask = mask.filter(ImageFilter.MaxFilter(faceless.DILATE_RADIUS * 2 + 1))
        mask = Image.composite(empty, mask, protect)
        mask = Image.composite(empty, mask, taken)
        masks[name] = mask
        taken = Image.composite(mask, taken, mask)
    return masks


def extract(original: Image.Image, skin: Image.Image, mask: Image.Image) -> Image.Image:
    """Solve original = layer over skin, inside mask."""
    width, height = original.size
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    source = original.load()
    plate = skin.load()
    region = mask.load()
    target = layer.load()

    box = mask.getbbox()
    if box is None:
        return layer
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            if region[x, y] == 0:
                continue
            sr, sg, sb, sa = source[x, y]
            pr, pg, pb, _ = plate[x, y]
            if sa < 8:
                continue
            distance = max(abs(sr - pr), abs(sg - pg), abs(sb - pb))
            coverage = min(1.0, distance / FULL_COVER)
            alpha = round(coverage * sa)
            if alpha < ALPHA_FLOOR:
                continue
            solve = max(coverage, COLOUR_COVERAGE_FLOOR)
            colour = []
            for channel, plate_value in ((sr, pr), (sg, pg), (sb, pb)):
                value = plate_value + (channel - plate_value) / solve
                colour.append(min(255, max(0, round(value))))
            target[x, y] = (colour[0], colour[1], colour[2], alpha)
    return layer


def round_trip_error(original: Image.Image, skin: Image.Image,
                     layers: list[Image.Image]) -> tuple[int, tuple[int, int]]:
    """Worst per-channel error after compositing the layers back over the skin."""
    rebuilt = skin.copy()
    for layer in layers:
        rebuilt.alpha_composite(layer)

    source = original.load()
    check = rebuilt.load()
    worst, where = 0, (0, 0)
    x0, y0, x1, y1 = faceless.FACE_WINDOW
    for y in range(y0, y1):
        for x in range(x0, x1):
            sr, sg, sb, sa = source[x, y]
            cr, cg, cb, ca = check[x, y]
            if sa < 8:
                continue
            error = max(abs(sr - cr), abs(sg - cg), abs(sb - cb))
            if error > worst:
                worst, where = error, (x, y)
    return worst, where


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True,
                        help="base master as it was before the face removal")
    parser.add_argument("--faceless", type=Path,
                        default=Path("assets/base_bodies/base_body_001_neutral_master.png"))
    parser.add_argument("--out-dir", type=Path,
                        default=Path("images/trait_candidates"))
    args = parser.parse_args(argv)

    if args.out_dir.resolve().is_relative_to(Path("assets").resolve()):
        raise SystemExit("refusing to write candidates under assets/")

    original = Image.open(args.original).convert("RGBA")
    skin = Image.open(args.faceless).convert("RGBA")
    if original.size != skin.size:
        raise SystemExit("original and faceless renders must share the canvas")

    masks = feature_masks(original)
    layers = {}
    for name, mask in masks.items():
        layer = extract(original, skin, mask)
        layers[name] = layer
        destination = args.out_dir / name / CATEGORY_PATHS[name]
        destination.parent.mkdir(parents=True, exist_ok=True)
        layer.save(destination)
        bounds = layer.getchannel("A").getbbox()
        opaque = sum(1 for p in layer.getchannel("A").tobytes() if p == 255)
        print(f"  {name:9s} bounds {bounds}  opaque px {opaque}  -> {destination}")

    worst, where = round_trip_error(original, skin, list(layers.values()))
    print(f"\nround trip: worst channel error {worst} at {where}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
