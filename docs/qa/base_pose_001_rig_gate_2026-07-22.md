# Pose 001 Rig Gate — 2026-07-22

## Result

**QA failed — no Pose 001 or neutral master was registered.**

All four audited PNGs decode completely at the native 1254 × 1254 canvas with RGBA and genuine transparency. Canvas compliance does not compensate for placement failure. The locked Pose 001 silhouette must begin at top-of-head Y 141, end at foot-baseline Y 1139, remain inside inclusive bounds `[233,129,1021,1139]`, and stay centered on X 627.

PIL alpha bounds use an exclusive right and bottom edge; the inclusive bounds below subtract one from those two values.

| Candidate | SHA-256 | Inclusive visible bounds | Geometry result | Manual observations |
|---|---|---|---|---|
| `base_pose_001_relaxed_open_candidate.png` | `f34f1306918710a499ba0d5e5595a98c6d157e1243f3717058aa6b3281bd2082` | `[410,72,836,1135]` | Fail: head is 69 px too high; horizontal silhouette center is X 623; foot ends 4 px above baseline | Front-facing and coherent, but shorts terminate above the required knee-length target. |
| `base_pose_001_relaxed_open_candidate_attempt_002.png` | `0b34edf641d7455026f925549d30a734c02f9e62bd0641150a27f88d3aef68f9` | `[378,48,870,1182]` | Fail: exceeds maximum top and bottom; head is 93 px too high; feet extend 43 px below baseline; center is X 624 | Clothing reads clearly and is knee-length; scale and placement are invalid. |
| `base_pose_001_relaxed_open_candidate_attempt_003.png` | `9fec3bb90243e03164a4f993f78337e7cd8c7e170ca04db73170ee0987b6eca7` | `[427,157,824,1108]` | Fail: head begins 16 px too low; feet end 31 px above baseline; center is X 625.5; hands remain too far inward | Best bounded attempt, but it misses the immutable head, foot, and hand anchors. |
| `base_pose_001_relaxed_open_candidate_attempt_004.png` | `48ab7bbfa16ddc59d4241285113d154d38900cd30cc76d86e0772ae4a8f4a0f7` | `[354,44,892,1171]` | Fail: exceeds maximum top and bottom; head is 97 px too high; feet extend 32 px below baseline; center is X 623 | The targeted rerender overcorrected scale and cannot be repaired by resampling. |

## Native-generation provenance

Attempts 002–004 were rendered natively at exactly 1254 × 1254 on a flat green removal field. The installed chroma-key helper changed only background alpha/color values and preserved the 1254 × 1254 raster dimensions. No candidate was resized, upscaled, downscaled, extended, or copied into `assets/base_bodies/`.

| Attempt | Native opaque source SHA-256 | Alpha-candidate SHA-256 |
|---|---|---|
| 002 | `534c66960333af349d051fbc4fa4b6a7f7e8ca99270e7e986af808aca4f05e83` | `0b34edf641d7455026f925549d30a734c02f9e62bd0641150a27f88d3aef68f9` |
| 003 | `1635fb2e9e03988a529fc761fcf857a4e0a57227b3b4138bb45fca30bc75cd51` | `9fec3bb90243e03164a4f993f78337e7cd8c7e170ca04db73170ee0987b6eca7` |
| 004 | `06136517946f92dca7cb549effd54511406b235121813ceb62df02512116a265` | `48ab7bbfa16ddc59d4241285113d154d38900cd30cc76d86e0772ae4a8f4a0f7` |

## Enforcement change

`scripts/intake_approved_base.py` now rejects a file when its alpha silhouette misses the locked top, foot, maximum bounds, or center axis. Facial, shoulder, waist, hand-anchor, clothing, anatomy, identity, and lighting checks remain manual overlay gates because those landmarks cannot be proven from the alpha silhouette alone.

## Decision

- Keep Issue #4 open.
- Keep all four images outside production directories and the registered manifest.
- Do not derive poses 002–005 from a failed master.
- Generate the next Pose 001 candidate natively against the coordinate guide and reject it if any locked geometry or visual check fails.
