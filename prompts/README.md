# Prompt Library

Use `00_locked_master_specification.md` at the beginning of each generation request and append `01_universal_avoid_block.md` at the end.

## Files

- `00_locked_master_specification.md` — canvas, rig, camera, lighting, quality, and isolation rules
- `01_universal_avoid_block.md` — standard exclusions
- `02_base_body.md` — neutral master body
- `03_hand_poses.md` — approved grip and hand-pose variants
- `04_hair_back.md` — rear hair layers
- `05_hair_front.md` — bangs and front hair layers
- `06_eyes_eyebrows_mouths.md` — isolated facial traits
- `07_expression_marks.md` — blush, stress, sweat, tears, and symbol overlays
- `08_outfits.md` — body-aligned wearable layers
- `09_head_and_neck_accessories.md` — isolated wearable accessories
- `10_hand_objects.md` — object layers tied to approved hand anchors
- `11_back_accessories.md` — wings, capes, cloaks, crests, and sigils
- `12_auras.md` — rear, floor, and front effects
- `13_backgrounds.md` — full-canvas environments
- `14_extraction_prompt.md` — rebuild one target trait from a flattened reference sheet
- `15_collection_generation_777.md` — exact 777-token output rules
- `16_native_1254_pose_001_candidate.md` — correct one native-resolution relaxed-open review candidate without promoting it to production
- `17_native_1254_backgrounds.md` — rebuild the eight supplied background references one at a time as native production candidates

Generate one asset per output. Never ask an image model to produce an entire final trait category as a single contact sheet.
