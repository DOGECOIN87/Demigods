# Demigods Collection — Continuation Handover Prompt

You are assuming production oversight of the **Demigods** 777-token NFT collection in `DOGECOIN87/Demigods`. Continue directly from the current `main` branch. Do not redesign the collection, weaken the locked modular-production contract, or conduct minting, metadata publication, release, or any on-chain action without explicit user authorization.

## Authoritative repository checkpoint

The repository is clean and synchronized with `origin/main` at commit **`a397f2d`** (`Complete neck accessory family`). The collection remains **770 generative tokens plus 7 reserved legendary one-of-ones**.

| Checkpoint item | Current state |
|---|---|
| Branch | `main...origin/main`, clean and synchronized |
| Registered production asset files | 76 |
| Registered backlog rows | 77, because DG-001 and DG-002 share the neutral master |
| Total backlog rows | 160 |
| Remaining pending rows | 84 |
| Complete categories | 9 of 16 |
| Latest rule-valid combination space | 1,982,177 |
| Latest 770-token saturation | 0.0% |
| Latest pushed commit | `a397f2d` |

The generated ledger in `docs/production_status.md` and the rows in `docs/trait-production-backlog.md` are authoritative. Older historical narrative elsewhere in the status document may describe superseded checkpoints.

## Work completed in this continuation

Two complete categories were generated, visually reviewed, normalized through the locked transform route, registered atomically, committed, and pushed.

| Batch | Backlog IDs | Result | Evidence |
|---|---|---|---|
| Back accessories | DG-021–DG-028 | Full 8-asset category registered | `docs/qa/back_accessories_001-005_review_sheet.png`, `docs/qa/back_accessories_006-008_review_sheet.png` |
| Neck accessories | DG-047–DG-054 | Full 8-asset category registered | `docs/qa/neck_accessories_001-005_review_sheet.png`, `docs/qa/neck_accessories_006-008_review_sheet.png` |

All 16 newly registered assets passed binary QA, the category trait rig gate, batch intake, and manifest registration. The repository validation checkpoint passed configuration validation, asset validation, manifest-consistency validation, production-status freshness validation, generator preflight, and the full unit suite. Asset validation continues to report the known non-blocking missing-ICC-profile warnings; these do not constitute registration failures.

## Current production status

| Category | Registered / total | Remaining | State |
|---|---:|---:|---|
| Backgrounds | 8 / 8 | 0 | Complete |
| Rear auras | 18 / 18 | 0 | Complete |
| Back accessories | 8 / 8 | 0 | Complete |
| Hair back | 8 / 8 | 0 | Complete |
| Base bodies | 5 / 5 | 0 | Complete |
| Outfits | 10 / 10 | 0 | Complete |
| Neck accessories | 8 / 8 | 0 | Complete |
| Hair front | 8 / 8 | 0 | Complete |
| Global finish | 3 / 3 | 0 | Complete |
| Head accessories | 0 / 10 | 10 | Not started |
| Hand objects | 0 / 12 | 12 | Not started |
| Front auras | 0 / 2 | 2 | Not started |
| Eyes | 0 / 24 | 24 | Not started |
| Eyebrows | 0 / 16 | 16 | Not started |
| Mouths | 0 / 12 | 12 | Not started |
| Expression marks | 0 / 8 | 8 | Not started |

The current backlog tally is **84 pending**, **0 candidate**, **0 QA-failed**, **0 approved**, and **77 registered** rows.

## Immediate next priority

Image generation was exhausted at the free-plan daily limit after the neck-accessory family was completed. No head-accessory candidates were generated. Resume with the head-accessory representative batch after image-generation capacity is available.

| Priority | Backlog IDs | Category | Intended batch |
|---:|---|---|---|
| 1 | DG-123–DG-127 | Head accessories | Gold pointed crown, large gold halo ring, green laurel wreath, black curved horns, silver winged circlet |
| 2 | DG-128–DG-132 | Head accessories | Silver ornate tiara, silver drop circlet, translucent white veil, pale-blue spiked tiara, gold low-profile circlet |
| 3 | DG-133–DG-144 | Hand objects | Generate only in exact pose-compatible sub-batches; respect every dependency in the backlog |
| 4 | DG-145–DG-146 | Front auras | Complete after foreground layering and rear-effect stress review |
| 5 | DG-055–DG-114 | Facial traits | Eyes, eyebrows, mouths, then expression marks in reviewable batches |

The exact descriptions, canonical filenames, reference-sheet cells, dependencies, and prompt references are in `docs/trait-production-backlog.md`. Do not invent additional backlog rows.

## Required workflow for every remaining asset or compatible batch

1. Read the applicable locked category prompt in `prompts/`, together with `prompts/00_locked_master_specification.md` and `prompts/01_universal_avoid_block.md`. Preserve the 1254 × 1254 RGBA canvas, shared rig coordinates, premium anime-chibi fantasy style, upper-left lighting, and transparent modular-layer role.
2. Generate one isolated source asset per backlog row. Never generate a full character, scene, product sheet, or multiple variants in one output. Generator-native 1920 × 1920 RGBA sources are acceptable only through the controlled transform route.
3. Preserve accepted raw generator bytes in `images/trait_candidates/<category>/` as immutable evidence. Retain rejected sources when they document a material design or placement rejection.
4. Normalize only with `scripts/normalize_generator_source.py`. Never upscale, crop meaningful art, repaint through code, or use a generic background-removal shortcut. Use an absolute source path and retain the transform provenance report.
5. Run `scripts/rig_gate_report.py` on every normalized candidate. Use `--trait --max-width-ratio 1.35` for ordinary partial layers, `--floor-aura` only for floor effects, and the documented category-specific mode where applicable.
6. Run `scripts/bulk_intake.py` without registration to create the provenance report, binary QA result, base composite, and batch review sheet. Use absolute paths for the drop directory, report, sheet, and QA note.
7. Inspect full-context composites with compatible registered layers and at least two contrasting registered backgrounds. Reject candidates that obscure the face, collide with hands or outfits, drift from anchors, expose seams or base-body pixels, contain a presentation matte, or break the intended layer order.
8. Record the decision in `docs/oversight_visual_review_2026-08-15.md` and retain a batch-specific note under `docs/qa/`.
9. Add compatibility rules in `config/compatibility.json` only when a verified dependency or collision requires them. Register approved candidates atomically through `scripts/bulk_intake.py --register-approved <DG-IDs>`.
10. Run `python3 scripts/validate_config.py`, `python3 scripts/validate_assets.py assets`, `python3 scripts/validate_manifest_consistency.py`, `python3 scripts/report_production_status.py --check`, and `python3 scripts/generate_777.py --preflight-only`. Run `python3 -m unittest discover -s tests -v` after material policy or code changes.
11. Check `git status --short --branch`, commit each validated batch atomically, and push `main`. Include canonical assets, immutable source evidence, transform reports, intake report and review sheet, composites, review notes, manifest/backlog/ledger updates, compatibility changes, and any reusable renderer source.

## Implementation lessons preserved from prior checkpoints

- `normalize_generator_source.py` requires an absolute source argument for provenance recording.
- `bulk_intake.py` should receive absolute drop, report, sheet, and QA-note paths; relative paths can complete candidate work and then fail while printing the result path.
- The generator-source transform is strictly reduction-only. Floor-ring sources must be generated as low, wide ellipses because the normalizer enforces the ordinary lower trait bound.
- Review visual placement rather than relying only on binary success. Prior rejected designs included outfit layers with exposed base feet and organic floor rings that were too tall.
- The back-accessory and neck-accessory batches passed only after width-bound and placement adjustments through the approved normalizer. Their final canonical files are the registered bytes; source evidence and transform reports are retained in the repository.
- Do not treat image-generation quota exhaustion as a production approval or a reason to invent placeholder assets. Resume generation when capacity is available.

## Non-negotiable safeguards

- Every registered asset must be a genuine 1254 × 1254 RGBA PNG with true alpha. Never register checkerboard, matte, opaque, cropped, or presentation-background art.
- Never resample registered assets outside the documented normalization procedure, and never edit immutable generator-source evidence in place.
- Preserve compatible layer rules in `config/compatibility.json`. Add accessory or hand-object rules only when verified through visual collision or dependency testing.
- Preserve the approved premium anime-chibi fantasy language, clean linework, shared frontal orthographic geometry, modular compositing, and upper-left key lighting.
- The seven legendary assets remain separate and reserved. They are not traits and must not enter the generative manifest.
- Do not mint, publish metadata, release, or conduct on-chain actions without explicit user approval after all remaining categories are complete and launch infrastructure is verified.

## Completion condition

The production task is complete only when all 160 backlog rows are registered or explicitly resolved through a documented user-approved policy change, all 16 categories are production complete, the generator produces 770 valid generative tokens under every compatibility rule, the seven legendary pieces remain reserved, validators and regression suites pass, launch infrastructure is verified, and the user explicitly approves the mint/release plan.

## Current handover metadata

- Handover date: 2026-08-15
- Repository: `DOGECOIN87/Demigods`
- Branch: `main`
- Commit: `a397f2d`
- Working tree at handover creation: clean
- On-chain actions performed in this continuation: none
