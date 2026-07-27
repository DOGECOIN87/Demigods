from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import embed_srgb_profile


class EmbedSrgbProfileTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def write_png(self, mode: str = "RGBA") -> Path:
        path = self.make_root() / "asset.png"
        image = Image.new(mode, (64, 64), (10, 120, 200, 255)[: len(mode)])
        for x in range(0, 64, 8):
            image.paste((240, 90, 30, 255)[: len(mode)], (x, x, x + 4, x + 4))
        image.save(path)
        return path

    def test_profile_is_embedded(self) -> None:
        path = self.write_png()
        with Image.open(path) as before:
            self.assertIsNone(before.info.get("icc_profile"))

        changed, message = embed_srgb_profile.embed(path, embed_srgb_profile.srgb_profile_bytes())
        self.assertTrue(changed, message)
        with Image.open(path) as after:
            self.assertTrue(after.info.get("icc_profile"))

    def test_pixel_data_is_untouched(self) -> None:
        """The whole point: this tags metadata, it does not re-encode the image."""
        path = self.write_png()
        with Image.open(path) as image:
            image.load()
            before = image.tobytes()

        embed_srgb_profile.embed(path, embed_srgb_profile.srgb_profile_bytes())

        with Image.open(path) as image:
            image.load()
            self.assertEqual(image.tobytes(), before)

    def test_mode_and_size_are_preserved(self) -> None:
        for mode in ("RGBA", "RGB"):
            with self.subTest(mode=mode):
                path = self.write_png(mode)
                embed_srgb_profile.embed(path, embed_srgb_profile.srgb_profile_bytes())
                with Image.open(path) as image:
                    self.assertEqual(image.mode, mode)
                    self.assertEqual(image.size, (64, 64))

    def test_already_tagged_file_is_skipped_and_left_byte_identical(self) -> None:
        path = self.write_png()
        profile = embed_srgb_profile.srgb_profile_bytes()
        embed_srgb_profile.embed(path, profile)
        digest = embed_srgb_profile.sha256_file(path)

        changed, message = embed_srgb_profile.embed(path, profile)
        self.assertFalse(changed)
        self.assertEqual(message, "already tagged")
        self.assertEqual(
            embed_srgb_profile.sha256_file(path), digest,
            "re-running must not churn hashes of already-tagged assets",
        )

    def test_registered_assets_are_all_tagged(self) -> None:
        root = Path(__file__).resolve().parent.parent
        assets = root / "assets"
        if not assets.is_dir():
            self.skipTest("assets directory not present")

        untagged = []
        for path in sorted(assets.rglob("*.png")):
            with Image.open(path) as image:
                if not image.info.get("icc_profile"):
                    untagged.append(path.name)
        self.assertEqual(untagged, [], "every production asset must declare sRGB explicitly")


if __name__ == "__main__":
    unittest.main()
