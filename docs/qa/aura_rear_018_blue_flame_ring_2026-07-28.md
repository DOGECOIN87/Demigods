# QA — DG-161 blue flame ring, extraction from a co-created candidate

Date: 2026-07-28
Backlog row: DG-161
Candidate: `images/trait_candidates/rear_auras/aura_rear_018_blue_flame_ring_candidate.png`
Source: `images/trait_candidates/grok_1784755724820.png`

## Why this row exists

DG-161 is the first backlog row sourced from a co-created candidate rather than a
reference cell. The design — a blue flame rising above a luminous floor ring —
appears in no repository catalog; it exists only as an image that was already
sitting unsorted in `images/trait_candidates/`. `prompts/12_auras.md` governs the
category and defines the design language, so the row is inside the backlog's
stated scope, but it is a deliberate exception and not a precedent for inventing
rows.

## The source is not what it looks like

The file presents as a clean native layer: 1254 x 1254, RGBA, alpha 0–255, and
fully transparent corners with RGB `(0,0,0)` at stddev 0. Every one of those
checks passes, and all of them are misleading.

**The alpha is perfectly binary.** 32.85% of pixels sit at exactly 0 and 67.15%
at exactly 255, with *nothing* in between. That is not a soft-edged effect layer;
it is an opaque image with transparent letterbox padding. Sampling the borders
confirms the shape: the top and bottom rows carry content while the left and
right columns are empty, so the alpha channel is a rectangle, not a silhouette.

**The content region carries a baked transparency checkerboard.** The corner
probe that looked clean was sampling the letterbox bars, not the artwork. Inside
the content rectangle the field measures mean 247 at stddev 6.6–9.3, against
~0.6 for a genuinely flat field (`PoLVl.jpg`) and ~18 for a known baked checker
(`s1sqd.jpg`). The field is also near-white, not black.

A first extraction with `--field black` therefore used the wrong polarity *and*
carried the checker straight through into the derived alpha, producing a visible
checkered rectangle over any background.

## What worked

The checker amplitude (±7 levels) is small next to the flame's contrast, so a
white-field extraction with the cut placed above the checker clears it — but
only after cropping away the black letterbox bars, which a white-field pass
would otherwise read as maximally opaque content.

```
# 1. crop to the true content rect given by the alpha bbox
# 2. extract against the white field
python scripts/extract_effect_layer.py <cropped> \
    --out assets/rear_auras/aura_rear_018_blue_flame_ring.png \
    --field white --white-cut 232 --target-height 950 --center-y 660
```

`--white-cut 215` also clears the checker but leaves more edge haze; 232 is
crisper and was chosen.

## Verification

- Alpha softness: **37.89%** of pixels now sit strictly between 0 and 255, versus
  **0.00%** in the source. The layer has genuine soft falloff.
- Peak alpha 181 — never opaque, correct for a glow.
- Bounds `[306,240,947,1130]`, centre X 626.5 against the locked 627.
- Rig gate passes in **both** `--floor-aura` and the stricter `--trait` mode; the
  effect sits above the foot baseline, so it needs no ground-plane exemption.
- Composited over white the flame stays bright with no dark matte and no checker
  artifact. Preview: `docs/qa/aura_rear_018_blue_flame_ring_preview.png`.

## Status

**Candidate awaiting human visual approval.** Held under
`images/trait_candidates/rear_auras/`, not `assets/rear_auras/`, because the
generator scans `assets/<category>/` and anything placed there is immediately
live.

## Note for the remaining unsorted candidates

Two lessons generalise. First, a transparent-corner probe proves nothing about a
letterboxed image — probe inside the content rect. Second, a baked checkerboard
is not always fatal: when its amplitude is small against the subject, a
field extraction with the cut placed above it recovers a clean layer. That does
*not* rescue `s1sqd.jpg` (DG-019 lavender lightning), where the bolt is white,
the checker squares are white, and the two are inseparable — and which
additionally carries burned-in `X: 627 / Y: 0` UI text.
