from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import build_global_finish, rig_gate_report


ROOT = Path(__file__).resolve().parent.parent


class GlobalFinishBuilderTests(unittest.TestCase):
    def test_every_variant_stays_under_the_alpha_ceiling(self) -> None:
        """A finish that can reach opacity would hide the art it grades."""
        for name, (tint, peak, angle, falloff) in build_global_finish.VARIANTS.items():
            with self.subTest(variant=name):
                image = build_global_finish.render(tint, peak, angle, falloff)
                _, alpha_max = image.getchannel("A").getextrema()
                self.assertLessEqual(alpha_max, rig_gate_report.GLOBAL_FINISH_MAX_ALPHA)
                self.assertEqual(alpha_max, peak)

    def test_render_is_full_canvas_rgba(self) -> None:
        tint, peak, angle, falloff = build_global_finish.VARIANTS["global_finish_001_soft_bloom"]
        image = build_global_finish.render(tint, peak, angle, falloff)
        self.assertEqual(image.size, (1254, 1254))
        self.assertEqual(image.mode, "RGBA")

    def test_colour_channels_never_darken_toward_gray(self) -> None:
        """Matte contamination is the failure mode the aura builders exist to avoid.

        Colour must stay constant across the ramp so a low-alpha pixel reads as
        its own hue rather than as dark gray.
        """
        tint, peak, angle, falloff = build_global_finish.VARIANTS["global_finish_002_gilded_warm"]
        image = build_global_finish.render(tint, peak, angle, falloff)
        colours = {px[:3] for px in image.getdata()}
        self.assertEqual(colours, {tint})

    def test_gradient_is_directional(self) -> None:
        """Peak alpha sits on the key-light side, falling off toward the opposite corner."""
        tint, peak, angle, falloff = build_global_finish.VARIANTS["global_finish_001_soft_bloom"]
        image = build_global_finish.render(tint, peak, angle, falloff)
        alpha = image.getchannel("A")
        self.assertGreater(alpha.getpixel((0, 0)), alpha.getpixel((1253, 1253)))

    def test_variants_are_visually_distinct(self) -> None:
        """Three recolours of one identical ramp would not be three assets."""
        signatures = set()
        for tint, peak, angle, falloff in build_global_finish.VARIANTS.values():
            signatures.add((tint, peak, angle, falloff))
        self.assertEqual(len(signatures), len(build_global_finish.VARIANTS))


class GlobalFinishGateTests(unittest.TestCase):
    def setUp(self) -> None:
        spec = rig_gate_report.load_rig(ROOT / "config" / "collection.json")
        self.rig = spec["rig"]
        self.canvas = spec["canvas"]

    def write(self, image: Image.Image) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "finish.png"
        image.save(path)
        return path

    def analyze(self, path: Path, **kwargs) -> dict:
        return rig_gate_report.analyze(path, self.rig, self.canvas, 1, **kwargs)

    def checks(self, result: dict) -> dict[str, bool]:
        return {name: passed for name, passed, *_ in result["checks"]}

    def test_valid_finish_passes_global_finish_mode(self) -> None:
        tint, peak, angle, falloff = build_global_finish.VARIANTS["global_finish_003_cool_veil"]
        path = self.write(build_global_finish.render(tint, peak, angle, falloff))
        result = self.analyze(path, global_finish=True)
        self.assertTrue(result["passed"], result["checks"])

    def test_finish_over_the_ceiling_fails(self) -> None:
        image = Image.new("RGBA", (1254, 1254), (255, 240, 200, 200))
        result = self.analyze(self.write(image), global_finish=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["alpha_ceiling"])

    def test_fully_opaque_finish_fails(self) -> None:
        image = Image.new("RGBA", (1254, 1254), (255, 240, 200, 255))
        result = self.analyze(self.write(image), global_finish=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["not_opaque"])

    def test_wrong_canvas_fails_even_within_the_ceiling(self) -> None:
        image = Image.new("RGBA", (1024, 1024), (255, 240, 200, 30))
        result = self.analyze(self.write(image), global_finish=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["canvas"])

    def test_exemption_does_not_leak_into_trait_mode(self) -> None:
        """A full-canvas grade must still fail an ordinary partial-layer gate.

        This is the same containment the --floor-aura mode carries: the scoped
        allowance may not become a way to pass a layer that covers everything.
        """
        tint, peak, angle, falloff = build_global_finish.VARIANTS["global_finish_001_soft_bloom"]
        path = self.write(build_global_finish.render(tint, peak, angle, falloff))
        result = self.analyze(path, trait=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["max_bounds"])


if __name__ == "__main__":
    unittest.main()
