#!/usr/bin/env python3
"""Compose the final rare 1-of-1 images: focus-blurred, vignetted background + sharp cutout.

For every cutout in ``images/variations/cutouts_2026-10-09`` the original illustration is
re-rendered as follows:

1. Focus blur. The original is blurred with a disc (lens) kernel. The subject - every pixel
   the cutout keeps, grown by a small margin - is excluded from the blur and the blur is
   renormalised by the remaining weight, so the character's colours never smear into a halo
   around the sharp overlay. Where the subject hides a large area, a wide fallback blur of the
   surrounding background fills it (it is only ever seen through translucent parts).
2. Vignette. The blurred background is darkened towards the corners with a smooth elliptical
   falloff.
3. Overlay. The transparent cutout (character, held items, own magic, foreground items) is
   composited on top unchanged, so every fully opaque cutout pixel equals the source pixel.

Outputs are opaque RGB PNGs at the source's native size, with a manifest of SHA-256 digests
and parameters, and a contact sheet of the whole set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
CUTOUT_DIR = ROOT / "images/variations/cutouts_2026-10-09"
OUTPUT_DIR = ROOT / "images/one_of_ones/final_2026-10-10"
REFERENCE_WIDTH = 1254  # parameters are given for 1254 px and scaled to each image


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    path = path.resolve()
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def source_for(name: str) -> Path:
    recipe = json.loads((CUTOUT_DIR / "recipes" / f"{name}.json").read_text())
    if "source" in recipe:
        return ROOT / recipe["source"]
    return ROOT / "images/variations/complete_72" / f"{name}.png"


def disc_kernel(radius: float) -> np.ndarray:
    size = int(np.ceil(radius)) * 2 + 1
    yy, xx = np.mgrid[:size, :size] - size // 2
    # Anti-aliased disc: 1 inside, linear falloff over the last pixel.
    kernel = np.clip(radius + 0.5 - np.hypot(xx, yy), 0, 1).astype(np.float32)
    return kernel / kernel.sum()


def focus_blur(rgb: np.ndarray, subject: np.ndarray, radius: float, margin: int) -> np.ndarray:
    """Disc blur of the background only; subject pixels carry no weight."""
    keep_out = subject > 8
    if margin:
        keep_out = cv2.dilate(keep_out.astype(np.uint8), np.ones((2 * margin + 1,) * 2, np.uint8)) > 0
    weight = (~keep_out).astype(np.float32)
    img = rgb.astype(np.float32)
    kernel = disc_kernel(radius)
    num = cv2.filter2D(img * weight[..., None], -1, kernel, borderType=cv2.BORDER_REFLECT)
    den = cv2.filter2D(weight, -1, kernel, borderType=cv2.BORDER_REFLECT)
    sigma = radius * 6
    wide_num = cv2.GaussianBlur(img * weight[..., None], (0, 0), sigma, borderType=cv2.BORDER_REFLECT)
    wide_den = cv2.GaussianBlur(weight, (0, 0), sigma, borderType=cv2.BORDER_REFLECT)
    near = num / np.maximum(den, 1e-6)[..., None]
    far = wide_num / np.maximum(wide_den, 1e-6)[..., None]
    if (wide_den < 1e-3).any():  # subject covers the whole neighbourhood: plain blur as last resort
        plain = cv2.GaussianBlur(img, (0, 0), sigma)
        far = np.where((wide_den < 1e-3)[..., None], plain, far)
    blend = np.clip(den / 0.25, 0, 1)[..., None]  # trust the lens blur once a quarter of its disc is background
    return near * blend + far * (1 - blend)


def vignette(rgb: np.ndarray, strength: float, inner: float, power: float) -> np.ndarray:
    h, w = rgb.shape[:2]
    yy, xx = np.mgrid[:h, :w].astype(np.float32)
    d = np.hypot((xx - (w - 1) / 2) / ((w - 1) / 2), (yy - (h - 1) / 2) / ((h - 1) / 2)) / np.sqrt(2)
    t = np.clip((d - inner) / (1 - inner), 0, 1)
    ramp = t * t * (3 - 2 * t)  # smoothstep: no visible ring where the darkening starts
    return rgb * (1 - strength * ramp ** power)[..., None]


def compose(source: np.ndarray, cutout: np.ndarray, params: dict) -> np.ndarray:
    scale = source.shape[1] / REFERENCE_WIDTH
    alpha = cutout[..., 3].astype(np.float32) / 255.0
    background = focus_blur(source, cutout[..., 3], params["blur_radius"] * scale,
                            max(1, round(params["subject_margin"] * scale)))
    background = vignette(background, params["vignette_strength"], params["vignette_inner"],
                          params["vignette_power"])
    out = cutout[..., :3].astype(np.float32) * alpha[..., None] + background * (1 - alpha[..., None])
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def contact_sheet(paths: list[Path], destination: Path, columns: int, thumb: int) -> None:
    label = 18
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb, rows * (thumb + label)), (18, 18, 22))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        x, y = (i % columns) * thumb, (i // columns) * (thumb + label)
        with Image.open(path) as im:
            sheet.paste(im.convert("RGB").resize((thumb, thumb), Image.LANCZOS), (x, y + label))
        draw.text((x + 4, y + 3), path.stem.replace("Demigods_", "")[:30], fill=(235, 235, 240))
    sheet.save(destination, optimize=True)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("names", nargs="*", help="cutout stems to render (default: all)")
    p.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    p.add_argument("--blur-radius", type=float, default=9.0, help="lens blur radius at 1254 px")
    p.add_argument("--subject-margin", type=float, default=3.0, help="px around the subject kept out of the blur")
    p.add_argument("--vignette-strength", type=float, default=0.42, help="darkening at the very corners, 0-1")
    p.add_argument("--vignette-inner", type=float, default=0.38, help="normalised radius where darkening starts")
    p.add_argument("--vignette-power", type=float, default=1.3)
    p.add_argument("--sheet-columns", type=int, default=11)
    p.add_argument("--sheet-thumb", type=int, default=240)
    p.add_argument("--no-sheet", action="store_true")
    a = p.parse_args(argv)
    if not 0 <= a.vignette_strength <= 1 or not 0 <= a.vignette_inner < 1 or a.blur_radius <= 0:
        raise SystemExit("blur radius must be positive; vignette strength 0-1; vignette inner 0-<1")
    params = {k: getattr(a, k) for k in ("blur_radius", "subject_margin", "vignette_strength",
                                         "vignette_inner", "vignette_power")}
    names = a.names or sorted(p.stem for p in CUTOUT_DIR.glob("*.png") if p.name != "contact_sheet.png")
    a.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = a.output_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"files": {}}
    for name in names:
        src_path, cut_path = source_for(name), CUTOUT_DIR / f"{name}.png"
        with Image.open(src_path) as s, Image.open(cut_path) as c:
            source, cutout = np.asarray(s.convert("RGB")), np.asarray(c.convert("RGBA"))
        if source.shape[:2] != cutout.shape[:2]:
            raise SystemExit(f"size mismatch for {name}: {source.shape[:2]} vs {cutout.shape[:2]}")
        result = compose(source, cutout, params)
        dest = a.output_dir / f"{name}.png"
        payload = BytesIO()
        Image.fromarray(result, "RGB").save(payload, format="PNG", optimize=True)
        tmp = dest.with_suffix(".png.tmp")
        tmp.write_bytes(payload.getvalue())
        with Image.open(tmp) as check:
            check.load()
        tmp.replace(dest)
        manifest["files"][name] = {
            "source": rel(src_path), "source_sha256": digest(src_path),
            "cutout": rel(cut_path), "cutout_sha256": digest(cut_path),
            "output": rel(dest), "output_sha256": digest(dest),
            "dimensions": [result.shape[1], result.shape[0]],
        }
        print(f"{name} -> {rel(dest)}")
    manifest["parameters"] = params
    manifest["count"] = len(manifest["files"])
    manifest["files"] = dict(sorted(manifest["files"].items()))
    manifest_path.write_text(json.dumps(manifest, indent=1) + "\n")
    if not a.no_sheet:
        outputs = [a.output_dir / f"{n}.png" for n in manifest["files"]]
        order = [p for p in outputs if p.stem.startswith("Demigods_")] + [p for p in outputs if not p.stem.startswith("Demigods_")]
        contact_sheet(order, a.output_dir / "contact_sheet.png", a.sheet_columns, a.sheet_thumb)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
