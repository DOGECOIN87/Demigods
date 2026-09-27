#!/usr/bin/env python3
"""Fit a render of a hand holding an item onto the body, and make a review sheet.

The round-2 painted-in-hand objects (006, 007, 008 and 012) were fitted this way;
see prompts/hand_objects_handover_2026-09-27.md. It never writes into the
repository: output goes to --out, by default /tmp/in_hand_fits/ITEM for fit and
/tmp/in_hand_fits/<source name> for overview and zoom. Once a fit is chosen, add
its scale and offset to a batch in scripts/register_in_hand_objects.py and run
that script to register it.

The render is cleaned the same way registration cleans it (alpha below 16 is
dropped, specks under 0.2% of the largest piece are removed), reduced by SCALE
and pasted so the painted hand's centre (CX, CY, in source px) lands on the
centre of the body's own hand; then alpha of 250 or more is set to 255, as
registration does, so the layer matches what registration will write.

Usage:
  python scripts/fit_in_hand_render.py overview SOURCE [--out DIR]
      render downscaled with a 100 px grid in SOURCE px
  python scripts/fit_in_hand_render.py zoom SOURCE X0 Y0 X1 Y1 [--out DIR]
      source crop with a 25 px grid, labels in SOURCE px
  python scripts/fit_in_hand_render.py measure SOURCE POSE X0 Y0 X1 Y1
      skin extent, width and centre of the painted hand inside that SOURCE box, plus the body hand's.
      Keep the box tight round the hand: cream pages and parchment count as skin.
  python scripts/fit_in_hand_render.py fit SOURCE ITEM CX CY WIDTH [--scale S] [--tag T] [--out DIR]
      without --scale, the painted hand (WIDTH source px wide) is reduced to the body hand's width;
      with --scale, that reduction is used instead (e.g. to keep the item at its old size).
      Writes layerT.png, reviewT.png and metricsT.json. The review compares the fit with the
      item's old art (commit 788454a, before the in-hand versions), drawn as it rendered then.

ITEM is the hand object number (001 to 012); its pose comes from its registered asset name.
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

try:
    from scripts import hidden_layers
    from scripts.register_in_hand_objects import CANVAS, OPAQUE_FROM, clean_render
except ImportError:  # Direct execution from scripts/.
    import hidden_layers  # type: ignore[no-redef]
    from register_in_hand_objects import CANVAS, OPAQUE_FROM, clean_render  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parent.parent
# the last commit before the in-hand versions replaced the hand objects: the old art, and its size
OLD_ART_COMMIT = "788454a"
BASE = {
    2: {"path": ROOT / "assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png",
        # the hand below the wrist line
        "hand_poly": [(370, 736), (440, 730), (492, 746), (492, 835), (370, 835)],
        "outfits": ["outfit_007_brown_leather_long_coat_pose_002.png", "outfit_009_navy_high_collar_coat_pose_002.png",
                    "outfit_002_storm_guardian_pose_002.png", "outfit_008_olive_ragged_cloak_pose_002.png"]},
    4: {"path": ROOT / "assets/base_bodies/base_pose_004_viewer_left_palm_up.png",
        "hand_poly": [(360, 715), (445, 708), (492, 728), (492, 800), (360, 800)],
        "outfits": ["outfit_007_brown_leather_long_coat_pose_004.png", "outfit_009_navy_high_collar_coat_pose_004.png",
                    "outfit_004_lunar_oracle_pose_004.png", "outfit_008_olive_ragged_cloak_pose_004.png",
                    "outfit_006_black_layered_hooded_robe_pose_004.png"]},
}
BG = (235, 235, 240, 255)


def skin_mask(rgba: np.ndarray) -> np.ndarray:
    r, g, b, a = [rgba[..., i].astype(int) for i in range(4)]
    return (a > 128) & (r > 190) & (r - b > 25) & (r - b < 120) & (g > 130) & (r >= g) & (g >= b - 5)


def skin_stats(rgba: np.ndarray, region: np.ndarray) -> dict | None:
    m = skin_mask(rgba) & region
    m = ndimage.binary_closing(m, iterations=2) & region
    lab, n = ndimage.label(m)
    if n == 0:
        return None
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 0.05 * sizes.max()])
    ys, xs = np.nonzero(keep)
    return {"bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
            "width": int(xs.max() - xs.min() + 1), "height": int(ys.max() - ys.min() + 1),
            "centroid": [round(float(xs.mean()), 1), round(float(ys.mean()), 1)], "pixels": int(keep.sum())}


def poly_mask(poly, size=CANVAS) -> np.ndarray:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m) > 0


def base_hand(pose: int) -> dict:
    base = Image.open(BASE[pose]["path"]).convert("RGBA")
    return {"image": base, **skin_stats(np.asarray(base), poly_mask(BASE[pose]["hand_poly"]))}


def registered_asset(item: str) -> Path:
    matches = glob.glob(str(ROOT / f"assets/hand_objects/hand_object_{item}_*.png"))
    if len(matches) != 1:
        raise SystemExit(f"hand object {item}: expected one registered asset, found {matches}")
    return Path(matches[0])


def pose_of(item: str) -> int:
    name = registered_asset(item).name
    return int(name.split("_pose_")[1][:3])


def old_art(item: str) -> Image.Image:
    """The item's art before the in-hand work: the size the fit should keep."""
    rel = registered_asset(item).relative_to(ROOT).as_posix()
    data = subprocess.run(["git", "-C", str(ROOT), "show", f"{OLD_ART_COMMIT}:{rel}"],
                          capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data)).convert("RGBA")


def body_under(pose: int, outfit: str | None, base: Image.Image) -> Image.Image:
    """The body as the renderer draws it: a dressed outfit hides the base body, any other goes over it."""
    canvas = Image.new("RGBA", CANVAS, BG)
    if outfit is None or outfit not in hidden_layers.dressed_outfits():
        canvas.alpha_composite(base)
    if outfit is not None:
        canvas.alpha_composite(Image.open(ROOT / "assets/outfits" / outfit).convert("RGBA"))
    return canvas


def on_bg(im: Image.Image, colour=(120, 170, 120, 255)) -> Image.Image:
    bg = Image.new("RGBA", im.size, colour)
    bg.alpha_composite(im)
    return bg


def grid(im: Image.Image, step: int, scale: float, origin=(0, 0)) -> Image.Image:
    d = ImageDraw.Draw(im)
    w, h = im.size
    x = 0
    while x * scale <= w:
        d.line([(x * scale, 0), (x * scale, h)], fill=(255, 0, 0))
        d.text((x * scale + 2, 2), str(origin[0] + x), fill=(200, 0, 0))
        x += step
    y = 0
    while y * scale <= h:
        d.line([(0, y * scale), (w, y * scale)], fill=(0, 0, 255))
        d.text((2, y * scale + 2), str(origin[1] + y), fill=(0, 0, 200))
        y += step
    return im


def cmd_overview(source: Path, out: Path) -> None:
    im = on_bg(clean_render(source))
    k = 4 if im.width > 1500 else 2
    small = im.resize((im.width // k, im.height // k)).convert("RGB")
    out.mkdir(parents=True, exist_ok=True)
    grid(small, 100, 1 / k).save(out / "overview.png")
    print(out / "overview.png")


def cmd_zoom(source: Path, box: tuple[int, int, int, int], out: Path) -> None:
    x0, y0, x1, y1 = box
    im = on_bg(clean_render(source)).crop(box)
    scale = min(3.0, 900 / max(x1 - x0, y1 - y0))
    im = im.resize((round(im.width * scale), round(im.height * scale))).convert("RGB")
    out.mkdir(parents=True, exist_ok=True)
    grid(im, 25, scale, (x0, y0)).save(out / "zoom.png")
    print(out / "zoom.png")


def cmd_measure(source: Path, pose: int, box: tuple[int, int, int, int]) -> None:
    render = np.asarray(clean_render(source))
    region = np.zeros(render.shape[:2], bool)
    x0, y0, x1, y1 = box
    region[y0:y1, x0:x1] = True
    b = base_hand(pose)
    print(json.dumps({"painted_hand": skin_stats(render, region),
                      "base_hand": {k: b[k] for k in ("bbox", "width", "height", "centroid")}}, indent=1))


def cmd_fit(source: Path, item: str, cx: float, cy: float, width: float, scale: float | None, tag: str, out: Path) -> None:
    pose = pose_of(item)
    b = base_hand(pose)
    base = b["image"]
    render = clean_render(source)
    sb = render.getchannel("A").getbbox()
    source_touches_edge = bool(sb and (sb[0] == 0 or sb[1] == 0 or sb[2] == render.width or sb[3] == render.height))
    if scale is None:
        scale = b["width"] / width
    if scale <= 0:
        raise SystemExit(f"scale {scale}: must be above 0")
    if scale > 1:
        raise SystemExit(f"scale {scale:.4f}: renders are only ever reduced, never enlarged; a render drawn "
                         "smaller than the body needs a new render")
    size = (round(render.width * scale), round(render.height * scale))
    reduced = render.resize(size, Image.Resampling.LANCZOS)
    ox, oy = round(b["centroid"][0] - cx * scale), round(b["centroid"][1] - cy * scale)
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    layer.paste(reduced, (ox, oy), reduced)
    pixels = np.asarray(layer).copy()
    pixels[..., 3][pixels[..., 3] >= OPAQUE_FROM] = 255
    layer = Image.fromarray(pixels, "RGBA")
    la = pixels[..., 3]
    lb = layer.getchannel("A").getbbox()
    if lb is None:
        raise SystemExit("the fitted layer is empty: the offset puts the render off the canvas")
    touches_edge = lb[0] == 0 or lb[1] == 0 or lb[2] == CANVAS[0] or lb[3] == CANVAS[1]

    # body-hand pixels (below the wrist line) the layer leaves showing: they read as a second hand
    pm = poly_mask(BASE[pose]["hand_poly"])
    hand = pm & (np.asarray(base)[..., 3] > 128)
    core = ndimage.binary_erosion(hand, iterations=2)
    uncovered = hand & (la < 128)
    uncovered_core = core & (la < 128)

    old = old_art(item)
    ob = old.getchannel("A").getbbox()

    out.mkdir(parents=True, exist_ok=True)
    layer.save(out / f"layer{tag}.png")

    old_view = Image.new("RGBA", CANVAS, BG)
    old_view.alpha_composite(old)
    old_view.alpha_composite(base)
    tiles = [("old art on bare body", old_view)]
    for label, outfit in [("new on bare body", None)] + [(f"new on {o[7:30]}", o) for o in BASE[pose]["outfits"][:2]]:
        view = body_under(pose, outfit, base)
        view.alpha_composite(layer)
        tiles.append((label, view))
    W, H = 330, 495
    hx, hy = b["centroid"]
    zbox = (int(hx - 110), int(hy - 110), int(hx + 110), int(hy + 110))
    sheet = Image.new("RGB", (W * 4, H + 20 + 330 + 20), "white")
    d = ImageDraw.Draw(sheet)
    for i, (label, t) in enumerate(tiles):
        sheet.paste(t.crop((130, 110, 830, 1160)).resize((W, H)).convert("RGB"), (i * W, 18))
        d.text((i * W + 4, 2), label, fill="black")
    for i, (label, t) in enumerate([("grip on bare body", tiles[1][1]), ("grip on " + tiles[2][0][7:], tiles[2][1])]):
        sheet.paste(t.crop(zbox).resize((330, 330), Image.Resampling.LANCZOS).convert("RGB"), (i * W, H + 38))
        d.text((i * W + 4, H + 22), label, fill="black")
    arr = np.full((*CANVAS[::-1], 3), 255, np.uint8)
    arr[hand] = (180, 180, 180)
    arr[(la >= 128) & pm] = (140, 170, 230)
    arr[uncovered] = (230, 40, 40)
    sheet.paste(Image.fromarray(arr).crop(zbox).resize((330, 330), Image.Resampling.NEAREST), (2 * W, H + 38))
    d.text((2 * W + 4, H + 22), "red = body hand left showing", fill="black")
    sheet.paste(on_bg(render).resize((330, 330)).convert("RGB"), (3 * W, H + 38))
    d.text((3 * W + 4, H + 22), "source render", fill="black")
    sheet.save(out / f"review{tag}.png")

    metrics = {
        "item": item, "pose": pose, "source": str(source), "scale": round(scale, 4), "offset": [ox, oy],
        "painted_hand_source": {"centre": [cx, cy], "width": width},
        "base_hand": {"centroid": b["centroid"], "width": b["width"], "bbox": b["bbox"]},
        "output_bounds": [lb[0], lb[1], lb[2] - 1, lb[3] - 1], "touches_canvas_edge": touches_edge,
        "source_touches_edge": source_touches_edge,
        # whole layer (item and painted hand) against the old art (item only)
        "item_height_vs_old": round((lb[3] - lb[1]) / (ob[3] - ob[1]), 3),
        "item_width_vs_old": round((lb[2] - lb[0]) / (ob[2] - ob[0]), 3),
        "painted_hand_vs_body_hand_width": round(width * scale / b["width"], 3),
        "body_hand_pixels": int(hand.sum()), "body_hand_pixels_showing": int(uncovered.sum()),
        "body_hand_core_pixels_showing": int(uncovered_core.sum()),
        "layer": str(out / f"layer{tag}.png"), "review": str(out / f"review{tag}.png"),
    }
    (out / f"metrics{tag}.json").write_text(json.dumps(metrics, indent=1))
    print(json.dumps(metrics, indent=1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("overview"); p.add_argument("source", type=Path); p.add_argument("--out", type=Path)
    p = sub.add_parser("zoom"); p.add_argument("source", type=Path); p.add_argument("box", type=int, nargs=4)
    p.add_argument("--out", type=Path)
    p = sub.add_parser("measure"); p.add_argument("source", type=Path); p.add_argument("pose", type=int, choices=sorted(BASE))
    p.add_argument("box", type=int, nargs=4)
    p = sub.add_parser("fit"); p.add_argument("source", type=Path); p.add_argument("item")
    p.add_argument("cx", type=float); p.add_argument("cy", type=float); p.add_argument("width", type=float)
    p.add_argument("--scale", type=float); p.add_argument("--tag", default=""); p.add_argument("--out", type=Path)
    args = parser.parse_args()
    if getattr(args, "box", None) and (args.box[2] <= args.box[0] or args.box[3] <= args.box[1]):
        parser.error("the box is X0 Y0 X1 Y1 with X1 > X0 and Y1 > Y0")
    if args.command == "fit" and args.width <= 0:
        parser.error("WIDTH is the painted hand's width in source px and must be above 0")
    default_out = Path("/tmp/in_hand_fits") / (getattr(args, "item", None) or args.source.stem)
    out = getattr(args, "out", None) or default_out
    if args.command == "overview":
        cmd_overview(args.source, out)
    elif args.command == "zoom":
        cmd_zoom(args.source, tuple(args.box), out)
    elif args.command == "measure":
        cmd_measure(args.source, args.pose, tuple(args.box))
    else:
        cmd_fit(args.source, args.item, args.cx, args.cy, args.width, args.scale, args.tag, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
