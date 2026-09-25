from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from scripts import validate_config


class ValidateConfigTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def collection(self) -> dict[str, object]:
        value = copy.deepcopy(validate_config.LOCKED_COLLECTION)
        value["description"] = "A 777-piece modular chibi-fantasy generative collection."
        # `supply` is only the generative half; the reserved legendary IDs make up
        # the rest, and the validator checks the sum rather than either alone.
        value["legendary_token_ids"] = [111, 222, 333, 444, 555, 666, 777]
        return value

    def inventory(self, root: Path, entries: list[tuple[str, str]]) -> dict[str, str]:
        assets = root / "assets"
        for category, filename in entries:
            path = assets / category / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"placeholder")
        return validate_config.discover_trait_inventory(assets)

    def test_supply_and_reserved_ids_must_total_the_collection(self) -> None:
        value = self.collection()
        value["legendary_token_ids"] = [111, 222]
        errors, _ = validate_config.validate_collection(value)
        self.assertTrue(any("totals" in e for e in errors), errors)

    def test_reserved_ids_outside_the_collection_are_rejected(self) -> None:
        value = self.collection()
        value["legendary_token_ids"] = [111, 222, 333, 444, 555, 666, 900]
        errors, _ = validate_config.validate_collection(value)
        self.assertTrue(any("outside the collection" in e for e in errors), errors)

    def test_locked_collection_and_empty_rules_pass(self) -> None:
        errors, warnings = validate_config.validate_collection(self.collection())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

        compatibility_errors, _, requires_count, excludes_count = (
            validate_config.validate_compatibility(
                {"version": 1, "requires": [], "excludes": [], "notes": []},
                {},
            )
        )
        self.assertEqual(compatibility_errors, [])
        self.assertEqual(requires_count, 0)
        self.assertEqual(excludes_count, 0)

    def test_changed_locked_anchor_fails(self) -> None:
        collection = self.collection()
        collection["master_rig"]["eye_line_y"] = 368  # type: ignore[index]
        errors, _ = validate_config.validate_collection(collection)
        self.assertTrue(any("master_rig.eye_line_y" in error for error in errors))

    def test_missing_trait_reference_fails(self) -> None:
        errors, _, _, _ = validate_config.validate_compatibility(
            {
                "version": 1,
                "requires": [
                    {
                        "trait": "hand_object_001_staff.png",
                        "requires": "base_pose_002_vertical_grip.png",
                    }
                ],
                "excludes": [],
                "notes": [],
            },
            {},
        )
        self.assertTrue(any("missing production trait" in error for error in errors))

    def test_same_category_requirement_is_impossible(self) -> None:
        root = self.make_root()
        inventory = self.inventory(
            root,
            [
                ("eyes", "eyes_001_brown.png"),
                ("eyes", "eyes_002_blue.png"),
            ],
        )
        errors, _, _, _ = validate_config.validate_compatibility(
            {
                "version": 1,
                "requires": [
                    {
                        "trait": "eyes_001_brown.png",
                        "requires": "eyes_002_blue.png",
                    }
                ],
                "excludes": [],
                "notes": [],
            },
            inventory,
        )
        self.assertTrue(any("same-category requirement" in error for error in errors))

    def test_requires_and_excludes_contradiction_fails(self) -> None:
        root = self.make_root()
        inventory = self.inventory(
            root,
            [
                ("hand_objects", "hand_object_001_staff.png"),
                ("base_bodies", "base_pose_002_vertical_grip.png"),
            ],
        )
        errors, _, _, _ = validate_config.validate_compatibility(
            {
                "version": 1,
                "requires": [
                    {
                        "trait": "hand_object_001_staff.png",
                        "requires": "base_pose_002_vertical_grip.png",
                    }
                ],
                "excludes": [
                    {
                        "trait": "hand_object_001_staff.png",
                        "excludes": ["base_pose_002_vertical_grip.png"],
                    }
                ],
                "notes": [],
            },
            inventory,
        )
        self.assertTrue(any("requires and excludes" in error for error in errors))

    def hides_case(self, hides: list, requires: list | None = None) -> list[str]:
        root = self.make_root()
        inventory = self.inventory(
            root,
            [
                ("outfits", "outfit_007_coat_pose_002.png"),
                ("base_bodies", "base_pose_002_vertical_grip.png"),
            ],
        )
        compatibility = {
            "version": 1,
            "requires": requires if requires is not None else [
                {"trait": "outfit_007_coat_pose_002.png", "requires": "base_pose_002_vertical_grip.png"}
            ],
            "excludes": [],
            "hides": hides,
            "notes": [],
        }
        errors, warnings, _, _ = validate_config.validate_compatibility(compatibility, inventory)
        self.assertFalse(any("unrecognized compatibility keys" in w for w in warnings), warnings)
        hide_errors, _, _ = validate_config.validate_hides(compatibility, inventory)
        return errors + hide_errors

    def test_dressed_outfit_bound_to_its_base_may_hide_it(self) -> None:
        errors = self.hides_case([{"trait": "outfit_007_coat_pose_002.png", "hides": "base_bodies",
                                   "reason": "painted with the body intact"}])
        self.assertEqual(errors, [])

    def test_hiding_the_base_needs_a_pose_binding(self) -> None:
        """Without one, a dressed figure would be drawn over whichever pose was drawn."""
        errors = self.hides_case(
            [{"trait": "outfit_007_coat_pose_002.png", "hides": "base_bodies", "reason": "r"}],
            requires=[],
        )
        self.assertTrue(any("no requires rule binds it" in e for e in errors), errors)

    def test_hides_rejects_unknown_own_and_background_layers(self) -> None:
        errors = self.hides_case([
            {"trait": "outfit_007_coat_pose_002.png", "hides": ["capes"], "reason": "r"},
            {"trait": "outfit_007_coat_pose_002.png", "hides": "outfits", "reason": "r"},
            {"trait": "outfit_007_coat_pose_002.png", "hides": "backgrounds", "reason": "r"},
        ])
        self.assertTrue(any("unknown layer" in e for e in errors), errors)
        self.assertTrue(any("its own layer" in e for e in errors), errors)
        self.assertTrue(any("cannot hide the background" in e for e in errors), errors)

    def test_hides_needs_a_reason(self) -> None:
        errors = self.hides_case([{"trait": "outfit_007_coat_pose_002.png", "hides": "base_bodies"}])
        self.assertTrue(any("must give a reason" in e for e in errors), errors)

    def test_mutual_requirement_warns_but_passes(self) -> None:
        root = self.make_root()
        inventory = self.inventory(
            root,
            [
                ("hand_objects", "hand_object_001_staff.png"),
                ("base_bodies", "base_pose_002_vertical_grip.png"),
            ],
        )
        errors, warnings, _, _ = validate_config.validate_compatibility(
            {
                "version": 1,
                "requires": [
                    {
                        "trait": "hand_object_001_staff.png",
                        "requires": "base_pose_002_vertical_grip.png",
                    },
                    {
                        "trait": "base_pose_002_vertical_grip.png",
                        "requires": "hand_object_001_staff.png",
                    },
                ],
                "excludes": [],
                "notes": [],
            },
            inventory,
        )
        self.assertEqual(errors, [])
        self.assertTrue(any("mutual requirement" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
