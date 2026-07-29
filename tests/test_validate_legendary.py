from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import validate_legendary as vl


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)

    def write(self, name: str, image: Image.Image) -> Path:
        path = self.dir / name
        image.save(path)
        return path

    def results(self, path: Path) -> dict[str, bool]:
        checks, _ = vl.check(path)
        return {name: ok for name, ok, _ in checks}

    def test_valid_piece_passes(self) -> None:
        image = Image.new("RGB", vl.CANVAS, (90, 70, 140))
        self.assertTrue(all(self.results(self.write("ok.png", image)).values()))

    def test_wrong_canvas_fails(self) -> None:
        image = Image.new("RGB", (1024, 1024), (90, 70, 140))
        self.assertFalse(self.results(self.write("small.png", image))["dimensions"])

    def test_any_transparency_fails(self) -> None:
        """A transparent pixel means a background was keyed, not painted."""
        image = Image.new("RGBA", vl.CANVAS, (90, 70, 140, 255))
        image.putpixel((0, 0), (0, 0, 0, 0))
        self.assertFalse(self.results(self.write("keyed.png", image))["fully_opaque"])

    def test_truncated_file_is_reported_not_raised(self) -> None:
        path = self.dir / "broken.png"
        path.write_bytes(b"\x89PNG\r\n\x1a\n truncated")
        checks, _ = vl.check(path)
        self.assertEqual(checks[0][0], "decode")
        self.assertFalse(checks[0][1])

    def test_digest_is_stable_and_content_derived(self) -> None:
        a = self.write("a.png", Image.new("RGB", vl.CANVAS, (10, 20, 30)))
        b = self.write("b.png", Image.new("RGB", vl.CANVAS, (10, 20, 30)))
        c = self.write("c.png", Image.new("RGB", vl.CANVAS, (10, 20, 31)))
        self.assertEqual(vl.check(a)[1], vl.check(b)[1])
        self.assertNotEqual(vl.check(a)[1], vl.check(c)[1])


class RegisteredLegendaryTests(unittest.TestCase):
    ENTRIES = MANIFEST.get("legendary_one_of_ones", [])

    def test_seven_pieces_are_registered(self) -> None:
        self.assertEqual(len(self.ENTRIES), 7)

    def test_every_piece_passes_its_checks(self) -> None:
        for entry in self.ENTRIES:
            with self.subTest(piece=entry["id"]):
                checks, digest = vl.check(ROOT / entry["path"])
                self.assertTrue(all(ok for _, ok, _ in checks))
                self.assertEqual(digest, entry["sha256"])

    def test_artwork_is_unique(self) -> None:
        """'1 of 1' is the premise; a duplicate would destroy it silently."""
        digests = [e["sha256"] for e in self.ENTRIES]
        self.assertEqual(len(set(digests)), len(digests))

    def test_legendaries_stay_out_of_the_trait_ledger(self) -> None:
        """Mixing them in would corrupt the category counts in the status report."""
        trait_paths = {e["path"] for e in MANIFEST["registered_production_assets"]}
        for entry in self.ENTRIES:
            with self.subTest(piece=entry["id"]):
                self.assertNotIn(entry["path"], trait_paths)

    def test_generator_cannot_see_the_legendary_folder(self) -> None:
        """assets/legendary/ must never be discovered as a trait category."""
        from scripts.generate_777 import LAYER_ORDER

        self.assertNotIn("legendary", LAYER_ORDER)

    def test_no_finish_or_depth_pass_was_applied(self) -> None:
        for entry in self.ENTRIES:
            with self.subTest(piece=entry["id"]):
                self.assertEqual(entry["provenance"]["postprocessing"], [])


if __name__ == "__main__":
    unittest.main()
