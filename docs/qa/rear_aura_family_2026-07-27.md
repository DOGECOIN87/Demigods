# QA — Rear aura family and background depth treatment (2026-07-27)

Covers six rear auras registered on 2026-07-27 and the re-registration of backgrounds 001–004 with a depth treatment.

## Rear auras

All six are procedural renders, not image-generator output. Alpha is derived from a distance field rather than by keying a rendered backdrop, which is what produced the dark matte fringe in the rejected DG-015 attempt 001.

| ID | Path | Gate mode | Visible bounds | Result |
|---|---|---|---|---|
| aura_rear_001 | `aura_rear_001_blue_floor_ring.png` | `--floor-aura` | `[293,1035,960,1221]` | PASS |
| aura_rear_006 | `aura_rear_006_gold_radiance.png` | `--trait` | `[343,432,910,1127]` | PASS |
| aura_rear_007 | `aura_rear_007_green_neon_ring.png` | `--floor-aura` | `[293,1035,960,1221]` | PASS |
| aura_rear_008 | `aura_rear_008_gold_neon_ring.png` | `--floor-aura` | `[293,1035,960,1221]` | PASS |
| aura_rear_009 | `aura_rear_009_pink_neon_ring.png` | `--floor-aura` | `[293,1035,960,1221]` | PASS |
| aura_rear_010 | `aura_rear_010_white_neon_ring.png` | `--floor-aura` | `[293,1035,960,1221]` | PASS |

The four neon rings share DG-015's geometry exactly and differ only in palette, so their bounds are identical by construction.

### Ring seating and the `--floor-aura` exemption

The rings are seated on the foot baseline so the far arc passes behind the ankles and the near arc in front of the toes. Without that the character reads as standing *in front of* the ring rather than inside it. The near arc therefore falls below foot baseline Y 1139, which `maximum_character_bounds` forbids.

`rig_gate_report.py --floor-aura` is the scoped exemption: it keeps the X bounds and the top bound, moves the bottom limit to one row short of the canvas edge, and is refused to any asset that touches the final row, since reaching it means the glow is clipped. The exemption does not leak — every ring here still **fails** `--trait` by `B82`, so an ordinary partial layer cannot drift below the baseline unnoticed.

### Luminous alpha

Every semi-transparent pixel in all six assets carries a bright colour value. Asserted by test, not by eye: `tests/test_rig_gate_report.py::test_every_partial_alpha_pixel_stays_bright` fails if any pixel with `0 < alpha < 255` falls below luminance 120.

For contrast, the rejected DG-015 attempt 001 measured fringe luminance 74.6 against mean alpha 63.2 — luminance tracking alpha, the matte signature. Attempt 005 measures 185.8 against 76.2.

### Known warnings

- All six report **no embedded ICC profile**; confirm sRGB interpretation manually. This matches every previously registered asset.
- `aura_rear_006` reports **no fully opaque pixels**. Expected and correct: it is a soft glow with peak alpha 175 by design, never reaching 255.

## Background depth treatment

Backgrounds 001–004 were re-registered after a deterministic depth pass: 2.5 px Gaussian blur plus a corner vignette at strength 0.22, power 2.4, applied by `scripts/apply_background_depth.py`.

The treatment softens the background and darkens the corners so the scene recedes behind the sharp character. It is applied as a recorded post-process rather than requested in the generation prompt because an image generator will not reproduce the same blur radius and vignette falloff across eight separate renders, and an uneven set is visible the moment two tokens sit side by side.

`prompts/17` now requires backgrounds to be generated fully sharp and unvignetted, since asking the generator for the effect on top of this pass double-treats the image and destroys detail that cannot be recovered.

Each background's manifest entry records `postprocessing` and `postprocessing_script`; the originals remain recoverable from git history. Backgrounds 005–008 must receive the same pass before registration.

### Strength selection

0.3 vignette was evaluated first and read too heavy on the already-dark arcane library corners while sitting well on the light throne hall. 0.22 was adopted as one value across the set: per-background tuning would look better individually but breaks the set consistency that motivates doing this deterministically at all.

## Verification

- `validate_manifest_consistency.py`: PASS, 16 registered assets
- `validate_assets.py`: PASS, all production files
- `validate_config.py`: PASS, 16 available traits
- `report_production_status.py --check`: PASS
- Regression suite: 65 tests pass
