# Global finish — definition

Last updated: 2026-07-28

`16_global_finish` is the final entry in the locked layer stack. It has existed
in the validator and the layer documentation since the stack was locked, but it
had no artwork and no prompt, so the category sat source-gated and empty.

`docs/trait-production-backlog.md` recorded two acceptable ways to close that
gate: an explicit reference cell, or *a narrowly defined finish treatment that
remains a separate transparent layer*. No global-finish cell exists in any
repository reference sheet, and inventing one would mean inventing a design the
collection never approved. This document takes the second exit.

## What a global finish is

A global finish is a **full-canvas directional light grade** that restates the
collection's locked lighting across the finished frame:

- soft key from the upper left, at roughly 45 degrees
- form falloff toward the lower right
- constant hue, varying only in alpha

It introduces **no object**. That is the whole point of the definition: a layer
that adds no shape cannot collide with a trait, cannot occlude a face, cannot
contradict a background, and cannot become a de facto second aura. It changes
mood only.

## What it is not

- **Not a vignette.** Backgrounds already receive a corner vignette from the
  deterministic depth pass in `scripts/apply_background_depth.py`. A second
  vignette on top would double-treat every frame.
- **Not a prompted asset.** Like the background depth pass and the aura
  builders, it is rendered analytically. An image model will not reproduce the
  same gradient angle and falloff across three variants, and a finish that
  drifts between variants is not a finish.
- **Not a placeholder.** Each variant is a real, distinct grade. A fully
  transparent no-op layer would be a placeholder, which the repository update
  policy forbids counting as a production asset.

## The alpha ceiling

Peak alpha is capped at **64/255 (~25%)**, enforced by
`GLOBAL_FINISH_MAX_ALPHA` in `scripts/rig_gate_report.py`.

This is the rule that keeps the layer honest. A grade sitting on top of every
other layer is the one place in the stack where a mistake can damage every
token at once. Capping peak alpha means the worst a bad finish can do is tint
the frame — it can never hide the art beneath it. A finish that needs more than
25% opacity to read is not a finish; it is a background.

## Gating

The finish covers the whole canvas by design, so silhouette bounds, centering,
and the foot baseline do not describe it — the standard `--trait` mode
false-fails it on `max_bounds` for exactly the reason `--floor-aura` exists for
ground-plane rings.

```
python scripts/rig_gate_report.py --global-finish assets/global_finish/
```

That mode checks canvas size, the peak-alpha ceiling, and that the layer is
never fully opaque. It deliberately skips the geometry checks rather than
loosening them, so the exemption cannot leak into ordinary partial layers.

## The family

| Asset | Tint | Peak alpha | Reads as |
|---|---|---|---|
| `global_finish_001_soft_bloom` | warm white `(255, 246, 226)` | 40 | neutral lift on the key side |
| `global_finish_002_gilded_warm` | gold `(255, 214, 138)` | 56 | warm ceremonial light |
| `global_finish_003_cool_veil` | cool blue `(176, 214, 255)` | 48 | cool shadow-side veil |

Preview across a full composite: `docs/qa/global_finish_preview.png`.

## Optional, not mandatory

The category should be registered in `config/collection.json` under
`optional_categories` so that "no finish" remains a real outcome. Three variants
plus the absent branch give the category a factor of four, and a token with no
finish is the collection's baseline look rather than a defect.

## Status

The three variants are **candidates awaiting human visual approval**. They are
held in `images/trait_candidates/global_finish/` rather than
`assets/global_finish/`, because the generator discovers assets by scanning
`assets/<category>/` and anything placed there is immediately live. On approval,
render them to their canonical paths and register:

```
python scripts/build_global_finish.py --out-dir assets/global_finish
python scripts/rig_gate_report.py --global-finish assets/global_finish/
```

then add the manifest entries, flip DG-158–DG-160 to `registered`, add
`global_finish` to `optional_categories`, and regenerate the ledger.
