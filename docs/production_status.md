# Demigods Production Status

Last updated: 2026-07-22

## Current phase

**Phase 1 — Base-pose correction plus independent background production**

Production registration order remains locked. Candidate creation is now open across referenced categories and may be batched or performed before Pose 001 approval. No character-aligned candidate may be treated as production-ready until its required pose composite passes.

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

The former resolution blocker is removed. The original Pose 001 candidate and native attempts 002–004 are complete 1254 × 1254 RGBA PNGs with genuine transparency, but all fail one or more locked rig coordinates.

No Pose 001 attempt is a production asset. Required next correction:

- exact top-of-head Y 141, foot-baseline Y 1139, center X 627, and maximum bounds
- exact approved identity, proportions, and common hand anchors
- knee-length opaque training-uniform clothing
- anatomy, upper-left lighting, isolation, and foot-baseline review
- automated visible-geometry pass plus explicit human approval before copying into `assets/base_bodies/`
- exact SHA-256 registration only after approval

See `docs/qa/base_pose_001_rig_gate_2026-07-22.md`.

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
| Approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | Blocked by Pose 001 geometry | Evaluate only after a Pose 001 candidate passes all rig and visual gates. |
| Relaxed-open pose | `assets/base_bodies/base_pose_001_relaxed_open.png` | QA-failed; unregistered | Render another genuinely native candidate against the locked coordinate guide. |
| Viewer-left vertical grip | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | Canvas-compliant candidate | Normalize against the final approved Pose 001 master. |
| Viewer-right vertical grip | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | Candidate reference only | Normalize grip height against pose 002 after the master is approved. |
| Viewer-left palm-up | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |
| Centered two-hand grip | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | Candidate reference only | Reproduce from the final approved pose 001 master. |

## Background candidate intake

Eight distinct user-supplied 1024 × 1024 RGB JPEGs are preserved byte-for-byte under `images/background_candidates/` as the approved visual directions for backgrounds 001–008. Re-uploaded palace and crescent duplicates were excluded by SHA-256. The manifest records each original attachment filename, byte count, dimensions, mode, format, preservation state, intended production path, and exact digest.

No reference JPEG was resized or converted. Background 001 is registered with SHA-256 `2a82caf4833bc1f86f6d9ed1b7ba8a04c2344860a12b74f36f26c7cdeb4750d9`. Background 002 attempt 001 was rejected for cross-shaped altar finials; approved attempt 002 is registered with SHA-256 `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc`. Approved Background 003 attempt 001 is registered with SHA-256 `dfd632fd80b6279a35f74cb767fbdf1d5662f57bbad7f6db799d972edb9928f0`. Background 004 attempts 001 and 002 were rejected for foot-platform alignment failures; attempt 003 is a native 1254 × 1254 RGB approval candidate with SHA-256 `e2e2f183c4c28231e36114b1c80d2844774edd682e11b1d76b9dd0e77c58c2d9`. Backgrounds 005–008 remain unmodified reference-only inputs.

## Ordered trait backlog

`docs/trait-production-backlog.md` records 146 supported assets in dependency order. It inventories the base family, backgrounds 001–008, and every distinct asset identifiable in the dedicated aura, back-accessory, hair, outfit, accessory, facial-trait, and hand-object catalogs. The global-finish category is explicitly source-gated because the repository contains no identifiable finish design; no placeholder was invented.

## Verification state

- Asset validator tests: **10 passed**
- Exact-777 generator tests: **5 passed**
- Configuration preflight tests: **6 passed**
- Output-verification tests: **6 passed**
- Manifest-consistency tests: **6 passed**
- Combined regression total: **40 passed**
- Native 1254 pose-candidate binary QA: **5 of 5 passed**; each retains a missing-ICC-profile warning for manual sRGB confirmation
- Pose 001 binary decode: **passed**; locked visible-geometry intake: **failed** for the original and attempts 002–004
- Background 001 asset and manifest QA: **passed**; registered SHA-256 `2a82caf4833bc1f86f6d9ed1b7ba8a04c2344860a12b74f36f26c7cdeb4750d9`
- Background 002 attempt 001: **QA-failed** for prohibited cross-shaped altar finials; unregistered SHA-256 `7ef25fa04d6430b5e1a7ca688cc5755f28df5c4b9da6ec5d80d12507a1f0d2b0`
- Background 002 attempt 002: **passed, human-approved, and registered**; SHA-256 `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc`
- Background 003 attempt 001: **passed, human-approved, and registered**; SHA-256 `dfd632fd80b6279a35f74cb767fbdf1d5662f57bbad7f6db799d972edb9928f0`
- Background 004 attempt 001: **QA-failed** because the platform surface is substantially above foot baseline Y 1139; unregistered SHA-256 `0ce22870e010f729a3a8819035f1deef072476a0e47729d2632c4d79547b08f5`
- Background 004 attempt 002: **QA-failed** because `[627,1139]` lands on the vertical platform fascia; unregistered SHA-256 `702f8f7c5f5dee986bcb3bc66ec3f63006ff0730c4c641d86f1d9078e28f784d`
- Background 004 attempt 003: **binary, coordinate-overlay, and repository manual QA passed; human approval pending**; unregistered SHA-256 `e2e2f183c4c28231e36114b1c80d2844774edd682e11b1d76b9dd0e77c58c2d9`
- Latest completed GitHub Actions baseline: **passed — Production validation run #25**
- Production asset library: **3 registered backgrounds; 0 registered base bodies**

## Next production sequence

1. Create another genuinely native Pose 001 candidate using Prompt 16 and the locked coordinate guide; do not resample a failed attempt.
2. Require the automated visible-geometry intake gate, then manual facial, shoulder, waist, hand-anchor, clothing, anatomy, lighting, isolation, and composite QA.
3. After explicit approval, promote Pose 001 and determine whether it also qualifies as `base_body_001_neutral_master.png`.
4. Obtain explicit human visual approval for Background 004 attempt 003; register its exact bytes only after approval.
5. In parallel, use `prompts/19_individual_trait_asset_co_creation.md` to build separate prealignment candidates or batches from repository-supported references.
6. Normalize and approve poses 002–005 sequentially against Pose 001.
7. Composite representative assets from each category, correct alignment, and then register the backlog in dependency order.
8. Run configuration, asset, manifest, generator, and output verification at their corresponding production gates.

## Repository update policy

Progress is committed in small, auditable checkpoints. Each checkpoint must state:

- files added or changed
- QA performed
- validation result
- unresolved blocker
- next production asset

No prompt, placeholder, low-resolution preview, damaged binary, or contact sheet may be counted as a completed production asset.
