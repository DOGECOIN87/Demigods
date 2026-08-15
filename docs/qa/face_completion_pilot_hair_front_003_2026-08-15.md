# QA — Face-completion pilot: hair-front 003

**Date:** 2026-08-15
**Backlog ID:** DG-117
**Candidate:** `incoming/face_completion_pilot/hair_front_003_silver_straight_bangs.png`
**Source:** `images/trait_candidates/hair_front/hair_front_003_silver_straight_bangs_candidate_attempt_001.png`
**Intended production path:** `assets/hair_front/hair_front_003_silver_straight_bangs.png`

## Result

**Automated intake passed; human art-direction review rejected; asset remains unregistered.**

This is the first candidate processed under `docs/workflows/generator_source_transform.md`. The immutable 1920 × 1920 RGBA generator source was converted into a 1254 × 1254 RGBA review candidate through a recorded alpha-haze cleanup, transparent-margin crop, premultiplied LANCZOS reduction at scale `0.50880626`, and placement centered at X 627 with top Y 132. The normalized output passed complete decode, PNG, RGBA, genuine-alpha, locked-canvas, bounds, width-ratio, and transform-provenance checks.

| Gate | Result | Evidence |
|---|---|---|
| Source provenance | Pass | Source SHA-256 `a2e4e9e…f92e`; sidecar validates source and output hashes |
| Final canvas and alpha | Pass | 1254 × 1254 RGBA, `alpha_min=0`, `alpha_max=255` |
| Trait bounds and scale | Pass | `[367,132,886,697]`; width ratio 1.17x, below 1.35x ceiling |
| Base-body composite | Pass mechanically | `docs/qa/composites/hair_front_003_over_base.png` |
| Full-context art review | Reject | `docs/qa/face_completion_pilot_hair_front_003_full_context.png` |

The full-context review found that the fringe covered the eye line and most of the face, the side silhouette was too large relative to the registered rear-hair family, the seam to the rear hair was not clean, and green residual artifacts remained visible near several strand boundaries. Registration would therefore produce face-obscuring modular characters and is refused.

## Policy Validation

The candidate demonstrates that the new workflow can preserve source provenance, perform reduction-only normalization, produce a fully compliant final-canvas candidate, and retain all existing automated gates. It does not demonstrate acceptable art direction. The next DG-117 source must depict a shorter silver fringe that stops above the eye line and is designed against the paired rear-hair silhouette.
