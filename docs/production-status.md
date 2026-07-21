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
- Added deterministic exact-777 generator and metadata schema.
- Added compatibility configuration and QA documentation.
- Inspected the approved repository WebP and historical upload chunks.
- Documented the binary-integrity failure in `docs/qa/base_body_001_integrity_report.md`.
- Marked the approved visual reference as non-production-ready in `assets/asset_manifest.json`.

## Current production gate

| Asset | Intended path | State | Next action |
|---|---|---|---|
| Approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | Blocked | Restore the intact locked 2048×2048 RGBA source. |
| Relaxed-open pose | `assets/base_bodies/base_pose_001_relaxed_open.png` | Blocked | Inspect the restored neutral master; register the same artwork only if both hands are already relaxed and open. |
| Viewer-left vertical grip | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | Waiting | Begin only after pose 001 is approved. |
| Viewer-right vertical grip | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | Waiting | Begin only after pose 002 is approved. |
| Viewer-left palm-up | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | Waiting | Begin only after pose 003 is approved. |
| Centered two-hand grip | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | Waiting | Begin only after pose 004 is approved. |

## Canonical production directories

All production-ready base bodies and pose variants belong in `assets/base_bodies/`. The singular `assets/base_body/` directory contains source-reference documentation only and must not be scanned as an approved production layer.

## Next safe repository work

While Issue #4 remains open, work may continue only on production infrastructure that does not alter or approximate the locked avatar:

1. Harden automated asset validation.
2. Align the generator, manifest, and directory naming.
3. Add preflight and dry-run checks for exact-777 generation.
4. Add repository-level validation workflow and tests.
5. Keep the manifest and this ledger synchronized after each accepted change.

## Pause rule

Do not generate, upscale, reconstruct, or approximate any character-aligned artwork until the intact approved source passes binary, dimensional, alpha, anchor, anatomy, and visual QA.
