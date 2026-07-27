from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import refit_trait_layer, rig_gate_report


ROOT = Path(__file__).resolve().parent.parent


class RefitTraitLayerTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def layer(self, box: tuple[int, int, int, int]) -> Image.Image:
        image = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        image.paste((200, 200, 220, 255), box)
        return image

    def bounds(self, image: Image.Image) -> tuple[int, int, int, int]:
        return refit_trait_layer.visible_box(image)

    def test_scaling_reduces_width_by_the_requested_factor(self) -> None:
        source = self.layer((327, 200, 927, 700))  # 600 x 500
        result = refit_trait_layer.refit(source, scale=0.5, top_y=132)
        left, top, right, bottom = self.bounds(result)
        self.assertAlmostEqual(right - left + 1, 300, delta=2)
        self.assertAlmostEqual(bottom - top + 1, 250, delta=2)

    def test_result_is_centred_on_the_locked_axis(self) -> None:
        # Deliberately off-centre input: the refit must recentre it.
        source = self.layer((200, 200, 700, 700))
        result = refit_trait_layer.refit(source, scale=0.84, top_y=132)
        left, _, right, _ = self.bounds(result)
        self.assertAlmostEqual((left + right) / 2, refit_trait_layer.CENTER_X, delta=1)

    def test_top_is_seated_at_the_requested_y(self) -> None:
        source = self.layer((327, 400, 927, 900))
        result = refit_trait_layer.refit(source, scale=0.84, top_y=132)
        _, top, _, _ = self.bounds(result)
        self.assertEqual(top, 132)

    def test_canvas_is_preserved(self) -> None:
        """A refit must never change the native canvas."""
        source = self.layer((327, 200, 927, 700))
        result = refit_trait_layer.refit(source, scale=0.6, top_y=132)
        self.assertEqual(result.size, (1254, 1254))
        self.assertEqual(result.mode, "RGBA")

    def test_wrong_canvas_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            refit_trait_layer.refit(Image.new("RGBA", (1024, 1024)), scale=0.8, top_y=132)

    def test_non_positive_scale_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            refit_trait_layer.refit(self.layer((327, 200, 927, 700)), scale=0.0, top_y=132)

    def test_fully_transparent_layer_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            refit_trait_layer.refit(Image.new("RGBA", (1254, 1254), (0, 0, 0, 0)), scale=0.8, top_y=132)

    def test_registered_hair_back_meets_its_proportion_target(self) -> None:
        """Regression: the registered layer must stay near 1.2x, not 1.46x."""
        hair = ROOT / "assets" / "hair_back" / "hair_back_003_silver_long_wavy.png"
        base = ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png"
        if not hair.is_file() or not base.is_file():
            self.skipTest("registered assets not present")

        spec = rig_gate_report.load_rig(ROOT / "config" / "collection.json")
        result = rig_gate_report.analyze(
            hair, spec["rig"], spec["canvas"], 1,
            trait=True, base=rig_gate_report.base_metrics(base), max_width_ratio=1.35,
        )
        self.assertTrue(result["passed"], result["checks"])
        self.assertLessEqual(result["width_ratio"], 1.35)
        self.assertGreaterEqual(
            result["crown_offset"], 0,
            "rear hair must reach the head crown or a bald gap shows above the hairline",
        )


class GateProportionTests(unittest.TestCase):
    def setUp(self) -> None:
        spec = rig_gate_report.load_rig(ROOT / "config" / "collection.json")
        self.rig, self.canvas = spec["rig"], spec["canvas"]
        self.base = {"width": 443, "crown_y": 141}

    def make_layer(self, width: int, top: int = 132) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "layer.png"
        image = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        left = 627 - width // 2
        image.paste((200, 200, 220, 255), (left, top, left + width, top + 400))
        image.save(path)
        return path

    def analyze(self, path: Path, max_ratio: float | None):
        return rig_gate_report.analyze(
            path, self.rig, self.canvas, 1, trait=True, base=self.base, max_width_ratio=max_ratio
        )

    def test_over_wide_layer_fails_when_a_threshold_is_set(self) -> None:
        result = self.analyze(self.make_layer(647), 1.35)  # 1.46x, the original defect
        self.assertFalse(result["passed"])

    def test_in_proportion_layer_passes(self) -> None:
        result = self.analyze(self.make_layer(545), 1.35)  # 1.23x, the refit
        self.assertTrue(result["passed"], result["checks"])

    def test_threshold_is_opt_in_so_wings_are_not_false_failed(self) -> None:
        """Back accessories legitimately exceed body width; default is report-only."""
        result = self.analyze(self.make_layer(647), None)
        self.assertTrue(result["passed"], result["checks"])
        self.assertEqual(result["width_ratio"], 1.46)

    def test_crown_offset_sign_marks_a_bald_gap(self) -> None:
        below = self.analyze(self.make_layer(545, top=180), None)
        above = self.analyze(self.make_layer(545, top=132), None)
        self.assertLess(below["crown_offset"], 0, "starting below the crown leaves a bald gap")
        self.assertGreater(above["crown_offset"], 0)


if __name__ == "__main__":
    unittest.main()
