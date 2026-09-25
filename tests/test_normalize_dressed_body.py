"""The dressed-body normalizer: keying off black, re-levelling a matte, and the fit.

Each case is a defect found by rendering the first batch and enlarging it: a
one-pixel contour keyed out as background left pinholes through the navy boots,
and a uniform reduction of a long-legged render shrank its head until the shared
mouth sat on the chin. The synthetic figures here are built to reproduce each.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from scripts import normalize_dressed_body as normalizer

SKIN = (240, 200, 170)


def figure(*, top: int = 140, chin: int = 462, soles: int = 1144, head_width: int = 353,
           rgba: bool = False) -> np.ndarray:
    """A head, a neck and a body block on black (or transparent) 1254 canvas."""
    size = normalizer.CANVAS
    yy, xx = np.mgrid[0:size, 0:size]
    centre_y, radius_y, radius_x = (top + chin) / 2, (chin - top) / 2, head_width / 2
    head = ((xx - 627) / radius_x) ** 2 + ((yy - centre_y) / radius_y) ** 2 <= 1
    neck = (np.abs(xx - 627) <= 30) & (yy >= chin - 20) & (yy <= chin + 30)
    body = (np.abs(xx - 627) <= 150) & (yy >= chin + 25) & (yy <= soles)
    solid = head | neck | body
    image = np.zeros((size, size, 4 if rgba else 3), np.uint8)
    image[solid, :3] = SKIN
    if rgba:
        image[solid, 3] = 252  # generator mattes top out short of 255
        halo = np.zeros_like(solid)
        halo[1:, :] |= solid[:-1, :]
        halo[:-1, :] |= solid[1:, :]
        image[halo & ~solid, 3] = 12
        image[halo & ~solid, :3] = 255
    return image


def save(array: np.ndarray, root: Path) -> Path:
    path = root / "render.png"
    Image.fromarray(array, "RGBA" if array.shape[2] == 4 else "RGB").save(path)
    return path


class KeyFromBlackTests(unittest.TestCase):
    def test_contour_lines_stay_paint_and_real_gaps_open(self) -> None:
        image = np.zeros((200, 200, 3), np.uint8)
        image[40:160, 40:160] = SKIN
        image[100, 60:140] = (3, 2, 6)          # a near-black contour line, one pixel wide
        image[110:118, 70:78] = 0               # a real enclosed gap, eight pixels across
        _, alpha = normalizer.key_from_black(image)
        self.assertEqual(alpha[100, 100], 1.0, "a one-pixel contour was keyed out as a pinhole")
        self.assertEqual(alpha[113, 73], 0.0, "an enclosed gap stayed opaque")
        self.assertEqual(alpha[10, 10], 0.0)
        self.assertEqual(alpha[80, 120], 1.0)

    def test_edge_blend_takes_partial_alpha_and_the_art_colour(self) -> None:
        """A dim blend against black is part coverage; its colour is the art's, not the key's.

        Brightness at or above KEY_OPAQUE counts as paint rather than blend, so the
        renders' dark contour lines stay solid; the blend tested here is below it.
        """
        image = np.zeros((100, 100, 3), np.uint8)
        image[20:80, 20:80] = (120, 60, 30)
        image[20:80, 19] = (24, 12, 6)          # about a quarter covered against black
        colour, alpha = normalizer.key_from_black(image)
        self.assertTrue(0.2 < alpha[50, 19] < 0.4, alpha[50, 19])
        self.assertGreater(colour[50, 19, 0], 60, "the edge kept the key's black")
        self.assertEqual(alpha[50, 50], 1.0)


class RelevelTests(unittest.TestCase):
    def test_interior_becomes_opaque_and_halo_clears(self) -> None:
        rgba = np.zeros((10, 10, 4), np.uint8)
        rgba[2:8, 2:8] = (*SKIN, 252)
        rgba[1, 2:8] = (255, 255, 255, 12)
        _, alpha, ceiling = normalizer.relevel_alpha(rgba)
        self.assertEqual(ceiling, 252.0)
        self.assertEqual(alpha[5, 5], 1.0)
        self.assertEqual(alpha[1, 5], 0.0)


class FitTests(unittest.TestCase):
    def normalize(self, array: np.ndarray) -> tuple[np.ndarray, dict]:
        with tempfile.TemporaryDirectory() as temp:
            output, report = normalizer.normalize(save(array, Path(temp)))
        return np.asarray(output), report

    def test_crown_and_soles_land_on_the_rig(self) -> None:
        output, report = self.normalize(figure())
        rows = np.nonzero((output[..., 3] > 0).any(axis=1))[0]
        self.assertEqual((rows.min(), rows.max()), (141, 1139))
        self.assertLess(report["fit"]["body_scale"], 1.0)

    def test_a_long_body_does_not_shrink_the_head(self) -> None:
        """One uniform reduction to land these soles would take the head to 92%."""
        output, report = self.normalize(figure(soles=1230))
        solid = output[..., 3] >= 128
        widths = solid.sum(axis=1)
        self.assertGreater(widths[141:400].max(), 345, "the head was reduced with the legs")
        self.assertLess(report["fit"]["body_scale"], report["fit"]["head_scale"] - 0.05)
        rows = np.nonzero(solid.any(axis=1))[0]
        self.assertEqual(rows.max(), 1139)

    def test_an_rgba_matte_is_relevelled(self) -> None:
        output, report = self.normalize(figure(rgba=True))
        self.assertEqual(report["alpha_recovery"]["method"], "relevel_generator_matte")
        self.assertEqual(output[600, 627, 3], 255)

    def test_enlargement_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "enlarge"):
            self.normalize(figure(soles=1060))


if __name__ == "__main__":
    unittest.main()
