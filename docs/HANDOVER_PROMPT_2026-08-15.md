# Demigods Collection Continuation Handover Prompt

You are assuming production oversight of the **Demigods** 777-token NFT collection in the repository `DOGECOIN87/Demigods`. Continue work directly from the current `main` branch. Do not redesign the collection or loosen its quality bar.

## Published checkpoint

The branch is clean and synchronized with `origin/main` at commit `f427785` (`Register matched teal hair pair`). The collection model remains **770 generative tokens plus 7 legendary one-of-ones**.

The following seven matched hair families are now registered through the documented generator-source transformation workflow:

| Family | Rear asset | Front asset |
|---|---|---|
| Silver | `hair_back_003` | `hair_front_003` |
| Gold | `hair_back_001` | `hair_front_001` |
| Black | `hair_back_002` | `hair_front_002` |
| Violet | `hair_back_004` | `hair_front_004` |
| Blue | `hair_back_005` | `hair_front_005` |
| Pink | `hair_back_006` | `hair_front_006` |
| Teal | `hair_back_007` | `hair_front_007` |

Each front asset has a compatibility requirement binding it to its matching rear hair. Source evidence, QA review sheets, full-context composites, manifest records, generated ledger, and visual-review decisions are committed. The audited workflow is defined in `docs/workflows/generator_source_transform.md`.

## Immediate priority

Resume with the remaining red matched hair pair:

- `DG-036` — red long wavy rear hair
- `DG-122` — red front bangs

Then work through every remaining pending row in `docs/trait-production-backlog.md`, organized into logically compatible batches. Prioritize remaining hair, then outfits/accessories/aura layers, then facial traits. Do not mark an asset complete merely because it passes binary validation.

## Required workflow for every asset or compatible batch

1. Read the relevant locked prompt specification in `prompts/` and preserve existing style, rig, palette, and layer-role constraints.
2. Generate an isolated source image. Native 1254×1254 RGBA is preferred; generator-native source art is permitted only under the controlled transform policy.
3. Preserve the accepted source candidate in `images/trait_candidates/` as immutable evidence. Remove only duplicate opaque derivatives and temporary files.
4. Run `scripts/normalize_generator_source.py` with reduction-only scaling and a documented alpha threshold to create a candidate at the locked 1254×1254 rig.
5. Run `scripts/rig_gate_report.py --trait --max-width-ratio 1.35` on every candidate.
6. Run `scripts/bulk_intake.py` without registration to generate the review sheet and provenance report. Never bypass provenance-aware intake.
7. Render and visually inspect the intended layered full-context composite. Apply strict face visibility, seam, silhouette, layer-order, palette, and style-coherence review. Reject art that obscures the face unless that overlap is explicitly trait-specific, intentional, and visually readable.
8. Record the review decision in `docs/oversight_visual_review_2026-08-15.md`.
9. Register only approved assets through `scripts/bulk_intake.py --register-approved <DG-IDs>`, preserving required compatibility rules.
10. Update QA evidence, run `scripts/validate_config.py`, `scripts/validate_assets.py`, `scripts/validate_manifest_consistency.py`, `scripts/report_production_status.py --check`, and `scripts/generate_777.py --preflight-only`; run the full unit suite at material policy or code checkpoints.
11. Commit each validated batch atomically and push `main` after checking `git status --short --branch`.

## Non-negotiable safeguards

- Final registered assets must be genuine RGBA PNGs at the locked 1254×1254 canvas; no opaque checkerboard or presentation backgrounds.
- Do not resample or crop registered assets outside the documented normalization workflow.
- Keep generator-source transform provenance tamper-evident.
- Keep exact layer pairing rules in `config/compatibility.json` where front and rear hair must be matched.
- Preserve the approved visual style: premium anime-chibi fantasy, coherent upper-left lighting, clean linework, and clear modular compositing.
- Do not push unvalidated assets or perform minting, metadata publication, or any on-chain operation without explicit user authorization.

## Completion condition

The project is complete only when every backlog row is registered and every category is production complete; collection generation can produce the 770 generative tokens under all compatibility rules; the 7 legendary assets remain reserved; all validation and regression suites pass; collection metadata and launch infrastructure are verified; and the user has explicitly approved the mint/release plan.
