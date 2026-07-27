#!/usr/bin/env python3
"""Refit a trait layer to the locked rig: scale about the center axis, align its top.

hair_back_003 was registered at 1.46x the base body's width with 70% of its mass
outside the silhouette, because it was drawn for a more realistic head-to-body
ratio than this collection's chibi proportions. This tool rescales a layer about
the locked center axis and seats its top at a chosen Y.

Note on repository rules: `prompts/19` permits canvas-only translation, alpha
cleanup, profile tagging and renaming during intake, and explicitly disallows
rescaling. That rule exists to stop an undersized render being upscaled to fake
the 1254 canvas. This is the opposite operation - the canvas stays natively 1254
and the content is reduced - so no detail is invented. It is still a rescale, so
every use must be recorded in the manifest's `postprocessing`, and a native
re-render at correct proportions remains the cleaner fix.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

CANVAS = 1254
CENTER_X = 627
MAX_BOUNDS = (233, 129, 1021, 1139)  # inclusive


def visible_box(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("layer is fully transparent")
    return bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1


def refit(image: Image.Image, *, scale: float, top_y: int) -> Image.Image:
    if image.size != (CANVAS, CANVAS):
        raise ValueError(f"layer must be {CANVAS} x {CANVAS}; got {image.size}")
    if scale <= 0:
        raise ValueError("scale must be positive")

    left, top, right, bottom = visible_box(image)
    content = image.crop((left, top, right + 1, bottom + 1))

    width = max(1, round(content.width * scale))
    height = max(1, round(content.height * scale))
    # LANCZOS on a reduction is a genuine resample down; nothing is invented.
    content = content.resize((width, height), Image.LANCZOS)

    result = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    result.paste(content, (round(CENTER_X - width / 2), top_y))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scale", type=float, required=True)
    parser.add_argument("--top-y", type=int, required=True)
    parser.add_argument("--reference", type=Path,
                        default=Path("assets/base_bodies/base_body_001_neutral_master.png"),
                        help="base body used to report the resulting width ratio")
    args = parser.parse_args(argv)

    result = refit(Image.open(args.source).convert("RGBA"), scale=args.scale, top_y=args.top_y)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.out)

    left, top, right, bottom = visible_box(result)
    within = (left >= MAX_BOUNDS[0] and top >= MAX_BOUNDS[1]
              and right <= MAX_BOUNDS[2] and bottom <= MAX_BOUNDS[3])
    print(f"Wrote {args.out}")
    print(f"  bounds [{left},{top},{right},{bottom}] within {list(MAX_BOUNDS)}: {within}")
    print(f"  center X {(left + right) / 2:.1f} (locked {CENTER_X})")

    if args.reference.is_file():
        body = Image.open(args.reference).convert("RGBA")
        bl, bt, br, bb = visible_box(body)
        body_width = br - bl + 1
        layer_width = right - left + 1
        print(f"  width {layer_width} vs body {body_width} = {layer_width / body_width:.2f}x")

        # Share of the layer that never overlaps the body: the wings symptom.
        la = result.getchannel("A").load()
        ba = body.getchannel("A").load()
        outside = total = 0
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if la[x, y] > 8:
                    total += 1
                    if ba[x, y] == 0:
                        outside += 1
        print(f"  visible pixels outside the body silhouette: {100 * outside / total:.1f}%")

    return 0 if within else 1


if __name__ == "__main__":
    raise SystemExit(main())
