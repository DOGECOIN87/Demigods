from __future__ import annotations

import unittest

import numpy as np

from scripts import compose_final_one_of_ones as compose

PARAMS = {"blur_radius": 9.0, "subject_margin": 3.0, "vignette_strength": 0.42,
          "vignette_inner": 0.38, "vignette_power": 1.3}


def checkerboard(size: int = 256, cell: int = 8) -> np.ndarray:
    """Detailed background: a flat colour would hide the blur."""
    yy, xx = np.mgrid[:size, :size]
    board = ((xx // cell + yy // cell) % 2).astype(np.uint8)
    rgb = np.where(board[..., None] == 1, np.array([230, 220, 180], np.uint8), np.array([40, 60, 140], np.uint8))
    return rgb.astype(np.uint8)


def cutout_of(source: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    alpha = np.zeros(source.shape[:2], np.uint8)
    x0, y0, x1, y1 = box
    alpha[y0:y1, x0:x1] = 255
    return np.dstack([source, alpha])


class ComposeFinalTests(unittest.TestCase):
    def test_opaque_subject_pixels_are_untouched(self):
        source = checkerboard()
        source[100:160, 100:160] = (250, 10, 10)
        result = compose.compose(source, cutout_of(source, (100, 100, 160, 160)), PARAMS)
        self.assertEqual(result.shape, source.shape)
        np.testing.assert_array_equal(result[100:160, 100:160], source[100:160, 100:160])

    def test_background_is_blurred(self):
        source = checkerboard(cell=2)  # finer than the lens radius, which scales to ~1.8 px at 256 px
        result = compose.compose(source, cutout_of(source, (0, 0, 0, 0)), PARAMS)
        centre = (slice(96, 160), slice(96, 160))  # inside the vignette's untouched centre
        self.assertLess(result[centre].astype(float).std(), source[centre].astype(float).std() * 0.5)

    def test_subject_colour_does_not_halo_into_background(self):
        source = np.full((256, 256, 3), 40, np.uint8)
        source[96:160, 96:160] = (255, 0, 0)
        result = compose.compose(source, cutout_of(source, (96, 96, 160, 160)), PARAMS)
        ring = result[90:94, 100:156].astype(int)  # just outside the subject
        self.assertLess(int(ring[..., 0].max()) - 40, 6)

    def test_vignette_darkens_corners_not_centre(self):
        source = np.full((256, 256, 3), 200, np.uint8)
        result = compose.compose(source, cutout_of(source, (0, 0, 0, 0)), PARAMS)
        self.assertEqual(int(result[128, 128, 0]), 200)
        self.assertLess(int(result[0, 0, 0]), 200 * 0.65)
        self.assertGreater(int(result[0, 128, 0]), int(result[0, 0, 0]))

    def test_parameters_scale_with_image_width(self):
        for size in (128, 256):
            source = checkerboard(size)
            result = compose.compose(source, cutout_of(source, (0, 0, 0, 0)), PARAMS)
            self.assertEqual(result.shape, (size, size, 3))


if __name__ == "__main__":
    unittest.main()
