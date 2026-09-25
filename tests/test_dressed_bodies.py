"""Every registered dressed-body outfit is on the rig, takes the shared face, and is traceable.

A dressed body replaces the base in the render, so nothing checks it against a
body underneath. These assertions check it against what it has to agree with
instead: the rig rows every trait is drawn to, the shared face traits, the pose
it is bound to, and the immutable render it was normalized from.

The face numbers describe the accepted art rather than define it; see
FACE_OFF_HEAD_CEILING in scripts/intake_dressed_bodies.py.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from scripts import hidden_layers, intake_dressed_bodies, normalize_dressed_body

ROOT = Path(__file__).resolve().parent.parent


class DressedBodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = json.loads((ROOT / "config" / "compatibility.json").read_text())
        cls.dressed = sorted(hidden_layers.dressed_outfits(cls.rules))
        manifest = json.loads((ROOT / "assets" / "asset_manifest.json").read_text())
        cls.entries = {Path(e["path"]).name: e for e in manifest["registered_production_assets"]}
        cls.union = intake_dressed_bodies.face_trait_union()

    def figure(self, name: str) -> np.ndarray:
        with Image.open(ROOT / "assets" / "outfits" / name) as image:
            return np.asarray(image.convert("RGBA"))

    def test_registered_dressed_bodies_are_the_approved_renders(self) -> None:
        """What is registered is exactly what the review approved, no more, no less.

        A render withdrawn after registration keeps its source and its review
        record, marked withdrawn, so intake cannot register it again.
        """
        sources = json.loads((ROOT / "images" / "trait_candidates" / "outfits_dressed"
                              / "sources.json").read_text())
        approved = {r["target"] for r in sources["renders"]
                    if r.get("review", {}).get("decision") == "approved"}
        self.assertTrue(approved, "no approved dressed-body renders on record")
        self.assertEqual(set(self.dressed), approved)

    def test_each_is_bound_to_exactly_one_base_pose(self) -> None:
        for name in self.dressed:
            with self.subTest(outfit=name):
                bases = [r["requires"] for r in self.rules["requires"] if r["trait"] == name]
                self.assertEqual(len(bases), 1, f"{name} must bind exactly one pose")
                self.assertTrue((ROOT / "assets" / "base_bodies" / bases[0]).exists())
                pose = name.rsplit("_pose_", 1)[1][:3]
                self.assertEqual(bases[0], intake_dressed_bodies.BASES[pose],
                                 f"{name} is bound to a pose its filename does not name")

    def test_crown_soles_and_head_centre_are_on_the_rig(self) -> None:
        for name in self.dressed:
            with self.subTest(outfit=name):
                figure = self.figure(name)
                rows = np.nonzero((figure[..., 3] > 0).any(axis=1))[0]
                self.assertEqual((int(rows.min()), int(rows.max())), (141, 1139))
                measured = normalize_dressed_body.measure(figure[..., 3] / 255.0)
                self.assertAlmostEqual(measured["head_center"], 627.5, delta=1.5)

    def test_the_shared_face_lands_on_face_skin(self) -> None:
        for name in self.dressed:
            with self.subTest(outfit=name):
                clearance = intake_dressed_bodies.face_clearance(self.figure(name), self.union)
                self.assertLessEqual(clearance["off_head"], intake_dressed_bodies.FACE_OFF_HEAD_CEILING)
                self.assertLessEqual(clearance["on_outline"], intake_dressed_bodies.FACE_ON_OUTLINE_CEILING)

    def test_each_traces_to_its_immutable_render(self) -> None:
        for name in self.dressed:
            with self.subTest(outfit=name):
                entry = self.entries[name]
                provenance = entry["provenance"]
                self.assertEqual(provenance["origin"], "dressed_body_render")
                source = ROOT / provenance["source_path"]
                self.assertTrue(source.exists(), f"{name}'s source render is missing")
                digest = hashlib.sha256(source.read_bytes()).hexdigest()
                self.assertEqual(digest, provenance["source_sha256"],
                                 f"{name}'s source render has changed since it was normalized")


if __name__ == "__main__":
    unittest.main()
