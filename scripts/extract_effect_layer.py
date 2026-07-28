#!/usr/bin/env python3
"""Convert a flat-background effect render into a genuine soft-alpha RGBA layer.

Co-created aura/flame/burst candidates arrive as opaque RGB (or hard-keyed RGBA)
on a flat black or white studio field. Promoting them directly fails the
repository's genuine-alpha rule: the "transparent" area is only the cut corners,
the field itself is baked in as opaque pixels, and a dark baked halo would darken
any background it composites over.

This tool derives alpha analytically from the field instead of keying it out, so
the result is genuinely soft-edged and *bright at every alpha value* -- the same
"only ever adds light" property the procedural aura builders guarantee. It is a
deterministic post-process; every use is recorded in the manifest.

Two fields:

* ``--field black`` (additive glow): alpha comes from the pixel's luminance, so
  black -> fully transparent and bright -> opaque. The colour is un-premultiplied
  (RGB / alpha) so a faint edge keeps its vivid hue instead of fading to grey.
  Use for effects rendered on black (bursts, radiance, glows, light flames).

* ``--field white`` (subtractive / shadow form): alpha comes from how far the
  pixel sits from white, so white -> transparent and a dark, saturated form ->
  opaque. Use for dark "void" effects rendered on white.

The content is centred on the locked X axis and scaled/placed to a target box.
Nothing is invented: a reduction is a genuine resample, and the alpha is a
measured function of the source field.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

try:  # Optional acceleration; the pure-PIL fallback keeps CI (Pillow-only) working.
    import numpy as _np
except ImportError:  # pragma: no cover
    _np = None

CANVAS = 1254
CENTER_X = 627


def luminance(r: int, g: int, b: int) -> float:
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def _assemble(rgb, alpha, floor: int) -> Image.Image:
    """Stack an (H,W,3) uint8 RGB array and (H,W) float [0,1] alpha into RGBA."""
    a8 = (_np.clip(alpha, 0.0, 1.0) * 255.0).round().astype("uint8")
    a8[a8 < floor] = 0
    out = _np.dstack([rgb.astype("uint8"), a8])
    return Image.fromarray(out, "RGBA")


def derive_black_field(im: Image.Image, gamma: float, gain: float, floor: int) -> Image.Image:
    """Additive: alpha = luminance**gamma * gain; colour un-premultiplied to stay vivid."""
    src = im.convert("RGB")
    if _np is not None:
        arr = _np.asarray(src, dtype="float64")
        lum = (0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]) / 255.0
        a = _np.clip((lum ** gamma) * gain, 0.0, 1.0)
        inv = 1.0 / _np.maximum(a, 1e-3)
        rgb = _np.clip(arr * inv[..., None], 0, 255)
        return _assemble(rgb, a, floor)
    w, h = src.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sp = src.load()
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = sp[x, y]
            a = min(1.0, (luminance(r, g, b) ** gamma) * gain)
            if a * 255 < floor:
                continue
            inv = 1.0 / max(a, 1e-3)
            op[x, y] = (min(255, int(round(r * inv))), min(255, int(round(g * inv))),
                        min(255, int(round(b * inv))), int(round(a * 255)))
    return out


def derive_white_field(im: Image.Image, gamma: float, gain: float, floor: int,
                       white_cut: int = 255) -> Image.Image:
    """Subtractive: alpha ramps from a near-white cut down to black; colour kept as drawn.

    ``white_cut`` is the brightest ``min(R,G,B)`` still treated as pure background.
    A studio field is rarely a clean 255, so mapping everything at or above the cut
    to zero alpha removes the faint full-canvas haze that a plain 1-min/255 keying
    leaves behind.
    """
    src = im.convert("RGB")
    cut = max(1, min(255, white_cut))
    if _np is not None:
        arr = _np.asarray(src, dtype="float64")
        mn = arr.min(axis=2)
        coverage = _np.clip((cut - mn) / cut, 0.0, 1.0)
        a = _np.clip((coverage ** gamma) * gain, 0.0, 1.0)
        return _assemble(arr, a, floor)
    w, h = src.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sp = src.load()
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = sp[x, y]
            coverage = max(0.0, min(1.0, (cut - min(r, g, b)) / cut))
            a = min(1.0, (coverage ** gamma) * gain)
            if a * 255 < floor:
                continue
            op[x, y] = (r, g, b, int(round(a * 255)))
    return out


def visible_box(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("derived layer is fully transparent; adjust --gain/--floor")
    return bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1


def _alpha_centroid_x(crop: Image.Image) -> float:
    """Alpha-weighted horizontal centroid within a crop (columns)."""
    a = crop.getchannel("A")
    if _np is not None:
        arr = _np.asarray(a, dtype="float64")
        colw = arr.sum(axis=0)
        total = colw.sum()
        if total <= 0:
            return crop.width / 2.0
        return float((colw * _np.arange(crop.width)).sum() / total)
    hist = [0.0] * crop.width
    ap = a.load()
    for y in range(crop.height):
        for x in range(crop.width):
            hist[x] += ap[x, y]
    total = sum(hist)
    if total <= 0:
        return crop.width / 2.0
    return sum(i * w for i, w in enumerate(hist)) / total


def place(content: Image.Image, target_h: int, center_y: int, recenter_x: bool = False) -> Image.Image:
    """Crop to visible content, scale to target height, centre on the locked X axis.

    With ``recenter_x`` the content is centred by its alpha-weighted centroid rather
    than its bounding box, so a form that leans to one side still lands on X 627.
    """
    left, top, right, bottom = visible_box(content)
    crop = content.crop((left, top, right + 1, bottom + 1))
    scale = target_h / crop.height
    new_w = max(1, round(crop.width * scale))
    new_h = max(1, round(crop.height * scale))
    crop = crop.resize((new_w, new_h), Image.LANCZOS)
    anchor = _alpha_centroid_x(crop) if recenter_x else new_w / 2.0
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    canvas.paste(crop, (round(CENTER_X - anchor), round(center_y - new_h / 2)), crop)
    return canvas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--field", choices=("black", "white"), required=True)
    ap.add_argument("--gamma", type=float, default=1.0, help="alpha response curve; >1 tightens the core")
    ap.add_argument("--gain", type=float, default=1.0, help="multiply derived alpha (brighten the effect)")
    ap.add_argument("--floor", type=int, default=3, help="drop alpha below this (kills 1-2 level dust)")
    ap.add_argument("--white-cut", type=int, default=255,
                    help="white field only: brightest min(R,G,B) still treated as pure background")
    ap.add_argument("--target-height", type=int, help="scale visible content to this height in px")
    ap.add_argument("--center-y", type=int, default=780, help="vertical centre of the placed content")
    ap.add_argument("--recenter-x", action="store_true",
                    help="centre by alpha-weighted centroid instead of bounding box")
    ap.add_argument("--no-place", action="store_true", help="keep native geometry (already 1254 and aligned)")
    args = ap.parse_args(argv)

    im = Image.open(args.source)
    im.load()
    if args.field == "black":
        derived = derive_black_field(im, args.gamma, args.gain, args.floor)
    else:
        derived = derive_white_field(im, args.gamma, args.gain, args.floor, args.white_cut)

    if args.no_place:
        if derived.size != (CANVAS, CANVAS):
            raise SystemExit(f"--no-place requires a {CANVAS}x{CANVAS} source; got {derived.size}")
        result = derived
    else:
        target_h = args.target_height or int(derived.height)
        result = place(derived, target_h, args.center_y, args.recenter_x)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.out)

    a = result.getchannel("A")
    lo, hi = a.getextrema()
    left, top, right, bottom = visible_box(result)
    print(f"Wrote {args.out}")
    print(f"  alpha extrema=({lo},{hi})  visible bounds=[{left},{top},{right},{bottom}]  center_x={(left+right)/2:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
