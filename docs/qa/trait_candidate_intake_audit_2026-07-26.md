# Trait Candidate Intake Audit — 2026-07-26

## Scope

This checkpoint audits the loose files added directly under `images/trait_candidates/` by the two latest upload commits:

- `d06095ac09f51d0e788a7bfe34f441481d6f0895`
- `8e0d2934d06dd468c491eab86d619eef08d8ee7b`

The audit is intentionally non-destructive. No candidate is moved into `assets/`, registered in `assets/asset_manifest.json`, assigned a final production name, or counted as a completed production asset without binary QA, visual classification, provenance, dependency composites, and explicit human approval.

## Repository authority

Candidate intake follows:

- `prompts/19_individual_trait_asset_co_creation.md`
- `images/trait_candidates/README.md`
- `docs/trait-production-backlog.md`
- `docs/production_status.md`

Character-compatible candidates must ultimately be native 1254 × 1254 sRGB RGBA PNGs with genuine transparent alpha, one isolated category asset per file, full-canvas coordinates, no baked body or unrelated traits, and no resizing or resampling used to satisfy the canvas contract.

## Loose-upload inventory

### Commit `d06095ac09f51d0e788a7bfe34f441481d6f0895`

1. `images/trait_candidates/8yp7w (1).jpg`
2. `images/trait_candidates/Ak80y (1).jpg`
3. `images/trait_candidates/Ey6VY.jpg`
4. `images/trait_candidates/KDPWv.jpg`
5. `images/trait_candidates/TthCB.jpg`
6. `images/trait_candidates/dcUdT.jpg`
7. `images/trait_candidates/iscDz.jpg`
8. `images/trait_candidates/oI8Ej.jpg`
9. `images/trait_candidates/pngL4 (1).jpg`

### Commit `8e0d2934d06dd468c491eab86d619eef08d8ee7b`

10. `images/trait_candidates/2Zy4o.jpg`
11. `images/trait_candidates/Gucuc.jpg`
12. `images/trait_candidates/PoLVl.jpg`
13. `images/trait_candidates/grok_1784755724820.png`
14. `images/trait_candidates/grok_1784757226345.png`
15. `images/trait_candidates/s1sqd.jpg`

## Intake result

| Files | Current state | Production decision |
|---|---|---|
| 13 JPEG files | Untriaged source/candidate uploads | Blocked. JPEG cannot satisfy the required transparent modular-layer contract for character traits. Preserve as reference-only until visual classification identifies a repository-supported design and source cell. |
| 2 PNG files | Untriaged candidate uploads | Blocked pending complete decode, exact dimensions, color mode, alpha behavior, visible-bounds, source-provenance, category-isolation, rig-overlay, and visual review. PNG extension alone is not approval evidence. |

None of the fifteen files currently has enough recorded information to assign a backlog ID, canonical category, canonical production filename, pose dependency, source-reference cell, or production status beyond `candidate/untriaged`.

## Required classification fields

For each file, record all of the following before relocation or canonical naming:

```text
TEMPORARY FILE:
SHA-256:
DIMENSIONS:
FORMAT AND MODE:
ALPHA STATE:
VISIBLE BOUNDS:
PROPOSED CANONICAL CATEGORY:
SUPPORTED VISUAL DESCRIPTION:
SOURCE REFERENCE PATH:
SOURCE REFERENCE CELL OR REGION:
POSE / COMPATIBILITY DEPENDENCY:
PROPOSED BACKLOG ID:
PROPOSED CANDIDATE PATH:
BINARY QA RESULT:
ISOLATION RESULT:
RIG / LANDMARK RESULT:
COMPOSITE RESULT:
HUMAN VISUAL DECISION:
```

## Decision rules

### Preserve as reference-only

Use this decision when a file is a JPEG, flattened character, contact sheet, presentation card, background, multi-asset composition, low-resolution crop, or otherwise cannot function as a modular transparent layer. A recognizable design may still support a fresh native render using `prompts/19_individual_trait_asset_co_creation.md`.

### Reject as unsupported

Use this decision when the design cannot be tied to a dedicated repository catalog, prompt, preserved source, or identifiable backlog entry. Do not invent a new named character, trait, or category to accommodate an upload.

### Retain as review candidate

Use this decision only when the file fully decodes, is natively 1254 × 1254, follows the category RGB/RGBA contract, contains exactly one isolated supported asset, and has enough provenance to assign a category and intended dependency. Retention is not production approval.

### Promote to production

Promotion remains prohibited until the candidate passes binary validation, source-provenance review, locked-rig overlay, dependency composite, neighboring-layer stress test, explicit human approval, canonical naming, exact SHA-256 registration, manifest consistency, and the full repository validation suite.

## QA performed in this checkpoint

- Confirmed the two source commits and their exact changed-file inventories.
- Confirmed all fifteen uploads are outside `assets/` and therefore not registered production assets.
- Confirmed thirteen files use JPEG and cannot directly satisfy transparent character-trait requirements.
- Confirmed two files require binary and visual inspection before any category claim.
- Confirmed no production manifest modification is justified.
- Confirmed no loose upload may be represented as a finished generation sheet or production-complete asset.

## Unresolved blocker

The connector exposes repository paths and commit metadata but does not expose reliable decoded pixel inspection for these binary uploads in this audit. Therefore their visual category, dimensions, alpha state, visible bounds, and source-cell provenance remain unresolved. Guessing would violate the repository policy.

## Next production asset

The next unblocked creation task remains a repository-supported isolated trait candidate generated with `prompts/19_individual_trait_asset_co_creation.md`, while Pose 001 remains the character registration gate. The next background gate remains explicit human approval of Background 004 attempt 003, followed by native Background 005 production.
