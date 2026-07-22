# Demigods Production Status

Last updated: 2026-07-22

## Current phase

**Phase 1 — Base body and approved pose variants**

Production order remains locked. No later character-aligned category may be treated as production-ready until Pose 001 is manually approved and the pose family is normalized against it.

Tracked gate: [Issue #4 — Approve and promote the 1254 × 1254 Pose 001 master](https://github.com/DOGECOIN87/Demigods/issues/4)

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
- Canonical canvas revised to 1254 × 1254 with proportional rig migration and matching validator, generator, output, test, documentation, and prompt updates

## Active production gate

The former resolution blocker is removed. `images/pose_candidates/base_pose_001_relaxed_open_candidate.png` is already a complete 1254 × 1254 RGBA PNG with genuine transparency and now satisfies the canonical canvas requirement.

It is not yet a production asset. Required next review:

- exact approved identity and proportions
- proportional 1254 rig placement and common hand anchors
- knee-length opaque training-uniform clothing
- anatomy, upper-left lighting, isolation, and foot-baseline review
- explicit human approval before copying into `assets/base_bodies/`
- exact SHA-256 registration only after approval

See `docs/qa/canvas_standard_revision_1254.md`.

## Non-production pose candidates

Five regenerated RGBA pose candidates are preserved under `images/pose_candidates/`. Image 1 from the supplied pose references was selected as the visual basis for the relaxed-open candidate; the remaining candidates cover both vertical grips, viewer-left palm-up, and centered two-hand grip.

These files use the canonical canvas but remain **unapproved candidates**:

- all five completely decode as native 1254 × 1254 RGBA PNGs with genuine alpha
- none is registered in `assets/asset_manifest.json`
- none is discoverable by the collection generator
- poses 002–005 must be reconciled to the approved Pose 001 body, scale, and foot baseline
- pose 003 still requires viewer-right grip-anchor normalization

Their hashes and detailed QA status are recorded in `images/pose_candidates/README.md`.

If Pose 001 requires correction after manual QA, the controlled image request is documented in `prompts/16_native_1254_pose_001_candidate.md`. It requires a native 1254 × 1254 output and keeps the result outside the production registry until binary and manual QA both pass.

Prompt 16 generation attempt 001 and source gate audit 002 are retained as historical records of the former canvas rule. Their dimension conclusions are superseded by the 2026-07-22 canvas decision; their manual QA observations remain review inputs. See `docs/qa/base_pose_001_native_generation_attempt_001.md` and `docs/qa/base_pose_001_source_gate_audit_002.md`.

## Current production gate

| Asset | Canonical path | State | Next action |
|---|---|---|---|
| Approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | Manual approval pending | Determine whether the existing Pose 001 candidate qualifies as the shared neutral master. |
| Relaxed-open pose | `assets/base_bodies/base_pose_001_relaxed_open.png` | Canvas-compliant candidate | Complete manual QA; correct only if required, then explicitly approve and promote. |
| Viewer-left vertical grip | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | Canvas-compliant candidate | Normalize against the final approved Pose 001 master. |
| Viewer-right vertical grip | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | Candidate reference only | Normalize grip height against pose 002 after the master is approved. |
| Viewer-left palm-up | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |
| Centered two-hand grip | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |

## Background candidate intake

Eight distinct user-supplied 1024 × 1024 RGB JPEGs are preserved byte-for-byte under `images/background_candidates/` as the approved visual directions for backgrounds 001–008. Re-uploaded palace and crescent duplicates were excluded by SHA-256. The manifest records each original attachment filename, byte count, dimensions, mode, format, preservation state, intended production path, and exact digest.

They are not registered production backgrounds because the canonical output contract requires native 1254 × 1254 full-bleed opaque PNGs. No JPEG was resized or converted. Exact source SHA-256 values, intended production paths, and the sequential native-generation prompt are recorded in `images/background_candidates/README.md` and `prompts/17_native_1254_backgrounds.md`.

## Verification state

- Asset validator tests: **10 passed**
- Exact-777 generator tests: **5 passed**
- Configuration preflight tests: **6 passed**
- Output-verification tests: **6 passed**
- Manifest-consistency tests: **6 passed**
- Combined regression total: **33 passed**
- Native 1254 pose-candidate binary QA: **5 of 5 passed**; each retains a missing-ICC-profile warning for manual sRGB confirmation
- Pose 001 intake: **passed binary QA** with SHA-256 `f34f1306918710a499ba0d5e5595a98c6d157e1243f3717058aa6b3281bd2082`
- Latest completed GitHub Actions baseline: **passed — Production validation run #25**
- Production asset library: **empty pending Pose 001 manual approval**

## Next production sequence

1. Run binary intake on the existing 1254 × 1254 Pose 001 candidate without `--register`.
2. Complete manual identity, rig, clothing, anatomy, lighting, isolation, and baseline QA.
3. Correct only failed visual requirements, then repeat binary and manual QA.
4. After explicit approval, promote Pose 001 and determine whether it also qualifies as `base_body_001_neutral_master.png`.
5. Record exact SHA-256 values and dimensions in `registered_production_assets`, then run manifest consistency validation.
6. Normalize and approve poses 002–005 sequentially against Pose 001.
7. Run configuration, asset, manifest, generator, and output verification at their corresponding production gates.

## Repository update policy

Progress is committed in small, auditable checkpoints. Each checkpoint must state:

- files added or changed
- QA performed
- validation result
- unresolved blocker
- next production asset

No prompt, placeholder, low-resolution preview, damaged binary, or contact sheet may be counted as a completed production asset.
