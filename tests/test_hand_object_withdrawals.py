"""Hand objects the owner removed stay out of the collection and on the record.

`scripts/withdraw_hand_objects.py` lists them (2026-09-27: the violet blade). The
retired files moved to `incoming/`, which git ignores, so the manifest's withdrawal
records, with the hash of every file, are the durable record.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.withdraw_hand_objects import WITHDRAWN

ROOT = Path(__file__).resolve().parent.parent


class HandObjectWithdrawalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text(encoding="utf-8"))
        cls.compatibility = json.loads((ROOT / "config" / "compatibility.json").read_text(encoding="utf-8"))
        cls.records = {b["id"]: b for b in cls.manifest.get("blocked_assets", []) if b["id"] in WITHDRAWN}

    def test_withdrawn_hand_objects_stay_out(self) -> None:
        registered = {e["id"] for e in self.manifest["registered_production_assets"]}
        rules = json.dumps(self.compatibility)
        for asset_id in WITHDRAWN:
            with self.subTest(asset=asset_id):
                self.assertNotIn(asset_id, registered, f"{asset_id} was removed by the owner")
                name = Path(self.records[asset_id]["intended_path"]).name
                self.assertFalse((ROOT / "assets" / "hand_objects" / name).exists(),
                                 f"assets/hand_objects/{name} is back")
                self.assertNotIn(name, rules, f"a compatibility rule still names {name}")

    def test_the_withdrawal_is_recorded(self) -> None:
        for asset_id in WITHDRAWN:
            with self.subTest(asset=asset_id):
                record = self.records.get(asset_id)
                self.assertIsNotNone(record, f"{asset_id} has no withdrawal record")
                self.assertEqual(record.get("status"), "withdrawn")
                self.assertTrue(record.get("reason"))
                self.assertRegex(record.get("sha256", ""), r"^[0-9a-f]{64}$")
                retained = ROOT / record["retained_at"]
                if retained.exists():
                    self.assertEqual(hashlib.sha256(retained.read_bytes()).hexdigest(), record["sha256"])


if __name__ == "__main__":
    unittest.main()
