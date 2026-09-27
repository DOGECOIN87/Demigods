"""The owner's 2026-09-27 removal of headwear and auras stays in force and on the record.

Removed by decision, not for failing QA: the head accessory, rear aura and front aura
categories (`docs/qa/headwear_aura_removal_2026-09-27.md`). The retired files moved
to `incoming/`, which git ignores, so the manifest's withdrawal records, with the
hash of every file, are the durable record.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REMOVED_CATEGORIES = ("head_accessories", "rear_auras", "front_auras")
REMOVED_COUNT = 16


class HeadwearAuraRemovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text(encoding="utf-8"))
        cls.registered = cls.manifest["registered_production_assets"]
        cls.collection = json.loads((ROOT / "config" / "collection.json").read_text(encoding="utf-8"))

    def test_removed_categories_stay_empty(self) -> None:
        for category in REMOVED_CATEGORIES:
            with self.subTest(category=category):
                self.assertFalse(
                    [e for e in self.registered if e["category"] == category],
                    f"{category} was removed from the collection by the owner on 2026-09-27",
                )
                directory = ROOT / "assets" / category
                self.assertFalse(directory.is_dir() and any(directory.glob("*.png")),
                                 f"assets/{category}/ holds files again")
                self.assertNotIn(category, self.collection.get("optional_categories") or {})

    def test_the_removal_is_recorded(self) -> None:
        withdrawn = [b for b in self.manifest.get("blocked_assets", [])
                     if b.get("withdrawn_on") == "2026-09-27"]
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
