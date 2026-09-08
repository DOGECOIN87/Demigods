"""A trait must sit on the anatomy it is worn on.

Three whole categories shipped seated wrong, all from the same cause: a batch
normalized at one fixed width and seat instead of the seat each design needs.
Nothing in the existing gates could see it. Canvas size, alpha behaviour, maximum
bounds and width ratio are all satisfied by a layer sitting in completely the
wrong place — a choker halfway down the chest passes every one of them.

These assertions encode the anatomy the traits attach to, measured on the
registered base master, so a future batch cannot repeat it silently.
"""
from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

VISIBLE = 40

# Measured on assets/base_bodies/base_body_001_neutral_master.png.
THROAT_TOP, THROAT_BOTTOM = 465, 505       # chin to shoulder line
BODY_LEFT, BODY_RIGHT = 406, 848           # widest silhouette, arms included

# A neck accessory's clasp sits at the throat. Everything below it - a chain, a
# drop, the tails of a bow - is free to hang.
NECK_CLASP_BAND = (THROAT_TOP, THROAT_BOTTOM + 10)

# How many of a layer's topmost ink rows must land inside the body silhouette.
# One row could be a stray antialiased pixel; four is the piece genuinely
# touching what it hangs from.
CONTACT_ROWS = 4

# A wing pair has to clear the body to read as wings rather than as fins behind
# the shoulders. At the batch-wide 590 px the overhang was 74 px a side and every
# pair read as small; at 760 px it is 158 px a side.
MIN_WING_OVERHANG = 120

# Capes hang rather than spread, so they are measured on their drop instead.
CAPES = {
    "back_accessory_004_navy_formal_cape.png",
    "back_accessory_005_black_violet_ragged_cloak.png",
}


def visible_bounds(path: Path) -> tuple[int, int, int, int]:
    with Image.open(path) as image:
        alpha = image.convert("RGBA").getchannel("A")
    box = alpha.point(lambda v: 255 if v > VISIBLE else 0).getbbox()
    if box is None:
        raise AssertionError(f"{path.name} is fully transparent")
    return box[0], box[1], box[2] - 1, box[3] - 1


class NeckAccessorySeatingTests(unittest.TestCase):
    def test_every_neck_accessory_clasps_at_the_throat(self) -> None:
        """The whole category was refit to Y 545-555, which is mid-chest.

        The base body's throat is Y 465-505. Seated 50 px below it, every choker
        read as a chest strap and every pendant chain started below the
        collarbone with nothing holding it up.
        """
        directory = ROOT / "assets" / "neck_accessories"
        if not directory.is_dir():
            self.skipTest("neck_accessories not registered")
        low, high = NECK_CLASP_BAND
        for path in sorted(directory.glob("*.png")):
            with self.subTest(asset=path.name):
                top = visible_bounds(path)[1]
                self.assertTrue(
                    low <= top <= high,
                    f"{path.name} starts at Y{top}; a clasp belongs in the throat band "
                    f"Y{low}-Y{high}",
                )

    def test_every_neck_accessory_touches_the_body(self) -> None:
        """Being at the right height is not the same as being attached.

        Correcting the seat to the throat at Y 482 traded one error for another.
        These pieces are 150-175 px wide and the neck at Y 482 is 61 px, so the
        chain ends and band tips hung in open air either side of it - at the
        right height and attached to nothing. A necklace has to touch what it
        hangs from, so its topmost rows must land inside the silhouette.
        """
        directory = ROOT / "assets" / "neck_accessories"
        if not directory.is_dir():
            self.skipTest("neck_accessories not registered")
        with Image.open(ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png") as image:
            body = image.convert("RGBA").getchannel("A").point(lambda v: 255 if v > 128 else 0)
        width, _height = body.size

        def body_span(row: int):
            line = body.crop((0, row, width, row + 1)).tobytes()
            columns = [x for x, value in enumerate(line) if value]
            return (columns[0], columns[-1]) if columns else None

        for path in sorted(directory.glob("*.png")):
            with self.subTest(asset=path.name):
                with Image.open(path) as image:
                    alpha = image.convert("RGBA").getchannel("A")
                top = visible_bounds(path)[1]
                for row in range(top, top + CONTACT_ROWS):
                    line = alpha.crop((0, row, width, row + 1)).tobytes()
                    columns = [x for x, value in enumerate(line) if value > VISIBLE]
                    if not columns:
                        continue
                    span = body_span(row)
                    self.assertIsNotNone(span, f"{path.name}: no body at Y{row}")
                    self.assertGreaterEqual(
                        columns[0], span[0],
                        f"{path.name} reaches X{columns[0]} at Y{row}, past the body's X{span[0]}",
                    )
                    self.assertLessEqual(
                        columns[-1], span[1],
                        f"{path.name} reaches X{columns[-1]} at Y{row}, past the body's X{span[1]}",
                    )


class BackAccessorySeatingTests(unittest.TestCase):
    def test_every_wing_pair_clears_the_body(self) -> None:
        """Wings must extend past the silhouette on both sides.

        The whole category was normalized at 590 px - 74 px of overhang a side on
        a 443 px body - so every pair read as fins tucked behind the shoulders
        rather than wings, with the upper half hidden behind the head and hair.
        """
        directory = ROOT / "assets" / "back_accessories"
        if not directory.is_dir():
            self.skipTest("back_accessories not registered")
        for path in sorted(directory.glob("*.png")):
            if path.name in CAPES:
                continue
            with self.subTest(asset=path.name):
                left, _top, right, _bottom = visible_bounds(path)
                self.assertGreaterEqual(
                    BODY_LEFT - left, MIN_WING_OVERHANG,
                    f"{path.name} reaches only {BODY_LEFT - left} px past the body on the "
                    f"viewer-left; a wing pair needs {MIN_WING_OVERHANG}",
                )
                self.assertGreaterEqual(
                    right - BODY_RIGHT, MIN_WING_OVERHANG,
                    f"{path.name} reaches only {right - BODY_RIGHT} px past the body on the "
                    f"viewer-right; a wing pair needs {MIN_WING_OVERHANG}",
                )

    def test_capes_hang_from_the_shoulders_to_above_the_baseline(self) -> None:
        for name in sorted(CAPES):
            path = ROOT / "assets" / "back_accessories" / name
            if not path.exists():
                self.skipTest(f"{name} not registered")
            with self.subTest(asset=name):
                _left, top, _right, bottom = visible_bounds(path)
                self.assertLessEqual(top, 569, f"{name} starts below the shoulder line")
                self.assertLessEqual(bottom, 1139, f"{name} hangs past the foot baseline")
                self.assertGreaterEqual(bottom, 1000, f"{name} stops well short of the hem")


if __name__ == "__main__":
    unittest.main()


class OutfitFootwearTests(unittest.TestCase):
    """An outfit's footwear has to cover the leg it is drawn over.

    The base bodies have bare legs and feet. Nine of the ten outfits had footwear
    narrower than the leg by 7-17 px a side, so a strip of skin showed along each
    boot's outer edge on every token those outfits appeared in - up to 5469 px on
    `outfit_010`. No existing gate could see it: the garment was inside bounds, on
    the baseline, and the right width for its own torso.

    `outfit_002` keeps a larger allowance because its greaves genuinely stop above
    the ankle, and `outfit_005` and `outfit_010` are sandals whose straps are meant
    to leave skin between them - but that skin is interior, not a strip along the
    silhouette edge, and the numbers below pin it.
    """

    EXPOSED_LEG_CEILING = {
        "outfit_001_celestial_scholar_pose_001.png": 20,     # was 11
        "outfit_002_storm_guardian_pose_002.png": 220,       # was 845, open greave
        "outfit_003_verdant_alchemist_pose_003.png": 20,     # was 115
        "outfit_004_lunar_oracle_pose_004.png": 20,          # was 1315
        "outfit_005_sun_temple_pose_005.png": 20,            # was 2389
        "outfit_006_black_layered_hooded_robe.png": 25,      # was 2015
        "outfit_007_brown_leather_long_coat.png": 25,        # was 937
        "outfit_008_olive_ragged_cloak.png": 25,             # was 2698
        "outfit_009_navy_high_collar_coat.png": 20,          # was 3332
        "outfit_010_celestial_robe_white_gold.png": 30,      # was 5469
    }

    def test_no_outfit_leaves_the_leg_bare(self) -> None:
        from scripts.fit_boots_to_legs import exposed_leg_pixels, outfit_base_pairs

        for outfit_name, base_name in sorted(outfit_base_pairs().items()):
            with self.subTest(outfit=outfit_name):
                self.assertIn(outfit_name, self.EXPOSED_LEG_CEILING,
                              "new outfit: measure its exposed leg pixels and record a ceiling")
                with Image.open(ROOT / "assets" / "outfits" / outfit_name) as outfit_image:
                    outfit = outfit_image.convert("RGBA")
                with Image.open(ROOT / "assets" / "base_bodies" / base_name) as base_image:
                    base = base_image.convert("RGBA")
                exposed = exposed_leg_pixels(outfit, base)
                self.assertLessEqual(
                    exposed, self.EXPOSED_LEG_CEILING[outfit_name],
                    f"{outfit_name} leaves {exposed} px of bare leg showing below Y1000",
                )
