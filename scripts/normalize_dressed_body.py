#!/usr/bin/env python3
"""Normalize a dressed-body render onto the locked rig as a pose-bound outfit.

The collection's outfits were first painted as isolated garment layers to be
composited over a bare base body. Eight of ten never met the body they were
drawn for: the base's cream tank showed beside the garment at the waist and a
crescent of bare shoulder showed under the sleeve, and every repair that
warped, filled or stretched the garment edge was rendered, looked at, and
reverted (docs/handoff/outfit-refit-brief.md).

A *dressed body* takes the other route. The base pose and its outfit are painted
as one figure - bald, faceless, on the base's own proportions - so there is no
seam between garment and body to fit. It is registered as a pose-bound outfit
that ``hides`` its base in the render (see ``hides`` in config/compatibility.json):
the base still binds the pose, the hand objects and the metadata, and the face,
hair and head traits layer onto the dressed figure exactly as they do onto a
base.

This tool turns one generator render into a review candidate. It never edits
its source.

1. **Alpha.** An RGBA source keeps its own alpha. Generator mattes top out near
   252 rather than 255 and trail a low-alpha halo round the silhouette, so the
   interior is re-levelled to fully opaque and the halo below ``RGBA_HAZE`` is
   cleared. An RGB source must be painted on pure black. It is keyed by treating
   every near-black pixel as background - including the enclosed gaps under the
   arms and through a torn cloak, which are the same black - and by giving the
   silhouette's outer ``KEY_BAND`` pixels partial alpha in proportion to their
   brightness against the art just inside them. Colour is un-premultiplied from
   black, so an edge carries the art's colour rather than the key's. A black
   garment cannot be keyed off black; supply those as RGBA.
2. **Isolation.** Only the figure's connected silhouette is kept. Specks the
   generator scattered across the canvas are dropped and counted.
3. **Fit.** The crown goes on Y141, the head's centre on X627 and the soles on
   Y1139. The head and the body are reduced separately, because a render can
   draw the head at the rig's size and the legs long: the first black-robe
   renders did exactly that, and one uniform reduction to bring their soles up
   to Y1139 shrank the head by up to 7%, which put the shared mouth trait on the
   chin and the eye patches on the ears. So the head is scaled to put the chin
   on ``CHIN_Y``, where the other fifteen renders put it, and the body below the
   chin is scaled to land the soles; the two scales blend over ``BLEND_ROWS``
   of neck, below the face. When a render already has the rig's proportions the
   two scales agree and the fit is one uniform reduction. Enlargement is
   refused on either zone: a render smaller than the rig has to be generated
   again, not stretched. Resampling is premultiplied, separable Lanczos-3
   widened for the reduction, so no key colour bleeds into the edge.

Example:
    python scripts/normalize_dressed_body.py \\
      /abs/path/images/trait_candidates/outfits_dressed/<source>.png \\
      --out incoming/dressed_bodies/outfit_007_brown_leather_long_coat_pose_002.png
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
CENTER_X = 627
TOP_OF_HEAD_Y = 141
FOOT_BASELINE_Y = 1139
MAX_BOUNDS = (233, 129, 1021, 1139)

# Keying an RGB render off black. Brightness is the brightest channel, 0-255.
KEY_FLOOR = 8          # at or below this a pixel is background (the renders' black is 0-6)
KEY_OPAQUE = 64        # a boundary pixel this bright is opaque paint, not a blend with black
KEY_REFERENCE_FLOOR = 24
KEY_BAND = 2           # how many outer pixels of the silhouette may be partial
KEY_CORE = 3           # pixels this far inside are the reference for the band
KEY_MIN_ALPHA = 0.08   # dimmer blends than this are the generator's halo, not an edge

# Re-levelling an RGBA render's own matte.
RGBA_HAZE = 24         # the generators' halo sits at alpha 1-20 round the figure
RGBA_INTERIOR = 200    # alpha this high is interior; its median is the matte's ceiling

MIN_KEPT_COMPONENT = 200  # px; a separate piece this large is kept as art, not a speck
SOLID = 0.5               # alpha at which a row counts toward the crown or the soles
HEAD_BAND = (40, 200)     # rows below the crown whose centre is the head's centre
NECK_SEARCH = (250, 420)  # rows below the crown searched for the narrowest row, under the chin
# Where the narrowest row under the chin lands. Fifteen of the first twenty renders
# put it at Y459-463 after a uniform fit and take every face trait cleanly; the
# shared mouth reaches Y458, so a chin much higher than this lands on it.
CHIN_Y = 461
BLEND_ROWS = 50           # source rows below the chin over which head scale gives way to body scale
LANCZOS_LOBES = 3
OUTPUT_HAZE = 2 / 255     # resampling ringing below this is cleared


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key_from_black(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Recover (colour, alpha) from a render painted on black.

    Near-black is background only where it is at least three pixels across. The
    renders draw their contour lines in near-black too - the navy coat's gold trim
    is ringed with it - and a line one pixel wide keyed out as background left up
    to 900 pinholes per figure that showed the backdrop through the boots and
    cuffs. The gaps that really are background - under the arms, between fingers
    that touch, through a torn cloak - are wider than that, so a 3 x 3 opening
    keeps them and hands every thinner run back to the paint.
    """
    colour = rgb[..., :3].astype(np.float32)
    brightness = colour.max(axis=2)
    near_black = np.pad(brightness <= KEY_FLOOR, 2, constant_values=True)
    background = ndi.binary_opening(near_black, structure=np.ones((3, 3), bool))[2:-2, 2:-2]
    depth = ndi.distance_transform_cdt(~background, metric="chessboard")
    core = depth >= KEY_CORE
    reference = ndi.maximum_filter(np.where(core, brightness, 0.0), size=5)
    reference = np.where(
        reference > 0, np.clip(reference, KEY_REFERENCE_FLOOR, KEY_OPAQUE), KEY_OPAQUE
    )

    alpha = np.ones(brightness.shape, np.float32)
    band = ~background & (depth <= KEY_BAND)
    alpha[band] = np.clip(
        (brightness[band] - KEY_FLOOR) / (reference[band] - KEY_FLOOR), 0.0, 1.0
    )
    alpha[background] = 0.0
    alpha[alpha < KEY_MIN_ALPHA] = 0.0
    straight = np.clip(colour / np.maximum(alpha[..., None], 1e-6), 0.0, 255.0)
    straight[alpha <= 0] = 0.0
    return straight, alpha


def relevel_alpha(rgba: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Return (colour, alpha, ceiling) with the matte's interior made fully opaque."""
    colour = rgba[..., :3].astype(np.float32)
    raw = rgba[..., 3].astype(np.float32)
    interior = raw[raw >= RGBA_INTERIOR]
    if interior.size == 0:
        raise ValueError("RGBA source has no interior alpha at or above "
                         f"{RGBA_INTERIOR}; it is not an isolated figure")
    ceiling = float(np.median(interior))
    alpha = np.clip((raw - RGBA_HAZE) / (ceiling - RGBA_HAZE), 0.0, 1.0)
    colour[alpha <= 0] = 0.0
    return colour, alpha, ceiling


def keep_figure(colour: np.ndarray, alpha: np.ndarray) -> dict[str, int]:
    """Zero every piece not attached to the figure, in place; report what went."""
    labels, count = ndi.label(alpha > 0, structure=np.ones((3, 3), bool))
    if count == 0:
        raise ValueError("source has no visible pixels after alpha recovery")
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    largest = int(sizes.argmax())
    keep = (sizes >= MIN_KEPT_COMPONENT)
    keep[largest] = True
    keep[0] = False
    dropped = ~keep[labels] & (labels > 0)
    alpha[dropped] = 0.0
    colour[dropped] = 0.0
    return {
        "components": int(count),
        "kept_components": int(keep.sum()),
        "dropped_components": int(count - keep.sum()),
        "dropped_pixels": int(dropped.sum()),
    }


def measure(alpha: np.ndarray) -> dict[str, float]:
    """Crown, chin and sole rows and the head's centre, on solid pixels."""
    solid = alpha >= SOLID
    rows = np.nonzero(solid.any(axis=1))[0]
    if rows.size == 0:
        raise ValueError("source has no solid pixels")
    top, bottom = int(rows.min()), int(rows.max())
    centres = []
    for y in range(top + HEAD_BAND[0], top + HEAD_BAND[1]):
        xs = np.nonzero(solid[y])[0]
        if xs.size:
            centres.append((xs.min() + xs.max() + 1) / 2.0)
    if not centres:
        raise ValueError("could not measure the head")
    widths = solid.sum(axis=1)
    lo, hi = top + NECK_SEARCH[0], min(top + NECK_SEARCH[1], bottom)
    if hi <= lo:
        raise ValueError("figure is too short to find the chin")
    chin = lo + int(np.argmin(widths[lo:hi]))
    return {"top_row": top, "chin_row": chin, "bottom_row": bottom,
            "head_center": float(np.median(centres))}


def _lanczos(x: np.ndarray) -> np.ndarray:
    out = np.sinc(x) * np.sinc(x / LANCZOS_LOBES)
    out[np.abs(x) >= LANCZOS_LOBES] = 0.0
    return out


def _weights(centres: np.ndarray, scales: np.ndarray, size: int) -> np.ndarray:
    """(outputs x size) weights sampling a source axis at continuous `centres`.

    Output pixel i reads the source at centres[i] through a Lanczos kernel
    widened by 1/scales[i], so a reduction averages rather than aliases.
    """
    matrix = np.zeros((centres.size, size), np.float32)
    for index, (centre, scale) in enumerate(zip(centres, scales)):
        reach = LANCZOS_LOBES / scale
        taps = np.arange(max(int(np.floor(centre - reach)), 0),
                         min(int(np.ceil(centre + reach)) + 1, size))
        if taps.size == 0:
            continue
        kernel = _lanczos((taps + 0.5 - centre) * scale)
        total = kernel.sum()
        if total != 0:
            matrix[index, taps] = kernel / total
    return matrix


def zone_scales(measured: dict[str, float]) -> tuple[float, float]:
    """(head scale, body scale): the chin onto CHIN_Y, then the soles onto the baseline.

    Below the chin the scale blends from head to body over BLEND_ROWS; a smoothstep
    blend spends half its rows at each scale on average, so the body scale is
    solved with that allowance or the soles would miss the baseline by
    (head - body) * BLEND_ROWS / 2 px.
    """
    head = min(1.0, (CHIN_Y - TOP_OF_HEAD_Y) / (measured["chin_row"] - measured["top_row"]))
    chin_out = TOP_OF_HEAD_Y + head * (measured["chin_row"] - measured["top_row"])
    below = measured["bottom_row"] + 1 - measured["chin_row"]
    body = (FOOT_BASELINE_Y + 1 - chin_out - head * BLEND_ROWS / 2) / (below - BLEND_ROWS / 2)
    return head, body


def row_scale(y: np.ndarray, chin: float, head: float, body: float) -> np.ndarray:
    """Scale at source row y: head scale to the chin, smoothstep to body scale below it."""
    t = np.clip((y - chin) / BLEND_ROWS, 0.0, 1.0)
    return head + (body - head) * t * t * (3 - 2 * t)


def resample(colour: np.ndarray, alpha: np.ndarray, measured: dict[str, float],
             head: float, body: float) -> tuple[np.ndarray, np.ndarray]:
    """Two-zone premultiplied resample onto the canvas.

    Source row y lands at Y141 + the integral of the row scale from the crown;
    within a row, x lands at X627 + scale * (x - head centre). The vertical pass
    runs first, then each output row is resampled at its own scale - exact where
    the scale is constant and a negligible approximation over the neck blend.
    """
    height, width = alpha.shape
    top, chin = float(measured["top_row"]), float(measured["chin_row"])
    grid = np.linspace(0.0, float(height), height * 8 + 1)
    scale_grid = row_scale(grid, chin, head, body)
    increments = (scale_grid[1:] + scale_grid[:-1]) / 2 * np.diff(grid)
    landed = np.concatenate([[0.0], np.cumsum(increments)])
    landed += TOP_OF_HEAD_Y - np.interp(top, grid, landed)

    out_centres = np.arange(CANVAS) + 0.5
    src_rows = np.interp(out_centres, landed, grid)
    rows_scale = row_scale(src_rows, chin, head, body)
    vertical = _weights(src_rows, rows_scale, height)

    premultiplied = colour * alpha[..., None]
    planes = np.concatenate([premultiplied, alpha[..., None]], axis=2).astype(np.float32)
    stacked = vertical @ planes.reshape(height, -1)
    stacked = stacked.reshape(CANVAS, width, 4)

    out = np.zeros((CANVAS, CANVAS, 4), np.float32)
    keys = np.round(rows_scale, 6)
    for key in np.unique(keys):
        members = np.nonzero(keys == key)[0]
        src_cols = measured["head_center"] + (out_centres - (CENTER_X + 0.5)) / key
        horizontal = _weights(src_cols, np.full(CANVAS, key), width)
        block = stacked[members].transpose(1, 0, 2).reshape(width, -1)
        result = (horizontal @ block).reshape(CANVAS, members.size, 4)
        out[members] = result.transpose(1, 0, 2)

    out_alpha = np.clip(out[..., 3], 0.0, 1.0)
    out_alpha[out_alpha < OUTPUT_HAZE] = 0.0
    straight = np.clip(out[..., :3] / np.maximum(out_alpha[..., None], 1e-6), 0.0, 255.0)
    straight[out_alpha <= 0] = 0.0
    return straight, out_alpha


def normalize(source_path: Path) -> tuple[Image.Image, dict[str, Any]]:
    with Image.open(source_path) as probe:
        probe.load()
        source_mode, source_size = probe.mode, probe.size
        array = np.asarray(probe.convert("RGBA" if "A" in probe.getbands() else "RGB"))
    if source_size != (CANVAS, CANVAS):
        raise ValueError(f"source must be {CANVAS} x {CANVAS}; got {source_size}")

    if array.shape[2] == 4:
        colour, alpha, ceiling = relevel_alpha(array)
        recovery: dict[str, Any] = {
            "method": "relevel_generator_matte",
            "haze_threshold": RGBA_HAZE,
            "measured_interior_ceiling": ceiling,
        }
    else:
        colour, alpha = key_from_black(array)
        recovery = {
            "method": "key_from_black_unpremultiplied",
            "floor": KEY_FLOOR,
            "opaque": KEY_OPAQUE,
            "band_px": KEY_BAND,
            "min_alpha": KEY_MIN_ALPHA,
        }
    recovery["isolation"] = keep_figure(colour, alpha)

    measured = measure(alpha)
    head, body = zone_scales(measured)
    if body > 1.0:
        raise ValueError(
            f"the body spans rows {measured['chin_row']}-{measured['bottom_row']}; landing its soles "
            f"on Y{FOOT_BASELINE_Y} would enlarge it by {body:.4f}. Reduction only: generate it "
            "again at the rig's scale"
        )
    out_colour, out_alpha = resample(colour, alpha, measured, head, body)

    # Resampling blurs a pixel either side of the crown and soles; the rig's rows win.
    out_alpha[:TOP_OF_HEAD_Y] = 0.0
    out_alpha[FOOT_BASELINE_Y + 1:] = 0.0
    alpha8 = np.rint(out_alpha * 255).astype(np.uint8)
    colour8 = np.rint(out_colour).astype(np.uint8)
    colour8[alpha8 == 0] = 0
    output = Image.fromarray(np.dstack([colour8, alpha8]), "RGBA")

    bbox = output.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("normalized figure is empty")
    left, top, right, bottom = bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1
    if top != TOP_OF_HEAD_Y or bottom != FOOT_BASELINE_Y:
        raise ValueError(f"normalized figure spans Y{top}-Y{bottom}; the rig is "
                         f"Y{TOP_OF_HEAD_Y}-Y{FOOT_BASELINE_Y}")
    if left < MAX_BOUNDS[0] or right > MAX_BOUNDS[2]:
        raise ValueError(f"normalized figure spans X{left}-X{right}; the rig allows "
                         f"X{MAX_BOUNDS[0]}-X{MAX_BOUNDS[2]}")

    try:
        recorded_source = source_path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        recorded_source = source_path.as_posix()
    report: dict[str, Any] = {
        "origin": "dressed_body_render",
        "source_path": recorded_source,
        "source_sha256": sha256_file(source_path),
        "source_dimensions": list(source_size),
        "source_mode": source_mode,
        "alpha_recovery": recovery,
        "fit": {
            "method": "two_zone_premultiplied_lanczos_reduction",
            "source_crown_row": measured["top_row"],
            "source_chin_row": measured["chin_row"],
            "source_sole_row": measured["bottom_row"],
            "source_head_center_x": round(measured["head_center"], 2),
            "head_scale": round(head, 6),
            "body_scale": round(body, 6),
            "blend_rows_below_chin": BLEND_ROWS,
            "output_bounds": [left, top, right, bottom],
        },
        "normalization_script": "scripts/normalize_dressed_body.py",
    }
    return output, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="immutable 1254 x 1254 render (RGBA, or RGB on black)")
    parser.add_argument("--out", type=Path, required=True, help="normalized review candidate PNG")
    parser.add_argument("--report", type=Path, help="provenance JSON; defaults beside --out")
    args = parser.parse_args(argv)

    output, report = normalize(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.out)
    report["output_sha256"] = sha256_file(args.out)
    report_path = args.report or args.out.with_suffix(".provenance.json")
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    fit = report["fit"]
    print(f"Wrote {args.out}  head {fit['head_scale']:.4f}  body {fit['body_scale']:.4f}  "
          f"bounds {fit['output_bounds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
