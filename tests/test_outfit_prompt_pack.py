import hashlib
import unittest

from scripts import build_outfit_prompt_pack as pack


class OutfitPromptPackTests(unittest.TestCase):
    def test_pack_is_current(self) -> None:
        self.assertEqual(pack.main(["--check"]), 0)

    def test_every_prompt_attaches_only_its_base_pose(self) -> None:
        for outfit in pack.OUTFITS:
            for pose_id, pose in pack.POSES.items():
                with self.subTest(outfit=outfit["slug"], pose=pose_id):
                    text = pack.prompt(outfit, pose_id)
                    self.assertIn(f"assets/base_bodies/{pose['file']}", text)
                    self.assertNotIn("one_of_ones", text)
                    self.assertIn(pack.target(outfit, pose_id), text)

    def test_all_in_one_hashes_match_the_bases(self) -> None:
        for pose_id, pose in pack.POSES.items():
            with self.subTest(pose=pose_id):
                path = pack.ROOT / "assets" / "base_bodies" / pose["file"]
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), pack.BASE_SHA256[pose_id])

    def test_all_in_one_names_every_pose_and_outfit(self) -> None:
        text = pack.build_all_in_one()
        for pose_id in pack.POSES:
            self.assertIn(pack.base_url(pose_id), text)
        for outfit in pack.OUTFITS:
            self.assertIn(f"OUTFIT {outfit['number']}: {outfit['name']} (slug: {outfit['slug']})", text)


if __name__ == "__main__":
    unittest.main()
