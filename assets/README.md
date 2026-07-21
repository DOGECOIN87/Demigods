# Production Asset Library

Place approved final assets into the following category folders. Every character-compatible production PNG must remain on the full 2048 × 2048 transparent canvas at its final compositing coordinates.

```text
assets/
  backgrounds/
  rear_auras/
  back_accessories/
  hair_back/
  base_bodies/
  outfits/
  neck_accessories/
  eyes/
  eyebrows/
  mouths/
  expression_marks/
  hair_front/
  head_accessories/
  hand_objects/
  front_auras/
  global_finish/
```

## Base-body directory rule

All production-ready neutral bodies and hand-pose variants belong in `assets/base_bodies/`, including:

- `base_body_001_neutral_master.png`
- `base_pose_001_relaxed_open.png`
- `base_pose_002_viewer_left_vertical_grip.png`
- `base_pose_003_viewer_right_vertical_grip.png`
- `base_pose_004_viewer_left_palm_up.png`
- `base_pose_005_centered_two_hand_grip.png`

The singular `assets/base_body/` folder is reserved for source-reference documentation and damaged or optimized reference material. Files there are not production layers.

## Format rules

- Character-compatible production layers: 2048 × 2048 RGBA PNG with genuine transparency.
- Backgrounds: 2048 × 2048 PNG that fills the full canvas.
- No JPEG or WebP production assets.
- Preserve the full canvas; never tightly crop visible pixels.

Do not place flattened completed characters inside trait folders. Do not use character names in filenames. Keep rejected, damaged, draft, recovered, or guide-layer artwork outside the approved production directories.
