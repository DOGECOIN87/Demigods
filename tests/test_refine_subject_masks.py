"""Regression checks for preserving small props when masks are feathered."""
import unittest

from PIL import Image

from scripts.refine_subject_masks import add_held_effects


class ForegroundProtectionTests(unittest.TestCase):
    def test_ellipse_boundary_stays_fully_protected_with_exterior_feather(self):
        result = add_held_effects(Image.new('L', (64, 64)),
                                  [{'box': [20, 20, 40, 40], 'feather': 4}])
        self.assertEqual(result.getpixel((30, 20)), 255)
        self.assertEqual(result.getpixel((30, 30)), 255)
        self.assertGreater(result.getpixel((30, 17)), 0)
        self.assertLess(result.getpixel((30, 17)), 255)
        self.assertEqual(result.getpixel((0, 0)), 0)

    def test_thin_bow_string_polygon_is_not_weakened(self):
        result = add_held_effects(Image.new('L', (64, 64)),
                                  [{'polygon': [[20, 4], [22, 4], [42, 60], [40, 60]],
                                    'feather': 3}])
        self.assertEqual(result.getpixel((21, 4)), 255)
        self.assertEqual(result.getpixel((31, 32)), 255)


if __name__ == '__main__':
    unittest.main()
