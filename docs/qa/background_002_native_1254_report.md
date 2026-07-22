# Background 002 Native 1254 QA Report

Date: 2026-07-22

## Asset

- Backlog ID: `DG-008`
- Category: `backgrounds`
- Source reference: `images/background_candidates/background_002_violet_gothic_sanctum_reference.jpg`
- Source SHA-256: `ed6a2f8893e6d5b53e9bccec21daa2dafd06a469b8c4621d759cbfeabef6dfde`
- Current candidate: `images/background_candidates/native_candidates/background_002_violet_gothic_sanctum_candidate.png`
- Production path: `assets/backgrounds/background_002_violet_gothic_sanctum.png`
- Current candidate SHA-256: `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc`
- Production SHA-256: `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc`
- Prompt: `prompts/17_native_1254_backgrounds.md`, Background 002

## Candidate history

| Attempt | SHA-256 | Binary result | Manual result |
|---|---|---|---|
| 001 | `7ef25fa04d6430b5e1a7ca688cc5755f28df5c4b9da6ec5d80d12507a1f0d2b0` | Pass | Reject — several central altar pinnacles end in explicit cross-shaped finials, violating the symbol-removal requirement. |
| 002 | `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc` | Pass | Approved — repository manual QA passed and the user replied “Continue” directly to the explicit approval request after reviewing the displayed candidate. |

Attempt 002 was generated again from the exact preserved JPEG. It was not derived from, patched with, or postprocessed from attempt 001.

## Attempt 002 binary QA

| Check | Result |
|---|---|
| Complete PNG decode | Pass |
| Native dimensions | Pass — 1254 × 1254 |
| Mode | Pass — RGB |
| Full-canvas opacity | Pass |
| Filename/category | Pass |
| SHA-256 | Pass — `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc` |
| Source-reference integrity | Pass — source SHA-256 remains `ed6a2f8893e6d5b53e9bccec21daa2dafd06a469b8c4621d759cbfeabef6dfde` |
| Embedded ICC profile | Warning — absent; decoded colorspace confirmed as RGB/sRGB interpretation |

## Attempt 002 manual QA

- Preserves the source's symmetrical towering gothic nave, violet stained glass, dark stone columns, candlelit central altar, checkered floor, solemn mood, and deep architectural perspective.
- Replaces the source's statues and religious ornament with empty stone bays, leaf-bud finials, floral glass, and nonlinguistic geometric detail.
- Contains no character, creature, face, silhouette, readable letter, word, number, rune, caption, watermark, signature, UI, frame, or contact-sheet layout.
- Keeps the central floor corridor symmetrical and compositionally readable for a front-facing avatar.
- Lighting reads strongest from the upper-left stained glass with restrained candle warmth and darker lower-right architectural forms.
- Fills the canvas edge-to-edge without transparent pixels or borders.

## Decision

**Approved and registered.** The production file is byte-identical to approved attempt 002. Background 003 is the next independent background asset while Pose 001 remains unresolved.
