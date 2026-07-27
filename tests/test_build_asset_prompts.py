from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_asset_prompts, report_production_status


ROOT = Path(__file__).resolve().parent.parent

HEADER = (
    "| ID | Category | Visual description | Source reference | Dependency "
    "| Intended production path | Prompt | Status |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


class BuildAssetPromptsTests(unittest.TestCase):
    def backlog(self, rows: str) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "backlog.md"
        path.write_text(HEADER + rows, encoding="utf-8")
        return path

    def row(self, entry_id: str, path: str, status: str, source: str = "`FACE`, eyes r1c1") -> str:
        return (f"| {entry_id} | eyes | Dark eye pair | {source} | none "
                f"| `{path}` | `prompts/06.md` | {status} |\n")

    def test_registered_assets_are_skipped(self) -> None:
        backlog = self.backlog(
            self.row("DG-001", "assets/eyes/eyes_001_a.png", "registered")
            + self.row("DG-002", "assets/eyes/eyes_002_b.png", "pending")
        )
        rows = [r for r in build_asset_prompts.parse_rows(backlog) if r["status"] != "registered"]
        self.assertEqual([r["id"] for r in rows], ["DG-002"])

    def test_inline_markup_is_stripped_from_cells(self) -> None:
        """Edge-stripping left backticks sitting mid-cell, e.g. `FACE`, eyes r1c1."""
        backlog = self.backlog(self.row("DG-002", "assets/eyes/eyes_002_b.png", "pending"))
        row = build_asset_prompts.parse_rows(backlog)[0]
        self.assertNotIn("`", row["source"])
        self.assertNotIn("`", row["description"])

    def test_prompt_carries_the_hard_won_constraints(self) -> None:
        backlog = self.backlog(self.row("DG-002", "assets/eyes/eyes_002_b.png", "pending"))
        prompt = build_asset_prompts.render_prompt(build_asset_prompts.parse_rows(backlog)[0])
        for required in ("1254 x 1254", "DO NOT REMOVE A BACKGROUND",
                         "ALPHA MUST STAY BRIGHT", "STRAY PIXELS", "eyes_002_b.png"):
            self.assertIn(required, prompt)

    def test_background_prompts_require_a_floor_and_forbid_pre_grading(self) -> None:
        backlog = self.backlog(
            "| DG-011 | background | Solar temple | BG ref | none "
            "| `assets/backgrounds/background_005_solar.png` | `prompts/17.md` | pending |\n"
        )
        prompt = build_asset_prompts.render_prompt(build_asset_prompts.parse_rows(backlog)[0])
        self.assertIn("floor surface at foot baseline Y 1139", prompt)
        self.assertIn("FULLY SHARP and UNVIGNETTED", prompt)

    def test_generated_prompt_count_matches_the_ledger(self) -> None:
        """The prompt set and the ledger must agree on what is left to produce."""
        backlog = ROOT / "docs" / "trait-production-backlog.md"
        rows = [r for r in build_asset_prompts.parse_rows(backlog) if r["status"] != "registered"]
        covered = [r for r in rows if r["category"] in build_asset_prompts.CATEGORIES]

        entries, errors = report_production_status.parse_backlog(backlog)
        self.assertEqual(errors, [], errors)
        unregistered = [e for e in entries if e.status != "registered"]
        self.assertEqual(
            len(covered), len(unregistered),
            "every unregistered backlog asset must have a generated prompt",
        )

    def test_committed_prompts_are_current(self) -> None:
        generated = ROOT / "prompts" / "generated"
        if not generated.is_dir():
            self.skipTest("generated prompts not present")
        rows = [r for r in build_asset_prompts.parse_rows(ROOT / "docs" / "trait-production-backlog.md")
                if r["status"] != "registered" and r["category"] in build_asset_prompts.CATEGORIES]
        on_disk = sum(
            path.read_text(encoding="utf-8").count("```text")
            for path in generated.glob("*.md") if path.name != "index.md"
        )
        self.assertEqual(
            on_disk, len(rows),
            "prompts/generated is stale; run `python scripts/build_asset_prompts.py`",
        )


if __name__ == "__main__":
    unittest.main()
