from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import bulk_intake, normalize_generator_source

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (
    ROOT
    / "images"
    / "trait_candidates"
    / "hair_front"
    / "hair_front_003_silver_straight_bangs_candidate_attempt_001.png"
)


class GeneratorSourceNormalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)

    def test_low_opacity_matte_source_normalizes_to_locked_canvas(self) -> None:
        output, provenance = normalize_generator_source.normalize(
            SOURCE,
            target_width=520,
            top_y=132,
            alpha_threshold=120,
        )
        self.assertEqual(output.mode, "RGBA")
        self.assertEqual(output.size, (1254, 1254))
        self.assertEqual(output.getchannel("A").getpixel((0, 0)), 0)
        self.assertEqual(provenance["origin"], "generator_source_transform")
        self.assertEqual(provenance["source_dimensions"], [1920, 1920])
        self.assertLess(provenance["transform"]["scale"], 1.0)
        self.assertEqual(
            provenance["transform"]["placement"]["bounds"], [367, 132, 886, 697]
        )

    def test_opaque_source_is_rejected_before_any_transform(self) -> None:
        source = self.dir / "opaque.png"
        Image.new("RGB", (1920, 1920), (255, 255, 255)).save(source)
        with self.assertRaisesRegex(ValueError, "real alpha channel"):
            normalize_generator_source.normalize(source, target_width=520, top_y=132)

    def test_edge_touching_source_is_rejected(self) -> None:
        source = self.dir / "edge_touching.png"
        image = Image.new("RGBA", (1920, 1920), (0, 0, 0, 0))
        image.paste((255, 255, 255, 255), (0, 100, 600, 700))
        image.save(source)
        with self.assertRaisesRegex(ValueError, "touch a source-canvas edge"):
            normalize_generator_source.normalize(source, target_width=520, top_y=132)

    def test_intake_rejects_tampered_transform_provenance(self) -> None:
        candidate = self.dir / "candidate.png"
        output, provenance = normalize_generator_source.normalize(
            SOURCE,
            target_width=520,
            top_y=132,
            alpha_threshold=120,
        )
        output.save(candidate)
        provenance["output_sha256"] = "0" * 64
        candidate.with_suffix(".png.provenance.json").write_text(json.dumps(provenance))
        loaded, errors = bulk_intake.load_transform_provenance(candidate)
        self.assertIsNotNone(loaded)
        self.assertIn("transform provenance output SHA-256 does not match normalized candidate", errors)


if __name__ == "__main__":
    unittest.main()
