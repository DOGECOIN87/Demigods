"""The owner's 2026-09-26 trim of the trait library stays in force and on the record.

Removed by decision, not for failing QA: every outfit that does not exist in all
five poses, and the head accessory, rear aura, front aura and hand object
categories (`docs/qa/owner_trait_removal_2026-09-26.md`). The retired files moved
to `incoming/`, which git ignores, so the manifest's withdrawal records, with
the hash of every file, are the durable record.
"""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REMOVED_CATEGORIES = ("head_accessories", "rear_auras", "front_auras", "hand_objects")
POSES = 5
REMOVED_COUNT = 34


class OwnerTraitRemovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())
        cls.registered = cls.manifest["registered_production_assets"]

    def test_every_registered_outfit_comes_in_all_five_poses(self) -> None:
        families = Counter(re.sub(r"_pose_\d{3}$", "", Path(e["path"]).stem)
                           for e in self.registered if e["category"] == "outfits")
        self.assertTrue(families, "no outfit is registered")
        for family, poses in sorted(families.items()):
            with self.subTest(outfit=family):
                self.assertEqual(
                    poses, POSES,
                    f"{family} is registered in {poses} pose(s); the owner keeps only outfits "
                    f"that exist in all {POSES}",
                )

    def test_removed_categories_stay_empty(self) -> None:
        for category in REMOVED_CATEGORIES:
            with self.subTest(category=category):
                self.assertFalse(
                    [e for e in self.registered if e["category"] == category],
                    f"{category} was removed from the collection by the owner on 2026-09-26",
                )
                directory = ROOT / "assets" / category
                self.assertFalse(directory.is_dir() and any(directory.glob("*.png")),
                                 f"assets/{category}/ holds files again")

    def test_the_removal_is_recorded(self) -> None:
        withdrawn = [b for b in self.manifest.get("blocked_assets", [])
                     if b.get("withdrawn_on") == "2026-09-26"]
        self.assertEqual(len(withdrawn), REMOVED_COUNT,
                         f"the {REMOVED_COUNT} removed assets must stay on the record with their hashes")
        for entry in withdrawn:
            with self.subTest(asset=entry["id"]):
                self.assertEqual(entry.get("status"), "withdrawn")
                self.assertTrue(entry.get("reason"), f"{entry['id']} is withdrawn with no reason")
                self.assertRegex(entry.get("sha256", ""), r"^[0-9a-f]{64}$",
                                 f"{entry['id']} is withdrawn without the hash of its bytes")
                retained = ROOT / entry["retained_at"]
                if retained.exists():
                    self.assertEqual(hashlib.sha256(retained.read_bytes()).hexdigest(), entry["sha256"])


if __name__ == "__main__":
    unittest.main()
