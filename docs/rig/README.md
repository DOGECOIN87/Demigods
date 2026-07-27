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
