"""An outfit must not leave the base body's underwear showing beside it.

The base bodies wear a cream tank and shorts so they read as dressed on their
own. Outfits drawn narrower than that body show it: a cream band down the flank
between a coat's body and its own sleeve, or the shorts at the hip.

`outfit_005`, `outfit_009` and `outfit_010` were withdrawn on 2026-09-10 rather
than repaired, because closing their bands needed the garment redrawn at the
body's width and every mechanical repair moved something that was drawn.
`docs/qa/outfit_refit_2026-09-10.md` records the four that were tried.

## What the number below is, and is not

`BUDGET` describes the art that is registered today. It is not a target, and
passing it is not a statement that an outfit is well fitted: `outfit_007` sits
at 2567 px and still shows a band down its viewer-left flank, which is written
down in the QA note rather than hidden. The gate exists so that a later change
cannot make any outfit *worse* without a test going red, and so that a garment
of this kind cannot be registered without someone looking at it first.

Set it from what the accepted art measures, plus a small margin. Do not raise it
to make a new asset pass.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# The worst registered outfit measures 2567 px (outfit_007), and the rest sit
# between 40 and 2205. This is that worst case with room for antialiasing drift,
# not a budget anything was optimised down to.
BUDGET = 2700

# Withdrawn on 2026-09-10 for being drawn inside the body. A replacement has to
# be drawn to the body's width, so re-registering the same art would put the
# defect straight back.
WITHDRAWN = {
    "outfit_005_sun_temple_pose_005.png",
    "outfit_009_navy_high_collar_coat.png",
    "outfit_010_celestial_robe_white_gold.png",
}


class OutfitBodyFitTests(unittest.TestCase):
    def test_every_outfit_covers_the_base_body(self) -> None:
        from fit_outfit_torso import exposed_body_pixels
        from widen_sleeves import outfit_base_pairs

        pairs = outfit_base_pairs()
        self.assertTrue(pairs, "no outfit is bound to a base body")
        for name in sorted(pairs):
            with self.subTest(outfit=name):
                garment = Image.open(ROOT / "assets" / "outfits" / name)
                body = Image.open(ROOT / "assets" / "base_bodies" / pairs[name])
                showing = exposed_body_pixels(garment, body)
                self.assertLessEqual(
                    showing, BUDGET,
                    f"{name} leaves {showing} px of the base body showing beside it, "
                    f"against {BUDGET} for the art this gate was set from",
                )

    def test_the_narrow_outfits_stay_withdrawn(self) -> None:
        """The three withdrawn outfits must not come back as the same bytes.

        They are not bad art. They are drawn inside the body they are worn over,
        and nothing short of redrawing them at the body's width fixes that, so
        re-registering the retired file would restore the defect silently.
        """
        manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())
        registered = {Path(e["path"]).name
                      for e in manifest["registered_production_assets"]}
        # Matched by asset path, not by `DG-` id: two of the four assets retired
        # in this pass carry no `backlog_id`, and an id-based lookup skips them.
        blocked = {Path(b.get("intended_path", "")).name: b
                   for b in manifest.get("blocked_assets", [])}
        for name in sorted(WITHDRAWN):
            with self.subTest(outfit=name):
                self.assertNotIn(name, registered,
                                 f"{name} is registered again; it has to be redrawn to the "
                                 f"body's width first, not re-registered as it was")
                self.assertFalse((ROOT / "assets" / "outfits" / name).exists(),
                                 f"{name} is back in assets/outfits without being registered")
                entry = blocked.get(name)
                self.assertIsNotNone(entry, f"{name} is gone with no record of why")
                self.assertTrue(entry.get("reason"), f"{name} is withdrawn with no reason")
                self.assertTrue(entry.get("requirement"),
                                f"{name} is withdrawn with no requirement for its replacement")
                self.assertRegex(str(entry.get("sha256", "")), r"^[0-9a-f]{64}$",
                                 f"{name} is withdrawn without the SHA-256 it was retired at")

    def test_no_base_pose_is_left_without_an_outfit(self) -> None:
        """Every registered base has at least one outfit that can be worn on it.

        Outfits are not an optional category, so a base with no compatible outfit
        produces no valid token at all: the generator would simply stop drawing
        that pose. `base_pose_005` was withdrawn alongside `outfit_005` for
        exactly this reason, and the check is here so the next withdrawal cannot
        strand a pose quietly.
        """
        from widen_sleeves import outfit_base_pairs

        manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())
        bases = {Path(e["path"]).name for e in manifest["registered_production_assets"]
                 if e["category"] == "base_bodies"}
        worn = set(outfit_base_pairs().values())
        stranded = sorted(bases - worn)
        self.assertEqual(
            stranded, [],
            f"{stranded} have no outfit bound to them, so no token can be built on them",
        )


if __name__ == "__main__":
    unittest.main()
