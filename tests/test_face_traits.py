"""A face trait replaces a face that is already painted on.

The base bodies are not blank mannequins: `prompts/16` specifies "large warm-brown
eyes, small nose, and gentle closed-mouth smile", and every registered base has
them painted in. So an eyes, eyebrows or mouth layer has to *cover* the feature
underneath it, on every base, or the original shows beside the new one - and no
existing gate could see that, because a layer that covers nothing still passes
canvas, alpha, bounds and width-ratio checks.

These assertions measure the three things the family has to hold: coverage of the
baked feature across every base, clearance of the eyes by the layers that render
above them, and that no two eye colours ship visually identical.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Alpha at or below this is a soft edge, not coverage.
OPAQUE = 200

# Which baked feature each category has to cover.
COVERS = {"eyes": "eyes", "eyebrows": "eyebrows", "mouths": "mouth"}

# The eye regions, measured on the master. Mouths and expression marks render
# above the eyes layer, so neither may put ink over them.
EYE_REGIONS = ((505, 334, 584, 403), (669, 334, 748, 403))
EYE_BUDGET = 50


class FaceTraitCoverageTests(unittest.TestCase):
    """Every trait must hide the baked feature it stands in for, on every base."""

    @classmethod
    def setUpClass(cls) -> None:
        from scripts.build_face_traits import baked_footprints
        cls.footprints = baked_footprints()

    def test_every_face_trait_covers_the_baked_feature(self) -> None:
        for category, feature in COVERS.items():
            directory = ROOT / "assets" / category
            if not directory.is_dir():
                self.skipTest(f"{category} not registered")
            footprint = self.footprints[feature]
            self.assertGreater(footprint.sum(), 0, f"no baked {feature} measured")
            for path in sorted(directory.glob("*.png")):
                with self.subTest(asset=path.name):
                    with Image.open(path) as image:
                        alpha = np.asarray(image.convert("RGBA"))[..., 3]
                    uncovered = int((footprint & (alpha <= OPAQUE)).sum())
                    self.assertEqual(
                        uncovered, 0,
                        f"{path.name} leaves {uncovered} px of the baked {feature} showing",
                    )


class FaceTraitClearanceTests(unittest.TestCase):
    """A layer above the eyes must not cover them."""

    def opaque_over_eyes(self, path: Path) -> int:
        with Image.open(path) as image:
            alpha = np.asarray(image.convert("RGBA"))[..., 3]
        return sum(
            int((alpha[top:bottom + 1, left:right + 1] > OPAQUE).sum())
            for left, top, right, bottom in EYE_REGIONS
        )

    def test_mouths_and_marks_stay_clear_of_the_eyes(self) -> None:
        for category in ("mouths", "expression_marks"):
            directory = ROOT / "assets" / category
            if not directory.is_dir():
                self.skipTest(f"{category} not registered")
            for path in sorted(directory.glob("*.png")):
                with self.subTest(asset=path.name):
                    covered = self.opaque_over_eyes(path)
                    self.assertLessEqual(
                        covered, EYE_BUDGET,
                        f"{path.name} puts {covered} opaque pixels over the eyes; it renders "
                        f"above the eyes layer",
                    )

    def test_expression_marks_carry_no_skin_patch(self) -> None:
        """Marks are additive. A patch on one would erase whatever it sat over."""
        directory = ROOT / "assets" / "expression_marks"
        if not directory.is_dir():
            self.skipTest("expression_marks not registered")
        for path in sorted(directory.glob("*.png")):
            with self.subTest(asset=path.name):
                with Image.open(path) as image:
                    rgba = np.asarray(image.convert("RGBA")).astype(int)
                alpha = rgba[..., 3]
                red, green, blue = rgba[..., 0], rgba[..., 1], rgba[..., 2]
                skin = (
                    (alpha > OPAQUE) & (red > 224) & (green > 155) & (green < 240)
                    & (blue > 115) & (blue < 220) & ((red - blue) > 30) & ((red - green) > 12)
                )
                self.assertEqual(int(skin.sum()), 0,
                                 f"{path.name} paints skin; an expression mark is additive")


class EyePaletteTests(unittest.TestCase):
    def test_no_two_eye_pairs_are_visually_identical(self) -> None:
        """The backlog repeats three colour adjectives across its rows.

        Shipping two identical eye pairs under different filenames would be two
        trait values a holder cannot tell apart, so the repeats are separated by
        temperature and that separation is pinned here.
        """
        from scripts.build_face_traits import EYE_PALETTES, MIN_IRIS_DISTANCE

        colours = np.array([rgb for _name, rgb in EYE_PALETTES], float)
        self.assertEqual(len(colours), 24)
        for i in range(len(colours)):
            for j in range(i + 1, len(colours)):
                with self.subTest(pair=(EYE_PALETTES[i][0], EYE_PALETTES[j][0])):
                    self.assertGreaterEqual(
                        float(np.linalg.norm(colours[i] - colours[j])), MIN_IRIS_DISTANCE)

    def test_registered_eyes_differ_inside_the_iris(self) -> None:
        """The palette table is the intent; this measures the shipped pixels."""
        directory = ROOT / "assets" / "eyes"
        if not directory.is_dir():
            self.skipTest("eyes not registered")
        from scripts.build_face_traits import IRIS

        cx, cy, rx, ry = IRIS["eye_left"]
        rows, columns = np.mgrid[0:1254, 0:1254]
        iris = (((columns - cx) / rx) ** 2 + ((rows - cy) / ry) ** 2) <= 0.55

        means = {}
        for path in sorted(directory.glob("*.png")):
            with Image.open(path) as image:
                rgba = np.asarray(image.convert("RGBA")).astype(float)
            means[path.name] = rgba[..., :3][iris & (rgba[..., 3] > OPAQUE)].mean(axis=0)
        self.assertEqual(len(means), 24)
        names = sorted(means)
        for i, first in enumerate(names):
            for second in names[i + 1:]:
                with self.subTest(pair=(first, second)):
                    self.assertGreater(float(np.linalg.norm(means[first] - means[second])), 4.0)


class FrontAuraFlatnessTests(unittest.TestCase):
    """A front aura composites over the character, so it has to be read through.

    `aura_front_001` was deregistered on 2026-09-09 as a flat-shaded placeholder:
    126,276 opaque pixels in three colour buckets, laid over the front of every
    token it appeared on. Canvas, alpha, bounds and width-ratio checks all passed
    it. These measure the thing that actually failed.
    """

    # The accepted aura_front_002 measures 83 alpha levels, a 0.067 top-value
    # share and a 0.219 flat-neighbourhood share; the rejected placeholder
    # measures 28, 0.334 and 0.883.
    MIN_ALPHA_LEVELS = 64
    MAX_TOP_VALUE_SHARE = 0.12
    MAX_FLAT_SHARE = 0.62

    def test_no_front_aura_is_flat_shaded(self) -> None:
        from collections import Counter

        directory = ROOT / "assets" / "front_auras"
        if not directory.is_dir():
            self.skipTest("front_auras not registered")
        for path in sorted(directory.glob("*.png")):
            with self.subTest(asset=path.name):
                with Image.open(path) as image:
                    rgba = np.asarray(image.convert("RGBA")).astype(int)
                alpha = rgba[..., 3]
                read = alpha > 8
                self.assertGreater(int(read.sum()), 0, f"{path.name} is empty")
                self.assertEqual(int((alpha >= 250).sum()), 0,
                                 f"{path.name} has fully opaque pixels over the character")

                levels = len(np.unique(alpha[read]))
                counts = Counter(map(tuple, rgba[read].tolist()))
                share = counts.most_common(1)[0][1] / int(read.sum())
                gradient = np.zeros(alpha.shape, float)
                gradient[:-1] += np.abs(np.diff(alpha.astype(float), axis=0))
                gradient[:, :-1] += np.abs(np.diff(alpha.astype(float), axis=1))
                flat = float((gradient[read] < 1.0).mean())

                self.assertGreaterEqual(levels, self.MIN_ALPHA_LEVELS,
                                        f"{path.name} carries {levels} alpha levels")
                self.assertLessEqual(share, self.MAX_TOP_VALUE_SHARE,
                                     f"{path.name}: {share:.3f} of it is one value")
                self.assertLessEqual(flat, self.MAX_FLAT_SHARE,
                                     f"{path.name}: {flat:.3f} of it has no local variation")


if __name__ == "__main__":
    unittest.main()
