# `aura_front_001` rebuilt — 2026-09-09

The registered `aura_front_001` was deregistered earlier the same day as a
placeholder: 126,276 opaque pixels carrying three distinct colour buckets — hard
edged orange and gold triangles plus a few solid circles, with no internal value
structure. As a front aura it composites over the character, so it covered every
token it appeared on with opaque geometry. The details are in
`docs/qa/front_aura_001_placeholder_rejected_2026-09-09.md`.

The replacement is built as an effect rather than drawn as a shape.

## What it is

Four octaves of fractal value noise, advected upward, used twice: to modulate six
tongue envelopes, and to carve them into separate licks by a threshold that rises
with height. Near the base the envelope wins; higher up only the noise's peaks
survive, which is what makes licks rather than a plume.

Two details matter and both were failures first.

- **Intensity is compressed, not clipped.** A hard clip flattens every lick's core
  to one value; it took the layer's top-value share to 0.26, which is the
  placeholder's own failure mode. `1 - exp(-density/k)` approaches full intensity
  without ever landing on it.
- **Colour is compressed on a longer scale than opacity.** Without that the body of
  the flame saturated to the pale gold at the end of the ramp and read as a white
  wash rather than fire.

Nothing is drawn above Y 582, which is below the shoulder line at Y 569, so the
flame licks up the figure's body and never crosses its face.

## Measured against the collection's own two auras

No gate in the collection could tell a flame from three triangles, so the build
measures the thing that actually failed and refuses to write a file that fails it.
The limits sit between the accepted asset and the rejected one, nearer the accepted:

| Measure | placeholder (rejected) | `aura_front_002` (accepted) | limit | rebuilt `aura_front_001` |
|---|---|---|---|---|
| fully opaque pixels | 126,276 | 0 | 0 | **0** |
| distinct alpha levels | 28 | 83 | ≥ 64 | **144** |
| share of one single RGBA value | 0.334 | 0.067 | ≤ 0.10 | **0.008** |
| share with no local variation | 0.883 | 0.219 | ≤ 0.60 | **0.329** |
| peak alpha | 170 | 141 | — | 152 |

`tests/test_front_aura` in `tests/test_face_traits.py` applies the same three
measures to every registered front aura, so a future placeholder fails in CI rather
than in review.

`scripts/build_front_aura_flame.py`.
