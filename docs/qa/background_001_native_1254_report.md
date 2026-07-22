# Background 001 Native 1254 QA Report

Date: 2026-07-22

## Asset

- Backlog ID: `DG-007`
- Category: `backgrounds`
- Source reference: `images/background_candidates/background_001_celestial_throne_hall_reference.jpg`
- Source SHA-256: `b92287aaa4fe36fd4c1b8102367a51b635c8f912d91aca9db37e91aa4c20a8e8`
- Candidate: `images/background_candidates/native_candidates/background_001_celestial_throne_hall_candidate.png`
- Production path: `assets/backgrounds/background_001_celestial_throne_hall.png`
- Production SHA-256: `2a82caf4833bc1f86f6d9ed1b7ba8a04c2344860a12b74f36f26c7cdeb4750d9`
- Prompt: `prompts/17_native_1254_backgrounds.md`, Background 001

## Binary QA

| Check | Result |
|---|---|
| Complete PNG decode | Pass |
| Native dimensions | Pass — 1254 × 1254 |
| Mode | Pass — RGB |
| Full-canvas opacity | Pass |
| Filename/category | Pass |
| Candidate and production bytes | Pass — identical SHA-256 |
| Embedded ICC profile | Warning — absent; decoded colorspace confirmed as sRGB |

## Manual QA

- Preserves the source's symmetrical white-marble columns, navy banners and drapery, gold celestial ornament, distant central throne, blue carpet, and layered palace depth.
- Removes the source's readable `N` and `X` compass letters. Remaining star/compass rosettes are nonlinguistic ornamental geometry.
- Contains no character, creature, silhouette, UI, caption, watermark, signature, contact-sheet frame, or unrelated environment.
- Maintains a clear centered avatar staging corridor and coherent architectural perspective.
- Lighting reads from the upper-left with lower-right form shadows and warm secondary illumination.
- Fills the canvas without transparent pixels or borders.

The user directed production to remove the procedural blocks after viewing the candidate. Combined with passing binary and manual review, this records the human approval needed for registration.

## Decision

**Approved and registered.** Background 002 is the next independent background asset while Pose 001 remains unresolved.
