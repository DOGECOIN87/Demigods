# Head Accessories DG-123–DG-127 — Regenerated Batch Review

**Date:** 2026-08-15
**Category:** Head accessories
**Backlog rows:** DG-123–DG-127
**Generation revision:** regenerated with stricter central placement, wider transparent margins, explicit no-backdrop constraints, and a distinct transparent-background key. DG-124 was regenerated individually without a style-reference image after the first revised batch retained excessive backdrop noise.

## Revised processing parameters

| Candidate group | Source route | Alpha cleanup threshold | Normalization |
|---|---|---:|---|
| DG-123 | `head_accessory_001_gold_pointed_crown_regen1.png` | 32 | 520 px wide, centered X=627, top Y=129 |
| DG-124 | `head_accessory_002_large_gold_halo_regen2.png` | 32 | 520 px wide, centered X=627, top Y=129 |
| DG-125 | `head_accessory_003_green_laurel_regen1.png` | 64 | 520 px wide, centered X=627, top Y=129 |
| DG-126 | `head_accessory_004_black_curved_horns_regen1.png` | 64 | 500 px wide, centered X=627, top Y=129 |
| DG-127 | `head_accessory_005_silver_winged_circlet_regen1.png` | 80 | 520 px wide, centered X=627, top Y=129 |

Thresholds above the default were used only to clear documented low-opacity generator haze at the source perimeter; no meaningful trait pixels were cropped or repainted. The transform remained reduction-only and used `scripts/normalize_generator_source.py`.

## QA result

All five normalized candidates passed binary intake QA and the category trait rig gate. Each is a genuine 1254 × 1254 RGBA PNG with `alpha_min=0`, remains within the locked bounds, and stays below the 1.35× width ceiling. The review sheet shows the assets composited over the base master: crown, halo, laurel wreath, horns, and winged circlet are isolated and visually distinguishable, with no visible face, outfit, body, or background contamination in the reviewed composites.

| Backlog ID | Result | Normalized visible bounds | Width ratio |
|---|---|---|---:|
| DG-123 | Automated QA pass; visual review pass | `[367,129,886,488]` | 1.17× |
| DG-124 | Automated QA pass; visual review pass | `[367,129,886,654]` | 1.17× |
| DG-125 | Automated QA pass; visual review pass | `[367,129,886,570]` | 1.17× |
| DG-126 | Automated QA pass; visual review pass | `[377,129,876,579]` | 1.13× |
| DG-127 | Automated QA pass; visual review pass | `[367,129,886,406]` | 1.17× |

The candidates remain **unregistered** because the user requested regeneration and QA, not production registration. No manifest, backlog, ledger, compatibility rule, minting, metadata publication, release, or on-chain action was performed. Registration can proceed as a separate explicit production step if desired.

Evidence: `docs/qa/head_accessories_001-005_review_sheet.png`, `docs/qa/head_accessories_001-005_rig_gate.json`, `docs/qa/head_accessories_001-005_intake.json`, and the per-candidate provenance reports under `incoming/head_accessories/`.
