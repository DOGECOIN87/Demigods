from __future__ import annotations

import colorsys
import unittest
from pathlib import Path

from PIL import Image

from scripts import build_face_recolours as recolours


ROOT = Path(__file__).resolve().parent.parent


class ContrastGateTests(unittest.TestCase):
    """The gate is only worth having if it actually runs.

    It sat broken for a commit: removing the weight argument from `shift` left
    a stale three-argument call inside the reporting path, so `--check-contrast`
    raised TypeError and exited non-zero for a reason that had nothing to do
    with contrast. Nothing exercised it.
    """

    def setUp(self) -> None:
        self.source = Image.open(
            ROOT / "assets" / "eyes" / "eyes_025_base_master_brown.png"
        ).convert("RGBA")
        self.skin = Image.open(
            ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png"
        ).convert("RGBA")

    def test_report_runs_over_every_registered_palette(self) -> None:
        rows, backgrounds = recolours.contrast_report(
            self.source, self.skin, recolours.EYE_PALETTES
        )
        self.assertEqual(len(rows), len(recolours.EYE_PALETTES))
        self.assertTrue(backgrounds, "no background met the saturation floor")

    def test_every_palette_clears_both_contrast_floors(self) -> None:
        rows, _ = recolours.contrast_report(
            self.source, self.skin, recolours.EYE_PALETTES
        )
        for row in rows:
            name = row["palette"].name
            self.assertGreaterEqual(
                row["skin"], recolours.MIN_SKIN_DISTANCE,
                f"{name} iris is too close to skin to read",
            )
            if row["exempt"]:
                continue
            _, gap = row["nearest"]
            self.assertGreaterEqual(
                gap, recolours.MIN_BACKGROUND_HUE_SEPARATION,
                f"{name} iris shares a hue band with a registered background",
            )

    def test_only_the_master_and_neutrals_are_exempt(self) -> None:
        rows, _ = recolours.contrast_report(
            self.source, self.skin, recolours.EYE_PALETTES
        )
        for index, row in enumerate(rows):
            if not row["exempt"]:
                continue
            self.assertTrue(
                index == 0 or row["saturation"] < recolours.NEUTRAL_SATURATION,
                f"{row['palette'].name} is exempt without being the master or neutral",
            )


class RecolourInvariantTests(unittest.TestCase):
    def test_partial_recolour_never_leaves_the_two_endpoint_hues(self) -> None:
        """Mixing must happen in RGB, not along the hue circle.

        Interpolating the hue angle from the source brown toward magenta takes
        a half-weight pixel through green, which drew a dashed rainbow along the
        top edge of every recoloured eye.
        """
        palette = next(p for p in recolours.EYE_PALETTES if p.name == "magenta")
        original = (222, 137, 88)
        shifted = recolours.shift(original, palette)
        for step in range(1, 10):
            mixed = recolours.blend(original, shifted, step / 10)
            for index in range(3):
                low = min(original[index], shifted[index])
                high = max(original[index], shifted[index])
                self.assertGreaterEqual(mixed[index] + 1, low)
                self.assertLessEqual(mixed[index] - 1, high)

    def test_shift_preserves_value(self) -> None:
        palette = next(p for p in recolours.EYE_PALETTES if p.name == "teal")
        for original in ((222, 137, 88), (68, 45, 34), (129, 72, 61)):
            _, _, before = colorsys.rgb_to_hsv(*(c / 255 for c in original))
            _, _, after = colorsys.rgb_to_hsv(
                *(c / 255 for c in recolours.shift(original, palette))
            )
            self.assertAlmostEqual(before, after, delta=1 / 255)

    def test_registered_recolours_share_the_source_alpha(self) -> None:
        source = Image.open(
            ROOT / "assets" / "eyes" / "eyes_025_base_master_brown.png"
        ).convert("RGBA")
        expected = source.getchannel("A").tobytes()
        found = 0
        for path in sorted((ROOT / "assets" / "eyes").glob("*_recolour_*.png")):
            with Image.open(path) as image:
                self.assertEqual(
                    image.convert("RGBA").getchannel("A").tobytes(), expected,
                    f"{path.name} changed the alpha channel",
                )
            found += 1
        self.assertGreater(found, 0, "no eye recolours are registered")

    def test_registered_recolours_are_all_distinct(self) -> None:
        blobs = []
        for path in sorted((ROOT / "assets" / "eyes").glob("*.png")):
            with Image.open(path) as image:
                blobs.append(image.convert("RGBA").tobytes())
        self.assertEqual(len(blobs), len(set(blobs)), "two eye assets are identical")


if __name__ == "__main__":
    unittest.main()
