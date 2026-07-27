from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import report_production_status


BACKLOG_HEADER = (
    "| ID | Category | Visual description | Source reference | Dependency "
    "| Intended production path | Prompt | Status |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


class ProductionStatusTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def backlog_row(self, entry_id: str, path: str, status: str) -> str:
        return f"| {entry_id} | base body | desc | REF | none | `{path}` | `prompts/01.md` | {status} |\n"

    def write_backlog(self, root: Path, rows: str) -> Path:
        path = root / "backlog.md"
        path.write_text(BACKLOG_HEADER + rows, encoding="utf-8")
        return path

    def manifest(
        self,
        *,
        registered: list[tuple[str, str]],
        pending: list[str],
        directories: list[str] | None = None,
    ) -> dict[str, object]:
        return {
            "production_directories": {
                name: f"assets/{name}" for name in (directories or ["base_bodies", "hair_back"])
            },
            "registered_production_assets": [
                {
                    "id": path.rsplit("/", 1)[-1],
                    "category": category,
                    "path": path,
                    "status": "production_ready",
                }
                for category, path in registered
            ],
            "pending_categories": pending,
        }

    def build(
        self,
        manifest: dict[str, object],
        rows: str,
    ) -> report_production_status.ProductionStatus:
        root = self.make_root()
        entries, errors = report_production_status.parse_backlog(self.write_backlog(root, rows))
        return report_production_status.build_status(manifest, entries, errors)

    def test_registered_and_pending_counts_are_derived_from_manifest(self) -> None:
        rows = (
            self.backlog_row("DG-001", "assets/base_bodies/base_body_001_neutral.png", "registered")
            + self.backlog_row("DG-002", "assets/hair_back/hair_back_001_gold.png", "pending")
        )
        manifest = self.manifest(
            registered=[("base_bodies", "assets/base_bodies/base_body_001_neutral.png")],
            pending=["hair_back"],
        )
        status = self.build(manifest, rows)
        self.assertTrue(status.passed, status.errors)
        self.assertEqual(status.total_registered, 1)
        self.assertEqual(status.backlog_total, 2)
        by_category = {item.category: item for item in status.categories}
        self.assertEqual(by_category["base_bodies"].state, "complete")
        self.assertEqual(by_category["hair_back"].remaining, 1)
        self.assertEqual(by_category["hair_back"].state, "not started")

    def test_shared_production_path_counts_once(self) -> None:
        """DG-001 and DG-002 both resolve to the neutral master in the real backlog."""
        shared = "assets/base_bodies/base_body_001_neutral.png"
        rows = self.backlog_row("DG-001", shared, "registered") + self.backlog_row(
            "DG-002", shared, "registered"
        )
        manifest = self.manifest(registered=[("base_bodies", shared)], pending=["hair_back"])
        status = self.build(manifest, rows)
        self.assertTrue(status.passed, status.errors)
        self.assertEqual(status.backlog_total, 1)
        self.assertEqual(status.status_counts["registered"], 2)

    def test_backlog_registered_without_manifest_entry_fails(self) -> None:
        rows = self.backlog_row(
            "DG-001", "assets/base_bodies/base_body_001_neutral.png", "registered"
        )
        manifest = self.manifest(registered=[], pending=["base_bodies", "hair_back"])
        status = self.build(manifest, rows)
        self.assertFalse(status.passed)
        self.assertTrue(
            any("does not register it" in error for error in status.errors), status.errors
        )

    def test_manifest_entry_without_backlog_row_fails(self) -> None:
        rows = self.backlog_row("DG-001", "assets/base_bodies/base_body_001_neutral.png", "pending")
        manifest = self.manifest(
            registered=[("hair_back", "assets/hair_back/hair_back_009_unlisted.png")],
            pending=["base_bodies", "hair_back"],
        )
        status = self.build(manifest, rows)
        self.assertFalse(status.passed)
        self.assertTrue(
            any("no backlog row claims that path" in error for error in status.errors),
            status.errors,
        )

    def test_stale_pending_category_fails(self) -> None:
        rows = self.backlog_row(
            "DG-001", "assets/base_bodies/base_body_001_neutral.png", "registered"
        )
        manifest = self.manifest(
            registered=[("base_bodies", "assets/base_bodies/base_body_001_neutral.png")],
            pending=["base_bodies", "hair_back"],
        )
        status = self.build(manifest, rows)
        self.assertFalse(status.passed)
        self.assertTrue(
            any("lists base_bodies as pending" in error for error in status.errors), status.errors
        )

    def test_category_without_backlog_rows_is_source_gated(self) -> None:
        rows = self.backlog_row(
            "DG-001", "assets/base_bodies/base_body_001_neutral.png", "registered"
        )
        manifest = self.manifest(
            registered=[("base_bodies", "assets/base_bodies/base_body_001_neutral.png")],
            pending=["global_finish"],
            directories=["base_bodies", "global_finish"],
        )
        status = self.build(manifest, rows)
        self.assertTrue(status.passed, status.errors)
        by_category = {item.category: item for item in status.categories}
        self.assertEqual(by_category["global_finish"].state, "source-gated")
        self.assertIn("global_finish", status.pending_categories)

    def test_unknown_backlog_status_is_rejected(self) -> None:
        rows = self.backlog_row("DG-001", "assets/base_bodies/base_body_001_neutral.png", "shipped")
        root = self.make_root()
        _, errors = report_production_status.parse_backlog(self.write_backlog(root, rows))
        self.assertTrue(any("status must be one of" in error for error in errors), errors)

    def test_replace_block_requires_markers(self) -> None:
        with self.assertRaises(ValueError):
            report_production_status.replace_block("no markers here", "block")

    def test_repository_status_document_is_current(self) -> None:
        """The committed ledger must match what the manifest and backlog imply."""
        root = Path(__file__).resolve().parent.parent
        manifest = report_production_status.load_manifest(root / "assets" / "asset_manifest.json")
        entries, errors = report_production_status.parse_backlog(
            root / "docs" / "trait-production-backlog.md"
        )
        status = report_production_status.build_status(manifest, entries, errors)
        self.assertTrue(status.passed, status.errors)

        document = (root / "docs" / "production_status.md").read_text(encoding="utf-8")
        updated = report_production_status.replace_block(document, report_production_status.render_block(status))
        self.assertEqual(
            document,
            updated,
            "docs/production_status.md is stale; run `python scripts/report_production_status.py --write`",
        )


if __name__ == "__main__":
    unittest.main()
