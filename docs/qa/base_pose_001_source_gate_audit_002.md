# Base Pose 001 Source Gate Audit 002

Date: 2026-07-21
Audited `main`: `f3ee920385fc682c644f053ff8b5499824650b3c`

## Conclusion

**Blocked — visual production stopped.**

No approved, genuinely native 2048 × 2048 RGBA source with a transparent background is present in the repository or was supplied for this production pass. Prompt 16 therefore cannot proceed past its hard execution gate. No image was resized, upscaled, reconstructed, copied into `assets/base_bodies/`, registered, or assigned a production SHA-256.

## Source availability audit

The complete image inventory contains:

- the damaged approved WebP at `assets/base_body/base_body_001_neutral_master.webp`; and
- five non-production pose candidates under `images/pose_candidates/`, all 1254 × 1254 RGBA PNGs.

There is no PNG at either canonical production path:

- `assets/base_bodies/base_body_001_neutral_master.png`
- `assets/base_bodies/base_pose_001_relaxed_open.png`

The production registry remains empty by design.

## Binary QA of the selected Pose 001 reference

Command:

```bash
python scripts/intake_approved_base.py \
  images/pose_candidates/base_pose_001_relaxed_open_candidate.png \
  --report /tmp/demigods_pose001_intake.json
```

| Check | Expected | Observed | Result |
|---|---|---|---|
| Complete PNG decode | Successful | Successful | Pass |
| Dimensions | 2048 × 2048 | 1254 × 1254 | **Fail** |
| Color mode | RGBA | RGBA | Pass |
| Genuine alpha | Present | Alpha extrema 0–255 | Pass |
| Visible bounds | Locked rig | `(410, 72, 837, 1136)` | **Fail** |
| Embedded ICC profile | sRGB preferred | Missing | Warning |
| SHA-256 | Informational only | `f34f1306918710a499ba0d5e5595a98c6d157e1243f3717058aa6b3281bd2082` | Not registrable |

The intake script returned `passed_binary_qa: false` because the dimensions are not the locked native canvas size.

## Manual visual QA

| Area | Observation | Result |
|---|---|---|
| Anatomy | One centered front-facing character; two coherent arms, two legs, five fingers per hand, and five toes per foot. | Pass as reference only |
| Clothing | Opaque separate sleeveless top and shorts are visible, but the shorts terminate above the locked knee-length target. | **Fail** |
| Lighting | Upper-left highlights and lower-right form shading are broadly consistent with the locked direction. | Pass as reference only |
| Camera | Front-facing and approximately orthographic. | Pass as reference only |
| Head anchor | Visible top begins at Y 72. The locked top-of-head target scaled only for comparison to the 1254 reference is approximately Y 141. | **Fail** |
| Waist/torso placement | The torso and waistband sit above the scaled locked rig position. | **Fail** |
| Hand anchors | The relaxed hands do not establish production-valid anchors on the required 2048 canvas. | **Fail** |
| Foot baseline | The visible lower bound is near the scaled baseline, but a low-resolution coordinate coincidence cannot qualify the source or override the other rig failures. | Not eligible |
| Alpha isolation | Transparent surroundings with no baked floor or contact shadow. | Pass as reference only |

Manual review cannot promote an undersized source. Passing traits above describe the visual reference only and do not constitute approval.

## Repository validation

- Regression tests: **31 passed**.
- Locked configuration and compatibility audit: **passed** with zero available production traits.
- Asset/manifest preproduction audit: **passed with `--allow-empty`** and the damaged WebP correctly ignored as a non-production reference.
- Registered-production manifest consistency: **passed** for zero registered assets.
- Generator preflight: **failed as expected** because required categories `backgrounds` and `base_bodies` are absent.

The generator failure is a production-readiness result, not a validator defect.

## Decision

- Do not execute poses 002–005.
- Do not add `base_body_001` or `base_pose_001` to `registered_production_assets`.
- Do not add production SHA-256 values to the manifest.
- Do not alter the current blocked manifest state.
- Keep Prompt 16 and all 1254 × 1254 candidates outside production.

## Next required action

Supply the intact, explicitly approved 2048 × 2048 RGBA master PNG with genuine transparency. Then run binary intake without `--register`, complete manual identity/rig/clothing/lighting QA, obtain explicit human approval, and only then register Pose 001 before deriving poses 002–005 sequentially.
