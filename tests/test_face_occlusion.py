"""A head-worn trait must not cover the face it is worn above.

Every head accessory in this collection passed canvas, alpha, maximum-bounds and
width-ratio checks while sitting across the character's eyes, because none of
those measurements can tell a band worn on a head from one lying over a face.
Four separate review rounds were needed to catch by eye what this file checks by
measurement: the crown's band cut across both upper eyelids, the laurel's
branches flanked the eyes, and two circlets crossed the brow. Widening a trait
is what usually causes it - a proportional reduction grows the height with the
width, so a wider band drops lower unless its height is held.

The eye and eyebrow regions below are measured off the registered base master,
whose face is baked in, so they are fixed for the collection.
"""
from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Measured on assets/base_bodies/base_body_001_neutral_master.png as
# (left, top, right, bottom), inclusive.
EYE_REGIONS = ((505, 334, 584, 403), (669, 334, 748, 403))

# Alpha at or below this is a soft edge, not coverage.
OPAQUE = 128

# A trait may clip a few pixels of a region's corner without hiding anything.
EYE_BUDGET = 200

# Traits that legitimately hang past the face, with the reason and their own
# ceiling. A drape is not headwear sitting too low, but it still may not close
# over the eyes, so it carries a real number rather than an exemption.
DRAPING = {
    "head_accessory_008_translucent_white_veil.png": (
        3200, "sheer veil drapes down both sides of the face; the panels cross the outer "
              "corners of the eye regions and the eyes read through them"),
}

# Lowest opaque row each trait is approved to reach, pinning the seat that four
# review rounds arrived at. The eye rule above is the hard limit; this catches
# drift before it gets there, in either direction, and makes a reseat a
# deliberate edit to this table rather than a silent change.
LOWEST_INK_CEILING = {
    "head_accessory_001_gold_pointed_crown.png": 326,
    "head_accessory_002_large_gold_halo.png": 251,
    "head_accessory_003_green_laurel.png": 340,
    "head_accessory_004_black_curved_horns.png": 316,
    "head_accessory_005_silver_winged_circlet.png": 326,
    "head_accessory_006_silver_ornate_tiara.png": 360,
    "head_accessory_007_silver_drop_circlet.png": 359,
    "head_accessory_008_translucent_white_veil.png": 552,
    "head_accessory_009_pale_blue_spiked_tiara.png": 293,
    "head_accessory_010_gold_low_circlet.png": 327,
}


def opaque_pixels(alpha: Image.Image, regions) -> int:
    """Count pixels the layer actually hides inside the given regions."""
    total = 0
    for left, top, right, bottom in regions:
        patch = alpha.crop((left, top, right + 1, bottom + 1))
        total += sum(1 for value in patch.tobytes() if value > OPAQUE)
    return total


class HeadAccessoryFaceClearanceTests(unittest.TestCase):
    def head_accessories(self):
        directory = ROOT / "assets" / "head_accessories"
        if not directory.is_dir():
            self.skipTest("head_accessories not registered yet")
        return sorted(directory.glob("*.png"))

    def test_no_head_accessory_covers_the_eyes(self) -> None:
        for path in self.head_accessories():
            with self.subTest(asset=path.name):
                with Image.open(path) as image:
                    alpha = image.convert("RGBA").getchannel("A")
                covered = opaque_pixels(alpha, EYE_REGIONS)
                budget = DRAPING.get(path.name, (EYE_BUDGET, ""))[0]
                self.assertLessEqual(
                    covered, budget,
                    f"{path.name} puts {covered} opaque pixels over the eyes; "
                    f"a head-worn trait belongs above them",
                )

    def test_lowest_ink_stays_where_it_was_approved(self) -> None:
        """Catch a reseat before it reaches the eyes.

        The eye rule is the hard limit and says nothing until a trait is already
        over the face. These ceilings pin the seat each design was approved at,
        so widening a trait - which grows its height and drops its lowest row -
        fails here first.
        """
        for path in self.head_accessories():
            with self.subTest(asset=path.name):
                self.assertIn(path.name, LOWEST_INK_CEILING,
                              "new head accessory: measure its lowest row and record a ceiling")
                with Image.open(path) as image:
                    alpha = image.convert("RGBA").getchannel("A")
                box = alpha.point(lambda v: 255 if v > OPAQUE else 0).getbbox()
                self.assertIsNotNone(box, f"{path.name} has no opaque pixels")
                lowest = box[3] - 1
                self.assertLessEqual(
                    lowest, LOWEST_INK_CEILING[path.name],
                    f"{path.name} now reaches Y{lowest}; it was approved no lower than "
                    f"Y{LOWEST_INK_CEILING[path.name]}",
                )


if __name__ == "__main__":
    unittest.main()
