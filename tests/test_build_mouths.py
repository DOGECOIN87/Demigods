from __future__ import annotations

import hashlib
import itertools
import unittest
from pathlib import Path

from PIL import Image

from scripts import build_mouths


ROOT = Path(__file__).resolve().parent.parent
MOUTH_DIR = ROOT / "assets" / "mouths"

# Band the mouth anchor lives in; everything registered draws inside it.
WINDOW = (560, 400, 700, 480)
SKIN = (253, 199, 163)

# Floors taken from the measured set, with margin. The first version of this
# category failed both: five closed mouths varied only in length, and every open
# mouth was an ellipse at the same anchor.
MAX_SHAPE_OVERLAP = 0.75
MIN_COLOUR_DISTANCE = 60.0


def registered() -> list[Path]:
    return sorted(MOUTH_DIR.glob("*.png"))


class MouthDiversityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.paths = registered()
        self.assertGreaterEqual(len(self.paths), 13, "mouth category has shrunk")
        self.masks: list[set[tuple[int, int]]] = []
        self.flats = []
        for path in self.paths:
            with Image.open(path) as handle:
                image = handle.convert("RGBA")
            alpha = image.getchannel("A").load()
            self.masks.append({
                (x, y)
                for y in range(WINDOW[1], WINDOW[3])
                for x in range(WINDOW[0], WINDOW[2])
                if alpha[x, y] > 128
            })
            over_skin = Image.new("RGB", image.size, SKIN)
            over_skin.paste(image.convert("RGB"), mask=image.getchannel("A"))
            self.flats.append((image.getchannel("A").load(), over_skin.load()))

    def test_no_two_mouths_are_pixel_identical(self) -> None:
        digests = {}
        for path in self.paths:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertNotIn(digest, digests,
                             f"{path.name} is byte-identical to {digests.get(digest)}")
            digests[digest] = path.name

    def test_no_pair_shares_too_much_of_its_shape(self) -> None:
        for i, j in itertools.combinations(range(len(self.paths)), 2):
            union = len(self.masks[i] | self.masks[j])
            if union == 0:
                continue
            overlap = len(self.masks[i] & self.masks[j]) / union
            self.assertLess(
                overlap, MAX_SHAPE_OVERLAP,
                f"{self.paths[i].name} and {self.paths[j].name} share "
                f"{overlap:.2f} of their shape",
            )

    def test_every_pair_is_visibly_different_over_the_ink(self) -> None:
        """Shape overlap alone would pass two mouths that differ only in colour.

        Measured over the union of the two mouths' ink rather than the whole
        band, because averaging across mostly-empty skin drags every pair toward
        zero and hides real similarity.
        """
        for i, j in itertools.combinations(range(len(self.paths)), 2):
            alpha_i, colour_i = self.flats[i]
            alpha_j, colour_j = self.flats[j]
            union = [
                (x, y)
                for y in range(WINDOW[1], WINDOW[3])
                for x in range(WINDOW[0], WINDOW[2])
                if alpha_i[x, y] > 40 or alpha_j[x, y] > 40
            ]
            self.assertTrue(union)
            distance = sum(
                max(abs(colour_i[x, y][k] - colour_j[x, y][k]) for k in range(3))
                for x, y in union
            ) / len(union)
            self.assertGreater(
                distance, MIN_COLOUR_DISTANCE,
                f"{self.paths[i].name} and {self.paths[j].name} differ by only "
                f"{distance:.1f} over their ink",
            )

    def test_every_mouth_sits_on_the_locked_axis(self) -> None:
        for path in self.paths:
            with Image.open(path) as handle:
                box = handle.convert("RGBA").getchannel("A").getbbox()
            centre = (box[0] + box[2] - 1) / 2
            self.assertAlmostEqual(centre, build_mouths.ANCHOR[0], delta=2.5,
                                   msg=f"{path.name} is off the centre axis")

    def test_the_builder_still_offers_both_kinds(self) -> None:
        kinds = {design["kind"] for _, design in build_mouths.MOUTHS}
        self.assertEqual(kinds, {"stroke", "fill"},
                         "the set must keep both closed and open mouths")


if __name__ == "__main__":
    unittest.main()
