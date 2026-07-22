from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import intake_approved_base


class ApprovedBaseIntakeGeometryTests(unittest.TestCase):
    def make_png(self, bbox: tuple[int, int, int, int]) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "candidate.png"
        image = Image.new("RGBA", intake_approved_base.EXPECTED_SIZE, (0, 0, 0, 0))
        image.paste((220, 190, 160, 255), bbox)
        image.save(path)
        return temp, path

    def inspect(self, bbox: tuple[int, int, int, int]) -> dict[str, object]:
        temp, path = self.make_png(bbox)
        self.addCleanup(temp.cleanup)
        return intake_approved_base.inspect_source(path)

    def test_exact_locked_geometry_passes(self) -> None:
        report = self.inspect((400, 141, 855, 1140))
        self.assertTrue(report["passed_binary_qa"], report["errors"])
        self.assertTrue(report["rig_geometry"]["passed"])

    def test_wrong_head_top_fails(self) -> None:
        report = self.inspect((400, 140, 855, 1140))
        self.assertFalse(report["passed_binary_qa"])
        self.assertTrue(any("top of visible head" in error for error in report["errors"]))

    def test_wrong_foot_baseline_fails(self) -> None:
        report = self.inspect((400, 141, 855, 1139))
        self.assertFalse(report["passed_binary_qa"])
        self.assertTrue(any("foot baseline" in error for error in report["errors"]))

    def test_pixels_outside_maximum_bounds_fail(self) -> None:
        report = self.inspect((232, 141, 1023, 1140))
        self.assertFalse(report["passed_binary_qa"])
        self.assertTrue(any("maximum character bounds" in error for error in report["errors"]))

    def test_decentered_silhouette_fails(self) -> None:
        report = self.inspect((410, 141, 855, 1140))
        self.assertFalse(report["passed_binary_qa"])
        self.assertTrue(any("not centered" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
