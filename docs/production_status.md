# Demigods Production Status

Last updated: 2026-07-21

## Current phase

**Phase 1 — Base body and approved pose variants**

Production order remains locked. No later character-aligned category may be treated as production-ready until the approved base source is restored and the pose family is completed.

Tracked blocker: [Issue #4 — Restore intact approved 2048 × 2048 base avatar source](https://github.com/DOGECOIN87/Demigods/issues/4)

## Completed repository foundations

- Locked master canvas, anchors, lighting, layer order, naming, and export rules
- Compatibility configuration and metadata schema
- Prompt and reference-sheet libraries
- Approved visual design documentation
- Binary-integrity investigation and QA report
- Non-destructive approved-source intake script and workflow
- Canonical production paths under `assets/base_bodies/`
- Manifest-level production-directory and blocker tracking
- Layer-aware PNG validation with complete decode verification, category/path checks, three-digit numbering, SHA-256 reporting, and manifest auditing
- Exact-777 generator preflight, deterministic dry run, capacity checks, stale-output protection, duplicate rejection, exact count verification, and trait/image provenance hashes
- Production-hardening PR #8 merged into `main` as `0bbfc05dc0700bcaaf878d6a20e16051c160d83c`
- Locked collection and compatibility preflight with six passing tests
- Configuration-preflight PR #9 merged into `main` as `570d64f30521e7d393d32060d0916d177c444eb7`
- Independent generated-output verifier added with six passing tamper-detection tests
- Final acceptance workflow documented for dry-run and rendered output verification
- Output-verification GitHub Actions run #25 completed successfully
- Registered-production-asset manifest consistency checker with SHA-256, dimensions, status, path/category, and binary QA verification

## Active blocker

`base_body_001_neutral_master.png` and `base_pose_001_relaxed_open.png` are blocked because the current approved WebP is damaged and the historical upload chunks are incomplete.

Required input:

- exact approved avatar artwork
- 2048 × 2048 pixels
- RGBA PNG
- genuine transparent background
- full uncropped avatar
- locked placement, lighting, outfit, and proportions

See `docs/qa/base_body_001_integrity_report.md`.

## Non-production pose candidates

Five regenerated RGBA pose candidates are preserved under `images/pose_candidates/`. Image 1 from the supplied pose references was selected as the visual basis for the relaxed-open candidate; the remaining candidates cover both vertical grips, viewer-left palm-up, and centered two-hand grip.

These files are explicitly **not production assets**:

- all are 1254 × 1254 instead of the locked 2048 × 2048 canvas
- none is registered in `assets/asset_manifest.json`
- none is discoverable by the collection generator
- pose 003 still requires viewer-right grip-anchor normalization

Their hashes and detailed QA status are recorded in `images/pose_candidates/README.md`.

The next controlled image request is documented in `prompts/16_native_2048_pose_001_candidate.md`. It permits one native 2048 × 2048 relaxed-open review candidate, explicitly forbids resizing the 1254 × 1254 references, and keeps the result outside the production registry until binary and manual QA both pass. This contingency does not supersede the preferred intact-source intake path or close Issue #4.

Prompt 16 generation attempt 001 was stopped by its hard gate: the image service returned a 1254 × 1254 RGB PNG without alpha rather than a native 2048 × 2048 RGBA source. The intermediate was not resized, alpha-extracted, committed, or registered. See `docs/qa/base_pose_001_native_generation_attempt_001.md` for the binary and rig findings.

## Current production gate

| Asset | Canonical path | State | Next action |
|---|---|---|---|
| Approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | Blocked | Restore and validate the intact locked source. |
| Relaxed-open pose | `assets/base_bodies/base_pose_001_relaxed_open.png` | Candidate reference only | Reproduce the selected candidate as a true rig-aligned 2048 × 2048 source. |
| Viewer-left vertical grip | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |
| Viewer-right vertical grip | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | Candidate reference only | Normalize grip height against pose 002 after the master is approved. |
| Viewer-left palm-up | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |
| Centered two-hand grip | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |

## Verification state

- Asset validator tests: **8 passed**
- Exact-777 generator tests: **5 passed**
- Configuration preflight tests: **6 passed**
- Output-verification tests: **6 passed**
- Manifest-consistency tests: **6 passed**
- Combined regression total: **31 passed**
- Latest completed GitHub Actions baseline: **passed — Production validation run #25**
- Production asset library: **empty by design while Issue #4 remains open**

## Next production sequence

1. Intake and validate the intact approved master PNG.
2. Register `assets/base_bodies/base_body_001_neutral_master.png` without redesigning it.
3. Record its exact file hash and dimensions in `registered_production_assets`, then run the manifest consistency checker.
4. Determine whether the same artwork satisfies `base_pose_001_relaxed_open.png`.
5. Register the shared artwork or create only the required arm/hand correction.
6. Complete poses 002–005 sequentially.
7. Run configuration, asset, manifest, generator, and output verification at their corresponding production gates.

## Repository update policy

Progress is committed in small, auditable checkpoints. Each checkpoint must state:

- files added or changed
- QA performed
- validation result
- unresolved blocker
- next production asset

No prompt, placeholder, low-resolution preview, damaged binary, or contact sheet may be counted as a completed production asset.
