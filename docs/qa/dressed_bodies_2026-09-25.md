# Dressed-body outfits - intake QA, 2026-09-25

## What arrived

Twenty renders, uploaded by the owner to the repository root in `9d23ad7` and `20c7e97` and moved unchanged to `images/trait_candidates/outfits_dressed/`: four outfit families in all five poses, each painted **with the body intact** - bald, faceless, on the base's proportions. Fifteen are RGB on pure black (brown coat, olive cloak, navy coat); the five black-robe renders are RGBA with their own matte, since a black robe cannot be keyed off black. Poses were read from the hands against `assets/base_bodies/`; `sources.json` beside the renders records every mapping, SHA-256 and review decision.

The owner also said neckwear can be omitted, and that the collection needs about 700 generative artworks.

## Decisions

- **Twenty dressed bodies registered** as pose-bound outfits, DG-162 to DG-181. Each `requires` its base pose and `hides` it: the base is selected - it binds the pose, the hand objects and the metadata - but not drawn. Mechanism in `scripts/hidden_layers.py`, validated by `validate_config.validate_hides`.
- **Outfits 006-009 retired** (DG-042 to DG-045, now `withdrawn`). Each was one garment layer fitted to Pose 001 only. The dressed families replace them in every pose; keeping both would put two versions of one outfit in Pose 001. Bytes retained in `incoming/outfits_superseded_2026-09-25/`, hashes in `blocked_assets`.
- **Neck accessories withdrawn by the owner** (DG-047 to DG-054). They were already out of `assets/` since 2026-09-10; the rows now close as `withdrawn` and each record carries the decision. `withdrawn` is a new backlog status for rows closed by recorded decision; the ledger no longer counts them as remaining work.
- **Outfits 001-005 and 010 stay** as their original single-pose garment layers until dressed renders replace them. Prompts for the thirty missing renders: `prompts/dressed_body_pose_pack_2026-09-25.md`.
- **Black robe, Pose 002: hand objects excluded.** Its fist is drawn 20 px inside the base's, and every vertical-grip object is seated at the base fist (438, 772); on this figure each hung beside the hand. The pose still appears, empty-handed.

## Results

| Row | Asset | Source | Source crown-soles | Head scale | Body scale | Face px off head / on outline |
|---|---|---|---|---|---|---|
| DG-162 | `outfit_006_black_layered_hooded_robe_pose_001.png` | RGBA | 40-1184 | 0.941 | 0.840 | 226 / 433 |
| DG-163 | `outfit_006_black_layered_hooded_robe_pose_002.png` | RGBA | 107-1184 | 1.000 | 0.892 | 234 / 293 |
| DG-164 | `outfit_006_black_layered_hooded_robe_pose_003.png` | RGBA | 139-1177 | 0.994 | 0.945 | 450 / 520 |
| DG-165 | `outfit_006_black_layered_hooded_robe_pose_004.png` | RGBA | 139-1163 | 0.985 | 0.969 | 371 / 396 |
| DG-166 | `outfit_006_black_layered_hooded_robe_pose_005.png` | RGBA | 142-1178 | 1.000 | 0.945 | 417 / 451 |
| DG-167 | `outfit_007_brown_leather_long_coat_pose_001.png` | RGB | 140-1144 | 0.994 | 0.994 | 368 / 331 |
| DG-168 | `outfit_007_brown_leather_long_coat_pose_002.png` | RGB | 140-1144 | 0.994 | 0.994 | 247 / 174 |
| DG-169 | `outfit_007_brown_leather_long_coat_pose_003.png` | RGB | 140-1144 | 0.997 | 0.993 | 314 / 341 |
| DG-170 | `outfit_007_brown_leather_long_coat_pose_004.png` | RGB | 140-1144 | 0.997 | 0.993 | 277 / 286 |
| DG-171 | `outfit_007_brown_leather_long_coat_pose_005.png` | RGB | 140-1144 | 1.000 | 0.991 | 248 / 318 |
| DG-172 | `outfit_008_olive_ragged_cloak_pose_001.png` | RGB | 140-1144 | 0.994 | 0.994 | 357 / 345 |
| DG-173 | `outfit_008_olive_ragged_cloak_pose_002.png` | RGB | 139-1144 | 0.991 | 0.994 | 397 / 344 |
| DG-174 | `outfit_008_olive_ragged_cloak_pose_003.png` | RGB | 140-1144 | 0.997 | 0.993 | 318 / 338 |
| DG-175 | `outfit_008_olive_ragged_cloak_pose_004.png` | RGB | 140-1144 | 0.997 | 0.993 | 252 / 283 |
| DG-176 | `outfit_008_olive_ragged_cloak_pose_005.png` | RGB | 139-1145 | 0.994 | 0.991 | 331 / 309 |
| DG-177 | `outfit_009_navy_high_collar_coat_pose_001.png` | RGB | 140-1147 | 0.994 | 0.990 | 354 / 310 |
| DG-178 | `outfit_009_navy_high_collar_coat_pose_002.png` | RGB | 139-1147 | 0.994 | 0.988 | 284 / 238 |
| DG-179 | `outfit_009_navy_high_collar_coat_pose_003.png` | RGB | 140-1147 | 0.997 | 0.988 | 317 / 312 |
| DG-180 | `outfit_009_navy_high_collar_coat_pose_004.png` | RGB | 140-1148 | 0.997 | 0.987 | 279 / 267 |
| DG-181 | `outfit_009_navy_high_collar_coat_pose_005.png` | RGB | 139-1147 | 0.997 | 0.987 | 256 / 288 |

Every output has its crown on Y 141, its soles on Y 1139 and its head centred on X 627 within half a pixel. The face column counts where the union of all 60 shared face traits would land off the head or on its drawn outline; the registered base bodies themselves measure 90-252 off the head, from the feathered rims of the blush and eye patches at the cheek-ear junction. These numbers describe the accepted art. The ceilings in `scripts/intake_dressed_bodies.py` sit just above them to catch a regression; they are not what decided acceptance.

## What was looked at

- `dressed_bodies_2026-09-25/figures_over_base_silhouette.png` - every figure with its base's silhouette in red. Head, hands and feet sit on the base's in all twenty; the black robe's lower hem and hood are wider by design.
- `dressed_bodies_2026-09-25/faces_worst_case_traits.png` - every face with the widest blush, lowest mouth and highest brow. All twenty clear the jaw and ears.
- Edges at 3x on white and on saturated red: no black fringe, no halo, no matte colour at the cuffs, boots, tatters or hood.
- Every Pose 002 figure with all eight grip objects, and every Pose 004 figure with all four palm objects. Brown, olive and navy hold them where the original storm guardian and lunar oracle do, within 1-4 px at the hand's outer edge; the black robe's palm is 16 px inward and still reads correctly with the orb, books and talisman; its fist does not (above).
- `dressed_bodies_2026-09-25/sample_tokens_seed_dressed-bodies-qa-1.png` - forty tokens from the real generator (`--supply 40 --seed dressed-bodies-qa-1 --allow-nonstandard-supply`). The base never shows under a dressed figure. The see-through look on the black robe's hem in token 0033 is the orange front aura drawn over it, by design; without the aura the robe is opaque.
- A dry run of 770 tokens (`--seed dressed-bodies-dry-1 --dry-run`) completes with 603 dressed-body tokens and no duplicate signatures.

## Approaches that failed

1. **One uniform reduction per render.** Right for the fifteen renders on the rig's proportions, wrong for the black robe: its renders draw the head at the base's size and the body 2-12% longer, so bringing the soles up to Y 1139 shrank the head by up to 7%. The shared mouth landed on the chin and the eye patches on the ears; the face check measured 1288-2530 px off the head against 226-450 now. Replaced by the two-zone fit: head scaled to the shared chin row, body scaled below it, blended over 50 rows of neck.
2. **Keying every near-black pixel as background.** The renders draw contour lines in near-black too - the navy coat's gold trim is ringed with it - so each one-pixel run of contour became a pinhole: up to 907 per navy figure, showing the backdrop through boots and cuffs on a light ground. Replaced by a 3 x 3 opening: near-black at least three pixels across is background (the gaps under the arms and between fingers are), anything thinner is paint.
3. **Leaving the base drawn under the dressed figure.** The two silhouettes agree to a few pixels, not exactly; a second, bare figure would show at every fingertip and boot that differs. The base is now hidden, not covered.

## Found and not changed

- **Sampling skew, pre-existing.** The generator draws every category independently and rejects invalid combinations. Hand objects fit only Poses 002 and 004, so those poses survive the draw more often: in the 770 dry run Pose 002 is 28% of tokens and Poses 001, 003 and 005 are 14-19%, and only 19% of tokens hold an object although `optional_categories.hand_objects` is 0.6. Choosing the hand object from those compatible with the chosen pose would fix both; it changes every seed's output, so it was left for the owner's decision. The owner asked for it the same day: fixed in `docs/qa/generator_sampling_2026-09-25.md`.
- `hair_back_003_silver_long_wavy.png` carries about 12,500 px of low-alpha strands outside its locks, visible as faint grey wisps over a dark background (token 0017). Registered 2026-08-15; not touched here.
- The six original garment layers (outfits 001-005, 010) keep the fit defects recorded in `docs/handoff/outfit-refit-brief.md` until dressed renders replace them.
