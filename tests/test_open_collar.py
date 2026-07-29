from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

from scripts import open_collar as oc


ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254


def fake_base(neck_left=596, neck_right=660, top=440, bottom=600) -> Image.Image:
    """A stand-in body: an opaque neck column."""
    im = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    im.paste((240, 200, 170, 255), (neck_left, top, neck_right + 1, bottom))
    return im


def sealed_collar(left=560, right=700, top=470, bottom=560) -> Image.Image:
    """A stand-in garment whose opening is painted solid across the neck."""
    im = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    im.paste((30, 60, 70, 255), (left, top, right + 1, bottom))
    return im


class OpenCollarTests(unittest.TestCase):
    def test_neck_becomes_visible(self) -> None:
        base, outfit = fake_base(), sealed_collar()
        before = oc.neck_visibility(outfit, base)
        result, cleared = oc.open_collar(
            outfit, base, top=474, close_by=512, half_top=33, half_bottom=9
        )
        after = oc.neck_visibility(result, base)
        self.assertGreater(cleared, 0)
        self.assertGreater(after, before)

    def test_collar_rim_outside_the_neck_is_untouched(self) -> None:
        """The rim is what distinguishes an opened collar from a hole."""
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(
            outfit, base, top=474, close_by=512, half_top=33, half_bottom=9
        )
        rim = result.getchannel("A").load()
        for x in (565, 575, 690, 698):          # well outside the neck column
            for y in (480, 495, 510):
                self.assertEqual(rim[x, y], 255, f"rim eroded at ({x},{y})")

    def test_nothing_above_the_span_is_touched(self) -> None:
        base, outfit = fake_base(), sealed_collar()
        original = outfit.getchannel("A").load()
        result, _ = oc.open_collar(
            outfit, base, top=474, close_by=512, half_top=33, half_bottom=9
        )
        after = result.getchannel("A").load()
        for y in (470, 471, 472, 473):
            self.assertEqual(after[627, y], original[627, y])

    def test_garment_closes_below_the_span(self) -> None:
        """Removal must fade out, not end on a horizontal cut."""
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(
            outfit, base, top=474, close_by=512, half_top=33, half_bottom=9
        )
        alpha = result.getchannel("A").load()
        self.assertEqual(alpha[627, 520], 255)
        self.assertEqual(alpha[627, 540], 255)

    def test_opening_narrows_into_a_v(self) -> None:
        """A straight column produced the hard vertical edges this replaces."""
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(
            outfit, base, top=474, close_by=512, half_top=33, half_bottom=9
        )
        alpha = result.getchannel("A").load()
        def opened_width(y):
            return sum(1 for x in range(560, 701) if alpha[x, y] < 128)
        self.assertGreater(opened_width(480), opened_width(500))

    def test_edges_are_soft_not_binary(self) -> None:
        """Anti-aliased input must yield anti-aliased output."""
        base = fake_base()
        # Soften the neck edge so the mask has intermediate values.
        from PIL import ImageFilter
        base.putalpha(base.getchannel("A").filter(ImageFilter.GaussianBlur(1.5)))
        result, _ = oc.open_collar(
            sealed_collar(), base, top=474, close_by=512, half_top=33, half_bottom=9
        )
        alpha = result.getchannel("A")
        values = {alpha.getpixel((x, 490)) for x in range(590, 670)}
        self.assertTrue(any(0 < v < 255 for v in values), "no intermediate alpha")


class RegisteredOutfitNeckTests(unittest.TestCase):
    """Regression guard: the two repaired collars must stay open."""

    CASES = [
        ("outfit_002_storm_guardian_pose_002.png",
         "base_pose_002_viewer_left_vertical_grip.png", 24.0),
        ("outfit_003_verdant_alchemist_pose_003.png",
         "base_pose_003_viewer_right_vertical_grip.png", 22.0),
    ]

    def test_repaired_collars_show_the_neck(self) -> None:
        for outfit_name, base_name, floor in self.CASES:
            with self.subTest(outfit=outfit_name):
                outfit = Image.open(ROOT / "assets" / "outfits" / outfit_name).convert("RGBA")
                base = Image.open(ROOT / "assets" / "base_bodies" / base_name).convert("RGBA")
                self.assertGreater(oc.neck_visibility(outfit, base), floor)


if __name__ == "__main__":
    unittest.main()
