# QA — Face-completion pilot: hair-front 003 attempt 005

**Date:** 2026-08-15
**Backlog ID:** DG-117
**Registered asset:** `assets/hair_front/hair_front_003_silver_straight_bangs.png`
**Immutable generator source:** `images/trait_candidates/hair_front/hair_front_003_silver_straight_bangs_candidate_attempt_005.png`
**Registration route:** `scripts/normalize_generator_source.py` → `scripts/bulk_intake.py --register-approved DG-117`

## Approval

**Approved and registered.** The candidate is the first production trait promoted under the generator-source transformation workflow. It passed automated transform-provenance, binary, alpha, locked-canvas, bounds, width-ratio, and base-body composite gates, then passed human art-direction review in the full registered context.

| Check | Result | Evidence |
|---|---|---|
| Immutable source | Pass | RGBA 1920 × 1920 source; SHA-256 is recorded in the manifest provenance |
| Controlled transform | Pass | Alpha cleanup threshold 120, transparent-margin crop, premultiplied LANCZOS reduction only, centered locked-rig placement |
| Final asset | Pass | 1254 × 1254 RGBA PNG with genuine transparent alpha |
| Rig gate | Pass | Bounds `[417,132,836,618]`; width ratio 0.95x, below the 1.35x hair-front ceiling |
| Intake provenance | Pass | Source and normalized-output digests verified before promotion |
| Human art review | Pass | Eyes, eyebrows, nose, and mouth remain visible; front layer blends credibly into the registered silver rear hair |
| Compatibility | Pass | Registration added `hair_front_003_silver_straight_bangs.png → hair_back_003_silver_long_wavy.png` |

## Visual review

The revised short fringe keeps the facial focal area visible while supplying a clear silver hair silhouette. Its controlled scale and thin temple strands integrate with the registered rear-hair layer rather than creating the oversized, face-covering helmet form rejected in the earlier pilot. The full-context review is preserved at `docs/qa/face_completion_pilot_hair_front_003_attempt_005_full_context.png`; the automated intake report is `docs/qa/face_completion_pilot_hair_front_003_attempt_005_report.json`.
