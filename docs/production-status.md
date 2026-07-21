# Demigods Production Status

Last updated: 2026-07-20

This file is the repository-level production ledger. Update it whenever an asset, validation gate, compatibility rule, generator milestone, or blocker changes.

## Current phase

**Phase 1 — Base body and approved pose variants**

Overall state: **BLOCKED ON SOURCE RECOVERY**

Tracked blocker: [Issue #4 — Restore intact approved 2048×2048 base avatar source](https://github.com/DOGECOIN87/Demigods/issues/4)

## Completed repository work

- Locked master rig coordinates and canvas specification.
- Locked lighting, camera, naming, export, and layer-order rules.
- Inspected the approved repository WebP and historical upload chunks.
- Documented the binary-integrity failure in `docs/qa/base_body_001_integrity_report.md`.
- Marked the approved visual reference as non-production-ready in `assets/asset_manifest.json`.
- Standardized production base bodies and pose variants under `assets/base_bodies/`.
- Added a live blocker issue and canonical production ledger.
- Hardened `scripts/validate_assets.py` with complete binary decoding, PNG-only production enforcement, alpha rules, bounds checks, category-aware naming, SHA-256 reporting, and manifest validation.
- Hardened `scripts/generate_777.py` with library preflight, PNG-only discovery, deterministic dry runs, combination-capacity checks, stale-output protection, exact output-count verification, duplicate-signature rejection, and trait/image provenance hashes.
- Added 12 automated validator and generator tests.
- Added `.github/workflows/validate-repository.yml` for continuous JSON, Python, test, asset, and manifest validation.
- Updated metadata schema, repository README, production workflow, and asset-directory documentation.

## Current production gate

| Asset | Intended path | State | Next action |
|---|---|---|---|
| Approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | Blocked | Restore the intact locked 2048 × 2048 RGBA source. |
| Relaxed-open pose | `assets/base_bodies/base_pose_001_relaxed_open.png` | Blocked | Inspect the restored neutral master; register the same artwork only if both hands are already relaxed and open. |
| Viewer-left vertical grip | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | Waiting | Begin only after pose 001 is approved. |
| Viewer-right vertical grip | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | Waiting | Begin only after pose 002 is approved. |
| Viewer-left palm-up | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | Waiting | Begin only after pose 003 is approved. |
| Centered two-hand grip | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | Waiting | Begin only after pose 004 is approved. |

## Canonical production directories

All production-ready base bodies and pose variants belong in `assets/base_bodies/`. The singular `assets/base_body/` directory contains source-reference documentation only and must not be scanned as an approved production layer.

## Infrastructure verification state

- Local synthetic validator tests: **7 passed**.
- Local synthetic generator tests: **5 passed**.
- Continuous repository workflow: **pending branch/PR execution**.
- Production asset validation: **empty library permitted only while Issue #4 remains open**.

## Next safe repository work

1. Run and verify the new continuous validation workflow.
2. Merge the production-hardening checkpoint to `main` after CI passes.
3. Restore the intact approved master source under Issue #4.
4. Validate and register `base_body_001_neutral_master.png`.
5. Determine and register or produce `base_pose_001_relaxed_open.png`.

## Pause rule

Do not generate, upscale, reconstruct, or approximate any character-aligned artwork until the intact approved source passes binary, dimensional, alpha, anchor, anatomy, and visual QA.
