#!/usr/bin/env python3
"""Lift the base master's baked eyes, eyebrows and mouth into isolated layers.

The base body is not a blank mannequin. `prompts/16` specifies "large warm-brown
eyes, small nose, and gentle closed-mouth smile", and the registered master has
them painted in. Face traits are therefore overlays that *replace* a face that is
already there, which has two consequences the collection has never written down:

1. A face trait must cover the feature underneath it. A trait smaller than the
   baked one leaves the original showing through.
2. The approved face already is the collection's face. Its eye pair, eyebrow pair
   and mouth are on-model, on-rig, painted in the locked style, and positioned by
   the artist rather than by a placement rule.

So the facial system is built from that art rather than beside it. This module
separates each feature from the skin it is painted on, giving a layer that
composites back over the master **exactly** - the round trip is asserted, not
assumed - and can then be recoloured or reshaped into variants that land on the
rig by construction.

## How the separation works

Over the feature's region the image is a mix of the feature and the skin behind
it: `observed = alpha * feature + (1 - alpha) * skin`. Two unknowns, one equation,
so the skin has to come from somewhere.

It comes from the surrounding face. The skin field is reconstructed by diffusing
the genuine skin around each feature inward across it - repeatedly blurring while
holding the known skin fixed, which converges on the smooth gradient the boundary
implies. The cheek and forehead are a smooth field, so this is a good estimate of
what is behind the eye rather than a guess at it.

Alpha is then the *minimum* value that keeps the recovered feature colour inside
[0, 255]:

    alpha = max over channels of |observed - skin| / headroom

taking `headroom` as the room left toward white or black in the direction the
pixel actually differs. Solving for the smallest alpha rather than assuming one
is what makes the round trip exact: substituting back gives
`skin + (observed - skin)`, which is the observed pixel, for every pixel. Where a
pixel is genuinely opaque - the lash line, the iris - a core mask pins alpha to 1
so the interior does not come back translucent.

The result is a clean layer with no matte contamination: the alpha is derived
analytically rather than keyed, so no skin tone is smeared into the edges.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png"

# Regions enclosing each baked feature, measured on the master. Each is chosen so
# its border is genuine skin, which is what the diffusion needs to work from.
REGIONS = {
    "eye_left": (500, 330, 594, 410),
    "eye_right": (659, 330, 753, 410),
    "eyebrows": (500, 296, 756, 334),
    "mouth": (596, 428, 660, 452),
}

# The iris ellipse, measured on the master: centre and radii.
IRIS = {
    "eye_left": (559.0, 374.0, 28.5, 27.5),
    "eye_right": (694.0, 374.0, 28.5, 27.5),
}

# A pixel differing from the reconstructed skin by more than this is feature, not
# a soft edge, and is pinned fully opaque.
CORE_THRESHOLD = 26.0


def skin_mask(rgb: np.ndarray) -> np.ndarray:
    """Pixels that are the character's skin rather than a painted feature."""
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return (
        (red > 224) & (green > 155) & (green < 240) & (blue > 115) & (blue < 220)
        & ((red - blue) > 30) & ((red - green) > 12)
    )


def known_skin(rgb: np.ndarray) -> np.ndarray:
    """Skin the reconstruction may treat as known, with painted highlights removed.

    The style paints a pale warm highlight along the top of each eyebrow. It is
    light enough to pass as skin, so holding it fixed diffuses its brightness
    across the whole reconstruction and the patch comes out lighter than the
    forehead around it - which shows as a pale crescent wherever the trait's own
    brow no longer covers it. Skin near a feature varies smoothly by a few units;
    the highlight runs 13-17 above it. Excluding the bright tail puts the highlight
    where it belongs, in the feature that moves with the trait.
    """
    skin = skin_mask(rgb.astype(int))
    if not skin.any():
        return skin
    limit = np.percentile(rgb[skin][:, 2], 60) + 8.0
    return skin & (rgb[..., 2] <= limit)


def _box_blur(field: np.ndarray, radius: int = 2) -> np.ndarray:
    padded = np.pad(field, ((radius, radius), (radius, radius), (0, 0)), mode="edge")
    rolling = np.cumsum(padded, axis=0)
    rolling = np.vstack([np.zeros((1,) + rolling.shape[1:]), rolling])
    vertical = (rolling[2 * radius + 1:] - rolling[:-2 * radius - 1]) / (2 * radius + 1)
    rolling = np.cumsum(vertical, axis=1)
    rolling = np.hstack([np.zeros((rolling.shape[0], 1, rolling.shape[2])), rolling])
    return (rolling[:, 2 * radius + 1:] - rolling[:, :-2 * radius - 1]) / (2 * radius + 1)


def reconstruct_skin(rgb: np.ndarray, known: np.ndarray, radius: int = 24) -> np.ndarray:
    """Estimate the skin behind a feature as a weighted average of the skin around it.

    This is a normalized convolution: the image and the known-pixel mask are each
    blurred, and their ratio is the average of the genuine skin within `radius`,
    with unknown pixels contributing nothing. It is smooth by construction and its
    colour is the colour of the neighbours.

    It replaces an iterated hold-and-blur relaxation, which is the textbook
    harmonic fill and looked right in isolation but shipped a visible defect: over
    a band as long and thin as the eyebrow the relaxation had not converged, so the
    patch came out mottled, and it drifted about 4/255 down in red against the
    surrounding skin. Composited, that is a pale grey crescent sitting on the brow
    line of every token whose eyebrow trait moved the brow off it.
    """
    if not known.any():
        return rgb.astype(float)
    weight = known.astype(float)[..., None]
    value = _box_blur(rgb.astype(float) * weight, radius)
    mass = _box_blur(np.repeat(weight, 3, axis=2), radius)
    return value / np.maximum(mass, 1e-6)


def unmix(observed: np.ndarray, skin: np.ndarray, core: np.ndarray):
    """Minimum-alpha separation of `observed` into a layer over `skin`."""
    difference = observed - skin
    headroom = np.maximum(np.where(difference >= 0, 255.0 - skin, skin), 1.0)
    alpha = np.clip(np.maximum((np.abs(difference) / headroom).max(axis=2), core), 0.0, 1.0)
    feature = np.clip(skin + difference / np.maximum(alpha, 1e-6)[..., None], 0, 255)
    return alpha, feature


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


def _connected_to(mask: np.ndarray, seed: np.ndarray) -> np.ndarray:
    current = seed & mask
    while True:
        grown = _grow(current) & mask
        if grown.sum() == current.sum():
            return grown
        current = grown


def extract(name: str, master: Image.Image | None = None):
    """Return the isolated layer for one baked feature, plus its round-trip error."""
    image = master or Image.open(MASTER).convert("RGBA")
    rgb = np.asarray(image.convert("RGBA")).astype(float)[..., :3]
    left, top, right, bottom = REGIONS[name]
    patch = rgb[top:bottom, left:right]

    skin = reconstruct_skin(patch, known_skin(patch))
    difference = np.abs(patch - skin).max(axis=2)
    core = _grow(difference > CORE_THRESHOLD).astype(float)
    alpha, feature = unmix(patch, skin, core)

    keep = np.ones(alpha.shape, dtype=bool)
    if name in IRIS:
        # Keep only the eye blob. The region's corners catch the ear outline and
        # the eyebrow tail, which belong to other traits and are deliberately
        # dropped - so the round trip is asserted over what the layer claims to
        # carry, and the discarded pixels are counted rather than hidden.
        height, width = alpha.shape
        rows, columns = np.mgrid[0:height, 0:width]
        cx, cy, rx, ry = IRIS[name]
        inside = (((columns + left - cx) / rx) ** 2 + ((rows + top - cy) / ry) ** 2) <= 1.0
        keep = _grow(_connected_to(alpha > 0.15, inside), 2)
        discarded = int(((alpha > 0.15) & ~keep).sum())
        alpha = np.where(keep, alpha, 0.0)
    else:
        discarded = 0

    restored = alpha[..., None] * feature + (1 - alpha[..., None]) * skin
    error = float(np.abs(restored - patch)[keep].max())
    return dict(name=name, box=(left, top, right, bottom), alpha=alpha,
                rgb=feature, skin=skin, round_trip_error=error, discarded=discarded)


def as_layer(extracted: dict) -> Image.Image:
    """Place an extracted feature on the full locked canvas."""
    left, top, right, bottom = extracted["box"]
    patch = np.zeros((bottom - top, right - left, 4), dtype=np.uint8)
    patch[..., :3] = np.round(extracted["rgb"]).astype(np.uint8)
    patch[..., 3] = np.round(extracted["alpha"] * 255).astype(np.uint8)
    canvas = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
    canvas.paste(Image.fromarray(patch, "RGBA"), (left, top))
    return canvas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=Path("incoming/face_features"))
    args = parser.parse_args(argv)
    out = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    for name in REGIONS:
        extracted = extract(name)
        as_layer(extracted).save(out / f"{name}.png")
        opaque = int((extracted["alpha"] >= 0.999).sum())
        visible = int((extracted["alpha"] > 0).sum())
        print(f"{name:12s} round-trip max error {extracted['round_trip_error']:.4f}"
              f"   visible {visible:6d} px, fully opaque {opaque:6d}"
              f"   discarded {extracted['discarded']:5d}")
    print(f"\nwritten to {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
