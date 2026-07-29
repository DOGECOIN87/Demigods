from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image, ImageFilter

from scripts import open_collar as oc


ROOT = Path(__file__).resolve().parent.parent
CANVAS = 1254
RIM = dict(rim_centre=502.0, rim_rise=12.0, half=32.0)


def fake_base(neck_left=596, neck_right=660, top=440, bottom=600) -> Image.Image:
    """Stand-in body: an opaque neck column."""
    im = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    im.paste((240, 200, 170, 255), (neck_left, top, neck_right + 1, bottom))
    return im


def sealed_collar(left=560, right=700, top=470, bottom=560) -> Image.Image:
    """Stand-in garment whose opening is painted solid across the neck."""
    im = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    im.paste((30, 60, 70, 255), (left, top, right + 1, bottom))
    return im


class OpenCollarTests(unittest.TestCase):
    def test_neck_becomes_visible(self) -> None:
        base, outfit = fake_base(), sealed_collar()
        before = oc.neck_visibility(outfit, base)
        result, cleared = oc.open_collar(outfit, base, **RIM)
        self.assertGreater(cleared, 0)
        self.assertGreater(oc.neck_visibility(result, base), before)

    def test_bottom_edge_is_crisp_not_faded(self) -> None:
        """A crossfade reads as a smear, not as fabric.

        The first working version faded removal out over ~18 rows and produced a
        muddy translucent band where skin and collar blended. The transition must
        complete within a couple of rows.
        """
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(outfit, base, **RIM)
        alpha = result.getchannel("A").load()
        column = [alpha[627, y] for y in range(490, 512)]
        partial = [v for v in column if 20 < v < 235]
        self.assertLessEqual(len(partial), 2, f"soft ramp of {len(partial)} rows: {column}")

    def test_rim_arc_is_lower_at_the_centre(self) -> None:
        """The opening follows the collar's own rim, which dips at the middle."""
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(outfit, base, **RIM)
        alpha = result.getchannel("A").load()

        def last_open_row(x):
            rows = [y for y in range(472, 540) if alpha[x, y] < 40]
            return max(rows) if rows else -1

        self.assertGreater(last_open_row(627), last_open_row(603))

    def test_collar_rim_outside_the_neck_is_untouched(self) -> None:
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(outfit, base, **RIM)
        rim = result.getchannel("A").load()
        for x in (565, 575, 690, 698):
            for y in (480, 495, 510):
                self.assertEqual(rim[x, y], 255, f"rim eroded at ({x},{y})")

    def test_nothing_above_the_span_is_touched(self) -> None:
        base, outfit = fake_base(), sealed_collar()
        original = outfit.getchannel("A").load()
        result, _ = oc.open_collar(outfit, base, **RIM)
        after = result.getchannel("A").load()
        for y in range(465, oc.TOP):
            self.assertEqual(after[627, y], original[627, y])

    def test_garment_closes_below_the_rim(self) -> None:
        base, outfit = fake_base(), sealed_collar()
        result, _ = oc.open_collar(outfit, base, **RIM)
        alpha = result.getchannel("A").load()
        self.assertEqual(alpha[627, 515], 255)
        self.assertEqual(alpha[627, 540], 255)

    def test_horizontal_edges_inherit_the_base_anti_aliasing(self) -> None:
        base = fake_base()
        base.putalpha(base.getchannel("A").filter(ImageFilter.GaussianBlur(1.5)))
        result, _ = oc.open_collar(sealed_collar(), base, **RIM)
        alpha = result.getchannel("A")
        values = {alpha.getpixel((x, 485)) for x in range(590, 670)}
        self.assertTrue(any(0 < v < 255 for v in values), "no intermediate alpha")


class RegisteredOutfitNeckTests(unittest.TestCase):
    """Regression guard: the two repaired collars must stay open."""

    CASES = [
        ("outfit_002_storm_guardian_pose_002.png",
         "base_pose_002_viewer_left_vertical_grip.png", 25.0),
        ("outfit_003_verdant_alchemist_pose_003.png",
         "base_pose_003_viewer_right_vertical_grip.png", 28.0),
    ]

    def test_repaired_collars_show_the_neck(self) -> None:
        for outfit_name, base_name, floor in self.CASES:
            with self.subTest(outfit=outfit_name):
                outfit = Image.open(ROOT / "assets" / "outfits" / outfit_name).convert("RGBA")
                base = Image.open(ROOT / "assets" / "base_bodies" / base_name).convert("RGBA")
                self.assertGreater(oc.neck_visibility(outfit, base), floor)


if __name__ == "__main__":
    unittest.main()
