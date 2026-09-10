"""A fitted outfit must not leave the base body's underwear showing beside it.

The base bodies wear a cream tank and shorts so they read as dressed on their
own. Two outfits were drawn narrower than that body and showed it: a cream band
ran from the armpit to below the knee on both sides of `outfit_002`, and
`outfit_003` showed the shorts at both hips. `scripts/fit_outfit_torso.py`
warps those garments out to the body.

Only the outfits in that script's `FITTED` list are gated. The other eight were
each tried and rejected by eye: moving a garment's edge stretches the fabric
behind it, and on a coat that drags a lapel, a belt end or a trim line out with
it. Their remaining shortfall is recorded in the QA note rather than hidden
behind a budget that would pass anything.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# What easing a warp in and out of its run leaves behind at the ends.
BUDGET = 1400


class OutfitBodyFitTests(unittest.TestCase):
    def test_fitted_outfits_cover_the_base_body(self) -> None:
        from fit_outfit_torso import FITTED, exposed_body_pixels
        from widen_sleeves import outfit_base_pairs

        pairs = outfit_base_pairs()
        self.assertTrue(FITTED, "no outfit is listed as fitted")
        for name in sorted(FITTED):
            with self.subTest(outfit=name):
                self.assertIn(name, pairs, f"{name} is not bound to a base body")
                garment = Image.open(ROOT / "assets" / "outfits" / name)
                body = Image.open(ROOT / "assets" / "base_bodies" / pairs[name])
                showing = exposed_body_pixels(garment, body)
                self.assertLessEqual(
                    showing, BUDGET,
                    f"{name} leaves {showing} px of the base body showing beside it",
                )


if __name__ == "__main__":
    unittest.main()
