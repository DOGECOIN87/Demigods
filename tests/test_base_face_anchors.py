"""Every base body must put its face where the shared face traits are drawn.

Eyes, eyebrows and mouths are one layer each, shared by every base and placed by
rig anchor rather than per base. That only works if the bases agree on where the
face is. `base_pose_005` did not: its eye line sat at Y 350.8 against the other
four at Y 368.5-371.8, and its chin and shoulder junction were 24 px high - a
smaller head on a longer body. A shared eye pair seated on the collection's eye
line would have left a 20 px band of pose 005's baked eyes showing above it.

The silhouette rig gate passed it. Canvas, top of head, foot baseline, centre X
and maximum bounds are all measured at the outline's extremes, and pose 005 met
every one; the whole deviation was interior. These assertions measure the anatomy
instead, so a base that does not share the face rig fails before anything is
built on top of it.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The consensus the four compliant bases hold, and the locked rows.
TOP_OF_HEAD = 141.0
FOOT_BASELINE = 1139.0
EYE_LINE = 370.3
CHIN = 476.5
SHOULDER = 496.3

# The four agree within 3.3 px on the eye line and 2 px on the chin and shoulder.
# 6 px leaves room for a differently drawn pose without letting a face drift far
# enough to show under a shared trait.
TOLERANCE = 6.0


class BaseFaceAnchorTests(unittest.TestCase):
    def test_every_base_body_shares_the_face_rig(self) -> None:
        from scripts.refit_pose_005_proportions import landmarks_of

        directory = ROOT / "assets" / "base_bodies"
        bases = sorted(directory.glob("*.png"))
        self.assertTrue(bases, "no base bodies registered")
        expected = {
            "top_of_head": TOP_OF_HEAD,
            "foot_baseline": FOOT_BASELINE,
            "eye_line": EYE_LINE,
            "chin": CHIN,
            "shoulder": SHOULDER,
        }
        for path in bases:
            measured = landmarks_of(path)
            for anchor, target in expected.items():
                with self.subTest(base=path.name, anchor=anchor):
                    tolerance = 0.0 if anchor in ("top_of_head", "foot_baseline") else TOLERANCE
                    self.assertLessEqual(
                        abs(measured[anchor] - target), tolerance,
                        f"{path.name}: {anchor} measures Y{measured[anchor]:.1f}, "
                        f"the collection sits at Y{target}",
                    )


if __name__ == "__main__":
    unittest.main()
