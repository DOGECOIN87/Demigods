# QA — outfit_001 foot-baseline breach and clip

Date: 2026-07-28
Asset: `assets/outfits/outfit_001_celestial_scholar_pose_001.png`

## Defect

The asset was registered on 2026-07-28 but failed the partial-layer rig gate:

```
max_bounds  FAIL  [407,475,848,1144]  [233,129,1021,1139]  B5
```

Its visible pixels reached Y 1144, five pixels below the locked foot baseline at
Y 1139. The other four registered outfits are clean (bottoms at Y 1138–1139).

The breach is genuine geometry, not stray dust: the boot soles are drawn with a
rounded bottom taper running from Y 1140 (98 opaque px) to Y 1144 (28 px of pure
anti-aliasing). Because every background establishes its floor at Y 1139, the
character read as standing slightly *through* the floor.

The defect predates the batch tooling. It surfaced when the whole outfit folder
was run through the new `scripts/bulk_intake.py` path, which gates every
candidate rather than only newly generated ones.

## Options considered

**Rescale (`refit_trait_layer.py`, scale 0.992537, top Y 475).** Produces
bounds `[408,475,846,1139]`, centered at X 627, and passes the gate. Rejected:
the garment is drawn to fit a shared body that does not shrink with it. At 0.75%
reduction the boots no longer covered the base body's feet, and the bare toes
became visible below both soles. That trades a five-pixel bounds breach for
visible skin on every token using this outfit — a worse defect.

**Clip to the locked bounds.** Leaves the garment at its drawn size, so it still
covers the body completely, and terminates the sole exactly on the ground plane.
A sole resting on a floor is flat at the floor line, so the clipped edge is what
the geometry should have been. Accepted.

## Applied fix

```
python scripts/clip_trait_to_bounds.py \
    assets/outfits/outfit_001_celestial_scholar_pose_001.png --in-place
```

```
overhang  {'left': 0, 'top': 0, 'right': 0, 'bottom': 5}
bounds    [407, 475, 848, 1144] -> [407, 475, 848, 1139]
removed   343 px (0.2835% of the layer)
```

`clip_trait_to_bounds.py` refuses overhangs deeper than 12 px or clips removing
more than 1% of the visible layer, because either signals a layer drawn at the
wrong scale or position — which needs a re-render or a refit, not a clip. This
overhang is 5 px and 0.28%, well inside both.

## Verification

- Rig gate `--trait --max-width-ratio 1.15`: **PASS** on canvas, transparent
  background, `max_bounds` `[407,475,848,1139]`, and width ratio 1.00x.
- Visual check at 3x over `background_001_celestial_throne_hall`: sole terminates
  on the ground line, gold trim intact, no exposed skin. Compared side by side
  against the original and the rejected rescale.
- Manifest updated: SHA-256 `5df00232eaa9b6a495e9522149864f321e8eea8de9335cdb7bb334238c822958`,
  `postprocessing` records `clip_to_max_bounds_y1139`.

## Note on the original bytes

This edits an asset that already carried human approval. The change is a
five-pixel alpha clip that removes no design detail and alters no colour channel;
the approved design is unchanged. The original digest was
`791ad8b6c6534e7afa401ca65e598ffc07675c33ecad2d84fe6b769ab4cd43f2`.
