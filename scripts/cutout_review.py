#!/usr/bin/env python3
"""Remove the background from ONE flattened one-of-one illustration at a time.

The workflow is deliberately per image (see docs/qa/background_removal_2026-10-09.md):

1. ``predict NAME`` runs two segmentation models (isnet-anime and BiRefNet-general)
   on a single source and caches both raw mattes.
2. The image is reviewed by eye and a recipe for that image is written to
   ``recipes/NAME.json``: notes on what is kept and removed, which matte to start
   from, and hand-placed corrections (regions forced to keep or remove, edge
   snapping, colour keys, small-island cleanup).
   ``grid NAME --crop X0 Y0 X1 Y1`` draws a coordinate grid over any region of the
   source, a raw matte or the current result, for placing those corrections.
3. ``render NAME`` applies that image's recipe, writes the transparent PNG and a
   review sheet (cutout over magenta and over dark grey) so the edges, held items
   and foreground items can be checked before moving to the next image.

Models are the rembg ONNX releases, run directly with onnxruntime. Point
``--models`` at a folder containing ``isnet-anime.onnx`` and
``birefnet-general.onnx``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "images/variations/cutouts_2026-10-09"
RECIPE_DIR = OUT_DIR / "recipes"
MODEL_SPECS = {
    "isnet": ("isnet-anime.onnx", (0.485, 0.456, 0.406), (1.0, 1.0, 1.0), False),
    "birefnet": ("birefnet-general.onnx", (0.485, 0.456, 0.406), (0.229, 0.224, 0.225), True),
}


def predict_matte(model_dir: Path, key: str, image: Image.Image) -> np.ndarray:
    import onnxruntime as ort

    import fcntl

    filename, mean, std, sigmoid = MODEL_SPECS[key]
    small = np.asarray(image.convert("RGB").resize((1024, 1024), Image.LANCZOS), dtype=np.float32)
    small /= max(float(small.max()), 1e-6)
    small = (small - np.array(mean, np.float32)) / np.array(std, np.float32)
    tensor = small.transpose(2, 0, 1)[None].astype(np.float32)
    # One model in memory at a time: BiRefNet needs several GB of RAM on CPU.
    with open(model_dir / ".inference.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        session = ort.InferenceSession(str(model_dir / filename), providers=["CPUExecutionProvider"])
        out = session.run(None, {session.get_inputs()[0].name: tensor})[0][0, 0]
        del session
    if sigmoid:
        out = 1.0 / (1.0 + np.exp(-out))
    out = (out - out.min()) / max(float(out.max() - out.min()), 1e-6)
    matte = Image.fromarray((out * 255).astype(np.uint8)).resize(image.size, Image.LANCZOS)
    return np.asarray(matte)


def source_path(name: str) -> Path:
    recipe = load_recipe(name)
    if "source" in recipe:
        return ROOT / recipe["source"]
    return ROOT / "images/variations/complete_72" / f"{name}.png"


def cache_dir(args) -> Path:
    path = Path(args.cache)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_recipe(name: str) -> dict:
    path = RECIPE_DIR / f"{name}.json"
    return json.loads(path.read_text()) if path.exists() else {}


def poly_mask(shape, polys) -> np.ndarray:
    canvas = Image.new("L", (shape[1], shape[0]), 0)
    draw = ImageDraw.Draw(canvas)
    for pts in polys:
        draw.polygon([tuple(p) for p in pts], fill=255)
    return np.asarray(canvas) > 0


def apply_recipe(rgb: np.ndarray, mattes: dict[str, np.ndarray], recipe: dict) -> np.ndarray:
    base = recipe.get("base", "birefnet")
    if base == "max":
        alpha = np.maximum(mattes["isnet"], mattes["birefnet"]).astype(np.float32)
    elif base == "min":
        alpha = np.minimum(mattes["isnet"], mattes["birefnet"]).astype(np.float32)
    else:
        alpha = mattes[base].astype(np.float32)
    lo, hi = recipe.get("levels", [8, 247])
    alpha = np.clip((alpha - lo) / max(hi - lo, 1) * 255.0, 0, 255)

    for op in recipe.get("ops", []):
        kind = op["op"]
        region = poly_mask(alpha.shape, op["polys"]) if "polys" in op else None
        if kind == "use":  # take another model's matte (or the min of both) inside the region
            if op["model"] == "min":
                alt = np.minimum(mattes["isnet"], mattes["birefnet"]).astype(np.float32)
            else:
                alt = mattes[op["model"]].astype(np.float32)
            ulo, uhi = op.get("levels", [lo, hi])
            alt = np.clip((alt - ulo) / max(uhi - ulo, 1) * 255.0, 0, 255)
            if op.get("combine") == "max":  # add the other matte without weakening this one
                alt = np.maximum(alt, alpha)
            alpha[region] = alt[region]
        elif kind == "keep":  # region is entirely subject
            if op.get("feather"):  # soft edge for depth-blurred foreground props
                soft = cv2.GaussianBlur(region.astype(np.float32), (0, 0), op["feather"]) * 255
                alpha = np.maximum(alpha, soft)
            else:
                alpha[region] = 255
        elif kind == "drop_dark":  # inside region, fade out pixels darker than the bright subject (sky seen through effect loops)
            lum = rgb.astype(np.float32).mean(axis=2)
            d0, d1 = op["ramp"]
            factor = np.clip((lum - d0) / (d1 - d0), 0, 1)
            factor = cv2.GaussianBlur(factor, (0, 0), op.get("feather", 0.8))
            alpha[region] = alpha[region] * factor[region]
        elif kind == "drop_warm":  # inside region, fade out pixels warmer (red minus blue) than the cool item
            warm = rgb[..., 0].astype(np.float32) - rgb[..., 2].astype(np.float32)
            w0, w1 = op["ramp"]
            factor = np.clip((w1 - warm) / (w1 - w0), 0, 1)
            factor = cv2.GaussianBlur(factor, (0, 0), op.get("feather", 0.7))
            alpha[region] = alpha[region] * factor[region]
        elif kind == "key_rb":  # inside region, opacity from red-minus-blue (warm props on cool water/sky)
            score = rgb[..., 0].astype(np.float32) - rgb[..., 2].astype(np.float32)
            if op.get("invert"):
                score = -score
            k0, k1 = op["ramp"]
            keyed = np.clip((score - k0) / (k1 - k0), 0, 1) * 255
            keyed = cv2.GaussianBlur(keyed, (0, 0), op.get("feather", 1.0))
            keyed[~region] = 0
            alpha = np.maximum(alpha, keyed)
        elif kind == "remove":  # region is entirely background
            alpha[region] = 0
        elif kind == "remove_color":  # inside region, drop pixels near a background colour
            ref = np.array(op["rgb"], np.float32)
            dist = np.linalg.norm(rgb.astype(np.float32) - ref, axis=2)
            hit = dist < op.get("tol", 30)
            if region is not None:
                hit &= region
            alpha[hit] = 0
        elif kind == "submatte":  # model re-run on a crop, for foreground props at the frame edge
            x0, y0, x1, y1 = op["box"]
            sub = mattes[f"sub:{op.get('model', 'birefnet')}:{x0},{y0},{x1},{y1}"].astype(np.float32)
            sub = np.clip((sub - lo) / max(hi - lo, 1) * 255.0, 0, 255)
            if "polys" in op:
                sub[~region[y0:y1, x0:x1]] = 0
            alpha[y0:y1, x0:x1] = np.maximum(alpha[y0:y1, x0:x1], sub)
        elif kind == "grabcut":  # snap a hand-drawn shape to real edges inside a local box
            x0, y0, x1, y1 = op["box"]
            gc = np.full((y1 - y0, x1 - x0), cv2.GC_PR_BGD, np.uint8)
            local = alpha[y0:y1, x0:x1]
            gc[local > 200] = cv2.GC_FGD
            fg = poly_mask(alpha.shape, op["fg"])[y0:y1, x0:x1]
            gc[fg & (local <= 200)] = cv2.GC_PR_FGD
            if "sure_fg" in op:
                gc[poly_mask(alpha.shape, op["sure_fg"])[y0:y1, x0:x1]] = cv2.GC_FGD
            if "bg" in op:
                gc[poly_mask(alpha.shape, op["bg"])[y0:y1, x0:x1]] = cv2.GC_BGD
            bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
            cv2.grabCut(np.ascontiguousarray(rgb[y0:y1, x0:x1, ::-1]), gc, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
            cut = np.isin(gc, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.float32)
            sigma = op.get("feather", 0.7)  # wider for depth-blurred foreground props
            cut = cv2.GaussianBlur(cut, (0, 0), sigma) * 255
            if op.get("within_fg", True):  # never grow past the drawn shape
                grow = cv2.dilate(fg.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
                cut[~grow] = np.minimum(cut[~grow], local[~grow])
            alpha[y0:y1, x0:x1] = np.maximum(local, cut)
        elif kind == "keep_matte_above":  # inside region, harden matte >= t to fully opaque
            hit = region & (alpha >= op.get("t", 64))
            alpha[hit] = 255
        elif kind == "fill_holes":  # close enclosed transparent holes smaller than max_area
            solid = alpha > 127
            holes = ndimage.binary_fill_holes(solid) & ~solid
            labels, n = ndimage.label(holes)
            if n:
                sizes = ndimage.sum(holes, labels, range(1, n + 1))
                small = np.isin(labels, np.nonzero(sizes <= op.get("max_area", 400))[0] + 1)
                if region is not None:
                    small &= region
                alpha[small] = 255
        else:
            raise ValueError(f"unknown op {kind}")

    # Drop disconnected specks smaller than min_island (background flecks).
    min_island = recipe.get("min_island", 150)
    if min_island:
        solid = alpha > 24
        labels, n = ndimage.label(solid)
        if n:
            sizes = ndimage.sum(solid, labels, range(1, n + 1))
            tiny = np.isin(labels, np.nonzero(sizes < min_island)[0] + 1)
            alpha[tiny] = 0
    return alpha.astype(np.uint8)


def decontaminate(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Replace colour of soft edge pixels with the nearest solid subject colour."""
    solid = alpha >= 250
    if solid.all() or not solid.any():
        return rgb
    _, idx = ndimage.distance_transform_edt(~solid, return_indices=True)
    nearest = rgb[idx[0], idx[1]]
    a = (alpha.astype(np.float32) / 255.0)[..., None]
    soft = (alpha > 0) & (alpha < 250)
    out = rgb.copy()
    blend = (rgb * a + nearest * (1 - a)).astype(np.uint8)
    out[soft] = blend[soft]
    return out


def review_sheet(rgb: np.ndarray, alpha: np.ndarray, path: Path, crop=None) -> None:
    def panel(bg):
        base = np.empty_like(rgb)
        base[:] = bg
        a = alpha.astype(np.float32)[..., None] / 255.0
        return (rgb * a + base * (1 - a)).astype(np.uint8)

    panels = [rgb, panel((255, 0, 255)), panel((40, 40, 40))]
    if crop:
        x0, y0, x1, y1 = crop
        panels = [p[y0:y1, x0:x1] for p in panels]
    h = panels[0].shape[0]
    scale = 620 / h
    interp = cv2.INTER_AREA if scale < 1 else cv2.INTER_NEAREST
    tiles = [cv2.resize(p, None, fx=scale, fy=scale, interpolation=interp) for p in panels]
    sheet = np.concatenate([np.pad(t, ((0, 0), (0, 6), (0, 0)), constant_values=255) for t in tiles], axis=1)
    Image.fromarray(sheet).save(path)


def cmd_predict(args) -> None:
    src = source_path(args.name)
    with Image.open(src) as im:
        im = im.convert("RGB")
        for key in MODEL_SPECS:
            dest = cache_dir(args) / f"{args.name}.{key}.png"
            if not dest.exists():
                Image.fromarray(predict_matte(Path(args.models), key, im)).save(dest)
    print(f"cached mattes for {args.name}")


def cmd_render(args) -> None:
    recipe = load_recipe(args.name)
    if not recipe:
        raise SystemExit(f"no recipe at {RECIPE_DIR / (args.name + '.json')}")
    rgb, alpha = compute(args, recipe)
    review = cache_dir(args) / f"{args.name}.review.png"
    review_sheet(rgb, alpha, review, args.crop)
    if not args.preview:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"{args.name}.png"
        rgba = np.dstack([decontaminate(rgb, alpha), alpha])
        tmp = out.with_suffix(".tmp.png")
        Image.fromarray(rgba, "RGBA").save(tmp, optimize=True)
        tmp.replace(out)
        print(f"wrote {out.relative_to(ROOT)} sha256={hashlib.sha256(out.read_bytes()).hexdigest()[:12]}")
    print(f"review sheet {review}")


def compute(args, recipe: dict):
    src = source_path(args.name)
    with Image.open(src) as im:
        rgb = np.asarray(im.convert("RGB"))
    mattes = {k: np.asarray(Image.open(cache_dir(args) / f"{args.name}.{k}.png").convert("L")) for k in MODEL_SPECS}
    for op in recipe.get("ops", []):
        if op["op"] == "submatte":
            key = op.get("model", "birefnet")
            x0, y0, x1, y1 = op["box"]
            dest = cache_dir(args) / f"{args.name}.sub.{key}.{x0}_{y0}_{x1}_{y1}.png"
            if not dest.exists():
                crop = Image.fromarray(rgb[y0:y1, x0:x1])
                Image.fromarray(predict_matte(Path(args.models), key, crop)).save(dest)
            mattes[f"sub:{key}:{x0},{y0},{x1},{y1}"] = np.asarray(Image.open(dest).convert("L"))
    return rgb, apply_recipe(rgb, mattes, recipe)


def cmd_grid(args) -> None:
    """Zoomed crop with a labelled pixel grid, for placing recipe coordinates."""
    src = source_path(args.name)
    with Image.open(src) as im:
        rgb = np.asarray(im.convert("RGB"))
    if args.matte != "none":
        if args.matte == "result":
            _, a = compute(args, load_recipe(args.name))
        else:
            a = np.asarray(Image.open(cache_dir(args) / f"{args.name}.{args.matte}.png").convert("L"))
        a = a.astype(np.float32)[..., None] / 255
        rgb = (rgb * a + np.array([255, 0, 255]) * (1 - a)).astype(np.uint8)
    x0, y0, x1, y1 = args.crop
    crop = Image.fromarray(rgb[y0:y1, x0:x1])
    s = args.scale or max(1, min(5, 900 // max(crop.width, crop.height)))
    crop = crop.resize((crop.width * s, crop.height * s), Image.NEAREST)
    pad, step = 34, args.step
    sheet = Image.new("RGB", (crop.width + pad, crop.height + pad), "white")
    sheet.paste(crop, (pad, pad))
    draw = ImageDraw.Draw(sheet)
    for gx in range((x0 // step + 1) * step, x1, step):
        X = pad + (gx - x0) * s
        draw.line([(X, pad), (X, pad + crop.height)], fill=(0, 255, 0) if gx % (step * 5) == 0 else (255, 255, 0))
        if gx % (step * 2) == 0:
            draw.text((X - 10, 2 if (gx // (step * 2)) % 2 else 16), str(gx), fill="black")
    for gy in range((y0 // step + 1) * step, y1, step):
        Y = pad + (gy - y0) * s
        draw.line([(pad, Y), (pad + crop.width, Y)], fill=(0, 255, 0) if gy % (step * 5) == 0 else (255, 255, 0))
        if gy % (step * 2) == 0:
            draw.text((0, Y - 5), str(gy), fill="black")
    dest = cache_dir(args) / f"{args.name}.grid.png"
    sheet.save(dest)
    print(dest)


def cmd_compare(args) -> None:
    """Sheet of the raw model mattes over magenta, for choosing a starting matte."""
    src = source_path(args.name)
    with Image.open(src) as im:
        rgb = np.asarray(im.convert("RGB"))
    tiles = [rgb]
    for key in MODEL_SPECS:
        a = np.asarray(Image.open(cache_dir(args) / f"{args.name}.{key}.png").convert("L")).astype(np.float32)[..., None] / 255
        tiles.append((rgb * a + np.array([255, 0, 255]) * (1 - a)).astype(np.uint8))
    if args.crop:
        x0, y0, x1, y1 = args.crop
        tiles = [t[y0:y1, x0:x1] for t in tiles]
    h = tiles[0].shape[0]
    scale = 620 / h if h > 620 else 1.0
    tiles = [cv2.resize(t, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) for t in tiles]
    sheet = np.concatenate([np.pad(t, ((0, 0), (0, 6), (0, 0)), constant_values=255) for t in tiles], axis=1)
    dest = cache_dir(args) / f"{args.name}.compare.png"
    Image.fromarray(sheet).save(dest)
    print(dest)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--models", default=os.environ.get("CUTOUT_MODELS", "models"))
    p.add_argument("--cache", default=os.environ.get("CUTOUT_CACHE", "cutout_cache"))
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("predict", cmd_predict), ("compare", cmd_compare), ("render", cmd_render), ("grid", cmd_grid)):
        s = sub.add_parser(name)
        s.add_argument("name")
        s.add_argument("--crop", type=int, nargs=4, required=name == "grid")
        if name == "render":
            s.add_argument("--preview", action="store_true", help="write only the review sheet")
        if name == "grid":
            s.add_argument("--step", type=int, default=20)
            s.add_argument("--scale", type=int)
            s.add_argument("--matte", choices=("none", "birefnet", "isnet", "result"), default="none")
        s.set_defaults(fn=fn)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
