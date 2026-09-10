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

import json
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


class NeckAccessoryWithdrawalTests(unittest.TestCase):
    """The neck accessory category is withdrawn, and must not come back untouched.

    Two passes were spent seating these eight pieces - out of mid-chest to the
    throat, then to the row where each one's topmost ink lands inside the
    silhouette - and both were fixing the wrong thing. Rendered over an outfit
    they are chest-wide bands and bows lying across the collarbones and the
    garment's own collar, and pendants hanging from points outside the neck. A
    150-175 px ornament cannot be seated on a 61 px neck.

    The seating assertions that used to live here would have passed on the
    re-registered files, because they measured where the pieces sit. This measures
    the thing that was actually wrong: how big they are against the anatomy.

    `docs/qa/neck_accessories_withdrawn_2026-09-10.md`.
    """

    # The base master's neck is 61 px across at Y 482. A choker wraps it; a chain
    # meets it. Neither is twice its width.
    NECK_WIDTH = 61
    MAX_WIDTH_RATIO = 1.6

    def test_no_neck_accessory_is_registered_without_being_redrawn(self) -> None:
        directory = ROOT / "assets" / "neck_accessories"
        if not directory.is_dir():
            return
        for path in sorted(directory.glob("*.png")):
            with self.subTest(asset=path.name):
                left, _top, right, _bottom = visible_bounds(path)
                width = right - left + 1
                self.assertLessEqual(
                    width / self.NECK_WIDTH, self.MAX_WIDTH_RATIO,
                    f"{path.name} is {width} px wide against a {self.NECK_WIDTH} px neck. The "
                    f"category was withdrawn on 2026-09-10 for exactly this; a re-registered "
                    f"piece has to be drawn to the neck, not re-seated onto it",
                )

    def test_the_withdrawal_is_recorded(self) -> None:
        manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())
        registered = [e for e in manifest["registered_production_assets"]
                      if e["category"] == "neck_accessories"]
        withdrawn = [b for b in manifest.get("blocked_assets", [])
                     if str(b.get("id", "")).startswith("neck_accessory")]
        if registered:
            self.skipTest("neck accessories have been redrawn and re-registered")
        self.assertEqual(len(withdrawn), 8,
                         "the eight withdrawn neck accessories must stay on the record "
                         "with their reason, so the category is not quietly forgotten")
        for entry in withdrawn:
            with self.subTest(asset=entry["id"]):
                self.assertTrue(entry.get("reason"), f"{entry['id']} is withdrawn with no reason")
                self.assertTrue(entry.get("requirement"),
                                f"{entry['id']} is withdrawn with no requirement for its replacement")
                self.assertTrue((ROOT / entry["retained_at"]).exists(),
                                f"{entry['id']}'s withdrawn bytes are not where the manifest says")


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


if __name__ == "__main__":
    unittest.main()
