# Owner trait removal — 2026-09-26

On 2026-09-26 the owner removed, by decision rather than for failing QA:

- every outfit that does not exist in all five poses: outfits 001–005 and 010, each one garment layer drawn for a single pose
- the head accessory (headwear) category
- the rear aura and front aura categories
- the hand object category

## What left the collection

| Category | Registered assets withdrawn | Backlog rows closed |
|---|---|---|
| `outfits` (001–005, 010) | 6 | 6 |
| `head_accessories` | 6 | 10 |
| `rear_auras` | 8 | 18 |
| `front_auras` | 2 | 2 |
| `hand_objects` | 12 | 12 |
| **Total** | **34** | **48** |

`scripts/withdraw_owner_removed_traits.py` made the change:

- Each registered file moved to `incoming/owner_removed_2026-09-26/<category>/`. `incoming/.gitignore` keeps it out of the tree, and git history keeps the bytes at the recorded hash.
- Each manifest entry became a `withdrawn` record in `blocked_assets` with its hash, retained path and reason. The six outfits also record that they may return only as a dressed-body family rendered in all five poses.
- The 14 head accessories and rear auras that QA had already retired now also carry the owner's decision.
- Every backlog row in the four removed categories closed as `withdrawn`, whatever its earlier state, as did the six outfits' rows. `pending_categories` no longer lists `head_accessories` or `rear_auras`.
- Removed from `config/compatibility.json`:
  - the 18 `requires` rules naming a removed trait: 12 hand objects binding a pose, and the six outfits
  - the one `excludes` rule, which listed only hand objects
- Removed from `optional_categories` in `config/collection.json`: `rear_auras`, `head_accessories` and `hand_objects`.

The four categories stay in the layer order, as neckwear did, so a redesigned set could return.

Candidate art for these categories under `images/trait_candidates/` is untouched working material and was never part of the collection.

## The collection now

- **119 registered assets.** The outfit category is the four dressed-body families 006–009, each in all five poses: 20 files. Every token wears one of them, and it hides the base pose it was painted over.
- **Preflight passes.** There are 1,480,411,054 rule-valid combinations, down from 1,557,203,364,348. 770 tokens use 0.0% of either.
- **Grip poses hold nothing.** Poses 002, 003 and 005 were built to hold an object, and now close on nothing.
  - The vertical grips read as relaxed fists.
  - The two-hand grip reads as clasped hands.
  - Checked at full size on the sample below: no fragment of a removed object survives in any dressed render.
- **Sample:** [`owner_trait_removal_2026-09-26/sample_tokens_seed_sheet25-ec9dd68c.png`](owner_trait_removal_2026-09-26/sample_tokens_seed_sheet25-ec9dd68c.png). This is 25 tokens from the real generator (`--supply 25 --seed sheet25-ec9dd68c --allow-nonstandard-supply`).

## Tests

- **New: `tests/test_owner_trait_removal.py`.** It holds the decision in place:
  - every registered outfit exists in all five poses
  - the four categories stay empty
  - the 34 withdrawal records keep their reasons and hashes
- **`test_outfit_necklines` and `test_outfit_sleeves`** measure a garment layer against the base body under it. None is left, since every outfit is dressed and hides its base. Their guard therefore changed from "some outfit is bound to a base" to "every registered outfit is either bound to a base, and measured, or dressed". A pairing that breaks still fails.
- **`test_open_collar` and `test_outfit_body_fit`** hold regression cases for outfits 002 and 003: their repaired collars and fitted torsos. A case that is no longer registered must be on the record as withdrawn. One that returns meets the gate again.
- **`scripts/despeckle_chroma_residue.py`** no longer exempts the green laurel, since the laurel is gone. `test_chroma_residue` rejects an exemption for an asset that is not present.
