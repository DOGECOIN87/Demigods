# Production Asset Library

Place approved final assets into the canonical category folders below. Every character-compatible production file must remain on the full 2048 × 2048 canvas at final compositing coordinates.

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

The singular `assets/base_body/` folder is a source-reference and documentation area. Files there are not automatically treated as approved production layers.

## Format rules

- Production character layers: 2048 × 2048 RGBA PNG with genuine transparency.
- Production backgrounds: 2048 × 2048 PNG; full-canvas opaque imagery is permitted only in this category.
- No JPEG production assets.
- No WebP production assets.
- Never tightly crop visible pixels; preserve the full master canvas.

Do not place flattened completed characters inside trait folders. Do not use character names in filenames. Keep rejected, damaged, draft, recovered, or guide-layer artwork outside the approved production directories.
