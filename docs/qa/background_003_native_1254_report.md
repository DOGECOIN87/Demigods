# Background 003 Native 1254 QA Report

Date: 2026-07-22

## Asset

- Backlog ID: `DG-009`
- Category: `backgrounds`
- Source reference: `images/background_candidates/background_003_arcane_library_reference.jpg`
- Source SHA-256: `afc64910b8f1c44f49f33294a71f8228961025ae8a8f7f46b40def2a268e2785`
- Current candidate: `images/background_candidates/native_candidates/background_003_arcane_library_candidate.png`
- Intended production path: `assets/backgrounds/background_003_arcane_library.png`
- Current candidate SHA-256: `dfd632fd80b6279a35f74cb767fbdf1d5662f57bbad7f6db799d972edb9928f0`
- Prompt: `prompts/17_native_1254_backgrounds.md`, Background 003

## Binary QA

| Check | Result |
|---|---|
| Complete PNG decode | Pass |
| Native dimensions | Pass — 1254 × 1254 |
| Mode | Pass — RGB |
| Full-canvas opacity | Pass |
| Filename/category | Pass |
| SHA-256 | Pass — `dfd632fd80b6279a35f74cb767fbdf1d5662f57bbad7f6db799d972edb9928f0` |
| Source-reference integrity | Pass — source SHA-256 remains `afc64910b8f1c44f49f33294a71f8228961025ae8a8f7f46b40def2a268e2785` |
| Embedded ICC profile | Warning — absent; decoded colorspace confirmed as RGB/sRGB interpretation |

## Manual QA

- Preserves the source's towering dark-wood bookcases, pointed moonlit window, suspended cyan lights, layered books and desks, warm candle accents, and deep symmetrical perspective.
- Moves desks, open books, and book stacks to the outer edges, leaving the central avatar corridor and foot area unobstructed.
- Replaces the source's written floor circle with smooth concentric rings, dots, short radial ticks, and simple nonlinguistic geometry.
- Contains no readable letters, words, numbers, book titles, labels, runes, pseudo-writing, character, face, creature, silhouette, UI, frame, watermark, signature, or contact-sheet layout.
- Uses cool high-window illumination with stronger upper-left accents, restrained warm practical lights, and darker lower-right architectural forms.
- Fills the canvas edge-to-edge without transparent pixels or borders.

## Decision

**Candidate — not registered.** Attempt 001 passes automated and repository manual QA but requires explicit human visual approval before it may be copied to the production path or added to `registered_production_assets`.
