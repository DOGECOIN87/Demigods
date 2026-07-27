#!/usr/bin/env python3
"""Recolour the recovered face layers into interim eye and eyebrow variants.

`extract_face_layers.py` recovers one eye pair, one eyebrow pair and one mouth
from the base master. One of each means every token shares a face, which is the
same repetition problem the hair recolours were built to reduce. These vary the
colour until the painted `FACE` sheet cells land.

Only hue and saturation move; **value is untouched**, so every painted gradient,
the pupil, the lash weight and the upper-left key light survive exactly. Two
bands are passed through unchanged:

- Sclera and catchlights, which are bright and near-neutral. Whites stay white.
- Anything close in colour to the skin behind it *and above the eye opening*.
  The eyelid highlight over the lash is a warm skin tone at saturation 0.38, so
  a saturation threshold alone lets it through and a cyan variant grows a cyan
  eyelid. Colour alone is not enough either: the lower iris highlight is the
  same warm tan, so a pure skin-proximity guard leaves a beige blob sitting in
  every recoloured iris. The two are separated by position — the eye opening
  starts at the topmost sclera pixel, and skin protection applies only above it.

## Contrast

Palettes are chosen against measurement, not taste. Two different things are
measured, because the eye has two different neighbours:

- **Against skin**, which is what physically surrounds the iris, plain RGB
  distance is the right measure and every palette clears it comfortably. The
  iris is dark and the face is light; that is what makes an eye read at 210 px.
- **Against the backgrounds**, RGB distance is the wrong measure and was tried
  first: the iris body and the backgrounds behind the head are both mid-dark, so
  every palette scored "close" including ones that obviously read. What actually
  goes wrong there is hue camouflage -- an iris sharing the scene's colour
  identity stops looking like a separate object -- so the gate is minimum hue
  separation from each background's dominant hue behind the head.

Three of the four registered backgrounds sit in a blue-violet band (220-253
degrees) and the fourth is warm gold (14 degrees). Requiring 40 degrees of
clearance from all four leaves the greens, teals and magentas, which is why the
palette list looks the way it does rather than spanning the wheel evenly. Add a
background in a new hue band and `--check-contrast` will say so.

Near-neutral irises are exempt from the hue rule -- grey has no hue to clash
with -- and are carried by value contrast against skin instead. The recovered
base master brown is also exempt and reported separately: it is the approved
painted artwork, not a palette choice, and sits 8 degrees from the warm
background.

Scope, stated plainly: this varies COLOUR only. The eye shape, brow shape and
lash structure are identical in every output, so the recolours give many eye
*colours* and one eye *design*. The 24 `FACE` sheet cells are distinct
paintings, so these do NOT satisfy DG-055 to DG-078 and must not be filed as
them.
"""

from __future__ import annotations

import argparse
import colorsys
import glob
import math
from pathlib import Path

from PIL import Image, ImageFilter

# Sclera and catchlights: bright and near-neutral.
BRIGHT_VALUE = 0.80
BRIGHT_SATURATION = 0.20

# Skin proximity, as a max-channel distance from the pixel of the faceless base
# directly behind. Below NEAR the pixel is eyelid and is left alone; above FAR
# it is eye artwork and takes the full shift.
SKIN_NEAR = 45.0
SKIN_FAR = 85.0

# Softening applied to the eye-interior mask before it is used as a weight.
INTERIOR_FEATHER = 1.6

# Region the head occupies, used to sample what a background actually shows
# behind the face rather than averaging the whole plate.
HEAD_WINDOW = (470, 290, 790, 470)

# Locked canvas centre, used to tell the two eyes apart.
CENTER_X = 627

# Contrast floors. Skin is RGB distance; backgrounds are hue degrees.
MIN_SKIN_DISTANCE = 70.0
MIN_BACKGROUND_HUE_SEPARATION = 40.0

# A background flatter than this has no hue to clash with and is not gated.
BACKGROUND_SATURATION_FLOOR = 0.15
# An iris flatter than this has no hue of its own and is not gated.
NEUTRAL_SATURATION = 0.18


class Palette:
    def __init__(self, name: str, hue: float, saturation: float):
        self.name = name
        self.hue = hue / 360.0
        self.saturation = saturation


# Hues are placed away from both the skin (about 22 degrees) and the blue-violet
# band the backgrounds occupy (220-253 degrees). Greens, teals and magentas
# clear both; the neutrals clear them on value instead of hue.
EYE_PALETTES = [
    Palette("brown", 22, 0.50),        # the recovered master; exempt from the hue gate
    Palette("gold", 58, 0.80),
    Palette("olive", 76, 0.60),
    Palette("lime", 94, 0.62),
    Palette("jade", 118, 0.62),
    Palette("spring", 136, 0.60),
    Palette("emerald", 152, 0.66),
    Palette("teal", 176, 0.64),
    Palette("orchid", 300, 0.58),
    Palette("magenta", 318, 0.64),
    Palette("rose", 332, 0.62),
    Palette("grey", 210, 0.12),
    Palette("charcoal", 24, 0.08),
]

# Eyebrows are matched to the registered hair colours so a token can pair them.
BROW_PALETTES = [
    Palette("brown", 22, 0.55),
    Palette("silver", 214, 0.10),
    Palette("gold", 40, 0.60),
    Palette("black", 24, 0.14),
    Palette("violet", 274, 0.46),
    Palette("blue", 218, 0.52),
    Palette("pink", 334, 0.46),
    Palette("teal", 178, 0.48),
    Palette("red", 358, 0.58),
]

SOURCES = {
    "eyes": ("assets/eyes/eyes_025_base_master_brown.png", EYE_PALETTES, "eyes", 25),
    "eyebrows": ("assets/eyebrows/eyebrows_017_base_master_brown.png", BROW_PALETTES,
                 "eyebrows", 17),
}

SKIN_PLATE = Path("assets/base_bodies/base_body_001_neutral_master.png")


def shift(rgb: tuple[int, int, int], palette: Palette) -> tuple[int, int, int]:
    """Full recolour of one pixel: target hue, scaled saturation, same value."""
    red, green, blue = rgb
    _, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    # Keep the source's own saturation modelling -- the iris edge is less
    # saturated than its centre, and flattening that costs the painted depth.
    new_saturation = min(1.0, palette.saturation * (saturation / 0.50))
    out = colorsys.hsv_to_rgb(palette.hue, new_saturation, value)
    return round(out[0] * 255), round(out[1] * 255), round(out[2] * 255)


def blend(original: tuple[int, int, int], shifted: tuple[int, int, int],
          weight: float) -> tuple[int, int, int]:
    """Partial recolour, mixed in RGB rather than in hue.

    Interpolating the hue angle between the source brown and a distant target
    sweeps the intermediate pixels through every hue in between: a half-weight
    pixel on the way to magenta comes out green. That painted a dashed rainbow
    along the top edge of every recoloured eye. Mixing the two RGB results has
    no such path.
    """
    return tuple(round(original[i] + (shifted[i] - original[i]) * weight)
                 for i in range(3))


def eye_interiors(source: Image.Image, skin: Image.Image,
                  box: tuple[int, int, int, int]) -> Image.Image:
    """Rows of the eye openings, so the socket shading around them is spared.

    The extracted eye layer carries a soft skin-toned halo -- the socket shadow
    the artist painted around the opening. Recoloured, it becomes a magenta or
    green glow on the cheek. It cannot be separated by colour, because the lower
    iris highlight is the same warm tan, so it is separated by enclosure: the
    definite ink (lashes, outline, iris, everything far from skin) is found as
    two components and each is closed row by row. The sclera and the lower
    highlight fall inside; the halo falls outside.
    """
    read = source.load()
    plate = skin.load()
    definite = []
    for y in range(box[1], box[3]):
        row = []
        for x in range(box[0], box[2]):
            red, green, blue, alpha = read[x, y]
            if alpha < 200:
                continue
            pr, pg, pb, _ = plate[x, y]
            if max(abs(red - pr), abs(green - pg), abs(blue - pb)) > SKIN_FAR:
                row.append(x)
        if row:
            definite.append((y, row))

    interior = Image.new("L", source.size, 0)
    paint = interior.load()
    for y, row in definite:
        for side in ("left", "right"):
            side_row = [x for x in row if (x < CENTER_X) == (side == "left")]
            if len(side_row) < 2:
                continue
            for x in range(min(side_row), max(side_row) + 1):
                paint[x, y] = 255
    return interior


def recolour(source: Image.Image, skin: Image.Image, palette: Palette) -> Image.Image:
    result = source.copy()
    read = source.load()
    plate = skin.load()
    write = result.load()
    box = source.getchannel("A").getbbox()
    if box is None:
        raise SystemExit("source layer is empty")
    # Softened so the interior does not end on a hard ragged edge; the row-span
    # boundary moves by a pixel or two between rows and a binary mask makes that
    # visible as stipple.
    interior = eye_interiors(source, skin, box).filter(
        ImageFilter.GaussianBlur(INTERIOR_FEATHER)).load()

    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            red, green, blue, alpha = read[x, y]
            if alpha == 0:
                continue
            _, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            if value > BRIGHT_VALUE and saturation < BRIGHT_SATURATION:
                continue
            pr, pg, pb, _ = plate[x, y]
            distance = max(abs(red - pr), abs(green - pg), abs(blue - pb))
            skin_weight = (distance - SKIN_NEAR) / (SKIN_FAR - SKIN_NEAR)
            weight = max(interior[x, y] / 255.0, min(1.0, max(0.0, skin_weight)))
            if weight <= 0.0:
                continue
            new = blend((red, green, blue), shift((red, green, blue), palette), weight)
            write[x, y] = (new[0], new[1], new[2], alpha)
    return result


def iris_colour(source: Image.Image, palette: Palette) -> tuple[float, float, float]:
    """Mean colour of the iris body after recolouring, weighted by opacity.

    Sampled from the mid-value band, which is the iris face rather than its
    shadow or the lash, because that is the part a viewer reads as eye colour.
    """
    read = source.load()
    box = source.getchannel("A").getbbox()
    total = [0.0, 0.0, 0.0]
    count = 0
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            red, green, blue, alpha = read[x, y]
            if alpha < 250:
                continue
            _, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            if not (0.30 <= value <= 0.78 and saturation >= 0.25):
                continue
            new = shift((red, green, blue), palette, 1.0)
            for index in range(3):
                total[index] += new[index]
            count += 1
    if count == 0:
        raise SystemExit(f"no iris pixels sampled for {palette.name}")
    return tuple(channel / count for channel in total)


def mean_colour(image: Image.Image, window: tuple[int, int, int, int]) -> tuple[float, float, float]:
    small = image.convert("RGB").crop(window).resize((48, 27))
    pixels = small.load()
    total = [0.0, 0.0, 0.0]
    for y in range(27):
        for x in range(48):
            for index, channel in enumerate(pixels[x, y]):
                total[index] += channel
    return tuple(channel / (48 * 27) for channel in total)


def dominant_hue(image: Image.Image,
                 window: tuple[int, int, int, int]) -> tuple[float, float]:
    """Saturation-weighted circular mean hue, and mean saturation.

    A plain average of hue angles is meaningless across the 360/0 wrap, and an
    unweighted one lets a large flat grey area outvote the colour that actually
    identifies the scene.
    """
    small = image.convert("RGB").crop(window).resize((64, 36))
    pixels = small.load()
    x_sum = y_sum = saturation_sum = 0.0
    for y in range(36):
        for x in range(64):
            red, green, blue = pixels[x, y]
            hue, saturation, _ = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            saturation_sum += saturation
            if saturation > 0.12:
                x_sum += math.cos(hue * 2 * math.pi) * saturation
                y_sum += math.sin(hue * 2 * math.pi) * saturation
    hue = (math.degrees(math.atan2(y_sum, x_sum)) + 360.0) % 360.0
    return hue, saturation_sum / (64 * 36)


def hue_separation(a: float, b: float) -> float:
    gap = abs(a - b) % 360.0
    return min(gap, 360.0 - gap)


def distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def contrast_report(source: Image.Image, skin: Image.Image,
                    palettes: list[Palette]) -> list[dict]:
    skin_colour = mean_colour(skin, HEAD_WINDOW)
    backgrounds = []
    for path in sorted(glob.glob("assets/backgrounds/*.png")):
        hue, saturation = dominant_hue(Image.open(path), HEAD_WINDOW)
        if saturation >= BACKGROUND_SATURATION_FLOOR:
            backgrounds.append((Path(path).stem, hue))

    rows = []
    for index, palette in enumerate(palettes):
        colour = iris_colour(source, palette)
        hue, saturation, _ = colorsys.rgb_to_hsv(*(channel / 255 for channel in colour))
        against = [(name, hue_separation(hue * 360.0, background))
                   for name, background in backgrounds]
        rows.append({
            "palette": palette,
            "iris": colour,
            "hue": hue * 360.0,
            "saturation": saturation,
            "skin": distance(colour, skin_colour),
            "nearest": min(against, key=lambda pair: pair[1]) if against else None,
            "exempt": index == 0 or saturation < NEUTRAL_SATURATION,
        })
    return rows, backgrounds


def print_report(rows: list[dict], backgrounds: list[tuple[str, float]]) -> bool:
    print("backgrounds sampled behind the head:")
    for name, hue in backgrounds:
        print(f"  {hue:6.1f} deg  {name}")
    print()
    print(f"{'palette':11s} {'iris rgb':16s} {'hue':>6s} {'vs skin':>8s} "
          f"{'hue gap':>8s}  nearest background")
    ok = True
    for row in rows:
        r, g, b = (round(c) for c in row["iris"])
        name, gap = row["nearest"]
        flags = []
        if row["skin"] < MIN_SKIN_DISTANCE:
            flags.append("SKIN")
        if not row["exempt"] and gap < MIN_BACKGROUND_HUE_SEPARATION:
            flags.append("HUE")
        if flags:
            ok = False
        note = "exempt" if row["exempt"] else " ".join(flags) or "ok"
        print(f"{row['palette'].name:11s} ({r:3d},{g:3d},{b:3d})    {row['hue']:6.1f} "
              f"{row['skin']:8.1f} {gap:8.1f}  {name[:30]:32s} {note}")
    print(f"\nfloors: skin distance >= {MIN_SKIN_DISTANCE:.0f}, "
          f"background hue separation >= {MIN_BACKGROUND_HUE_SEPARATION:.0f} deg")
    print("exempt: the recovered master brown, and irises under "
          f"saturation {NEUTRAL_SATURATION}")
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", choices=sorted(SOURCES), action="append")
    parser.add_argument("--out-dir", type=Path, default=Path("images/trait_candidates"))
    parser.add_argument("--skin", type=Path, default=SKIN_PLATE)
    parser.add_argument("--report", action="store_true",
                        help="print the contrast table and write nothing")
    parser.add_argument("--check-contrast", action="store_true",
                        help="exit non-zero if any palette is under a contrast floor")
    args = parser.parse_args(argv)

    if args.out_dir.resolve().is_relative_to(Path("assets").resolve()):
        raise SystemExit("refusing to write candidates under assets/")

    skin = Image.open(args.skin).convert("RGBA")
    failed = False

    for category in (args.category or sorted(SOURCES)):
        source_path, palettes, prefix, first = SOURCES[category]
        source = Image.open(source_path).convert("RGBA")

        if args.report or args.check_contrast:
            if category != "eyes":
                continue
            print(f"{category} contrast, sampled behind the head {HEAD_WINDOW}\n")
            rows, backgrounds = contrast_report(source, skin, palettes)
            if not print_report(rows, backgrounds):
                failed = True
            continue

        destination_dir = args.out_dir / category
        destination_dir.mkdir(parents=True, exist_ok=True)
        print(f"{category} from {source_path}")
        blobs = []
        for offset, palette in enumerate(palettes):
            if offset == 0:
                continue  # index 0 is the source itself, already registered
            image = recolour(source, skin, palette)
            number = f"{first + offset:03d}"
            destination = destination_dir / f"{prefix}_{number}_recolour_{palette.name}.png"
            image.save(destination)
            same_alpha = (image.getchannel("A").tobytes()
                          == source.getchannel("A").tobytes())
            blobs.append(image.tobytes())
            print(f"  {palette.name:10s} -> {destination.name}  alpha preserved: {same_alpha}")
        print(f"  {len(blobs)} recolours, {len(set(blobs))} distinct\n")

    if args.check_contrast:
        print("\nFAIL — a palette is under a contrast floor" if failed
              else "\nPASS — every palette clears both contrast floors")
        return 1 if failed else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
