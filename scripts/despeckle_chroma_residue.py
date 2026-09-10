#!/usr/bin/env python3
"""Remove chroma-key residue from registered assets.

Several traits were produced by keying a green backdrop out of a rendered image.
The key was not complete: saturated key-green pixels survive *inside* the art as
isolated specks, fully opaque, in assets whose palettes contain no green at all -
two green dots in violet bangs, a scatter through pink hair, specks on the base
bodies' skin. They appear on every token those traits land on.

No gate could see them. Canvas, alpha behaviour, bounds and width ratio are all
satisfied by a layer with green confetti in it, and the existing chroma work
measured the *edge* fringe rather than the interior.

## Telling residue from paint

The collection contains genuinely green art - a laurel wreath, an emerald eye
pair, a green neon ring, a verdant legendary - so "is this pixel green" is not the
question, and no measurement separates the two cases cleanly. Two were tried and
both failed on real assets:

- **How much of the asset is green.** `aura_rear_005_lavender_lightning` is 20.5 %
  key-green and every one of those pixels is residue: the green traces the outline
  of each lavender tongue. Meanwhile `base_pose_004` is 0.28 % and all of it is
  residue too. Share does not order the two cases.
- **How clustered the green is.** The laurel measures 0.314 on a local-density
  scale and the contaminated lightning ring 0.296; the emerald eyes measure 0.645
  and the contaminated lavender lightning also 0.645. The distributions overlap.

So the classification is a short list, made by looking at each asset that carries
any key-green at all and recorded below with what was seen. That is honest about
how the decision was made, and it is auditable. A guard refuses to touch any
unlisted asset that is more than 30 % key-green, so a future genuinely green trait
fails loudly here instead of being quietly repainted.

The repair diffuses the surrounding art inward across each speck, holding the
known pixels fixed, which converges on the colour the neighbourhood implies.
Alpha is never touched, so no silhouette moves.

    python scripts/despeckle_chroma_residue.py --in-place
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
METHOD = "chroma_residue_despeckle_2026-09-10"

# A pixel this much greener than both its red and blue, and this bright in green,
# is the key colour rather than a shade of the art.
GREEN_MARGIN = 40
GREEN_FLOOR = 90

# The margin the spill gradient is followed out to, once a speck has been found.
# The key does not stop at a hard edge: around every flagged pixel sits a skirt
# that is green by less than GREEN_MARGIN. Left in place it is exactly as visible -
# the lavender aura came back with a sage rim where the lime one had been - and it
# also feeds green back into the repair, because an unflagged pixel is held fixed
# and diffused from. So the residue is grown along the gradient rather than cut at
# the detection threshold.
SPILL_MARGIN = 12
SPILL_REACH = 10

# Alpha below this is a soft edge whose colour barely reaches the composite.
VISIBLE = 60

# Assets whose green is the art. Each was rendered against a dark ground and
# looked at; the note is what was seen.
GREEN_BY_DESIGN = {
    "assets/head_accessories/head_accessory_003_green_laurel.png":
        "a laurel wreath - the green fills the leaves",
    "assets/eyes/eyes_012_emerald.png":
        "the emerald iris of this collection's own eye palette",
    "assets/rear_auras/aura_rear_007_green_neon_ring.png":
        "built procedurally by scripts/build_aura_floor_ring.py --palette green; the "
        "green is smooth and unspeckled",
    "assets/legendary/legendary_007_verdant_archivist.png":
        "the verdant legendary - green foliage throughout",
}

# An unlisted asset greener than this is refused rather than repaired: it is more
# likely a new green trait than a keying failure, and that call belongs to a person.
REFUSE_ABOVE_SHARE = 0.30


def _grow(mask: np.ndarray, steps: int = 1) -> np.ndarray:
    grown = mask.copy()
    for _ in range(steps):
        nudged = grown.copy()
        nudged[1:, :] |= grown[:-1, :]
        nudged[:-1, :] |= grown[1:, :]
        nudged[:, 1:] |= grown[:, :-1]
        nudged[:, :-1] |= grown[:, 1:]
        grown = nudged
    return grown


def key_green(rgba: np.ndarray) -> np.ndarray:
    alpha = rgba[..., 3]
    red, green, blue = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    return (alpha > VISIBLE) & (green - np.maximum(red, blue) > GREEN_MARGIN) & (green > GREEN_FLOOR)


def green_share(rgba: np.ndarray) -> float:
    visible = rgba[..., 3] > VISIBLE
    if not visible.any():
        return 0.0
    return float(key_green(rgba).sum()) / float(visible.sum())


def spill_skirt(rgba: np.ndarray, flagged: np.ndarray) -> np.ndarray:
    """Grow each speck along its spill gradient rather than cutting it at the threshold."""
    visible = rgba[..., 3] > VISIBLE
    green = rgba[..., 1].astype(int) - np.maximum(rgba[..., 0], rgba[..., 2]).astype(int)
    spill = visible & (green > SPILL_MARGIN)
    residue = _grow(flagged) & visible
    for _ in range(SPILL_REACH):
        grown = _grow(residue) & spill
        if grown.sum() == residue.sum():
            break
        residue = grown | residue
    return _grow(residue) & visible


def repair(rgba: np.ndarray, residue: np.ndarray, iterations: int = 220) -> np.ndarray:
    """Diffuse the surrounding art across each speck, holding known pixels fixed.

    Work is confined to the residue's bounding box plus a margin. The diffusion is
    local by nature, so a full-canvas relaxation would only spend time on pixels
    that never change.
    """
    known = (rgba[..., 3] > VISIBLE) & ~residue
    if not known.any() or not residue.any():
        return rgba
    ys, xs = np.nonzero(residue)
    top, bottom = max(int(ys.min()) - 24, 0), min(int(ys.max()) + 25, rgba.shape[0])
    left, right = max(int(xs.min()) - 24, 0), min(int(xs.max()) + 25, rgba.shape[1])

    window = (slice(top, bottom), slice(left, right))
    patch_residue = residue[window]
    patch_known = known[window]
    source = rgba[window][..., :3].astype(float)
    field = source.copy()
    if patch_known.any():
        field[patch_residue] = source[patch_known].mean(axis=0)
    hold = patch_known[..., None]
    for _ in range(iterations):
        blurred = field.copy()
        blurred[1:-1, 1:-1] = (
            field[:-2, 1:-1] + field[2:, 1:-1] + field[1:-1, :-2] + field[1:-1, 2:]
        ) / 4.0
        field = np.where(hold, source, blurred)

    # Keep the original pixel's brightness and take only its colour from the
    # diffusion. Replacing the pixel outright flattens whatever shading the key
    # was sitting on - the lavender aura's tongues came back as smooth grey - while
    # rescaling the diffused colour to the original luminance keeps the form and
    # changes the hue, which is all that was wrong with it.
    weights = np.array([0.299, 0.587, 0.114])
    original_luma = source @ weights
    diffused_luma = np.maximum(field @ weights, 1e-3)
    relit = np.clip(field * (original_luma / diffused_luma)[..., None], 0, 255)

    out = rgba.copy()
    patch = out[window]
    patch[..., :3] = np.where(patch_residue[..., None],
                              np.round(relit).astype(rgba.dtype), patch[..., :3])
    out[window] = patch
    return despill(out, residue)


def despill(rgba: np.ndarray, residue: np.ndarray, reach: int = 4) -> np.ndarray:
    """Pull the key colour out of the band immediately around each speck.

    A hard threshold removes the core of the residue and leaves its gradient: the
    lavender aura came back with a sage rim where the lime one had been, because
    those pixels are green by less than the flagging margin. Clamping green to the
    larger of red and blue is the standard despill, and it is only safe where green
    is known not to belong - so it is applied only in a few pixels around a pixel
    already confirmed as key colour, fading out with distance. Nothing elsewhere in
    the asset is touched, and a genuinely olive or yellow-green trait far from any
    residue is left exactly as painted.
    """
    visible = rgba[..., 3] > VISIBLE
    band = np.zeros(residue.shape, float)
    reached = residue.copy()
    for step in range(1, reach + 1):
        grown = _grow(reached)
        band[grown & ~reached & visible] = 1.0 - (step - 1) / reach
        reached = grown
    if not band.any():
        return rgba

    red = rgba[..., 0].astype(float)
    green = rgba[..., 1].astype(float)
    blue = rgba[..., 2].astype(float)
    clamped = np.minimum(green, np.maximum(red, blue))
    out = rgba.copy()
    out[..., 1] = np.round(green * (1 - band) + clamped * band).astype(rgba.dtype)
    return out


def despeckle(path: Path, relative: str) -> tuple[np.ndarray | None, dict]:
    rgba = np.asarray(Image.open(path).convert("RGBA")).astype(np.int16)
    share = green_share(rgba)
    flagged = key_green(rgba)
    report = {"key_green": int(flagged.sum()), "share": round(share, 5)}
    if not flagged.any():
        report["action"] = "clean"
        return None, report
    if relative in GREEN_BY_DESIGN:
        report["action"] = f"green by design: {GREEN_BY_DESIGN[relative]}"
        return None, report
    if share > REFUSE_ABOVE_SHARE:
        raise SystemExit(
            f"{relative} is {share*100:.1f}% key-green and is not listed as green by design. "
            "If it is a new green trait, add it to GREEN_BY_DESIGN with what you saw; if it is "
            "a keying failure this severe, it needs a re-key rather than a despeckle."
        )
    residue = spill_skirt(rgba, flagged)
    report.update({"repaired": int(residue.sum()), "action": "repaired"})
    return repair(rgba, residue).astype(np.uint8), report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args(argv)
    if not args.in_place and not args.out_dir:
        print("error: pass --in-place or --out-dir")
        return 1

    manifest = json.loads(MANIFEST.read_text())
    by_path = {entry["path"]: entry for entry in manifest["registered_production_assets"]}

    changed = 0
    for relative, entry in sorted(by_path.items()):
        path = ROOT / relative
        if not path.exists() or path.suffix != ".png":
            continue
        repaired, report = despeckle(path, relative)
        if repaired is None:
            if report["key_green"]:
                print(f"{relative:58s} skipped  {report['action']}")
            continue
        destination = path if args.in_place else args.out_dir / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        Image.fromarray(repaired, "RGBA").save(destination)
        after = hashlib.sha256(destination.read_bytes()).hexdigest()
        print(f"{relative:60s} repaired {report['repaired']:5d} px "
              f"({report['key_green']} key-green, {report['share']*100:.3f}%)")
        if args.in_place:
            entry["sha256"] = after
            provenance = entry.setdefault("provenance", {})
            steps = list(provenance.get("postprocessing", []))
            if METHOD not in steps:
                steps.append(METHOD)
            provenance["postprocessing"] = steps
            provenance["chroma_despeckle_script"] = "scripts/despeckle_chroma_residue.py"
            provenance[f"pre_{METHOD}_sha256"] = before
            provenance[f"post_{METHOD}_sha256"] = after
            provenance["chroma_despeckle_note"] = (
                f"{report['repaired']} px of surviving chroma key removed. The asset carried "
                f"{report['key_green']} saturated key-green pixels, {report['share']*100:.3f}% of its "
                "visible area, in a palette that has no green in it; they were opaque specks inside "
                "the art rather than an edge fringe, so the earlier chroma passes did not reach them. "
                "Each speck's colour is diffused in from the surrounding art with the known pixels held "
                "fixed. Alpha is untouched."
            )
        changed += 1

    if args.in_place and changed:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{changed} asset(s) repaired")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
