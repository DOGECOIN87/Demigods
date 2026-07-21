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

    def save_rgba(self, path: Path, *, opaque: bool = False, touch_edge: bool = False) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
        if opaque:
            image = Image.new("RGBA", (2048, 2048), (10, 20, 30, 255))
        else:
            left = 0 if touch_edge else 900
            image.paste((255, 0, 0, 255), (left, 900, 1100, 1100))
        image.save(path)

    def test_valid_transparent_asset_passes(self) -> None:
        root = self.make_root() / "assets"
        path = root / "eyes" / "eyes_001_warm_brown.png"
        self.save_rgba(path)
        result = validate_assets.validate_asset(path, root, 2048, 2048)
        self.assertTrue(result.passed, result.errors)
        self.assertEqual(result.visible_bbox, (900, 900, 1100, 1100))

    def test_fully_opaque_trait_fails(self) -> None:
        root = self.make_root() / "assets"
        path = root / "eyes" / "eyes_001_warm_brown.png"
        self.save_rgba(path, opaque=True)
        result = validate_assets.validate_asset(path, root, 2048, 2048)
        self.assertFalse(result.passed)
        self.assertTrue(any("fully opaque" in error for error in result.errors))

    def test_edge_touching_non_effect_trait_fails(self) -> None:
        root = self.make_root() / "assets"
        path = root / "eyes" / "eyes_001_warm_brown.png"
        self.save_rgba(path, touch_edge=True)
        result = validate_assets.validate_asset(path, root, 2048, 2048)
        self.assertFalse(result.passed)
        self.assertTrue(any("touch a canvas edge" in error for error in result.errors))

    def test_opaque_background_passes(self) -> None:
        root = self.make_root() / "assets"
        path = root / "backgrounds" / "background_001_celestial_temple.png"
        self.save_rgba(path, opaque=True)
        result = validate_assets.validate_asset(path, root, 2048, 2048)
        self.assertTrue(result.passed, result.errors)

    def test_transparent_background_fails(self) -> None:
        root = self.make_root() / "assets"
        path = root / "backgrounds" / "background_001_celestial_temple.png"
        self.save_rgba(path)
        result = validate_assets.validate_asset(path, root, 2048, 2048)
        self.assertFalse(result.passed)
        self.assertTrue(any("background alpha" in error for error in result.errors))

    def test_wrong_category_prefix_fails(self) -> None:
        root = self.make_root() / "assets"
        path = root / "eyes" / "mouth_001_smile.png"
        self.save_rgba(path)
        result = validate_assets.validate_asset(path, root, 2048, 2048)
        self.assertFalse(result.passed)
        self.assertTrue(any("prefix" in error for error in result.errors))

    def test_manifest_accepts_blocked_reference(self) -> None:
        repository = self.make_root()
        assets = repository / "assets"
        (repository / "docs").mkdir(parents=True)
        (repository / "docs" / "production-status.md").write_text("status\n", encoding="utf-8")
        (assets / "base_body").mkdir(parents=True)
        (assets / "base_body" / "base_body_001_neutral_master.webp").write_bytes(b"reference")
        manifest = {
            "target_supply": 777,
            "master_canvas": {"width": 2048, "height": 2048},
            "status_ledger": "docs/production-status.md",
            "production_directories": {
                category: f"assets/{category}" for category in validate_assets.PRODUCTION_CATEGORIES
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
