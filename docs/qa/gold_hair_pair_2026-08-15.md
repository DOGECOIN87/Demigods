# QA — Gold hair pair: DG-029 and DG-115

**Date:** 2026-08-15
**Registered rear hair:** `assets/hair_back/hair_back_001_gold_long_wavy.png`
**Registered front hair:** `assets/hair_front/hair_front_001_gold_parted_bangs.png`
**Immutable source evidence:**

- `images/trait_candidates/hair_back/hair_back_001_gold_long_wavy_candidate_attempt_001.png`
- `images/trait_candidates/hair_front/hair_front_001_gold_parted_bangs_candidate_attempt_001.png`

## Approval

**Approved and registered as a matched modular pair.** Both candidates passed transform-provenance, binary, alpha, locked-canvas, bounds, and hair width-ratio gates. The full-context composite confirmed a coherent honey-gold palette, aligned crown overlap, clear face opening, and a balanced long-wavy silhouette behind the shoulders.

| Asset | Backlog ID | Final bounds | Width ratio | Disposition |
|---|---:|---|---:|---|
| Gold long wavy rear hair | DG-029 | `[362,132,891,740]` | 1.20x | Registered |
| Gold parted bangs | DG-115 | `[417,132,836,470]` | 0.95x | Registered |

The front asset requires the matching rear asset through `config/compatibility.json`. This prevents detached bangs and maintains the intended full hairstyle. Both final assets were produced using `scripts/normalize_generator_source.py` with a reduction-only transform and entered the asset library through `scripts/bulk_intake.py --register-approved`.

## Visual evidence

- Automated intake sheet: `docs/qa/gold_hair_pair_review.png`
- Full-context composite: `docs/qa/gold_hair_pair_full_context.png`
- Intake and provenance report: `docs/qa/gold_hair_pair_report.json`

The full-context review confirms the eyes, eyebrows, nose, and mouth remain visible; there is no unacceptable matte, crop, seam, layer-order, or color-family mismatch at the review scale.
