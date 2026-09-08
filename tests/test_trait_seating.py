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
