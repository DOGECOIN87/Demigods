"""A sleeve must not leave a strip of bare arm along its own outer edge.

Two of the coats were drawn narrower than the arm they cover. A seam of bare
skin ran from the shoulder to the cuff down both sleeves - about 13 px on
`outfit_010` and 14 px on `outfit_009`, five thousand pixels each - and it was
on every token those outfits appeared in.

Nothing could see it. Canvas, alpha, maximum bounds and the width ratio are all
satisfied by a coat whose sleeves are too narrow, and the exposed-leg gate stops
at the knee. `scripts/widen_sleeves.py` warps the sleeve edge out to the
silhouette; this measures what is left, so a future outfit that arrives narrow
fails here rather than in review.

The measurement stops one pixel short of the silhouette on purpose. The art
draws the body's outline outside every garment, so the last bare column at the
edge is that outline and not a seam - which is why `MIN_GAP` is 2 and why the
repair stops just inside it.
"""
from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# A few rows can survive where a sleeve meets a cuff without reading as a seam:
# the cuff is already the width of the wrist and does not move, so the fabric
# above it eases back in to meet it.
BUDGET = 60


class OutfitSleeveTests(unittest.TestCase):
    def test_no_sleeve_leaves_bare_arm_along_its_edge(self) -> None:
        from scripts.widen_sleeves import outfit_base_pairs, exposed_strip_pixels

        pairs = outfit_base_pairs()
        self.assertTrue(pairs, "no outfit is bound to a base")
        for outfit_name, base_name in sorted(pairs.items()):
            with self.subTest(outfit=outfit_name):
                garment = Image.open(ROOT / "assets" / "outfits" / outfit_name)
                body = Image.open(ROOT / "assets" / "base_bodies" / base_name)
                bare = exposed_strip_pixels(garment, body)
                self.assertLessEqual(
                    bare, BUDGET,
                    f"{outfit_name} leaves {bare} px of bare arm along its sleeve edge; the "
                    f"sleeve is narrower than the arm it is drawn over",
                )


if __name__ == "__main__":
    unittest.main()
