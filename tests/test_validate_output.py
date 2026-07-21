from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import generate_777, validate_output


class ValidateOutputTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def save_background(self, path: Path, value: int) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (16, 16), (value, value, value, 255)).save(path)

    def save_trait(self, path: Path, value: int, offset: int) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        image.paste((value, 0, 0, 255), (offset, 4, offset + 6, 12))
        image.save(path)

    def generate(self, root: Path, *, dry_run: bool = False) -> Path:
        assets = root / "assets"
        self.save_background(assets / "backgrounds" / "background_001_one.png", 10)
        self.save_background(assets / "backgrounds" / "background_002_two.png", 20)
        self.save_trait(assets / "base_bodies" / "base_body_001_one.png", 100, 3)
        self.save_trait(assets / "base_bodies" / "base_pose_002_two.png", 200, 7)

        config_path = root / "config.json"
        compatibility_path = root / "compatibility.json"
        config_path.write_text('{"test": true}\n', encoding="utf-8")
        compatibility_path.write_text('{"requires": [], "excludes": []}\n', encoding="utf-8")

        output = root / "output"
        generate_777.generate_collection(
            assets_root=assets,
            output=output,
            collection={
                "name": "Demigods",
                "description": "Test collection",
                "canvas": {"width": 16, "height": 16},
            },
            compatibility={"requires": [], "excludes": []},
            seed="fixed-seed",
            supply=4,
            max_attempts=1000,
            dry_run=dry_run,
            overwrite=False,
            config_path=config_path,
            compatibility_path=compatibility_path,
        )
        return output

    def test_valid_rendered_output_passes(self) -> None:
        root = self.make_root()
        output = self.generate(root)
        result = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
        )
        self.assertTrue(result.passed, result.errors)
        self.assertEqual(result.metadata_files, 4)
        self.assertEqual(result.image_files, 4)
        self.assertEqual(result.unique_trait_signatures, 4)
        self.assertEqual(result.unique_image_hashes, 4)

    def test_tampered_image_hash_fails(self) -> None:
        root = self.make_root()
        output = self.generate(root)
        image_path = output / "images" / "0001.png"
        Image.new("RGBA", (16, 16), (1, 2, 3, 255)).save(image_path)
        result = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("image_sha256 does not match" in error for error in result.errors))
        self.assertTrue(any("manifest image_hashes" in error for error in result.errors))

    def test_missing_metadata_file_fails(self) -> None:
        root = self.make_root()
        output = self.generate(root)
        (output / "metadata" / "0003.json").unlink()
        result = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("missing metadata files" in error for error in result.errors))

    def test_duplicate_trait_signature_fails(self) -> None:
        root = self.make_root()
        output = self.generate(root)
        first = json.loads((output / "metadata" / "0001.json").read_text(encoding="utf-8"))
        second_path = output / "metadata" / "0002.json"
        second = json.loads(second_path.read_text(encoding="utf-8"))
        second["trait_signature"] = first["trait_signature"]
        second_path.write_text(json.dumps(second, indent=2) + "\n", encoding="utf-8")

        manifest_path = output / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["trait_signatures"][1] = first["trait_signature"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        result = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("unique trait signatures" in error for error in result.errors))

    def test_dry_run_requires_explicit_allowance(self) -> None:
        root = self.make_root()
        output = self.generate(root, dry_run=True)
        refused = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
        )
        self.assertFalse(refused.passed)
        self.assertTrue(any("not a final collection" in error for error in refused.errors))

        allowed = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
            allow_dry_run=True,
        )
        self.assertTrue(allowed.passed, allowed.errors)
        self.assertEqual(allowed.image_files, 0)

    def test_attribute_layer_order_tampering_fails(self) -> None:
        root = self.make_root()
        output = self.generate(root)
        metadata_path = output / "metadata" / "0001.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["attributes"] = list(reversed(metadata["attributes"]))
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

        result = validate_output.validate_output(
            output,
            expected_supply=4,
            expected_size=(16, 16),
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("canonical layer order" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
