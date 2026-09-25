from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import generate_777


class Generate777Tests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def save_background(self, path: Path, value: int) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (16, 16), (value, value, value, 255)).save(path)

    def save_trait(self, path: Path, value: int) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        image.paste((value, 0, 0, 255), (4, 4, 12, 12))
        image.save(path)

    def build_assets(self, root: Path) -> Path:
        assets = root / "assets"
        self.save_background(assets / "backgrounds" / "background_001_one.png", 10)
        self.save_background(assets / "backgrounds" / "background_002_two.png", 20)
        self.save_trait(assets / "base_bodies" / "base_body_001_one.png", 30)
        self.save_trait(assets / "base_bodies" / "base_pose_002_two.png", 40)
        return assets

    def collection(self) -> dict[str, object]:
        return {
            "name": "Demigods",
            "description": "Test collection",
            "supply": 4,
            "canvas": {"width": 16, "height": 16},
        }

    def test_dry_run_generates_exact_unique_supply(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        output = root / "output"
        manifest = generate_777.generate_collection(
            assets_root=assets,
            output=output,
            collection=self.collection(),
            compatibility={"requires": [], "excludes": []},
            seed="fixed-seed",
            supply=4,
            max_attempts=1000,
            dry_run=True,
            overwrite=False,
        )
        self.assertEqual(manifest["supply"], 4)
        self.assertEqual(len(manifest["trait_signatures"]), 4)
        self.assertEqual(len(set(manifest["trait_signatures"])), 4)
        self.assertEqual(len(list((output / "metadata").glob("*.json"))), 4)
        self.assertEqual(len(list((output / "images").glob("*.png"))), 0)
        self.assertIsNone(manifest["image_provenance_hash"])

    def test_same_seed_is_deterministic(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        first = generate_777.generate_collection(
            assets_root=assets,
            output=root / "one",
            collection=self.collection(),
            compatibility={"requires": [], "excludes": []},
            seed="fixed-seed",
            supply=4,
            max_attempts=1000,
            dry_run=True,
            overwrite=False,
        )
        second = generate_777.generate_collection(
            assets_root=assets,
            output=root / "two",
            collection=self.collection(),
            compatibility={"requires": [], "excludes": []},
            seed="fixed-seed",
            supply=4,
            max_attempts=1000,
            dry_run=True,
            overwrite=False,
        )
        self.assertEqual(first["trait_signatures"], second["trait_signatures"])
        self.assertEqual(first["trait_provenance_hash"], second["trait_provenance_hash"])

    def test_capacity_failure_is_early_and_explicit(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        with self.assertRaisesRegex(ValueError, "theoretical combination space is only 4"):
            generate_777.generate_collection(
                assets_root=assets,
                output=root / "output",
                collection=self.collection(),
                compatibility={"requires": [], "excludes": []},
                seed="fixed-seed",
                supply=5,
                max_attempts=1000,
                dry_run=True,
                overwrite=False,
            )

    def test_rendered_run_records_image_hashes(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        output = root / "output"
        manifest = generate_777.generate_collection(
            assets_root=assets,
            output=output,
            collection=self.collection(),
            compatibility={"requires": [], "excludes": []},
            seed="fixed-seed",
            supply=4,
            max_attempts=1000,
            dry_run=False,
            overwrite=False,
        )
        self.assertEqual(len(list((output / "images").glob("*.png"))), 4)
        self.assertEqual(len(manifest["image_hashes"]), 4)
        self.assertIsNotNone(manifest["image_provenance_hash"])
        metadata = json.loads((output / "metadata" / "0001.json").read_text())
        self.assertTrue(metadata["image_sha256"])
        self.assertEqual(metadata["image"], "images/0001.png")

    def test_a_dressed_outfit_keeps_its_base_out_of_the_render(self) -> None:
        """The base stays in the metadata as the pose but is not drawn under the figure."""
        root = self.make_root()
        assets = root / "assets"
        self.save_background(assets / "backgrounds" / "background_001_one.png", 10)
        base = assets / "base_bodies" / "base_body_001_one.png"
        base.parent.mkdir(parents=True, exist_ok=True)
        wide = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        wide.paste((0, 200, 0, 255), (2, 2, 14, 14))  # a base wider than the figure
        wide.save(base)
        self.save_trait(assets / "outfits" / "outfit_001_dressed_pose_001.png", 90)
        rules = {
            "requires": [{"trait": "outfit_001_dressed_pose_001.png", "requires": "base_body_001_one.png"}],
            "excludes": [],
            "hides": [{"trait": "outfit_001_dressed_pose_001.png", "hides": "base_bodies", "reason": "r"}],
        }
        output = root / "output"
        generate_777.generate_collection(
            assets_root=assets, output=output, collection=self.collection(), compatibility=rules,
            seed="fixed-seed", supply=1, max_attempts=100, dry_run=False, overwrite=False,
        )
        with Image.open(output / "images" / "0001.png") as image:
            pixels = image.convert("RGBA")
            self.assertEqual(pixels.getpixel((2, 2)), (10, 10, 10, 255), "the hidden base was drawn")
            self.assertEqual(pixels.getpixel((8, 8)), (90, 0, 0, 255))
        metadata = json.loads((output / "metadata" / "0001.json").read_text())
        self.assertIn("base_bodies", [a["trait_type"] for a in metadata["attributes"]])

    def test_a_pose_bound_trait_does_not_skew_the_pose(self) -> None:
        """Hand objects fit one pose; that pose must not be drawn more often for it.

        Drawing every category independently and discarding broken combinations
        kept a pose-A draw whenever it had an object and a pose-B draw only when it
        had none, so pose A took about 71% of tokens and objects fell well under
        their configured rate. Drawn in layer order, the pose comes first and evenly.
        """
        assets = {
            "base_bodies": [Path("base_body_001_a.png"), Path("base_pose_002_b.png")],
            "hand_objects": [Path("hand_object_001_staff.png"), Path("hand_object_002_sword.png")],
        }
        rules = {"requires": [
            {"trait": "hand_object_001_staff.png", "requires": "base_body_001_a.png"},
            {"trait": "hand_object_002_sword.png", "requires": "base_body_001_a.png"},
        ]}
        rng = __import__("random").Random(7)
        draws = [generate_777.choose_selection(rng, assets, {"hand_objects": 0.6}, rules)
                 for _ in range(4000)]
        self.assertFalse(any(generate_777.violates_rules(s, rules) for s in draws))
        on_a = [s for s in draws if s["base_bodies"].name == "base_body_001_a.png"]
        self.assertAlmostEqual(len(on_a) / len(draws), 0.5, delta=0.04)
        with_object = sum("hand_objects" in s for s in on_a)
        self.assertAlmostEqual(with_object / len(on_a), 0.6, delta=0.04)

    def test_requirements_and_exclusions_are_met_as_they_are_drawn(self) -> None:
        assets = {
            "hair_back": [Path("hair_back_001_gold.png"), Path("hair_back_002_black.png")],
            "outfits": [Path("outfit_001_robe.png"), Path("outfit_002_coat.png")],
            "hair_front": [Path("hair_front_001_gold.png"), Path("hair_front_002_black.png")],
            "hand_objects": [Path("hand_object_001_staff.png")],
        }
        rules = {
            "requires": [
                {"trait": "hair_front_001_gold.png", "requires": "hair_back_001_gold.png"},
                {"trait": "hair_front_002_black.png", "requires": "hair_back_002_black.png"},
            ],
            "excludes": [{"trait": "outfit_002_coat.png", "excludes": ["hand_object_001_staff.png"]}],
        }
        rng = __import__("random").Random(3)
        for _ in range(500):
            selection = generate_777.choose_selection(rng, assets, {"hand_objects": 0.9}, rules)
            self.assertIsNotNone(selection)
            self.assertFalse(generate_777.violates_rules(selection, rules), selection)
            self.assertEqual(selection["hair_front"].name.split("_")[3],
                             selection["hair_back"].name.split("_")[3])

    def test_optional_category_is_sometimes_absent(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        # Add an optional third category so tokens exist both with and without it.
        self.save_trait(assets / "rear_auras" / "aura_rear_001_one.png", 50)
        self.save_trait(assets / "rear_auras" / "aura_rear_002_two.png", 60)
        collection = self.collection()
        collection["optional_categories"] = {"rear_auras": 0.5}
        collection["supply"] = 8
        manifest = generate_777.generate_collection(
            assets_root=assets,
            output=root / "output",
            collection=collection,
            compatibility={"requires": [], "excludes": []},
            seed="fixed-seed",
            supply=8,
            max_attempts=100000,
            dry_run=True,
            overwrite=False,
        )
        # 2 bg x 2 base x (2 rear auras + 1 absent branch) = 12 >= 8.
        self.assertEqual(manifest["theoretical_combination_space"], 12)
        self.assertEqual(manifest["optional_categories"], {"rear_auras": 0.5})
        raws = manifest["trait_signatures"]
        self.assertEqual(len(raws), 8)
        self.assertEqual(len(set(raws)), 8)
        records = [
            json.loads((root / "output" / "metadata" / f"{i:04d}.json").read_text())
            for i in range(1, 9)
        ]
        has_aura = [any(a["trait_type"] == "rear_auras" for a in r["attributes"]) for r in records]
        self.assertIn(True, has_aura)
        self.assertIn(False, has_aura)

    def test_required_category_cannot_be_optional(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        collection = self.collection()
        collection["optional_categories"] = {"backgrounds": 0.5}
        with self.assertRaisesRegex(ValueError, "required category cannot be optional"):
            generate_777.generate_collection(
                assets_root=assets,
                output=root / "output",
                collection=collection,
                compatibility={"requires": [], "excludes": []},
                seed="fixed-seed",
                supply=4,
                max_attempts=1000,
                dry_run=True,
                overwrite=False,
            )

    def test_nonempty_output_requires_overwrite(self) -> None:
        root = self.make_root()
        assets = self.build_assets(root)
        output = root / "output"
        output.mkdir()
        (output / "stale.txt").write_text("stale", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "output directory is not empty"):
            generate_777.generate_collection(
                assets_root=assets,
                output=output,
                collection=self.collection(),
                compatibility={"requires": [], "excludes": []},
                seed="fixed-seed",
                supply=4,
                max_attempts=1000,
                dry_run=True,
                overwrite=False,
            )


if __name__ == "__main__":
    unittest.main()
