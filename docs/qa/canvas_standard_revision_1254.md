# Canvas Standard Revision — 1254 × 1254

Date: 2026-07-22

## Decision

The canonical Demigods production canvas is now **1254 × 1254 pixels**. The prior native-resolution requirement is superseded and must not be used by current prompts, validators, generator defaults, output checks, or production acceptance decisions.

The existing pose-candidate PNGs were generated natively at 1254 × 1254. They must not be resized or upscaled. Canvas compliance is a binary prerequisite only and does not by itself establish production approval.

## Rig migration

The shared rig was proportionally rebased from the former canvas and rounded once to canonical integer coordinates:

| Anchor | 1254 coordinate |
|---|---:|
| Canvas center | X 627 |
| Top of head | Y 141 |
| Head center | X 627, Y 343 |
| Eye line | Y 367 |
| Mouth center | X 627, Y 441 |
| Shoulder line | Y 569 |
| Waist center | X 627, Y 808 |
| Viewer-left hand | X 404, Y 772 |
| Viewer-right hand | X 850, Y 772 |
| Foot baseline | Y 1139 |
| Maximum bounds | X 233–1021, Y 129–1139 |

These coordinates replace the former canvas-specific values. Future character-aligned assets must use the values in `config/collection.json` as the machine-readable source of truth.

## Existing pose-candidate state

All five files under `images/pose_candidates/` completely decode as 1254 × 1254 RGBA PNGs with genuine alpha. Their previously recorded SHA-256 values remain unchanged.

Remaining gates:

- Pose 001: manual identity, proportional-rig, knee-length clothing, anatomy, lighting, and isolation approval.
- Poses 002–005: reconcile body, scale, center line, and foot baseline to the approved Pose 001 master before promotion.
- Pose 003: normalize the viewer-right vertical grip to the common hand anchor.
- Every promoted file: copy only after approval, then record its exact SHA-256 and run manifest consistency validation.

## Historical reports

Earlier QA reports correctly describe the rules and tool outputs that existed when those audits ran. Their former dimension failures are historical and no longer control current acceptance. Other documented visual failures remain actionable until reviewed or corrected.
