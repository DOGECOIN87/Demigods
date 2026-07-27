from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import rig_gate_report


ROOT = Path(__file__).resolve().parent.parent


class RigGateModeTests(unittest.TestCase):
    def setUp(self) -> None:
        spec = rig_gate_report.load_rig(ROOT / "config" / "collection.json")
        self.rig = spec["rig"]
        self.canvas = spec["canvas"]
        self.baseline = self.rig["foot_baseline_y"]

    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def write_band(self, top: int, bottom: int, left: int = 400, right: int = 860) -> Path:
        """A transparent canvas with one opaque horizontal band."""
        path = self.make_root() / "candidate.png"
        image = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        image.paste((140, 190, 250, 255), (left, top, right, bottom))
        image.save(path)
        return path

    def checks(self, result: dict) -> dict[str, bool]:
        return {name: passed for name, passed, *_ in result["checks"]}

    def analyze(self, path: Path, **kwargs) -> dict:
        return rig_gate_report.analyze(path, self.rig, self.canvas, 1, **kwargs)

    def test_floor_aura_allows_the_near_arc_below_the_foot_baseline(self) -> None:
        path = self.write_band(self.baseline - 60, self.baseline + 80)
        result = self.analyze(path, floor_aura=True)
        self.assertTrue(result["passed"], result["checks"])
        self.assertTrue(self.checks(result)["max_bounds"])

    def test_trait_mode_still_rejects_pixels_below_the_foot_baseline(self) -> None:
        """The floor-aura exemption must not leak into ordinary partial layers."""
        path = self.write_band(self.baseline - 60, self.baseline + 80)
        result = self.analyze(path, trait=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["max_bounds"])

    def test_floor_aura_still_enforces_horizontal_bounds(self) -> None:
        bounds = self.rig["maximum_character_bounds"]
        path = self.write_band(self.baseline - 60, self.baseline + 80, left=bounds[0] - 40, right=1200)
        result = self.analyze(path, floor_aura=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["max_bounds"])

    def test_floor_aura_still_enforces_the_top_bound(self) -> None:
        bounds = self.rig["maximum_character_bounds"]
        path = self.write_band(bounds[1] - 40, self.baseline)
        result = self.analyze(path, floor_aura=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["max_bounds"])

    def test_floor_aura_touching_the_canvas_edge_is_clipped_and_fails(self) -> None:
        """Reaching the final row means the glow is cut off, not merely low."""
        path = self.write_band(self.baseline - 60, self.canvas["height"])
        result = self.analyze(path, floor_aura=True)
        self.assertFalse(self.checks(result)["max_bounds"])

    def test_floor_aura_just_clear_of_the_canvas_edge_passes(self) -> None:
        path = self.write_band(self.baseline - 60, self.canvas["height"] - 2)
        result = self.analyze(path, floor_aura=True)
        self.assertTrue(result["passed"], result["checks"])

    def test_floor_aura_requires_genuine_transparency(self) -> None:
        path = self.make_root() / "opaque.png"
        Image.new("RGBA", (1254, 1254), (140, 190, 250, 255)).save(path)
        result = self.analyze(path, floor_aura=True)
        self.assertFalse(result["passed"])
        self.assertFalse(self.checks(result)["transparent_bg"])

    def test_registered_floor_ring_candidate_passes_floor_aura_mode(self) -> None:
        candidate = (
            ROOT
            / "images"
            / "trait_candidates"
            / "rear_auras"
            / "aura_rear_001_blue_floor_ring_candidate_attempt_005.png"
        )
        if not candidate.is_file():
            self.skipTest("DG-015 candidate not present")
        result = self.analyze(candidate, floor_aura=True)
        self.assertTrue(result["passed"], result["checks"])


class FloorRingBuilderTests(unittest.TestCase):
    def test_ring_is_seated_so_the_near_arc_passes_below_the_foot_baseline(self) -> None:
        from scripts import build_aura_floor_ring as builder

        image = builder.render()
        bbox = image.getchannel("A").getbbox()
        left, top, right, bottom = bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1

        self.assertGreater(bottom, builder.FOOT_BASELINE_Y, "near arc must pass in front of the toes")
        self.assertLess(bottom, builder.CANVAS - 1, "ring must not clip the canvas edge")
        self.assertAlmostEqual((left + right) / 2, builder.CENTER_X, delta=1)
        self.assertGreaterEqual(left, builder.MAX_BOUNDS[0])
        self.assertLessEqual(right, builder.MAX_BOUNDS[2])

    def test_every_partial_alpha_pixel_stays_bright(self) -> None:
        """The matte failure of attempt 001: fringe luminance tracking alpha."""
        from scripts import build_aura_floor_ring as builder

        image = builder.render()
        total = 0
        dark = 0
        for r, g, b, a in image.getdata():
            if 0 < a < 255:
                total += 1
                if 0.2126 * r + 0.7152 * g + 0.0722 * b < 120:
                    dark += 1
        self.assertGreater(total, 0)
        self.assertEqual(dark, 0, "a luminous aura must never carry dark semi-transparent pixels")


if __name__ == "__main__":
    unittest.main()
