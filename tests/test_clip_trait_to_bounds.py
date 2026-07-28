from __future__ import annotations

import unittest

from PIL import Image

from scripts import clip_trait_to_bounds as clipper


CANVAS = 1254
X_MIN, Y_MIN, X_MAX, Y_MAX = clipper.MAX_BOUNDS


def layer(box: tuple[int, int, int, int]) -> Image.Image:
    """Opaque rectangle on a transparent 1254 canvas; box is inclusive."""
    image = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    left, top, right, bottom = box
    image.paste((40, 40, 60, 255), (left, top, right + 1, bottom + 1))
    return image


class ClipTests(unittest.TestCase):
    def test_small_bottom_overhang_is_clipped_to_the_baseline(self) -> None:
        """The outfit_001 case: boot soles tapering five pixels past the floor."""
        result, report = clipper.clip(layer((500, 475, 750, Y_MAX + 5)))
        self.assertEqual(clipper.visible_box(result), (500, 475, 750, Y_MAX))
        self.assertEqual(report["overhang"]["bottom"], 5)

    def test_clip_reports_what_it_removed(self) -> None:
        _, report = clipper.clip(layer((500, 475, 750, Y_MAX + 2)))
        self.assertEqual(report["removed_pixels"], 251 * 2)
        self.assertGreater(report["removed_share"], 0)

    def test_layer_already_within_bounds_is_refused(self) -> None:
        """Clipping a compliant layer would be a silent no-op edit."""
        with self.assertRaises(ValueError) as ctx:
            clipper.clip(layer((500, 475, 750, Y_MAX - 10)))
        self.assertIn("already within bounds", str(ctx.exception))

    def test_deep_overhang_is_refused(self) -> None:
        """A deep overhang means a misplaced layer, which a clip would amputate."""
        with self.assertRaises(ValueError) as ctx:
            clipper.clip(layer((500, 475, 750, Y_MAX + clipper.MAX_OVERHANG_PX + 1)))
        self.assertIn("exceeds", str(ctx.exception))

    def test_clip_removing_too_much_of_the_layer_is_refused(self) -> None:
        """A shallow but very wide clip can still be removing real artwork."""
        # A short layer sitting mostly below the baseline: overhang is within the
        # depth ceiling, but it costs far more than 1% of the layer.
        with self.assertRaises(ValueError) as ctx:
            clipper.clip(layer((500, Y_MAX - 4, 750, Y_MAX + 5)))
        self.assertIn("above the", str(ctx.exception))

    def test_horizontal_overhang_is_clipped_too(self) -> None:
        result, report = clipper.clip(layer((X_MIN - 3, 475, X_MAX + 3, 900)))
        left, _, right, _ = clipper.visible_box(result)
        self.assertEqual((left, right), (X_MIN, X_MAX))
        self.assertEqual(report["overhang"]["left"], 3)
        self.assertEqual(report["overhang"]["right"], 3)

    def test_wrong_canvas_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            clipper.clip(Image.new("RGBA", (1024, 1024), (0, 0, 0, 255)))

    def test_fully_transparent_layer_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            clipper.clip(Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0)))

    def test_colour_channels_are_untouched(self) -> None:
        """A clip edits alpha only; the approved design must not change."""
        source = layer((500, 475, 750, Y_MAX + 3))
        result, _ = clipper.clip(source)
        self.assertEqual(result.getpixel((600, 800))[:3], source.getpixel((600, 800))[:3])

    def test_clipped_pixels_are_fully_transparent(self) -> None:
        result, _ = clipper.clip(layer((500, 475, 750, Y_MAX + 5)))
        self.assertEqual(result.getchannel("A").getpixel((600, Y_MAX + 1)), 0)


class RegisteredOutfitTests(unittest.TestCase):
    def test_every_registered_outfit_is_within_the_locked_bounds(self) -> None:
        """Regression guard for the defect this script was written to fix."""
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent
        for path in sorted((root / "assets" / "outfits").glob("*.png")):
            with self.subTest(outfit=path.name):
                image = Image.open(path).convert("RGBA")
                left, top, right, bottom = clipper.visible_box(image)
                self.assertGreaterEqual(left, X_MIN)
                self.assertGreaterEqual(top, Y_MIN)
                self.assertLessEqual(right, X_MAX)
                self.assertLessEqual(bottom, Y_MAX)


if __name__ == "__main__":
    unittest.main()
