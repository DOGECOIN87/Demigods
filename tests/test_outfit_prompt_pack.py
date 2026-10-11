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


if __name__ == "__main__":
    unittest.main()
