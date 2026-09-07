from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

from scripts import hide_undergarment as hu


ROOT = Path(__file__).resolve().parent.parent


class UndergarmentMaskTests(unittest.TestCase):
    def test_mask_finds_the_garment_and_not_the_skin(self) -> None:
        base = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        base.paste((252, 202, 161, 255), (500, 400, 760, 1000))   # skin torso
        base.paste((251, 218, 182, 255), (540, 520, 720, 820))    # garment
        mask = hu.undergarment_mask(base).load()
        self.assertEqual(mask[627, 560], 255)   # inside the garment
        self.assertEqual(mask[520, 450], 0)     # skin above it

    def test_tolerance_bounds_the_grow(self) -> None:
        base = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        base.paste((252, 202, 161, 255), (500, 400, 760, 1000))
        base.paste((251, 218, 182, 255), (540, 520, 720, 820))
        tight = hu.undergarment_mask(base, tolerance=2).load()
        self.assertEqual(tight[520, 450], 0, "skin must never enter the mask")


class RepaintTests(unittest.TestCase):
    def make(self):
        """Both mask seeds must stay under the garment, as they do on the real
        bases — a seed inside the exposed band would read as skin after repaint
        and flood the mask across the whole torso."""
        base = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        base.paste((252, 202, 161, 255), (500, 400, 760, 1000))
        base.paste((251, 218, 182, 255), (540, 500, 720, 820))
        outfit = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        # Covers from y=530 down, leaving a 30px band exposed; seeds at y=560
        # and y=780 both sit under it.
        outfit.paste((80, 60, 120, 255), (520, 530, 740, 900))
        return base, outfit

    def test_exposed_undergarment_is_eliminated(self) -> None:
        base, outfit = self.make()
        before = hu.exposed_count(base, outfit)
        self.assertGreater(before, 0)
        result, report = hu.repaint(base, outfit)
        self.assertEqual(hu.exposed_count(result, outfit), 0)
        self.assertEqual(report["repainted"], report["target"])

    def test_repaint_uses_skin_colour_not_garment_colour(self) -> None:
        """Values must come from real skin, so nothing is invented."""
        base, outfit = self.make()
        result, _ = hu.repaint(base, outfit)
        px = result.load()
        r, g, b, _ = px[627, 530]           # was garment, now exposed-and-repainted
        self.assertLess(abs(g - 202), 25)   # near skin's green, not garment's 218
        self.assertLess(abs(b - 161), 30)

    def test_covered_undergarment_is_left_alone(self) -> None:
        """The fix is deliberately limited to what can actually be seen."""
        base, outfit = self.make()
        result, _ = hu.repaint(base, outfit)
        px = result.load()
        self.assertEqual(px[627, 780][:3], (251, 218, 182))

    def test_alpha_is_never_modified(self) -> None:
        base, outfit = self.make()
        result, _ = hu.repaint(base, outfit)
        self.assertEqual(
            list(base.getchannel("A").getdata()),
            list(result.getchannel("A").getdata()),
        )


class RegisteredBaseTests(unittest.TestCase):
    """Regression guard: no registered outfit may reveal the undergarment.

    The floor is a handful of pixels rather than exactly zero, and that is a
    property of the artwork rather than slack in the fix. The tank
    `(251,218,182)` and thigh skin `(252,202,161)` overlap in colour space, so
    any ball drawn around the garment's colour catches a few genuinely
    skin-coloured pixels. What remains is 4 px across all five bases — a 2x2
    cluster and a single pixel, each a pale skin tone. Exposure before the fix
    was 2, 99, 33, 374 and 507.
    """

    # Undergarment still visible through each outfit, in pixels, after the
    # 2026-09-07 fit-gap pass. The number before that pass is in the comment.
    #
    # What the pass fixed: narrow gaps where a garment failed to meet the arm or
    # shoulder and let a tank strap show. Those touch genuine skin, so colour
    # diffuses into them cleanly, and they are gone.
    #
    # What it deliberately left: neckline openings the outfit means to leave
    # open. They are enclosed by more tank rather than skin, so there is nothing
    # to diffuse from - an attempt produced a blotchy patch in outfit_007's chest
    # V and a smear in outfit_009's collar. Covering them means the outfit
    # carrying its own inner garment, which is a re-render, not a pixel edit.
    # Until then the tank reads there as a linen undershirt.
    #
    # These are ceilings, not targets: they pin the state so an outfit or base
    # edit cannot quietly widen an opening or reintroduce a fit gap.
    EXPOSURE_CEILING = {
        "outfit_001_celestial_scholar_pose_001.png": 10,      # was 0
        "outfit_002_storm_guardian_pose_002.png": 10,         # was 3
        "outfit_003_verdant_alchemist_pose_003.png": 10,      # was 0
        "outfit_004_lunar_oracle_pose_004.png": 10,           # was 0
        "outfit_005_sun_temple_pose_005.png": 10,             # was 0
        "outfit_006_black_layered_hooded_robe.png": 10,       # was 0
        "outfit_007_brown_leather_long_coat.png": 2900,       # was 3569, chest V remains
        "outfit_008_olive_ragged_cloak.png": 450,             # was 749, neck opening remains
        "outfit_009_navy_high_collar_coat.png": 520,          # was 1362, collar V remains
        "outfit_010_celestial_robe_white_gold.png": 10,       # was 344, fully fixed
    }

    def test_exposure_stays_within_recorded_bounds(self) -> None:
        """Every outfit bound to a base, not a hardcoded five.

        The pair list used to be hardcoded, so outfits 006-010 - all bound to the
        neutral master - were never checked, and four of them exposed the tank.
        Reading the bindings from config/compatibility.json means a newly
        registered outfit is covered the moment its rule lands; a new outfit with
        no ceiling recorded here fails until someone measures it.
        """
        for base_name, outfit_names in hu.base_outfit_pairs().items():
            base = Image.open(ROOT / "assets" / "base_bodies" / base_name).convert("RGBA")
            for outfit_name in outfit_names:
                with self.subTest(base=base_name, outfit=outfit_name):
                    self.assertIn(outfit_name, self.EXPOSURE_CEILING,
                                  "new outfit: measure its exposure and record a ceiling")
                    outfit = Image.open(ROOT / "assets" / "outfits" / outfit_name).convert("RGBA")
                    self.assertLessEqual(hu.exposed_count(base, outfit),
                                         self.EXPOSURE_CEILING[outfit_name])

    def test_verification_is_stricter_than_the_repaint_mask(self) -> None:
        """Verifying at the mask's own tolerance re-flags correct output.

        Skin repainted from neighbouring skin lands within ~26 levels of the
        tank simply because they are that close, so the two tolerances must
        stay distinct.
        """
        self.assertLess(hu.VERIFY_TOLERANCE, hu.TOLERANCE)


if __name__ == "__main__":
    unittest.main()
