# Demigods Production Status

Last updated: 2026-07-20

## Current phase

**Phase 1 — Base body and approved pose variants**

Production order remains locked. No later character-aligned category may be treated as production-ready until the approved base source is restored and the pose family is completed.

## Completed repository foundations

- Locked master canvas, anchors, lighting, layer order, naming, and export rules
- Deterministic 777-token generator and metadata schema
- Compatibility configuration
- Asset manifest
- Asset validation script
- Prompt and reference-sheet libraries
- Approved visual design documentation
- Binary-integrity investigation and QA report

## Active blocker

`base_pose_001_relaxed_open.png` is blocked because the current approved WebP is damaged and the historical upload chunks are incomplete.

Required input:

- Exact approved avatar artwork
- 2048 × 2048 pixels
- RGBA PNG
- Genuine transparent background
- Full uncropped body
- Locked placement, lighting, outfit, and proportions

See `docs/qa/base_body_001_integrity_report.md`.

## Next production sequence

1. Intake and validate the intact approved master PNG.
2. Register `base_body_001_neutral_master.png` without redesigning it.
3. Determine whether the same artwork satisfies `base_pose_001_relaxed_open.png`.
4. Register the shared artwork or create only the required arm/hand correction.
5. Complete poses 002–005 sequentially.
6. Run full asset validation and update the manifest after each accepted file.

## Repository update policy

Progress is committed in small, auditable checkpoints. Each checkpoint must state:

- files added or changed
- QA performed
- validation result
- unresolved blocker
- next production asset

No prompt, placeholder, low-resolution preview, damaged binary, or contact sheet may be counted as a completed production asset.
