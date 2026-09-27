from __future__ import annotations

import unittest

import numpy as np
from PIL import Image

from scripts import fit_in_hand_render


class UncoveredCountsTests(unittest.TestCase):
    def counts(self, covered: np.ndarray, hand: np.ndarray, core: np.ndarray, radius: int) -> dict:
        found = fit_in_hand_render.uncovered_counts(covered, hand, core, radius)
        return {(dx, dy): (core_showing, showing) for core_showing, showing, dx, dy in found}

    def test_finds_the_move_that_covers_the_hand(self) -> None:
        hand = np.zeros((20, 20), bool)
        hand[5:10, 5:10] = True
        core = np.zeros_like(hand)
        core[7, 7] = True
        covered = np.zeros_like(hand)
        covered[6:11, 7:12] = True  # the layer sits 2 px right of and 1 px below the hand
        counts = self.counts(covered, hand, core, 3)
        self.assertEqual(len(counts), 7 * 7)
        self.assertEqual(counts[(0, 0)], (0, 13))
        self.assertEqual(counts[(-2, -1)], (0, 0))

    def test_a_move_off_the_canvas_uncovers_the_edge(self) -> None:
        hand = np.zeros((10, 10), bool)
        hand[0:2, 3:6] = True
        covered = np.ones_like(hand)
        counts = self.counts(covered, hand, hand.copy(), 2)
        self.assertEqual(counts[(0, 0)], (0, 0))
        # moved down 1 px, the layer no longer reaches the top row
        self.assertEqual(counts[(0, 1)], (3, 3))


class PlaceTests(unittest.TestCase):
    def test_reduces_pastes_and_makes_near_opaque_alpha_opaque(self) -> None:
        render = Image.new("RGBA", (40, 40), (200, 100, 50, 253))
        layer = fit_in_hand_render.place(render, 0.5, (30, 40))
        self.assertEqual(layer.size, fit_in_hand_render.CANVAS)
        self.assertEqual(layer.getchannel("A").getbbox(), (30, 40, 50, 60))
        alpha = np.asarray(layer)[40:60, 30:50, 3]
        self.assertTrue((alpha == 255).all())


if __name__ == "__main__":
    unittest.main()
