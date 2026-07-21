# Base Pose 001 Native Generation Attempt 001

Date: 2026-07-21

## Conclusion

**Failed — retained outside production.**

Prompt `prompts/16_native_2048_pose_001_candidate.md` was executed once against `images/pose_candidates/base_pose_001_relaxed_open_candidate.png`. The image service returned a 1254 × 1254 RGB PNG rather than the required native 2048 × 2048 RGBA PNG. The hard gate therefore stopped the workflow before chroma-key removal, resizing, registration, or manifest changes.

The failed intermediate is not committed to the repository and is not a production asset.

## Automated binary findings

| Check | Expected | Observed | Result |
|---|---|---|---|
| File format | PNG | PNG | Pass |
| Complete decode | Successful | Successful | Pass |
| Dimensions | 2048 × 2048 | 1254 × 1254 | **Fail** |
| Color mode | RGBA | RGB | **Fail** |
| Alpha channel | Present with genuine transparency | Missing | **Fail** |
| ICC profile | Embedded sRGB profile preferred | Missing | Warning |
| File size | Informational | 1,251,539 bytes | Informational |
| SHA-256 | Informational | `782950512d5276d7296d55c272667346d18d25fd3920d2c49d50d96e37cd1700` | Informational |

The repository intake script returned `passed_binary_qa: false` with these errors:

- `dimensions are (1254, 1254), expected (2048, 2048)`
- `mode is RGB, expected RGBA`
- `missing alpha channel`

## Visual and rig observations

- One centered, front-facing, fully clothed character was produced.
- The separate sleeveless top and shorts read clearly as opaque fabric, but the hems terminate above the locked knee-length target and would require correction.
- The relaxed-open pose, face direction, five-finger hands, and five-toe feet are visually coherent.
- The temporary green background was not perfectly uniform; sampled corners were approximately RGB `(16, 239, 14)` and `(18, 245, 13)` rather than exact `#00ff00`.
- A 10% chroma-key tolerance estimated the character bounds as 455 × 1128 pixels at offset `+399+44` on the 1254-pixel canvas.
- The scaled locked top-of-head target is approximately Y 141, but the observed keyed bound begins near Y 44.
- The scaled locked foot baseline is approximately Y 1139, but the observed keyed bound extends to approximately Y 1172.

These placement differences independently fail the locked rig even if the dimension and alpha failures were ignored.

## Decision

- Do not resize or upscale the result.
- Do not extract alpha from this failed intermediate for production use.
- Do not copy it into `assets/base_bodies/`.
- Do not add it to `registered_production_assets`.
- Do not mark Pose 001 complete.

## Next required action

Supply the intact approved 2048 × 2048 RGBA master, or use an explicitly authorized image path that can render a genuinely native 2048 × 2048 source. Run binary and manual QA again before registration.
