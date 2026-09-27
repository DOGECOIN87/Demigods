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

    def in_hand_render(self, in_hand: list) -> tuple[int, int, int, int]:
        """Render one token of a base and a hand object that overlap at (8, 8)."""
        root = self.make_root()
        assets = root / "assets"
        self.save_background(assets / "backgrounds" / "background_001_one.png", 10)
        self.save_trait(assets / "base_bodies" / "base_body_001_one.png", 30)
        self.save_trait(assets / "hand_objects" / "hand_object_001_staff.png", 70)
        rules = {"requires": [], "excludes": [], "in_hand": in_hand}
        output = root / "output"
        generate_777.generate_collection(
            assets_root=assets, output=output, collection=self.collection(), compatibility=rules,
            seed="fixed-seed", supply=1, max_attempts=100, dry_run=False, overwrite=False,
        )
        with Image.open(output / "images" / "0001.png") as image:
            return image.convert("RGBA").getpixel((8, 8))

    def test_a_hand_object_is_drawn_behind_the_body_by_default(self) -> None:
        """The base's own fist covers the object's grip."""
        self.assertEqual(self.in_hand_render([]), (30, 0, 0, 255))

    def test_an_in_hand_object_is_drawn_over_the_body(self) -> None:
        """An object painted with its gripping hand shows that hand over the base's."""
        rule = {"trait": "hand_object_001_staff.png", "reason": "painted in hand"}
        self.assertEqual(self.in_hand_render([rule]), (70, 0, 0, 255))

    def test_in_hand_order_puts_the_object_before_the_front_aura(self) -> None:
        order = generate_777.render_order(in_hand=True)
        self.assertLess(order.index("head_accessories"), order.index("hand_objects"))
        self.assertEqual(order.index("hand_objects") + 1, order.index("front_auras"))
        self.assertEqual(sorted(order), sorted(generate_777.RENDER_LAYER_ORDER))

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
