from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

from scripts import intake_painted_outfit as intake


ROOT = Path(__file__).resolve().parent.parent
OUTFIT_DIR = ROOT / "assets" / "outfits"
BASE = ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png"

# The painted jaw line on the base master, found by scanning the centre column:
# luminance drops to 94 at Y 478 and the neck begins below it.
JAW_Y = 478


class OutfitFaceClearanceTests(unittest.TestCase):
    """No garment may cover the chin.

    Seating the collar purely for shoulder coverage drove it to Y 442, one pixel
    above the mouth anchor. The standing collars then swallowed the chin and jaw,
    and because `mouths` composites after `outfits`, an open mouth was drawn half
    on skin and half on the collar's dark opening. It shipped that way through a
    full registration and two QA sheets before anyone looked at a face closely.
    """

    def test_no_outfit_draws_above_the_jaw(self) -> None:
        outfits = sorted(OUTFIT_DIR.glob("*.png"))
        self.assertTrue(outfits, "no outfits registered")
        for path in outfits:
            with Image.open(path) as handle:
                layer = handle.convert("RGBA")
            intrusion = intake.chin_intrusion(layer)
            self.assertEqual(
                intrusion, 0,
                f"{path.name} covers {intrusion} px of the face above Y "
                f"{intake.CHIN_CLEAR_Y}; the chin will be missing",
            )

    def test_the_clearance_line_sits_below_the_painted_jaw(self) -> None:
        self.assertGreater(intake.CHIN_CLEAR_Y, JAW_Y)

    def test_every_outfit_starts_at_the_declared_collar_seat(self) -> None:
        for path in sorted(OUTFIT_DIR.glob("*.png")):
            with Image.open(path) as handle:
                box = handle.convert("RGBA").getchannel("A").getbbox()
            self.assertEqual(box[1], intake.COLLAR_TOP_Y,
                             f"{path.name} does not start at the collar seat")

    def test_mouths_never_overlap_a_registered_outfit(self) -> None:
        """A mouth drawn partly over the collar reads as a hole, not a mouth."""
        outfit_masks = []
        for path in sorted(OUTFIT_DIR.glob("*.png")):
            with Image.open(path) as handle:
                outfit_masks.append((path.name, handle.convert("RGBA").getchannel("A").load()))

        for mouth_path in sorted((ROOT / "assets" / "mouths").glob("*.png")):
            with Image.open(mouth_path) as handle:
                mouth = handle.convert("RGBA")
            alpha = mouth.getchannel("A").load()
            box = mouth.getchannel("A").getbbox()
            for name, outfit in outfit_masks:
                clash = sum(
                    1
                    for y in range(box[1], box[3])
                    for x in range(box[0], box[2])
                    if alpha[x, y] > 128 and outfit[x, y] > 128
                )
                self.assertEqual(
                    clash, 0,
                    f"{mouth_path.name} overlaps {name} by {clash} px",
                )


if __name__ == "__main__":
    unittest.main()
