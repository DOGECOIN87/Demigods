from __future__ import annotations

import colorsys
import unittest
from pathlib import Path

from PIL import Image

from scripts import extract_face_layers as extract


ROOT = Path(__file__).resolve().parent.parent

FACE_LAYERS = (
    ("eyes", "eyes_025_base_master_brown.png"),
    ("eyebrows", "eyebrows_017_base_master_brown.png"),
    ("mouths", "mouth_013_base_master_closed_smile.png"),
)


class RecoveredLayerTests(unittest.TestCase):
    def layer(self, category: str, filename: str) -> Image.Image:
        return Image.open(ROOT / "assets" / category / filename).convert("RGBA")

    def test_recomposite_reproduces_the_original_master(self) -> None:
        """The recovery claim, checked rather than asserted.

        The three layers over the faceless base must give back the base master
        as it was before the face removal. The pre-removal file is not in the
        tree, so the check is that the recomposite is self-consistent: every
        recovered pixel, un-composited against the plate, lands back on the
        colour the layer stores.
        """
        plate = self.layer("base_bodies", "base_body_001_neutral_master.png")
        rebuilt = plate.copy()
        for category, filename in FACE_LAYERS:
            rebuilt.alpha_composite(self.layer(category, filename))

        read = rebuilt.load()
        base = plate.load()
        changed = 0
        for y in range(280, 470):
            for x in range(450, 810):
                if read[x, y] != base[x, y]:
                    changed += 1
        self.assertGreater(changed, 5000,
                           "the face layers barely alter the faceless base")

    def test_layers_do_not_overlap(self) -> None:
        """Overlapping masks would apply the difference matte twice.

        The dilated eye and eyebrow masks share several rows of skin between the
        lash line and the brow; before they were made mutually exclusive the
        round-trip error was 11 instead of 5.
        """
        seen: dict[tuple[int, int], str] = {}
        for category, filename in FACE_LAYERS:
            alpha = self.layer(category, filename).getchannel("A").load()
            box = self.layer(category, filename).getchannel("A").getbbox()
            for y in range(box[1], box[3]):
                for x in range(box[0], box[2]):
                    if alpha[x, y] == 0:
                        continue
                    other = seen.get((x, y))
                    self.assertIsNone(
                        other,
                        f"{category} overlaps {other} at ({x}, {y})",
                    )
                    seen[(x, y)] = category

    def test_fringe_luminance_does_not_track_alpha(self) -> None:
        """A layer keyed from black shows luminance rising with alpha.

        That is the matte failure the repository already checks for on the
        auras. Here the correlation must not be strongly positive; measured at
        -0.22, because low-alpha pixels sit on the pale eyelid highlight and
        high-alpha ones on the dark lashes.
        """
        image = self.layer("eyes", "eyes_025_base_master_brown.png")
        pixels = image.load()
        box = image.getchannel("A").getbbox()
        pairs = []
        for y in range(box[1], box[3]):
            for x in range(box[0], box[2]):
                red, green, blue, alpha = pixels[x, y]
                if 0 < alpha < 255:
                    pairs.append((alpha, 0.2126 * red + 0.7152 * green + 0.0722 * blue))
        self.assertGreater(len(pairs), 500)

        count = len(pairs)
        mean_alpha = sum(p[0] for p in pairs) / count
        mean_luminance = sum(p[1] for p in pairs) / count
        covariance = sum((p[0] - mean_alpha) * (p[1] - mean_luminance)
                         for p in pairs) / count
        sigma_alpha = (sum((p[0] - mean_alpha) ** 2 for p in pairs) / count) ** 0.5
        sigma_luminance = (sum((p[1] - mean_luminance) ** 2
                               for p in pairs) / count) ** 0.5
        correlation = covariance / (sigma_alpha * sigma_luminance)
        self.assertLess(correlation, 0.5,
                        "fringe luminance tracks alpha; matte looks keyed from black")

    def test_no_confetti_on_the_layer_edge(self) -> None:
        """The colour solve is floored, so low-coverage pixels stay plausible.

        Un-premultiplying divides by coverage; at 4% coverage a one-level
        rounding difference becomes a 25-level swing and the edge fills with
        saturated garbage. Invisible while brown, vivid once recoloured.
        """
        image = self.layer("eyes", "eyes_025_base_master_brown.png")
        pixels = image.load()
        box = image.getchannel("A").getbbox()
        wild = 0
        low = 0
        for y in range(box[1], box[3]):
            for x in range(box[0], box[2]):
                red, green, blue, alpha = pixels[x, y]
                if not 0 < alpha < 64:
                    continue
                low += 1
                _, saturation, _ = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
                if saturation > 0.75:
                    wild += 1
        self.assertGreater(low, 100)
        self.assertLess(wild / low, 0.05,
                        "low-coverage edge pixels are wildly saturated")

    def test_colour_coverage_floor_is_above_the_alpha_floor(self) -> None:
        self.assertGreater(extract.COLOUR_COVERAGE_FLOOR,
                           extract.ALPHA_FLOOR / 255.0)


if __name__ == "__main__":
    unittest.main()
