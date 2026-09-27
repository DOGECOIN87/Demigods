# Headwear and aura removal — 2026-09-27

On 2026-09-27 the owner removed the headwear and aura traits from the collection, completely and by decision rather than for failing QA:

- the head accessory (headwear) category
- the rear aura category
- the front aura category

Hand objects and outfits are unaffected.

## What left the collection

| Category | Registered assets withdrawn | Backlog rows closed |
|---|---|---|
| `head_accessories` | 6 | 10 |
| `rear_auras` | 8 | 18 |
| `front_auras` | 2 | 2 |
| **Total** | **16** | **30** |

`scripts/withdraw_headwear_and_auras.py` made the change, following the neckwear precedent (`scripts/deregister_neck_accessories.py`):

- Each registered file moved to `incoming/owner_removed_2026-09-27/<category>/`. `incoming/.gitignore` keeps it out of the tree, and git history keeps the bytes at the recorded hash.
- Each manifest entry became a `withdrawn` record in `blocked_assets`, with its hash, retained path and reason.
- The 14 head accessories and rear auras that QA had already retired now also carry the owner's decision.
- Every backlog row in the three categories closed as `withdrawn`, whatever its earlier state.
- `pending_categories` no longer lists `head_accessories` or `rear_auras`.
- `rear_auras` and `head_accessories` left `optional_categories` in `config/collection.json`. `front_auras` was never optional: until now every token drew one.
- No compatibility rule named a removed trait, so `config/compatibility.json` is unchanged.

The three categories stay in the layer order, as neckwear did, so a redesigned set could return. Working material is untouched: candidate art under `images/trait_candidates/`, the prompts and the build scripts. None of it was ever part of the collection.

The global finish category (soft bloom, gilded warm, cool veil) is a whole-image lighting finish, not an aura, and stays.

## The collection now

- **137 registered assets**, down from 153.
- **Preflight passes.** There are 13,564,489,236 rule-valid combinations, down from 1,557,203,364,348. The 770 generative tokens use 0.0% of either.
- **Sample:** [`headwear_aura_removal_2026-09-27/sample_25_seed_20260927.png`](headwear_aura_removal_2026-09-27/sample_25_seed_20260927.png). This is 25 tokens from the real generator (`--supply 25 --seed 20260927 --allow-nonstandard-supply`). None carries headwear or an aura, and six hold an item.

## Tests

- **New: `tests/test_headwear_aura_removal.py`.** It holds the decision in place:
  - the three categories stay empty and off `optional_categories`
  - the 16 withdrawal records keep their reasons and hashes
- **Now skipped (they skip themselves when their category is empty, as the neckwear tests did):**
  - the headwear face-clearance checks in `tests/test_face_occlusion.py`
  - the front-aura flat-shading check in `tests/test_face_traits.py`
- **`scripts/despeckle_chroma_residue.py`** no longer exempts the green laurel, since the laurel is gone. `test_chroma_residue` rejects an exemption for an asset that is not present.

## Single traits removed the same day

After reviewing more 25-token samples, the owner removed three single traits:
- the storm guardian outfit (`outfit_002`), a garment drawn for pose 002 only;
- the violet blade (`hand_object_009`) and the round talisman (`hand_object_011`), which still had their old art, drawn behind the body.

`scripts/withdraw_traits.py` recorded them the same way:
- the files are in `incoming/owner_removed_2026-09-27/`
- each has a withdrawn record with its hash
- backlog rows DG-038, DG-141 and DG-143 closed
- the compatibility rules naming them went

`tests/test_trait_withdrawals.py` keeps them out.

The collar and body-fit regression cases for outfit 002, in `tests/test_open_collar.py` and `tests/test_outfit_body_fit.py`, now require an outfit that is not registered to be recorded as withdrawn. One that returns meets the gate again. `scripts/fit_in_hand_render.py` no longer lists outfit 002 among the pose-002 review outfits.

After these removals:
- The library is 134 assets: ten hand objects, and 25 outfits (the other five single-pose garments and the four dressed families).
- Preflight passes with 10,300,450,406 rule-valid combinations.
