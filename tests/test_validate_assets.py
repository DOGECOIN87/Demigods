from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.validate_assets import validate_file


class ValidateAssetsTests(unittest.TestCase):
    def make_image(
        self,
        directory: Path,
        name: str,
        *,
        mode: str = "RGBA",
        size: tuple[int, int] = (2048, 2048),
        fill: tuple[int, ...] = (0, 0, 0, 0),
        visible_box: tuple[int, int, int, int] | None = (400, 300, 1600, 1860),
    ) -> Path:
        path = directory / name
        image = Image.new(mode, size, fill)
        if visible_box is not None:
            patch_size = (visible_box[2] - visible_box[0], visible_box[3] - visible_box[1])
            if mode == "RGBA":
                patch = Image.new(mode, patch_size, (200, 180, 160, 255))
            else:
                patch = Image.new(mode, patch_size, (200, 180, 160))
            image.paste(patch, visible_box[:2])
        image.save(path)
        return path

    def test_valid_transparent_pose_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(Path(temp), "base_pose_001_relaxed_open.png")
            result = validate_file(path, 2048, 2048)
            self.assertTrue(result.passed, result.errors)

    def test_transparent_trait_must_be_rgba(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(
                Path(temp),
                "eyes_001_warm_brown.png",
                mode="RGB",
                fill=(0, 0, 0),
            )
            result = validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertIn("mode is RGB, expected RGBA", result.errors)

    def test_background_must_not_contain_transparency(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(Path(temp), "background_001_celestial_temple.png")
            result = validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertIn("background contains transparent pixels", result.errors)

    def test_wrong_dimensions_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(
                Path(temp),
                "mouth_001_small_smile.png",
                size=(1024, 1024),
                visible_box=(300, 300, 700, 700),
            )
            result = validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertTrue(any("size is" in error for error in result.errors))

    def test_unknown_prefix_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(Path(temp), "random_001_asset.png")
            result = validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertIn("filename does not match a recognized production asset prefix", result.errors)

    def test_visible_pixels_must_not_touch_edge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(
                Path(temp),
                "hair_front_001_side_bangs.png",
                visible_box=(0, 200, 1200, 1000),
            )
            result = validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertTrue(any("touch a canvas edge" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
