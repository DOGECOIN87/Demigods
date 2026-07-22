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
        return value

    def inventory(self, root: Path, entries: list[tuple[str, str]]) -> dict[str, str]:
        assets = root / "assets"
        for category, filename in entries:
            path = assets / category / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"placeholder")
        return validate_config.discover_trait_inventory(assets)

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
