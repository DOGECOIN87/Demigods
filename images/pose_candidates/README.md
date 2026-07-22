# Demigods Pose Candidates

These five images are transparent visual candidates for the locked base-pose family. The collection canvas was revised to their native 1254 × 1254 dimensions on 2026-07-22. Canvas compliance alone does not promote them: they remain reference material until each passes manual rig, anatomy, clothing, lighting, identity, and pose-consistency QA.

The relaxed-open image is the selected visual base for this candidate set. The other images preserve that general identity while demonstrating the required grip and palm directions.

## QA status

All five files:

- decode completely as PNG
- use RGBA mode
- contain genuine transparent and fully opaque pixels
- have transparent canvas corners
- contain one centered full-body character
- contain no prop, text, contact sheet, or baked checkerboard
- use the locked native 1254 × 1254 production canvas
- lack an embedded ICC profile

The former canvas-size failure is resolved, but Pose 001 fails the locked visible-geometry gate. Poses 002–005 must be reconciled to a future approved Pose 001 body, scale, and foot baseline; Pose 003 also keeps its viewer-right grip above the intended common waist-level anchor.

## Candidate inventory

| Pose | File | SHA-256 |
|---|---|---|
| Relaxed open | `base_pose_001_relaxed_open_candidate.png` | `f34f1306918710a499ba0d5e5595a98c6d157e1243f3717058aa6b3281bd2082` |
| Viewer-left vertical grip | `base_pose_002_viewer_left_vertical_grip_candidate.png` | `a5c26e809f12500e1f7de08a7e46f8bcbec58094ac2cf51b55f56a32cd098247` |
| Viewer-right vertical grip | `base_pose_003_viewer_right_vertical_grip_candidate.png` | `10ab82a6024503154afc017299f595e61aa82c4d13a373c91234942e5b7c60c4` |
| Viewer-left palm up | `base_pose_004_viewer_left_palm_up_candidate.png` | `f97eeae1b2f201c1c0a5d802b89a90e5a9de854934a0a810fc512b2c768d5a4c` |
| Centered two-hand grip | `base_pose_005_centered_two_hand_grip_candidate.png` | `00e3f3fbbc2dc06ab56e1f90a4c96be40b50537135b4a9076fa4dc88902b4772` |

## Pose 001 correction attempts

| Attempt | File | SHA-256 | Status |
|---|---|---|---|
| 002 | `base_pose_001_relaxed_open_candidate_attempt_002.png` | `0b34edf641d7455026f925549d30a734c02f9e62bd0641150a27f88d3aef68f9` | QA-failed: visible bounds `[378,48,870,1182]` exceed the top and foot limits. |
| 003 | `base_pose_001_relaxed_open_candidate_attempt_003.png` | `9fec3bb90243e03164a4f993f78337e7cd8c7e170ca04db73170ee0987b6eca7` | QA-failed: visible head Y 157 and foot Y 1108 miss the locked anchors; hands are too far inward. |
| 004 | `base_pose_001_relaxed_open_candidate_attempt_004.png` | `48ab7bbfa16ddc59d4241285113d154d38900cd30cc76d86e0772ae4a8f4a0f7` | QA-failed: visible bounds `[354,44,892,1171]` overcorrect scale and exceed top/bottom limits. |

See `docs/qa/base_pose_001_rig_gate_2026-07-22.md` for the complete audit.

## Promotion gate

A candidate may be promoted only after complete native 1254 × 1254 RGBA decoding succeeds, the automated visible-geometry gate passes, manual landmark-overlay and visual QA pass, explicit human approval is recorded, and the production manifest records its exact final SHA-256. Never resize a candidate to repair rig or pose drift.
