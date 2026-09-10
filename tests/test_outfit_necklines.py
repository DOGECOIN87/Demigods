"""An outfit must not show the base body's undergarment through its own opening.

The base bodies wear a neutral tank. Where an outfit is cut open at the chest it
was showing through: a flat cream panel with the tank's own neckline shading
crossing it as a hard horizontal step, framed by the coat's lapels. It looked like
cardboard, and it was on every token those outfits appeared in.

Nothing could see it. Canvas, alpha, maximum bounds, width ratio and the
exposed-leg gate are all satisfied by a coat with a hole at the collar, and the
base's own manifest note had already recorded the diagnosis and declined the fix
as "a re-render, not an edit". It is neither: the garment can be painted into the
opening, which is what `scripts/fix_outfit_necklines.py` does.

This measures what is visible through the opening, so a future outfit that leaves
the tank showing fails here rather than in review.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# A garment may legitimately close over the neck, and nothing registered does.
#
# `outfit_006` was exempted here as "a high cowl closing at the jaw is a
# garment". Rendered over the base and enlarged it was not: the cowl's opening
# was a flat near-black shape, values around (17,18,21) with no fold, seam or
# shading anywhere in it, arched up to y475 against a chin at 476.5. It covered
# the whole neck and the head read as sitting on a black dome. The cowl was
# opened on 2026-09-10 with the same cut `outfit_010`'s stand collar got, so the
# exemption is gone and every outfit is now measured.
CLOSED_BY_DESIGN: dict[str, str] = {}

# A few pixels can survive at a lapel's soft edge without reading as a panel.
# The measurement is confined to the torso's core by `exposed_tank`, because skin
# and the tank overlap in tone and a lit highlight on a bare arm passes the test.
BUDGET = 40


class OutfitNecklineTests(unittest.TestCase):
    def test_no_outfit_shows_the_undergarment_through_its_opening(self) -> None:
        from scripts.fix_outfit_necklines import outfit_base_pairs, exposed_tank

        pairs = outfit_base_pairs()
        self.assertTrue(pairs, "no outfit is bound to a base")
        for outfit_name, base_name in sorted(pairs.items()):
            with self.subTest(outfit=outfit_name):
                garment = np.asarray(Image.open(ROOT / "assets" / "outfits" / outfit_name)
                                     .convert("RGBA"))
                body = np.asarray(Image.open(ROOT / "assets" / "base_bodies" / base_name)
                                  .convert("RGBA"))
                showing = int(exposed_tank(garment, body).sum())
                self.assertLessEqual(
                    showing, BUDGET,
                    f"{outfit_name} shows {showing} px of the base's undergarment through its "
                    f"neckline; the outfit needs to carry its own inner garment",
                )

    def test_no_collar_caps_the_neck(self) -> None:
        """A stand collar has to be open at the top, or the head sits on a plug.

        `outfit_010`'s collar interior was painted as a flat slate disc. The outfit
        renders above the base, so the disc hid the neck and the collar read as an
        empty tube with a lid.
        """
        from scripts.fix_outfit_necklines import outfit_base_pairs

        # Between the chin at Y 476 and the shoulder junction at Y 496 the neck
        # should be skin, not garment, on at least this many rows.
        neck_rows = range(478, 496)
        for outfit_name, base_name in sorted(outfit_base_pairs().items()):
            if outfit_name in CLOSED_BY_DESIGN:
                continue
            with self.subTest(outfit=outfit_name):
                garment = np.asarray(Image.open(ROOT / "assets" / "outfits" / outfit_name)
                                     .convert("RGBA"))[..., 3]
                body = np.asarray(Image.open(ROOT / "assets" / "base_bodies" / base_name)
                                  .convert("RGBA"))
                skin = body[..., 3] > 128
                visible = 0
                for row in neck_rows:
                    columns = np.nonzero(skin[row] & (garment[row] <= 128))[0]
                    inner = columns[(columns > 580) & (columns < 675)]
                    if inner.size >= 8:
                        visible += 1
                self.assertGreaterEqual(
                    visible, 8,
                    f"{outfit_name} leaves the neck visible on only {visible} of "
                    f"{len(neck_rows)} rows between the chin and the shoulder",
                )


if __name__ == "__main__":
    unittest.main()
