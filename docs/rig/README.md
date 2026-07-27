# Rig guide and gate diagnostic

Tooling that speeds up the Pose 001 / base-master QA loop tracked in
[Issue #4](https://github.com/DOGECOIN87/Demigods/issues/4). Neither tool writes,
resizes, or registers a production asset — they only measure and visualize, so
they are safe to run on any candidate at any time.

## `scripts/rig_gate_report.py` — silhouette diagnostic

Measures a candidate's alpha silhouette against the locked rig in
`config/collection.json` and prints the exact per-anchor pixel deltas (the same
numbers the manual QA table records), plus the scale/shift that would align it.
Complements `scripts/intake_approved_base.py`, which enforces a binary
accept/reject but does not report *how far off* a failing candidate is.

```bash
python scripts/rig_gate_report.py images/pose_candidates/        # a whole folder
python scripts/rig_gate_report.py path/to/new_candidate.png      # one new render
python scripts/rig_gate_report.py cand.png --json-report r.json  # machine-readable
```

Provable-from-alpha gates: top-of-head Y, foot-baseline Y, horizontal center X,
maximum bounds. Face/hand/waist/clothing/anatomy/lighting/identity remain manual
overlay gates. Exit code is non-zero if any candidate fails (CI-friendly).

**Symmetric vs. asymmetric assets.** The default center check uses the full
silhouette bounding box — correct for a symmetric master, but a raised arm or a
single wing legitimately skews it. For those, add `--pose-variant`, which judges
the **arm-free body center** (head band + lower-leg band) instead:

```bash
# base master (symmetric, full figure)
python scripts/rig_gate_report.py assets/base_bodies/base_body_001_neutral_master.png

# hand-pose variants (full figure, raised arm) — allow ~2 px body-center drift
python scripts/rig_gate_report.py --pose-variant --tolerance 2 incoming.png

# partial trait layers (hair, eyes, crown, wings) — only occupy their own region
python scripts/rig_gate_report.py --trait incoming.png

# ground-plane auras (floor rings, magic circles) — the near arc passes below the feet
python scripts/rig_gate_report.py --floor-aura incoming.png
```

`--trait` checks canvas size, genuine transparency, and max bounds, and skips the
full-figure head/foot/center gates (a hair layer never reaches the foot baseline).
Always confirm a trait's placement with a composite over the base body — see
`docs/qa/composites/` for examples.

**Proportion against the base body.** Canvas, transparency and bounds say nothing
about whether a layer is the right *size* for the character. `hair_back_003`
passed every silhouette gate at 1.46 × the body width and still read as wings in
composite, so `--trait` and `--floor-aura` now report a width ratio and a crown
offset whenever a base body is available:

```bash
# report only — default
python scripts/rig_gate_report.py --trait incoming.png

# enforce a ceiling for layers that should hug the figure
python scripts/rig_gate_report.py --trait incoming.png --max-width-ratio 1.35
```

`width vs base body` is the layer's width as a multiple of the base body's.
`crown offset` is signed: positive means the layer reaches above the head top,
negative means it starts below it and will leave a bald gap for rear hair.

The ceiling is **opt-in** on purpose. Rear hair sits near 1.2 ×, but back
accessories — wings, capes, mantles — legitimately exceed body width, and a
default ceiling would false-fail the entire category. Pass `--max-width-ratio`
for layers that should hug the figure and omit it elsewhere.

Refit an out-of-proportion layer with `scripts/refit_trait_layer.py`, which
scales about the locked centre axis and seats the top at a chosen Y. Prefer a
native re-render at correct proportions; refitting is a repair, not a production
method, and every use must be recorded in the manifest's `postprocessing`.

**Garment / skin separation.** The base mannequin wears a skin-toned tank top and
shorts, roughly 27 RGB units from cheek skin `(253,199,163)`. That is fine for a
base layer an outfit covers, and fatal if nothing covers it: at thumbnail size
the figure reads as unclothed. Outfits are gated on it:

```bash
python scripts/rig_gate_report.py --trait incoming.png \
  --max-width-ratio 1.15 --min-skin-contrast 70
```

`skin_contrast` is the mean RGB distance of the layer's opaque pixels from base
skin tone. The mannequin garment measures 27; a navy robe measures 274. The check
is opt-in because auras, effects and pale accessories legitimately sit near any
tone — only garments that must cover the body should enforce it.

**Ground-plane auras.** `maximum_character_bounds` stops at foot baseline Y 1139,
which is correct for the character but wrong for an effect lying on the floor. For
the character to read as standing *inside* a floor ring rather than in front of it,
the ring's far arc must pass behind the ankles and its near arc in front of the
toes — and the near arc is necessarily below Y 1139.

`--floor-aura` is that narrow exemption. It behaves like `--trait` but bounds the
bottom at the canvas edge instead of the foot baseline. The X bounds and the top
bound still apply, and the asset still may not touch the final canvas row, since
reaching it means the glow is clipped rather than merely low.

The exemption is deliberately scoped: the same file that passes `--floor-aura`
still fails `--trait`, so an ordinary partial layer can never drift below the
baseline unnoticed. Use `--floor-aura` only for effects that genuinely lie on the
ground plane.

## `scripts/build_rig_guide.py` — visual overlay

Renders every locked anchor to a transparent `docs/rig/rig_guide_1254.png`.
Overlay a candidate beneath it for visual QA, or attach it to the image
generator as the coordinate reference (see `prompts/16`).

```bash
python scripts/build_rig_guide.py
```

`overlay_attempt_003.png` is an example: the "best bounded" Pose 001 candidate
under the guide — centered and in-bounds, but ~1.05× too small (head below the
top line, feet above the baseline).
