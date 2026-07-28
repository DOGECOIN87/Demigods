# Background 004 Native 1254 QA Report

Date: 2026-07-28

## Decision

**Regenerated, approved, and registered.** The earlier soft illustrative
version was superseded after the collection-level background review found a
style mismatch and a bright lower-body hotspot.

- Production: `assets/backgrounds/background_004_crescent_star_dreamscape.png`
- Sharp candidate: `images/background_candidates/native_candidates/background_004_crescent_star_dreamscape_candidate_attempt_004.png`
- Production SHA-256: `68c1a41a42195196f35b4f666ba1ecd9bb19d236a7dd46f8f874c9b02bb2f91d`
- Candidate SHA-256: `b68f115c89f40948521eac98da39ca5333194fa1d62c50093985a80034ab6ddd`

## QA

- Pass: complete native 1254 × 1254 RGB PNG; fully opaque and full bleed.
- Pass: sharper architectural rendering now matches Backgrounds 001–003.
- Pass: avatar composite preserves head, hand, torso, and foot readability.
- Pass: broad floor supports the locked Y 1139 foot baseline.
- Pass: no text, runes, character, UI, watermark, or foreground aura.
- Applied deterministic 2.5 px Gaussian blur and 0.22 corner vignette at
  power 2.4 using `scripts/apply_background_depth.py`.
