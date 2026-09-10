# `aura_front_001` rebuilt — 2026-09-09

The registered `aura_front_001` was deregistered earlier the same day as a
placeholder: 126,276 opaque pixels carrying three distinct colour buckets — hard
edged orange and gold triangles plus a few solid circles, with no internal value
structure. As a front aura it composites over the character, so it covered every
token it appeared on with opaque geometry. The details are in
`docs/qa/front_aura_001_placeholder_rejected_2026-09-09.md`.

The replacement is built as an effect rather than drawn as a shape.

## What it is

Five octaves of fractal value noise, advected upward, used twice: to modulate
eight tongue envelopes, and to carve them into separate licks. The noise is
subtracted at every height, not only near the tips, because a flame is gaps as
much as it is fire.

Four details matter and every one of them was a failure first.

- **Tongues are combined by maximum, not by sum.** Eight overlapping Gaussians
  saturate wherever they meet, and after the intensity compression that came out
  as a filled slab with a hard bottom edge and hard sides — two orange rectangles
  washing over the character's coat on every token the aura landed on. It passed
  all three flatness measures below, because a gradient-filled rectangle is not
  flat; it was only visible in a rendered sample. Taking the maximum keeps each
  tongue its own shape and the character reads between the licks.
- **The noise field is stretched to its own 2nd–98th percentile.** Summed octaves
  pile up near the middle of their range, so an unstretched field only dents the
  envelope: the first version with maximum-combining gave smooth cones rather than
  torn licks.

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
| distinct alpha levels | 28 | 83 | ≥ 64 | **143** |
| share of one single RGBA value | 0.334 | 0.067 | ≤ 0.10 | **0.008** |
| share with no local variation | 0.883 | 0.219 | ≤ 0.60 | **0.085** |
| peak alpha | 170 | 141 | — | 151 |

These three catch flat shading, and they did not catch the slab. That is worth
recording plainly: a measure is only as good as the failure it was written for,
and the rendered sample is still what finds the rest. `scripts/build_front_aura_flame.py --install`
writes the measured numbers into the manifest entry, so what is recorded always
describes the bytes that shipped.

`tests/test_front_aura` in `tests/test_face_traits.py` applies the same three
measures to every registered front aura, so a future placeholder fails in CI rather
than in review.

`scripts/build_front_aura_flame.py`.
