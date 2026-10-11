# Outfits withdrawn (2026-10-11)

The owner removed all 25 registered outfits (outfit_001, 003, 004, 005, 010, and the
dressed-body families 006–009 in poses 001–005) because none suited the finished 1-of-1
artwork. `scripts/withdraw_all_outfits.py` moved the files to
`incoming/outfits_withdrawn_2026-10-11/outfits/` (untracked; history keeps the bytes at the
recorded hashes), recorded each as withdrawn in `assets/asset_manifest.json`, closed their
backlog rows, and dropped their compatibility rules.

The outfits category is optional, so the generator still runs (dry run: 770 unique tokens)
and renders the undressed base bodies until new outfits are registered. The outfit
neckline/sleeve/dressed-body tests skip while the category is empty.

Replacement plan: `docs/pose_anatomy_2026-10-11.md`.
