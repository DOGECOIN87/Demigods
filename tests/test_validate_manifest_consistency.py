from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import validate_assets, validate_manifest_consistency


class ManifestConsistencyTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def make_asset(self, root: Path, *, size: tuple[int, int] = (1254, 1254)) -> Path:
        path = root / "assets" / "base_bodies" / "base_body_001_neutral_master.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        image.paste((200, 180, 160, 255), (245, 184, 979, 1139))
        image.save(path)
        return path

    def manifest(self, entries: list[dict[str, object]]) -> dict[str, object]:
        return {
            "master_canvas": {"width": 1254, "height": 1254},
            "registered_production_assets": entries,
        }

    def write_manifest(self, root: Path, value: dict[str, object]) -> Path:
        path = root / "assets" / "asset_manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def registered_entry(self, path: Path) -> dict[str, object]:
        return {
            "id": "base_body_001",
            "category": "base_bodies",
            "path": "assets/base_bodies/base_body_001_neutral_master.png",
            "status": "production_ready",
            "sha256": validate_assets.sha256_file(path),
            "dimensions": [1254, 1254],
        }

    def test_empty_registry_passes_during_preproduction(self) -> None:
        root = self.make_root()
        manifest = self.write_manifest(root, self.manifest([]))
        result = validate_manifest_consistency.validate_manifest_consistency(manifest, root)
        self.assertTrue(result.passed, result.errors)
        self.assertEqual(result.checked, 0)

    def test_valid_registered_asset_passes(self) -> None:
        root = self.make_root()
        asset = self.make_asset(root)
        manifest = self.write_manifest(root, self.manifest([self.registered_entry(asset)]))
        result = validate_manifest_consistency.validate_manifest_consistency(manifest, root)
        self.assertTrue(result.passed, result.errors)
        self.assertEqual(result.checked, 1)

    def test_missing_registered_asset_fails(self) -> None:
        root = self.make_root()
        entry = self.registered_entry(self.make_asset(root))
        (root / str(entry["path"])).unlink()
        manifest = self.write_manifest(root, self.manifest([entry]))
        result = validate_manifest_consistency.validate_manifest_consistency(manifest, root)
        self.assertFalse(result.passed)
        self.assertTrue(any("does not exist" in error for error in result.errors))

    def test_sha256_mismatch_fails(self) -> None:
        root = self.make_root()
        entry = self.registered_entry(self.make_asset(root))
        entry["sha256"] = "0" * 64
        manifest = self.write_manifest(root, self.manifest([entry]))
        result = validate_manifest_consistency.validate_manifest_consistency(manifest, root)
        self.assertFalse(result.passed)
        self.assertTrue(any("SHA-256 does not match" in error for error in result.errors))

    def test_dimension_mismatch_fails(self) -> None:
        root = self.make_root()
        asset = self.make_asset(root, size=(1024, 1024))
        entry = self.registered_entry(asset)
        manifest = self.write_manifest(root, self.manifest([entry]))
        result = validate_manifest_consistency.validate_manifest_consistency(manifest, root)
        self.assertFalse(result.passed)
        self.assertTrue(any("dimensions are" in error for error in result.errors))

    def test_nonproduction_ready_status_fails(self) -> None:
        root = self.make_root()
        entry = self.registered_entry(self.make_asset(root))
        entry["status"] = "blocked"
        manifest = self.write_manifest(root, self.manifest([entry]))
        result = validate_manifest_consistency.validate_manifest_consistency(manifest, root)
        self.assertFalse(result.passed)
        self.assertTrue(any("status must be" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
