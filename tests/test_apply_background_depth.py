from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import apply_background_depth


class BackgroundDepthTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def source(self) -> Image.Image:
        """A detailed background: flat colour would hide both blur and vignette."""
        image = Image.new("RGB", apply_background_depth.CANVAS, (40, 60, 140))
        for x in range(0, apply_background_depth.CANVAS[0], 24):
            for y in range(0, apply_background_depth.CANVAS[1], 24):
                image.paste((230, 220, 180), (x, y, x + 12, y + 12))
        return image

    def treat(self, image: Image.Image, **kwargs) -> Image.Image:
        # Grade off by default so blur and vignette assertions stay isolated.
        options = {"blur_radius": 3.0, "vignette_strength": 0.3, "vignette_power": 2.4,
                   "grade": 0.0, "desaturate": 0.0, "darken": 1.0}
        options.update(kwargs)
        return apply_background_depth.apply_depth(image, **options)

    def test_output_keeps_canvas_mode_and_full_opacity(self) -> None:
        result = self.treat(self.source())
        self.assertEqual(result.size, apply_background_depth.CANVAS)
        self.assertEqual(result.mode, "RGB")

    def test_treatment_is_deterministic(self) -> None:
        """Re-running must reproduce identical bytes, or provenance is meaningless."""
        first = self.treat(self.source())
        second = self.treat(self.source())
        self.assertEqual(first.tobytes(), second.tobytes())

    def test_corners_are_darkened_and_the_centre_is_not(self) -> None:
        """Vignette only: blur is isolated out so a single sample stays meaningful."""
        source = self.source()
        result = self.treat(source, blur_radius=0.0)
        width, height = apply_background_depth.CANVAS

        def mean_luma(image: Image.Image, box: tuple[int, int, int, int]) -> float:
            region = image.crop(box).convert("L")
            data = list(region.getdata())
            return sum(data) / len(data)

        corner = (0, 0, 120, 120)
        centre = (width // 2 - 60, height // 2 - 60, width // 2 + 60, height // 2 + 60)

        self.assertLess(
            mean_luma(result, corner),
            mean_luma(source, corner) * 0.9,
            "corner must be visibly vignetted",
        )
        self.assertAlmostEqual(
            mean_luma(result, centre),
            mean_luma(source, centre),
            delta=mean_luma(source, centre) * 0.05,
            msg="the centre staging region must stay essentially untouched",
        )

    def test_blur_reduces_local_contrast(self) -> None:
        source = self.source()
        result = self.treat(source, vignette_strength=0.0)
        band_before = [source.getpixel((x, 600))[0] for x in range(560, 700)]
        band_after = [result.getpixel((x, 600))[0] for x in range(560, 700)]
        spread_before = max(band_before) - min(band_before)
        spread_after = max(band_after) - min(band_after)
        self.assertLess(spread_after, spread_before)

    def test_grade_pulls_disparate_scenes_toward_one_palette(self) -> None:
        """Two differently-tinted backgrounds must converge under the shared grade."""
        warm = Image.new("RGB", apply_background_depth.CANVAS, (210, 120, 40))
        cool = Image.new("RGB", apply_background_depth.CANVAS, (40, 120, 210))

        def mean(image: Image.Image) -> tuple[float, float, float]:
            data = list(image.getdata())
            n = len(data)
            return tuple(sum(px[i] for px in data) / n for i in range(3))

        before = sum(abs(a - b) for a, b in zip(mean(warm), mean(cool)))
        graded_warm = apply_background_depth.harmonise(warm, grade=0.34, desaturate=0.22, darken=0.93)
        graded_cool = apply_background_depth.harmonise(cool, grade=0.34, desaturate=0.22, darken=0.93)
        after = sum(abs(a - b) for a, b in zip(mean(graded_warm), mean(graded_cool)))
        self.assertLess(after, before, "the grade must reduce palette divergence")

    def test_grade_darkens_so_the_foreground_separates(self) -> None:
        scene = self.source()
        graded = apply_background_depth.harmonise(scene, grade=0.34, desaturate=0.22, darken=0.93)

        def luma(image: Image.Image) -> float:
            data = list(image.convert("L").getdata())
            return sum(data) / len(data)

        self.assertLess(luma(graded), luma(scene))

    def test_grade_can_be_disabled(self) -> None:
        scene = self.source()
        untouched = apply_background_depth.harmonise(scene, grade=0.0, desaturate=0.0, darken=1.0)
        self.assertEqual(untouched.tobytes(), scene.tobytes())

    def test_wrong_canvas_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.treat(Image.new("RGB", (1024, 1024), (10, 10, 10)))

    def test_refuses_to_write_into_assets(self) -> None:
        """Registered backgrounds are pinned by SHA-256; treated files are candidates."""
        source = self.make_root() / "bg.png"
        self.source().save(source)
        code = apply_background_depth.main([str(source), "--out-dir", "assets/backgrounds"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
