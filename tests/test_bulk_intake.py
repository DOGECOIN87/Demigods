from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import build_asset_prompts, bulk_intake


ROOT = Path(__file__).resolve().parent.parent
BACKLOG_TEXT = (ROOT / "docs" / "trait-production-backlog.md").read_text()
MANIFEST_PATH = ROOT / "assets" / "asset_manifest.json"


class HelperTests(unittest.TestCase):
    def test_asset_id_strips_the_descriptive_tail(self) -> None:
        self.assertEqual(
            bulk_intake.asset_id("assets/hair_back/hair_back_003_silver_long_wavy.png"),
            "hair_back_003",
        )
        self.assertEqual(
            bulk_intake.asset_id("assets/outfits/outfit_006_black_layered_hooded_robe.png"),
            "outfit_006",
        )

    def test_manifest_category_comes_from_the_path(self) -> None:
        self.assertEqual(
            bulk_intake.manifest_category("assets/hair_front/hair_front_001_gold.png"),
            "hair_front",
        )

    def test_width_ceiling_is_read_from_the_shared_gate_table(self) -> None:
        """Hair hugs the head; wings and capes legitimately exceed body width."""
        self.assertEqual(bulk_intake.max_width_ratio_for("hair back"), 1.35)
        self.assertEqual(bulk_intake.max_width_ratio_for("outfit"), 1.15)
        self.assertIsNone(bulk_intake.max_width_ratio_for("back accessory"))


class BinaryQATests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)

    def write(self, name: str, image: Image.Image) -> Path:
        path = self.dir / name
        image.save(path)
        return path

    def results(self, path: Path) -> dict[str, bool]:
        return {check: passed for check, passed, _ in bulk_intake.binary_qa(path)}

    def test_native_rgba_layer_passes(self) -> None:
        image = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        image.paste((200, 180, 255, 255), (500, 300, 700, 600))
        self.assertTrue(all(self.results(self.write("ok.png", image)).values()))

    def test_wrong_dimensions_fail(self) -> None:
        image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        image.paste((200, 180, 255, 255), (100, 100, 300, 300))
        self.assertFalse(self.results(self.write("small.png", image))["dimensions"])

    def test_fully_opaque_layer_has_no_genuine_alpha(self) -> None:
        image = Image.new("RGBA", (1254, 1254), (10, 10, 10, 255))
        self.assertFalse(self.results(self.write("opaque.png", image))["genuine_alpha"])

    def test_fully_transparent_layer_has_no_visible_pixels(self) -> None:
        image = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        self.assertFalse(self.results(self.write("empty.png", image))["visible_pixels"])

    def test_truncated_file_is_reported_not_raised(self) -> None:
        path = self.dir / "broken.png"
        path.write_bytes(b"\x89PNG\r\n\x1a\n truncated garbage")
        checks = bulk_intake.binary_qa(path)
        self.assertEqual(checks[0][0], "decode")
        self.assertFalse(checks[0][1])


class CompositeLayerOrderTests(unittest.TestCase):
    """Rear hair sits behind the body; outfits sit in front of it.

    Compositing in the wrong order produces a QA image that looks fine to the
    gate and wrong to a human, which is the exact thing the review sheet exists
    to catch.
    """

    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.trait = self.dir / "trait.png"
        image = Image.new("RGBA", (1254, 1254), (0, 0, 0, 0))
        # A band across the torso, where the base body is opaque.
        image.paste((255, 0, 0, 255), (500, 600, 760, 700))
        image.save(self.trait)

    def pixel(self, category: str) -> tuple[int, int, int]:
        out = bulk_intake.build_composite(self.trait, category, self.dir / f"{category}.png")
        return Image.open(out).convert("RGB").getpixel((627, 650))

    def test_hair_back_is_hidden_behind_the_body(self) -> None:
        self.assertNotEqual(self.pixel("hair_back"), (255, 0, 0))

    def test_outfit_covers_the_body(self) -> None:
        self.assertEqual(self.pixel("outfits"), (255, 0, 0))


class HairPairingRuleTests(unittest.TestCase):
    """Front bangs must match the rear hair colour and never float on a bald head."""

    def manifest(self, *paths: str) -> dict:
        return {"registered_production_assets": [{"path": p} for p in paths]}

    def test_front_layer_binds_to_the_matching_rear_layer(self) -> None:
        manifest = self.manifest("assets/hair_back/hair_back_004_violet_long_wavy.png")
        rule = bulk_intake.pair_hair_rule(
            "assets/hair_front/hair_front_004_violet_parted_bangs.png", manifest
        )
        self.assertEqual(rule["trait"], "hair_front_004_violet_parted_bangs.png")
        self.assertEqual(rule["requires"], "hair_back_004_violet_long_wavy.png")

    def test_no_rule_when_the_counterpart_is_not_registered(self) -> None:
        rule = bulk_intake.pair_hair_rule(
            "assets/hair_front/hair_front_007_teal_open_center.png", self.manifest()
        )
        self.assertIsNone(rule)

    def test_indices_are_not_cross_matched(self) -> None:
        manifest = self.manifest("assets/hair_back/hair_back_002_black_long_wavy.png")
        rule = bulk_intake.pair_hair_rule(
            "assets/hair_front/hair_front_005_blue_pointed_bangs.png", manifest
        )
        self.assertIsNone(rule)

    def test_backlog_rows_confirm_the_colour_alignment_the_rule_assumes(self) -> None:
        """hair_front_00N binds to hair_back_00N only if index N means one colour.

        The pairing rule matches on the three-digit index alone. That is only
        correct because both HAIR reference rows run the same eight colours in
        the same order, so this asserts it against the backlog rather than
        against a reading of a 128x96 preview.
        """
        rows = build_asset_prompts.parse_backlog(BACKLOG_TEXT)
        colours = ["gold", "black", "silver", "violet", "blue", "pink", "teal", "red"]
        for category, prefix in (("hair back", "hair_back"), ("hair front", "hair_front")):
            for index, colour in enumerate(colours, start=1):
                row = next(
                    r for r in rows
                    if r["category"] == category
                    and Path(r["path"]).name.startswith(f"{prefix}_{index:03d}")
                )
                with self.subTest(asset=Path(row["path"]).name):
                    haystack = f"{row['path']} {row['description']}".lower()
                    # "silver" appears as white-silver, "blue" as deep-blue.
                    self.assertIn(colour, haystack)

    def test_non_hair_assets_get_no_rule(self) -> None:
        manifest = self.manifest("assets/outfits/outfit_006_black_layered_hooded_robe.png")
        rule = bulk_intake.pair_hair_rule(
            "assets/outfits/outfit_006_black_layered_hooded_robe.png", manifest
        )
        self.assertIsNone(rule)


class RegistrationStatusTests(unittest.TestCase):
    """The status flip must accept every pre-registration state, and only those."""

    def flip(self, backlog_id: str, row_status: str) -> tuple[str, int]:
        import re

        row = (
            f"| {backlog_id} | rear aura | Some effect | `AURA`, cell 1 | dep | "
            f"`assets/rear_auras/aura_rear_099_x.png` | `prompts/12_auras.md` | {row_status} |"
        )
        pattern = re.compile(
            rf"^(\| {re.escape(backlog_id)} \|.*\| )(pending|candidate|approved)( \|?\s*)$",
            re.MULTILINE,
        )
        return pattern.subn(r"\1registered\3", row)

    def test_pending_flips(self) -> None:
        text, count = self.flip("DG-900", "pending")
        self.assertEqual(count, 1)
        self.assertTrue(text.rstrip().endswith("| registered |"))

    def test_candidate_flips(self) -> None:
        """Art in hand awaiting review is exactly what gets registered."""
        _, count = self.flip("DG-900", "candidate")
        self.assertEqual(count, 1)

    def test_approved_flips(self) -> None:
        _, count = self.flip("DG-900", "approved")
        self.assertEqual(count, 1)

    def test_already_registered_does_not_flip(self) -> None:
        """Guards against a re-run silently double-registering an asset."""
        _, count = self.flip("DG-900", "registered")
        self.assertEqual(count, 0)

    def test_qa_failed_does_not_flip(self) -> None:
        _, count = self.flip("DG-900", "QA-failed")
        self.assertEqual(count, 0)


class RegistrationAtomicityTests(unittest.TestCase):
    """A failed registration must leave no PNG under assets/<category>/.

    The generator discovers traits by scanning those folders, so a file copied
    before a later validation failed would put unapproved art straight into the
    collection while the manifest still disowned it.
    """

    def test_failed_registration_copies_nothing(self) -> None:
        import json as _json

        results = [{
            "id": "DG-999",
            "passed": True,
            "filename": "aura_rear_099_nonexistent.png",
            "source": "/nonexistent/aura_rear_099_nonexistent.png",
            "sha256": "0" * 64,
            "category": "rear_auras",
            "production_path": "assets/rear_auras/aura_rear_099_nonexistent.png",
            "description": "test",
            "composite": "docs/qa/composites/x.png",
            "failures": [],
        }]
        manifest_before = MANIFEST_PATH.read_text()
        backlog_before = (ROOT / "docs" / "trait-production-backlog.md").read_text()

        # DG-999 is in no backlog row, so the status flip fails after the
        # manifest entry is staged in memory.
        code = bulk_intake.register(results, {"DG-999"}, "docs/qa/test.json")

        self.assertEqual(code, 1)
        self.assertFalse((ROOT / results[0]["production_path"]).exists())
        self.assertEqual(MANIFEST_PATH.read_text(), manifest_before)
        self.assertEqual(
            (ROOT / "docs" / "trait-production-backlog.md").read_text(), backlog_before
        )
        # Manifest still parses and is unchanged in length.
        _json.loads(manifest_before)


class PromptResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.keys = build_asset_prompts.parse_source_keys(BACKLOG_TEXT)
        self.rows = {r["id"]: r for r in build_asset_prompts.parse_backlog(BACKLOG_TEXT)}

    def test_source_keys_resolve_to_repository_paths(self) -> None:
        self.assertEqual(
            self.keys["HAIR"], "images/reference_sheets/anime_hair_customization_asset_sheet.webp"
        )

    def test_every_backlog_category_has_a_layer_mapping(self) -> None:
        """A category with no template would silently drop out of every batch."""
        non_base = {
            r["category"] for r in self.rows.values()
            if r["category"] not in {"base body", "base pose", "background", "global finish"}
        }
        self.assertTrue(non_base <= set(build_asset_prompts.CATEGORY_LAYER), non_base)

    def test_every_emitted_gate_command_is_runnable(self) -> None:
        """GATES holds prose for layer 02; a per-asset prompt must print flags.

        The rear-aura template reads "--floor-aura for ground-plane rings;
        --trait for body-centred glows", which is guidance for a human reading
        the category template and an unrunnable command if pasted verbatim.
        """
        for row in self.rows.values():
            if row["category"] not in build_asset_prompts.CATEGORY_LAYER:
                continue
            with self.subTest(asset=row["id"]):
                flags = build_asset_prompts.gate_flags(row)
                for token in flags.split():
                    self.assertTrue(
                        token.startswith("--") or token.replace(".", "").isdigit(),
                        f"{row['id']} gate contains prose: {flags!r}",
                    )

    def test_ground_plane_rings_gate_as_floor_auras(self) -> None:
        """A ring is seated on the baseline, so --trait would fail it by design."""
        ring = next(r for r in self.rows.values() if "fire ring" in r["description"].lower())
        self.assertEqual(build_asset_prompts.gate_flags(ring), "--floor-aura")

    def test_body_centred_glows_gate_as_traits(self) -> None:
        glow = next(
            r for r in self.rows.values()
            if r["category"] == "rear aura" and "ring" not in r["description"].lower()
        )
        self.assertEqual(build_asset_prompts.gate_flags(glow), "--trait")

    def test_resolved_prompt_has_no_placeholders_left(self) -> None:
        prompt = build_asset_prompts.build_prompt(self.rows["DG-029"], self.keys)
        for placeholder in ("[SPECIFY", "[COLOR]", "[NUM]", "[STYLE]", "[TYPE]"):
            self.assertNotIn(placeholder, prompt)

    def test_resolved_prompt_carries_its_own_reference_cell(self) -> None:
        prompt = build_asset_prompts.build_prompt(self.rows["DG-032"], self.keys)
        self.assertIn("upper row cell 4", prompt)
        self.assertIn("anime_hair_customization_asset_sheet.webp", prompt)

    def test_hair_prompts_forbid_the_recolour_shortcut(self) -> None:
        """The eight HAIR cells are distinct cuts, not one design in eight colours."""
        prompt = build_asset_prompts.build_prompt(self.rows["DG-030"], self.keys)
        self.assertIn("DISTINCT CUTS", prompt)

    def test_prompt_names_the_canonical_output_file(self) -> None:
        prompt = build_asset_prompts.build_prompt(self.rows["DG-042"], self.keys)
        self.assertIn("outfit_006_black_layered_hooded_robe.png", prompt)

    def test_hair_first_batch_covers_the_three_visible_gaps(self) -> None:
        self.assertEqual(
            set(build_asset_prompts.BATCHES["hair-first"]),
            {"hair back", "hair front", "outfit"},
        )


if __name__ == "__main__":
    unittest.main()
