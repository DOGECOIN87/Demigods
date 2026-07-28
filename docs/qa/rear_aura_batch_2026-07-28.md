# Rear-aura batch QA — 2026-07-28

Three rear auras extended the category from six to nine registered assets. Each is
a native 1254 × 1254 RGBA layer with genuine soft alpha; none is a keyed
checkerboard or a flat opaque field.

## Assets

| Asset | Backlog | Route | Gate | Notes |
|---|---|---|---|---|
| `aura_rear_002_violet_radial_glow.png` | DG-016 | procedural `build_aura_radiance.py --palette violet` | `--trait` | Soft violet body glow; matches the cell's "soft violet circular radial glow". |
| `aura_rear_004_violet_void_flame.png` | DG-018 | co-created candidate → `extract_effect_layer.py --field white` | `--floor-aura` | Dark violet rising void flame; reaches the foot baseline, so the near arc runs to the ground. |
| `aura_rear_016_cosmic_sparkle_ring.png` | DG-156 | co-created candidate → `extract_effect_layer.py --field black` | `--trait` | Violet cosmic burst with radiating spokes; bright at every alpha. |

## Why the effect candidates were re-keyed rather than promoted

The two co-created candidates (`grok_1784757226345.png`, `PoLVl.jpg`) are opaque
RGB / hard-keyed RGBA on a flat studio field. Numerical inspection showed binary
alpha with a ~67% fully-opaque region — the "transparency" was only the cut
corners, and the cosmic candidate carried a dark opaque halo that would darken any
background. Promoting them directly would fail the genuine-alpha rule.

`scripts/extract_effect_layer.py` derives alpha analytically from the field
instead of keying it out:

* black field (cosmic burst): alpha = luminance, colour un-premultiplied, so the
  effect only ever adds light;
* white field (void flame): alpha ramps from a near-white cut down to black, so the
  studio haze is removed and the dark form keeps its drawn colour.

The keyed-from-white violet **radial glow** candidate (`Gucuc.jpg`) was rejected:
its derived alpha peaked near 22% and it was invisible over bright backgrounds
(fails "readable at NFT display size"). DG-016 was rendered procedurally instead,
which is cleaner and matches the primary cell description.

## Reproduce

```bash
python scripts/build_aura_radiance.py --palette violet --peak-alpha 235 --falloff 1.3 \
  --out images/trait_candidates/rear_auras/aura_rear_002_violet_radial_glow_candidate_attempt_004.png
python scripts/extract_effect_layer.py images/trait_candidates/PoLVl.jpg \
  --out .../aura_rear_004_violet_void_flame_candidate_attempt_002.png \
  --field white --white-cut 232 --gamma 1.1 --gain 1.5 --floor 6 --recenter-x \
  --target-height 980 --center-y 660
python scripts/extract_effect_layer.py images/trait_candidates/grok_1784757226345.png \
  --out .../aura_rear_016_cosmic_sparkle_ring_candidate_attempt_002.png \
  --field black --gamma 1.35 --gain 1.7 --floor 3 --target-height 968 --center-y 645
```

## Checks

- Production asset validation: PASS for all three (only the tolerated missing-ICC
  warning, plus the expected "no fully opaque pixels" note on the soft glow).
- Rig gate: radial glow and cosmic burst PASS `--trait`; void flame PASS
  `--floor-aura` (near arc intentionally below the foot baseline).
- Composite QA over bright (solar temple, throne hall) and dark (violet void)
  backgrounds: each reads as light behind the character and composites cleanly
  behind the silver rear hair and body.
