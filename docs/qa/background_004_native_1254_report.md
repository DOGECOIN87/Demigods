# Background 004 Native 1254 QA Report

Date: 2026-07-22

## Asset

- Backlog ID: `DG-010`
- Category: `backgrounds`
- Source reference: `images/background_candidates/background_004_crescent_star_dreamscape_reference.jpg`
- Source SHA-256: `7ef8cedff521095601e1225f6ad87f8024930c05d9e458dda138e92ae16c6d3e`
- Current candidate: `images/background_candidates/native_candidates/background_004_crescent_star_dreamscape_candidate.png`
- Intended production path: `assets/backgrounds/background_004_crescent_star_dreamscape.png`
- Current candidate SHA-256: `e2e2f183c4c28231e36114b1c80d2844774edd682e11b1d76b9dd0e77c58c2d9`
- Prompt: `prompts/18_native_1254_background_004_candidate.md`

## Candidate history

| Attempt | SHA-256 | Binary result | Manual result |
|---|---|---|---|
| 001 | `0ce22870e010f729a3a8819035f1deef072476a0e47729d2632c4d79547b08f5` | Pass | Reject — the platform surface sits substantially above the locked foot baseline, so a character ending at Y 1139 would appear below it. |
| 002 | `702f8f7c5f5dee986bcb3bc66ec3f63006ff0730c4c641d86f1d9078e28f784d` | Pass | Reject — the rig overlay places `[627,1139]` below the gold front rim on the platform's vertical fascia. |
| 003 | `e2e2f183c4c28231e36114b1c80d2844774edd682e11b1d76b9dd0e77c58c2d9` | Pass | Repository manual and coordinate-overlay QA pass; explicit human visual approval pending. |

Every attempt was rendered independently from the exact preserved JPEG. No failed image was resized, patched, extended, or used as the source of another attempt.

## Attempt 003 binary QA

| Check | Result |
|---|---|
| Complete PNG decode | Pass |
| Native dimensions | Pass — 1254 × 1254 |
| Mode | Pass — RGB |
| Full-canvas opacity | Pass |
| Filename/category | Pass |
| SHA-256 | Pass — `e2e2f183c4c28231e36114b1c80d2844774edd682e11b1d76b9dd0e77c58c2d9` |
| Source-reference integrity | Pass — source SHA-256 remains `7ef8cedff521095601e1225f6ad87f8024930c05d9e458dda138e92ae16c6d3e` |
| Embedded ICC profile | Warning — absent; decoded colorspace confirmed as RGB/sRGB interpretation |

## Attempt 003 manual and rig-composition QA

- Preserves the source's navy-violet dreamscape, layered lavender and warm-cream clouds, single luminous crescent, hanging gold stars, centered celestial platform, and whimsical fantasy mood.
- The Y 1139 coordinate overlay crosses the flat platform walking surface at X 627, above the outer rim; the maximum character-width box remains supported by the platform.
- Keeps clouds behind and outside the central character corridor while preserving readable contrast around the locked head, torso, hand, and foot regions.
- Platform detail uses circles, dots, radial lines, diamonds, and starbursts without readable letters, numbers, runes, pseudo-writing, compass marks, or typographic symbols.
- Contains no character, person, face, creature, humanoid silhouette, statue, UI, frame, caption, watermark, signature, contact sheet, unrelated environment, extra moon, or portal.
- Upper-left gold-white highlights and lower-right cloud/platform shadows remain coherent.
- Fills the canvas edge-to-edge without transparent pixels or borders.

## Decision

**Candidate — not registered.** Attempt 003 passes automated, coordinate-overlay, and repository manual QA but requires explicit human visual approval before it may be copied to production or added to `registered_production_assets`.
