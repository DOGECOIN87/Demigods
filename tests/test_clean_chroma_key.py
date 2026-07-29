from __future__ import annotations

import unittest

from PIL import Image

from scripts import clean_chroma_key as cleaner


def layer(size=(1254, 1254)) -> Image.Image:
    return Image.new("RGBA", size, (0, 0, 0, 0))


class GreenCountTests(unittest.TestCase):
    def test_counts_only_contaminated_opaque_pixels(self) -> None:
        im = layer()
        im.paste((10, 200, 10, 255), (600, 600, 610, 610))   # 100 green px
        im.paste((10, 200, 10, 0), (700, 700, 710, 710))     # transparent, ignored
        self.assertEqual(cleaner.green_pixels(im), 100)

    def test_green_at_or_below_neighbours_is_not_contamination(self) -> None:
        im = layer()
        im.paste((200, 200, 200, 255), (600, 600, 620, 620))
        self.assertEqual(cleaner.green_pixels(im), 0)


class DespillSafetyTests(unittest.TestCase):
    """The band restriction is the safety property, not a tuning knob.

    An unrestricted despill desaturated outfit_003's green potion bottles,
    shifting 173 px by more than 20 levels. Interior artwork must survive.
    """

    def test_interior_green_artwork_is_preserved(self) -> None:
        im = layer()
        # A large opaque block whose centre is deep inside the silhouette.
        im.paste((40, 60, 50, 255), (500, 500, 760, 760))
        im.paste((20, 220, 40, 255), (600, 600, 660, 660))  # green "object"
        result, _ = cleaner.clean(im, contract=1, band=3)
        px = result.load()
        self.assertEqual(px[630, 630][:3], (20, 220, 40))

    def test_edge_spill_is_removed(self) -> None:
        im = layer()
        im.paste((40, 60, 50, 255), (500, 500, 760, 760))
        # Contaminate the outer ring of the block.
        for x in range(500, 760):
            for y in (500, 501, 502, 757, 758, 759):
                im.putpixel((x, y), (30, 210, 40, 255))
        before = cleaner.green_pixels(im)
        result, report = cleaner.clean(im, contract=1, band=3)
        self.assertGreater(before, 0)
        self.assertLess(cleaner.green_pixels(result), before // 4)
        self.assertEqual(report["green_before"], before)

    def test_contract_erodes_the_alpha_edge(self) -> None:
        im = layer()
        im.paste((80, 80, 80, 255), (500, 500, 600, 600))
        result, _ = cleaner.clean(im, contract=1, band=3)
        before = im.getchannel("A").getbbox()
        after = result.getchannel("A").getbbox()
        self.assertGreater(after[0], before[0])
        self.assertLess(after[2], before[2])

    def test_report_fields_are_populated(self) -> None:
        im = layer()
        im.paste((30, 210, 40, 255), (500, 500, 560, 560))
        _, report = cleaner.clean(im)
        for key in ("green_before", "green_after", "despilled_px",
                    "artwork_shifts_over_20_levels"):
            self.assertIn(key, report)

    def test_clean_layer_is_left_alone(self) -> None:
        im = layer()
        im.paste((120, 90, 140, 255), (500, 500, 700, 700))
        result, report = cleaner.clean(im)
        self.assertEqual(report["green_before"], 0)
        self.assertEqual(report["despilled_px"], 0)


class RegisteredOutfitTests(unittest.TestCase):
    def test_registered_outfits_carry_no_meaningful_green_spill(self) -> None:
        """Regression guard for the defect this script was written to fix.

        outfit_002 is exempted: its spill runs through the collar interior rather
        than the alpha edge, and it is queued for a re-render — see
        docs/qa/outfit_chroma_key_cleanup_2026-07-29.md.
        """
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent
        for path in sorted((root / "assets" / "outfits").glob("*.png")):
            if "outfit_002" in path.name:
                continue
            with self.subTest(outfit=path.name):
                image = Image.open(path).convert("RGBA")
                self.assertLess(cleaner.green_pixels(image), 60)


if __name__ == "__main__":
    unittest.main()
