"""No registered asset may carry the chroma key it was cut out of.

Several traits were produced by keying a green backdrop out of a render, and the
key was not complete. Saturated key-green survived *inside* the art: two dots in
violet bangs, a scatter through pink hair, specks on the base bodies' skin, and -
worst - a lime rim around every tongue of `aura_rear_005_lavender_lightning`,
20.5 % of that asset. Each one appeared on every token its trait landed on.

Nothing could see it. Canvas, alpha behaviour, maximum bounds and width ratio are
all satisfied by a layer with green confetti in it, and the earlier chroma work
measured the silhouette's outer fringe rather than the interior.

The collection does contain green art, so the exemptions are named rather than
inferred: no measurement separated the two cases, and the reasoning is recorded
in `scripts/despeckle_chroma_residue.py`.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# A handful of pixels can survive a repair at a soft edge without being visible.
BUDGET = 8


class ChromaResidueTests(unittest.TestCase):
    def test_no_registered_asset_carries_key_green(self) -> None:
        from scripts.despeckle_chroma_residue import GREEN_BY_DESIGN, key_green

        manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())
        checked = 0
        for entry in manifest["registered_production_assets"]:
            relative = entry["path"]
            if relative in GREEN_BY_DESIGN:
                continue
            path = ROOT / relative
            if not path.exists():
                continue
            with self.subTest(asset=relative):
                with Image.open(path) as image:
                    rgba = np.asarray(image.convert("RGBA")).astype(int)
                flagged = int(key_green(rgba).sum())
                self.assertLessEqual(
                    flagged, BUDGET,
                    f"{relative} carries {flagged} saturated key-green pixels. If it is a new "
                    f"green trait, list it in GREEN_BY_DESIGN with what you saw; otherwise run "
                    f"scripts/despeckle_chroma_residue.py --in-place",
                )
            checked += 1
        self.assertGreater(checked, 100, "the manifest should hold the whole collection")

    def test_the_green_exemptions_are_still_registered_and_still_green(self) -> None:
        """An exemption that no longer names a real green asset is a hole in the gate."""
        from scripts.despeckle_chroma_residue import GREEN_BY_DESIGN, green_share

        for relative, reason in GREEN_BY_DESIGN.items():
            with self.subTest(asset=relative):
                path = ROOT / relative
                self.assertTrue(path.exists(), f"{relative} is exempt but not present")
                self.assertTrue(reason.strip(), f"{relative} is exempt with no reason recorded")
                with Image.open(path) as image:
                    rgba = np.asarray(image.convert("RGBA")).astype(int)
                self.assertGreater(
                    green_share(rgba), 0.01,
                    f"{relative} is exempt from the chroma gate but is barely green; the "
                    f"exemption should be removed",
                )


if __name__ == "__main__":
    unittest.main()
