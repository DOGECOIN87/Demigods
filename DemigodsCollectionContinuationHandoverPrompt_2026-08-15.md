# Demigods Collection — Continuation Handover Prompt

You are assuming production oversight of the **Demigods** 777-token NFT collection in `DOGECOIN87/Demigods`. Continue directly from the current `main` branch. Do **not** redesign the collection, weaken the locked modular-production contract, or conduct minting, metadata publication, or any on-chain action without explicit user authorization.

## Authoritative repository checkpoint

The repository is clean and synchronized with `origin/main` at commit **`ce28a0e`** (`Complete rear aura floor-ring family`). The collection remains **770 generative tokens plus 7 reserved legendary one-of-ones**.

| Checkpoint item | Current state |
|---|---|
| Branch | `main...origin/main`, clean and synchronized |
| Registered production asset files | 60 |
| Registered backlog rows | 61, because DG-001 and DG-002 share the neutral master asset |
| Backlog rows | 160 |
| Remaining pending rows | 100 |
| Complete categories | 7 of 16 |
| Latest collection preflight | Passed; rule-valid combination space 27,907 and 770-token saturation 2.8% |

The ledger in `docs/production_status.md` is generated and current. Treat its generated block and `docs/trait-production-backlog.md` as the authoritative live status, rather than the older historical narrative elsewhere in that file.

## Work completed in this continuation

Three validated production groups were generated, visually reviewed, registered, committed, and pushed.

| Batch | Backlog IDs | Result | Key repository checkpoint |
|---|---|---|---|
| Red matched hair pair | DG-036, DG-122 | Registered. The red rear hair and short red bangs preserve face visibility and carry the required front-to-rear compatibility rule. | `b313b82` |
| Remaining neutral-pose outfits | DG-042–DG-046 | Registered. Each is bound to `base_body_001_neutral_master.png`; the initial short placements were corrected by reduction-only renormalization before approval. | `af609a4` and `8cfb228` |
| Remaining rear auras | DG-017, DG-019, DG-151–DG-155, DG-157 | Registered. This completes the entire rear-aura category, including the low-profile elemental, ice, smoke, and water floor rings. | `41b9d04` and `ce28a0e` |

### Registered hair pair

| Family | Rear asset | Front asset | Compatibility requirement |
|---|---|---|---|
| Red | `hair_back_008_red_long_wavy.png` | `hair_front_008_red_short_bangs.png` | Front requires its matching red rear hair |

All eight matched hair families are now complete and registered: gold, black, silver, violet, blue, pink, teal, and red.

### Newly registered outfit assets

The remaining neutral-pose outfits are `outfit_006_black_layered_hooded_robe.png`, `outfit_007_brown_leather_long_coat.png`, `outfit_008_olive_ragged_cloak.png`, `outfit_009_navy_high_collar_coat.png`, and `outfit_010_celestial_robe_white_gold.png`. They are validated against Pose 001 and each has an explicit compatibility requirement in `config/compatibility.json`.

### Newly registered rear-aura assets

The newly completed rear-aura family includes the blue crystalline burst, lavender lightning wisps, orange fire ring, blue lightning ring, violet flame ring, pale-blue ice crystal ring, black smoke void ring, and cyan water splash ring. Full-context review evidence is retained under `docs/qa/`, including contrasting bright/dark-background composites.

## Current production status

| Category | Registered / total | Remaining | State |
|---|---:|---:|---|
| Backgrounds | 8 / 8 | 0 | Complete |
| Rear auras | 18 / 18 | 0 | Complete |
| Hair back | 8 / 8 | 0 | Complete |
| Base bodies | 5 / 5 | 0 | Complete |
| Outfits | 10 / 10 | 0 | Complete |
| Hair front | 8 / 8 | 0 | Complete |
| Global finish | 3 / 3 | 0 | Complete |
| Back accessories | 0 / 8 | 8 | Not started |
| Neck accessories | 0 / 8 | 8 | Not started |
| Head accessories | 0 / 10 | 10 | Not started |
| Hand objects | 0 / 12 | 12 | Not started |
| Front auras | 0 / 2 | 2 | Not started |
| Eyes | 0 / 24 | 24 | Not started |
| Eyebrows | 0 / 16 | 16 | Not started |
| Mouths | 0 / 12 | 12 | Not started |
| Expression marks | 0 / 8 | 8 | Not started |

## Immediate priority

Resume with the **back-accessory representative batch**, then continue in compatible batches through accessories and front effects before beginning the high-volume facial-trait families.

| Priority | Backlog IDs | Category | Intended first batch |
|---:|---|---|---|
| 1 | DG-021–DG-025 | Back accessories | Silver feathered wings, black-violet bat wings, cyan fairy wings, navy formal cape, black-violet ragged cloak |
| 2 | DG-026–DG-028 | Back accessories | Pale-blue crystal wings, luminous gold wings, olive-silver spiked wings |
| 3 | DG-047–DG-054 | Neck accessories | Full family; begin with black choker representative test |
| 4 | DG-123–DG-132 | Head accessories | Full family; begin with gold pointed crown representative test |
| 5 | DG-133–DG-144 | Hand objects | Respect exact pose dependencies; generate in pose-compatible sub-batches |
| 6 | DG-145–DG-146 | Front auras | Complete after rear effects and foreground layering review |
| 7 | DG-055–DG-114 | Facial traits | Eyes, brows, mouths, then expression marks in clearly reviewable batches |

The exact pending descriptions, canonical filenames, source-sheet cells, dependencies, and prompt references are in `docs/trait-production-backlog.md`. Do not invent additional backlog rows.

## Required workflow for every asset or compatible batch

1. Read the applicable locked category prompt in `prompts/`, plus `prompts/00_locked_master_specification.md` and `prompts/01_universal_avoid_block.md`. Preserve the 1254 × 1254 RGBA canvas, shared rig coordinates, premium anime-chibi fantasy style, upper-left lighting, and transparent-layer role.
2. Generate one isolated source asset per row. Do not generate a full character, scene, product sheet, or multiple variants in a single output. Generator-native 1920 × 1920 RGBA sources are acceptable only through the controlled transform route.
3. Preserve accepted raw generator bytes in `images/trait_candidates/<category>/` as immutable evidence. Keep rejected sources if they document a material design or placement rejection; remove only temporary duplicates and opaque derivatives that are not evidence.
4. Normalize only with `scripts/normalize_generator_source.py`; never upscale, crop meaningful art, repaint through code, or use a generic background-removal shortcut. Use an **absolute** source path and record the alpha threshold and transform provenance.
5. Run `scripts/rig_gate_report.py` on every normalized candidate. Use `--trait --max-width-ratio 1.35` for ordinary partial layers, `--floor-aura` only for floor effects, and category-appropriate modes where documented.
6. Run `scripts/bulk_intake.py` without registration to create the provenance report, binary QA result, base composite, and batch review sheet. Use absolute paths for its drop directory, report, and sheet arguments.
7. Render and inspect full-context composites with compatible registered layers and at least two contrasting registered backgrounds. Reject candidates that obscure the face, collide with hands or outfits, drift from anchors, leave visible seams or base-body pixels, have a presentation matte, or break the intended layer order.
8. Record the decision in `docs/oversight_visual_review_2026-08-15.md` and retain a batch-specific review note in `docs/qa/`.
9. For approved candidates only, add required compatibility rules in `config/compatibility.json`, then register atomically through `scripts/bulk_intake.py --register-approved <DG-IDs>`.
10. Run `python3 scripts/validate_config.py`, `python3 scripts/validate_assets.py assets`, `python3 scripts/validate_manifest_consistency.py`, `python3 scripts/report_production_status.py --check`, and `python3 scripts/generate_777.py --preflight-only`. Run the full unit suite, `python3 -m unittest discover -s tests -v`, after material policy or code changes.
11. Check `git status --short --branch`, then commit each validated batch atomically and push `main`. Include canonical assets, immutable source evidence, transform reports, batch report/sheet, base composites, full-context composites, review notes, manifest/backlog/ledger updates, compatibility changes, and any reusable renderer source.

## Current validation state

The final rear-aura registration checkpoint passed configuration validation, asset validation, manifest-consistency validation, production-status freshness validation, and the 777-generator preflight. The most recent full regression suite at the outfit policy checkpoint passed **196 tests**. Asset validation continues to emit existing non-blocking warnings that registered images have no embedded ICC profile; visual reviewers confirmed the intended sRGB rendering, and these warnings are not registration failures.

The following recent preflights all passed: the red hair pair, neutral-pose outfit family, the first five rear auras, and the final three rear auras. The latest artifact checkpoint is `ce28a0e`.

## Important implementation lessons from this checkpoint

- `normalize_generator_source.py` requires an absolute source argument for provenance recording. Relative source paths raise a `relative_to(ROOT)` error.
- `bulk_intake.py` should be invoked with absolute drop, sheet, and report paths. Relative report or sheet paths can complete candidate work but then fail while printing the result path.
- The generator-source transform is strictly reduction-only. Floor-ring sources must be generated as very low, wide ellipses; the normalizer enforces the ordinary lower trait bound, so source sizing and placement must accommodate a lower visible edge at Y 1139.
- Review visual placement, not just binary success. The first outfit normalization was rejected because boots ended above the foot baseline and exposed base feet; the first three organic floor-ring designs were rejected because they were too tall. Their replacements were re-rendered and re-reviewed before registration.
- The first remaining back-accessory generation batch was prepared conceptually but **not** generated: image-generation capacity was exhausted before it could start. There are no pending candidate files to register for DG-021–DG-025.

## Non-negotiable safeguards

- Every registered asset must be a genuine 1254 × 1254 RGBA PNG with true alpha; never register checkerboard, matte, opaque, cropped, or presentation-background art.
- Never resample registered assets outside the documented normalization procedure, and never edit immutable generator-source evidence in place.
- Preserve compatible layer rules in `config/compatibility.json`. Hair and pose-specific outfit requirements are already present; add accessory/hand-object rules only when verified through a visual collision or dependency test.
- Preserve the approved premium anime-chibi fantasy language, clean linework, shared frontal orthographic geometry, modular compositing, and upper-left key lighting.
- The seven legendary assets stay separate and reserved. They are not traits and must not enter the generative manifest.
- Do not mint, publish metadata, release, or conduct on-chain actions without explicit user approval after every remaining category is complete and all launch infrastructure is verified.

## Completion condition

The production task is complete only when all 160 backlog rows are registered or explicitly resolved through a documented user-approved policy change, all 16 categories are production complete, the generator can produce 770 valid generative tokens under every compatibility rule, the seven legendary pieces remain reserved, validators and regression suites pass, launch infrastructure is verified, and the user has explicitly approved the mint/release plan.
