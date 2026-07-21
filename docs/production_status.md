# Demigods Production Status

Last updated: 2026-07-20

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
- Thirteen local validator and generator regression tests passing
- Expanded GitHub Actions production-validation gate

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

## Current production gate

| Asset | Canonical path | State | Next action |
|---|---|---|---|
| Approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | Blocked | Restore and validate the intact locked source. |
| Relaxed-open pose | `assets/base_bodies/base_pose_001_relaxed_open.png` | Blocked | Determine whether the restored neutral master already qualifies. |
| Viewer-left vertical grip | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | Waiting | Begin only after pose 001 approval. |
| Viewer-right vertical grip | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | Waiting | Begin only after pose 002 approval. |
| Viewer-left palm-up | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | Waiting | Begin only after pose 003 approval. |
| Centered two-hand grip | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | Waiting | Begin only after pose 004 approval. |

## Verification state

- Local validator tests: **8 passed**
- Local generator tests: **5 passed**
- Combined local regression total: **13 passed**
- Branch continuous integration: **pending PR execution**
- Production asset library: **empty by design while Issue #4 remains open**

## Next production sequence

1. Run and verify continuous integration for the hardening branch.
2. Merge the verified infrastructure checkpoint into `main`.
3. Intake and validate the intact approved master PNG.
4. Register `assets/base_bodies/base_body_001_neutral_master.png` without redesigning it.
5. Determine whether the same artwork satisfies `base_pose_001_relaxed_open.png`.
6. Register the shared artwork or create only the required arm/hand correction.
7. Complete poses 002–005 sequentially.
8. Run full asset validation and update the manifest after each accepted file.

## Repository update policy

Progress is committed in small, auditable checkpoints. Each checkpoint must state:

- files added or changed
- QA performed
- validation result
- unresolved blocker
- next production asset

No prompt, placeholder, low-resolution preview, damaged binary, or contact sheet may be counted as a completed production asset.
