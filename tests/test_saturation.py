from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import generate_777


class EstimateValidSpaceTests(unittest.TestCase):
    """The preflight ceiling ignores compatibility rules; this closes that gap.

    A library of five pose-locked outfits and five base poses has five valid
    (outfit, pose) pairs, not twenty-five. Multiplying raw category counts
    overstated the real space fivefold, and the supply check was reading the
    overstated number.
    """

    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def assets(self, **categories: int) -> dict[str, list[Path]]:
        built = {}
        for category, count in categories.items():
            folder = self.root / category
            folder.mkdir(parents=True, exist_ok=True)
            files = []
            for index in range(1, count + 1):
                path = folder / f"{category}_{index:03d}.png"
                path.touch()
                files.append(path)
            built[category] = files
        return built

    def test_no_rules_leaves_the_ceiling_intact(self) -> None:
        assets = self.assets(backgrounds=4, outfits=3)
        space, fraction = generate_777.estimate_valid_space(assets, {}, {})
        self.assertEqual(space, 12)
        self.assertEqual(fraction, 1.0)

    def test_pose_locked_outfits_collapse_the_space(self) -> None:
        assets = self.assets(base_bodies=5, outfits=5)
        rules = {
            "requires": [
                {"trait": f"outfits_{i:03d}.png", "requires": f"base_bodies_{i:03d}.png"}
                for i in range(1, 6)
            ]
        }
        ceiling = generate_777.theoretical_space(assets, {})
        space, fraction = generate_777.estimate_valid_space(assets, {}, rules, samples=40000)
        self.assertEqual(ceiling, 25)
        # Exactly 5 of 25 pairings satisfy the rules.
        self.assertAlmostEqual(fraction, 0.2, delta=0.02)
        self.assertAlmostEqual(space, 5, delta=1)

    def test_excludes_reduce_the_space(self) -> None:
        assets = self.assets(hair_back=2, outfits=2)
        rules = {"excludes": [{"trait": "hair_back_001.png", "excludes": ["outfits_001.png"]}]}
        space, fraction = generate_777.estimate_valid_space(assets, {}, rules, samples=40000)
        self.assertAlmostEqual(fraction, 0.75, delta=0.02)
        self.assertAlmostEqual(space, 3, delta=1)

    def test_optional_category_absence_is_counted(self) -> None:
        assets = self.assets(backgrounds=2, rear_auras=3)
        space, _ = generate_777.estimate_valid_space(assets, {"rear_auras": 0.5}, {})
        self.assertEqual(space, 8)  # 2 x (3 + 1 absent branch)

    def test_empty_library_is_zero(self) -> None:
        space, fraction = generate_777.estimate_valid_space({}, {}, {})
        self.assertEqual(space, 0)
        self.assertEqual(fraction, 0.0)

    def test_estimate_is_deterministic(self) -> None:
        assets = self.assets(base_bodies=3, outfits=3)
        rules = {"requires": [{"trait": "outfits_001.png", "requires": "base_bodies_001.png"}]}
        first = generate_777.estimate_valid_space(assets, {}, rules)
        second = generate_777.estimate_valid_space(assets, {}, rules)
        self.assertEqual(first, second)


class SaturationReportTests(unittest.TestCase):
    def test_warns_when_the_supply_nearly_exhausts_the_space(self) -> None:
        report = generate_777.saturation_report(777, 800, 0.2, 4000)
        self.assertIn("97.1%", report)
        self.assertIn("effectively exhaustive", report)

    def test_warns_at_moderate_saturation(self) -> None:
        report = generate_777.saturation_report(777, 1200, 0.3, 4000)
        self.assertIn("stop being rare", report)

    def test_healthy_saturation_carries_no_warning(self) -> None:
        report = generate_777.saturation_report(777, 64800, 0.5, 130000)
        self.assertNotIn("WARNING", report)

    def test_reports_both_the_ceiling_and_the_valid_space(self) -> None:
        report = generate_777.saturation_report(777, 800, 0.2, 4000)
        self.assertIn("4000", report)
        self.assertIn("800", report)

    def test_zero_valid_space_does_not_divide_by_zero(self) -> None:
        report = generate_777.saturation_report(777, 0, 0.0, 0)
        self.assertNotIn("saturation", report)


if __name__ == "__main__":
    unittest.main()
