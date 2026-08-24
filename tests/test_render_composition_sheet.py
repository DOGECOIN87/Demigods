from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import render_composition_sheet as sheet

CANVAS = (64, 64)


class TraitLabelTests(unittest.TestCase):
    def test_strips_category_words_and_index(self) -> None:
        path = Path("hair_front_004_violet_parted_bangs.png")
        self.assertEqual(sheet.trait_label(path), "violet parted bangs")

    def test_keeps_stem_when_there_is_no_three_digit_index(self) -> None:
        self.assertEqual(sheet.trait_label(Path("mystery.png")), "mystery")

    def test_keeps_stem_when_nothing_follows_the_index(self) -> None:
        self.assertEqual(sheet.trait_label(Path("eyes_007.png")), "eyes_007")


class OptionalOverrideTests(unittest.TestCase):
    def test_none_when_unset(self) -> None:
        self.assertIsNone(sheet.parse_optional_overrides(None))
        self.assertIsNone(sheet.parse_optional_overrides([]))

    def test_parses_pairs(self) -> None:
        self.assertEqual(
            sheet.parse_optional_overrides(["hand_objects=0.5", "outfits=0.25"]),
            {"hand_objects": 0.5, "outfits": 0.25},
        )

    def test_rejects_missing_equals(self) -> None:
        with self.assertRaises(ValueError):
            sheet.parse_optional_overrides(["hand_objects"])

    def test_rejects_unknown_category(self) -> None:
        with self.assertRaises(ValueError):
            sheet.parse_optional_overrides(["hats=0.5"])


class SamplingTests(unittest.TestCase):
    def build_assets(self) -> dict[str, list[Path]]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        assets: dict[str, list[Path]] = {}
        for category, count in (("backgrounds", 4), ("base_bodies", 3), ("outfits", 3)):
            folder = root / category
            folder.mkdir(parents=True)
            files = []
            for index in range(1, count + 1):
                path = folder / f"{category}_{index:03d}_variant.png"
                Image.new("RGBA", CANVAS, (index * 20, 40, 60, 255)).save(path)
                files.append(path)
            assets[category] = files
        return assets

    def test_samples_are_unique_and_respect_rules(self) -> None:
        assets = self.build_assets()
        blocked = assets["outfits"][0].name
        rules = {
            "requires": [{"trait": blocked, "requires": "nothing_that_exists.png"}],
            "excludes": [],
        }
        picked = sheet.sample_compositions(
            assets=assets, rules=rules, optional={}, count=10, seed="t", max_attempts=5000
        )
        self.assertEqual(len(picked), 10)

        signatures = {sheet.raw_signature(selection) for selection in picked}
        self.assertEqual(len(signatures), 10, "compositions must be deduplicated by signature")

        chosen = {selection["outfits"].name for selection in picked}
        self.assertNotIn(blocked, chosen, "a trait whose requirement cannot be met must never appear")

    def test_same_seed_reproduces_the_same_sheet(self) -> None:
        assets = self.build_assets()
        rules = {"requires": [], "excludes": []}
        kwargs = dict(assets=assets, rules=rules, optional={}, count=6, max_attempts=5000)
        first = sheet.sample_compositions(seed="fixed", **kwargs)
        second = sheet.sample_compositions(seed="fixed", **kwargs)
        self.assertEqual(
            [sheet.raw_signature(s) for s in first],
            [sheet.raw_signature(s) for s in second],
        )

    def test_raises_when_the_library_cannot_fill_the_sheet(self) -> None:
        assets = self.build_assets()
        rules = {"requires": [], "excludes": []}
        # 4 backgrounds x 3 bodies x 3 outfits = 36 distinct compositions.
        with self.assertRaises(ValueError):
            sheet.sample_compositions(
                assets=assets, rules=rules, optional={}, count=37, seed="t", max_attempts=4000
            )


class RenderTests(unittest.TestCase):
    def build_selection(self) -> dict[str, Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        selection = {}
        for category in ("backgrounds", "outfits"):
            path = root / f"{category}_001_thing.png"
            Image.new("RGBA", CANVAS, (10, 120, 200, 255)).save(path)
            selection[category] = path
        return selection

    def test_compose_rejects_a_layer_off_the_master_canvas(self) -> None:
        selection = self.build_selection()
        wrong = Path(str(selection["outfits"]).replace(".png", "_big.png"))
        Image.new("RGBA", (128, 128), (0, 0, 0, 255)).save(wrong)
        selection["outfits"] = wrong
        with self.assertRaises(ValueError):
            sheet.compose(selection, CANVAS)

    def test_sheet_grid_fits_every_cell(self) -> None:
        selections = [self.build_selection() for _ in range(5)]
        image = sheet.render_sheet(
            selections, size=CANVAS, columns=3, thumb=40, title="test"
        )
        # 3 columns x 2 rows must be laid out, not silently clipped to one row.
        self.assertGreaterEqual(image.width, 3 * 40)
        self.assertGreaterEqual(image.height, 2 * 40)
        self.assertEqual(image.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
