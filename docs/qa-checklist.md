# Asset QA Checklist

## Geometry and rig
- [ ] 1254 × 1254 canvas.
- [ ] Front-facing orthographic appearance.
- [ ] No yaw, pitch, roll, perspective, scale, or pose drift.
- [ ] Correct eye line, mouth line, shoulders, waist, hands, and foot baseline.
- [ ] Full-canvas coordinates preserved.

## Layer isolation
- [ ] Exactly one category is present.
- [ ] No baked-in face, hair, clothing, hand object, accessory, aura, background, label, or name from another category.
- [ ] Invisible placement guides have been removed.
- [ ] Hidden overlap is sufficient to prevent seams.

## Transparency and edges
- [ ] True RGBA alpha for non-background assets.
- [ ] No rendered checkerboard or opaque rectangle.
- [ ] Asset is not fully transparent or fully opaque by mistake.
- [ ] Glow and particles have clean soft alpha falloff.
- [ ] No visible pixels are unintentionally clipped by a canvas edge.

## Lighting and finish
- [ ] Upper-left key light.
- [ ] Lower-right form shadows.
- [ ] Matching cool right rim light where appropriate.
- [ ] Consistent ambient fill, contrast, line weight, and shadow softness.
- [ ] Readable at small NFT display size.

## Compatibility
- [ ] Tested against unrelated hair, face, outfit, accessory, hand, and background variants.
- [ ] No unresolved collisions.
- [ ] Any necessary restriction is recorded in `config/compatibility.json`.
- [ ] Filename follows lowercase snake case and contains no character name.
