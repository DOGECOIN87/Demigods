# Asset QA Checklist

## Geometry and rig
- [ ] 1254 × 1254 canvas.
- [ ] Front-facing orthographic appearance.
- [ ] No yaw, pitch, roll, perspective, scale, or pose drift.
- [ ] Character pixels remain within `[233,129,1021,1139]`.
- [ ] Top of head Y 141 and head center `[627,343]`.
- [ ] Eye line Y 367 and mouth center `[627,441]`.
- [ ] Shoulder line Y 569 and waist center `[627,808]`.
- [ ] Hand anchors `[404,772]` and `[850,772]` for the selected pose.
- [ ] Foot baseline Y 1139 and body centered on X 627.
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
