from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import validate_assets


class ValidateAssetsTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def make_image(
        self,
        path: Path,
        *,
        mode: str = "RGBA",
        size: tuple[int, int] = (2048, 2048),
        fill: tuple[int, ...] = (0, 0, 0, 0),
        visible_box: tuple[int, int, int, int] | None = (400, 300, 1600, 1860),
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new(mode, size, fill)
        if visible_box is not None:
            patch_size = (visible_box[2] - visible_box[0], visible_box[3] - visible_box[1])
            patch = Image.new(
                mode,
                patch_size,
                (200, 180, 160, 255) if mode == "RGBA" else (200, 180, 160),
            )
            image.paste(patch, visible_box[:2])
        image.save(path)
        return path

    def test_valid_transparent_pose_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(Path(temp) / "base_pose_001_relaxed_open.png")
            result = validate_assets.validate_file(path, 2048, 2048)
            self.assertTrue(result.passed, result.errors)

    def test_three_digit_sequence_required(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(Path(temp) / "eyes_warm_brown.png")
            result = validate_assets.validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertTrue(any("three-digit" in error for error in result.errors))

    def test_folder_category_must_match_filename(self) -> None:
        root = self.make_root() / "assets"
        path = self.make_image(root / "eyes" / "mouth_001_smile.png")
        result = validate_assets.validate_file(path, 2048, 2048, category="eyes")
        self.assertFalse(result.passed)
        self.assertTrue(any("stored under" in error for error in result.errors))

    def test_background_must_not_contain_transparency(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(Path(temp) / "background_001_celestial_temple.png")
            result = validate_assets.validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertIn("background contains transparent pixels", result.errors)

    def test_aura_may_touch_canvas_edges(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "aura_front_001_glow.png"
            Image.new("RGBA", (2048, 2048), (100, 100, 255, 128)).save(path)
            result = validate_assets.validate_file(path, 2048, 2048)
            self.assertTrue(result.passed, result.errors)

    def test_non_effect_trait_may_not_touch_edge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self.make_image(
                Path(temp) / "hair_front_001_side_bangs.png",
                visible_box=(0, 200, 1200, 1000),
            )
            result = validate_assets.validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertTrue(any("touch a canvas edge" in error for error in result.errors))

    def test_corrupted_png_fails_complete_decode(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "eyes_001_warm_brown.png"
            path.write_bytes(b"\x89PNG\r\n\x1a\ntruncated")
            result = validate_assets.validate_file(path, 2048, 2048)
            self.assertFalse(result.passed)
            self.assertTrue(any("fully decode" in error for error in result.errors))

    def test_manifest_accepts_blocked_reference(self) -> None:
        repository = self.make_root()
        assets = repository / "assets"
        (repository / "docs").mkdir(parents=True)
        (repository / "docs" / "production_status.md").write_text("status\n", encoding="utf-8")
        (assets / "base_body").mkdir(parents=True)
        (assets / "base_body" / "base_body_001_neutral_master.webp").write_bytes(b"reference")
        manifest = {
            "target_supply": 777,
            "master_canvas": {"width": 2048, "height": 2048},
            "status_ledger": "docs/production_status.md",
            "production_directories": {
                category: f"assets/{category}"
                for category in validate_assets.PRODUCTION_CATEGORIES
            },
            "approved_visual_references": [
                {
                    "path": "assets/base_body/base_body_001_neutral_master.webp",
                    "production_ready": False,
                }
            ],
            "blocked_assets": [
                {"intended_path": "assets/base_bodies/base_pose_001_relaxed_open.png"}
            ],
        }
        manifest_path = assets / "asset_manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        result = validate_assets.validate_manifest(manifest_path, repository)
        self.assertTrue(result.passed, result.errors)
        self.assertTrue(result.warnings)


if __name__ == "__main__":
    unittest.main()
