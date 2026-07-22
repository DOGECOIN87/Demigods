# Demigods Trait Production Backlog

Last updated: 2026-07-22

This is the ordered production queue for the 1254 × 1254 modular collection. It inventories only assets supported by repository prompts, dedicated reference catalogs, or the eight preserved background references. Character names from the flattened concept sheets are not used as production trait names.

Status values are limited to `pending`, `candidate`, `QA-failed`, `approved`, and `registered`. A reference-sheet cell remains `pending` when its compressed preview is sufficient to identify a distinct design but not sufficient to approve final micro-detail. Such entries must be rebuilt from the cited cell with `prompts/14_extraction_prompt.md`; the preview must never be cropped or enlarged into production art.

## Source keys

| Key | Repository source |
|---|---|
| `POSE` | `images/pose_candidates/` plus `prompts/03_hand_poses.md` |
| `BG` | `images/background_candidates/` plus `prompts/17_native_1254_backgrounds.md` |
| `AURA` | `images/reference_sheets/back_accessories_and_aura_effects_catalog.webp` |
| `HAIR` | `images/reference_sheets/anime_hair_customization_asset_sheet.webp` |
| `OUTFIT` | `images/reference_sheets/fantasy_character_outfits_reference_sheet.webp` |
| `ACCESSORY` | `images/reference_sheets/fantasy_accessory_catalog_sheet.webp` |
| `FACE` | `images/reference_sheets/anime_character_creation_asset_sheet.webp` |
| `HAND` | `images/reference_sheets/fantasy_hand_held_items_asset_sheet.webp` |

The broader and theme-composite sheets in `images/reference_sheets/index.md` corroborate the visual system, but their tiny flattened composite cells are not treated as additional production assets where the same design is already represented in a dedicated catalog. This avoids double-counting baked character combinations as isolated traits.

## Phase A — Base body and pose family

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-001 | base body | Neutral bald, fully clothed shared mannequin master | `POSE` relaxed-open identity reference | Pose 001 must independently qualify | `assets/base_bodies/base_body_001_neutral_master.png` | `prompts/02_base_body.md` | pending |
| DG-002 | base pose | Both hands relaxed and open | `POSE/base_pose_001_relaxed_open_candidate.png`; attempts 002–004 | None; active master gate | `assets/base_bodies/base_pose_001_relaxed_open.png` | `prompts/16_native_1254_pose_001_candidate.md` | QA-failed |
| DG-003 | base pose | Viewer-left vertical grip; viewer-right relaxed | `POSE/base_pose_002_viewer_left_vertical_grip_candidate.png` | DG-002 | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | `prompts/03_hand_poses.md` | pending |
| DG-004 | base pose | Viewer-right vertical grip; viewer-left relaxed | `POSE/base_pose_003_viewer_right_vertical_grip_candidate.png` | DG-002 and grip height from DG-003 | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | `prompts/03_hand_poses.md` | pending |
| DG-005 | base pose | Viewer-left palm-up; viewer-right relaxed | `POSE/base_pose_004_viewer_left_palm_up_candidate.png` | DG-002 | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | `prompts/03_hand_poses.md` | pending |
| DG-006 | base pose | Centered two-handed grip | `POSE/base_pose_005_centered_two_hand_grip_candidate.png` | DG-002 | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | `prompts/03_hand_poses.md` | pending |

## Phase B — Native backgrounds 001–008

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-007 | background | Symmetrical white-marble celestial throne hall with navy drapery, gold ornament, blue carpet, and distant throne | `BG/background_001_celestial_throne_hall_reference.jpg` | None | `assets/backgrounds/background_001_celestial_throne_hall.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-008 | background | Violet gothic sanctum with tall nave, stained glass, dark stone, candles, and central altar | `BG/background_002_violet_gothic_sanctum_reference.jpg` | DG-007 sequential approval | `assets/backgrounds/background_002_violet_gothic_sanctum.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-009 | background | Moonlit arcane library with bookcases, arched window, cyan lights, desks, and abstract floor circle | `BG/background_003_arcane_library_reference.jpg` | DG-008 | `assets/backgrounds/background_003_arcane_library.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-010 | background | Navy-violet cloud dreamscape with crescent, hanging gold stars, and floating platform | `BG/background_004_crescent_star_dreamscape_reference.jpg` | DG-009 | `assets/backgrounds/background_004_crescent_star_dreamscape.png` | `prompts/18_native_1254_background_004_candidate.md` | pending |
| DG-011 | background | White-and-gold open-air solar temple with sky, clouds, star motif, and ceremonial platform | `BG/background_005_solar_sky_temple_reference.jpg` | DG-010 | `assets/backgrounds/background_005_solar_sky_temple.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-012 | background | Moonlit pale-marble balcony with arches, mountains, stars, and cool floor shadows | `BG/background_006_moonlit_marble_balcony_reference.jpg` | DG-011 | `assets/backgrounds/background_006_moonlit_marble_balcony.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-013 | background | Layered white-stone golden gateway with portal light, star emblem, stairs, and plants | `BG/background_007_golden_celestial_gateway_reference.jpg` | DG-012 | `assets/backgrounds/background_007_golden_celestial_gateway.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-014 | background | Circular violet void portal with floating platform, rocks, crystals, and smoke | `BG/background_008_violet_void_portal_reference.jpg` | DG-013 | `assets/backgrounds/background_008_violet_void_portal.png` | `prompts/17_native_1254_backgrounds.md` | pending |

## Phase C — Representative test assets, then remaining backlog in canonical layer order

### Rear auras

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-015 | rear aura | Blue elliptical floor/halo ring; classify behind body unless stress test requires front split | `AURA`, lower row cell 1 | Locked pose family | `assets/rear_auras/aura_rear_001_blue_floor_ring.png` | `prompts/12_auras.md` | pending |
| DG-016 | rear aura | Soft violet circular radial glow | `AURA`, lower row cell 2 | DG-015 representative test | `assets/rear_auras/aura_rear_002_violet_radial_glow.png` | `prompts/12_auras.md` | pending |
| DG-017 | rear aura | Blue crystalline energy burst | `AURA`, lower row cell 3 | DG-015 | `assets/rear_auras/aura_rear_003_blue_crystalline_burst.png` | `prompts/12_auras.md` | pending |
| DG-018 | rear aura | Dark violet rising void flame | `AURA`, lower row cell 4 | DG-015 | `assets/rear_auras/aura_rear_004_violet_void_flame.png` | `prompts/12_auras.md` | pending |
| DG-019 | rear aura | Pale-lavender vertical lightning wisps | `AURA`, lower row cell 5 | DG-015 | `assets/rear_auras/aura_rear_005_lavender_lightning.png` | `prompts/12_auras.md` | pending |
| DG-020 | rear aura | Soft gold radiant glow | `AURA`, lower row cell 6 | DG-015 | `assets/rear_auras/aura_rear_006_gold_radiance.png` | `prompts/12_auras.md` | pending |

### Back accessories

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-021 | back accessory | Pale silver feathered wing pair | `AURA`, upper row cell 1 | Locked pose family | `assets/back_accessories/back_accessory_001_silver_feathered_wings.png` | `prompts/11_back_accessories.md` | pending |
| DG-022 | back accessory | Black-violet bat wing pair | `AURA`, upper row cell 2 | DG-021 representative test | `assets/back_accessories/back_accessory_002_black_violet_bat_wings.png` | `prompts/11_back_accessories.md` | pending |
| DG-023 | back accessory | Translucent cyan fairy wing pair | `AURA`, upper row cell 3 | DG-021 | `assets/back_accessories/back_accessory_003_cyan_fairy_wings.png` | `prompts/11_back_accessories.md` | pending |
| DG-024 | back accessory | Deep navy formal cape | `AURA`, upper row cell 4 | DG-021 | `assets/back_accessories/back_accessory_004_navy_formal_cape.png` | `prompts/11_back_accessories.md` | pending |
| DG-025 | back accessory | Black-purple ragged cloak | `AURA`, upper row cell 5 | DG-021 | `assets/back_accessories/back_accessory_005_black_violet_ragged_cloak.png` | `prompts/11_back_accessories.md` | pending |
| DG-026 | back accessory | Pale-blue crystalline wing/mantle pair | `AURA`, upper row cell 6 | DG-021 | `assets/back_accessories/back_accessory_006_pale_blue_crystal_wings.png` | `prompts/11_back_accessories.md` | pending |
| DG-027 | back accessory | Luminous gold feathered wing pair | `AURA`, upper row cell 7 | DG-021 | `assets/back_accessories/back_accessory_007_gold_luminous_wings.png` | `prompts/11_back_accessories.md` | pending |
| DG-028 | back accessory | Olive-silver mechanical/spiked wing pair | `AURA`, upper row cell 8 | DG-021 | `assets/back_accessories/back_accessory_008_olive_silver_spiked_wings.png` | `prompts/11_back_accessories.md` | pending |

### Hair back

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-029 | hair back | Long wavy gold-blonde rear hair | `HAIR`, upper row cell 1 | Locked scalp and pose | `assets/hair_back/hair_back_001_gold_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-030 | hair back | Long wavy black rear hair | `HAIR`, upper row cell 2 | DG-029 representative test | `assets/hair_back/hair_back_002_black_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-031 | hair back | Long wavy white-silver rear hair | `HAIR`, upper row cell 3 | DG-029 | `assets/hair_back/hair_back_003_silver_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-032 | hair back | Long wavy violet rear hair | `HAIR`, upper row cell 4 | DG-029 | `assets/hair_back/hair_back_004_violet_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-033 | hair back | Long wavy deep-blue rear hair | `HAIR`, upper row cell 5 | DG-029 | `assets/hair_back/hair_back_005_blue_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-034 | hair back | Long wavy pink rear hair | `HAIR`, upper row cell 6 | DG-029 | `assets/hair_back/hair_back_006_pink_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-035 | hair back | Long wavy teal rear hair | `HAIR`, upper row cell 7 | DG-029 | `assets/hair_back/hair_back_007_teal_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-036 | hair back | Long wavy red rear hair | `HAIR`, upper row cell 8 | DG-029 | `assets/hair_back/hair_back_008_red_long_wavy.png` | `prompts/04_hair_back.md` | pending |

### Outfits

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-037 | outfit | White-silver celestial ceremonial robe | `OUTFIT`, row 1 cell 1 | Approved Pose 001 | `assets/outfits/outfit_001_celestial_robe_white_silver.png` | `prompts/08_outfits.md` | pending |
| DG-038 | outfit | Black long coat with split cape tails | `OUTFIT`, row 1 cell 2 | DG-037 representative test | `assets/outfits/outfit_002_black_split_tail_coat.png` | `prompts/08_outfits.md` | pending |
| DG-039 | outfit | Plum-gray long mage robe | `OUTFIT`, row 1 cell 3 | DG-037 | `assets/outfits/outfit_003_plum_gray_mage_robe.png` | `prompts/08_outfits.md` | pending |
| DG-040 | outfit | Black ragged hooded cloak outfit | `OUTFIT`, row 1 cell 4 | DG-037 | `assets/outfits/outfit_004_black_ragged_hooded_cloak.png` | `prompts/08_outfits.md` | pending |
| DG-041 | outfit | White and blue armored ceremonial mantle | `OUTFIT`, row 1 cell 5 | DG-037 | `assets/outfits/outfit_005_white_blue_armored_mantle.png` | `prompts/08_outfits.md` | pending |
| DG-042 | outfit | Black layered hooded long robe | `OUTFIT`, row 2 cell 1 | DG-037 | `assets/outfits/outfit_006_black_layered_hooded_robe.png` | `prompts/08_outfits.md` | pending |
| DG-043 | outfit | Brown leather long coat/robe | `OUTFIT`, row 2 cell 2 | DG-037 | `assets/outfits/outfit_007_brown_leather_long_coat.png` | `prompts/08_outfits.md` | pending |
| DG-044 | outfit | Olive-green ragged cloak outfit | `OUTFIT`, row 2 cell 3 | DG-037 | `assets/outfits/outfit_008_olive_ragged_cloak.png` | `prompts/08_outfits.md` | pending |
| DG-045 | outfit | Deep-navy high-collar long coat | `OUTFIT`, row 2 cell 4 | DG-037 | `assets/outfits/outfit_009_navy_high_collar_coat.png` | `prompts/08_outfits.md` | pending |
| DG-046 | outfit | Silver-white high-collar ceremonial robe | `OUTFIT`, row 2 cell 5; naming example in `docs/naming-and-export.md` | DG-037 | `assets/outfits/outfit_010_celestial_robe_white_gold.png` | `prompts/08_outfits.md` | pending |

### Neck accessories

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-047 | neck accessory | Plain black curved choker | `ACCESSORY`, lower row cell 1 | Approved Pose 001 and outfit test | `assets/neck_accessories/neck_accessory_001_black_choker.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-048 | neck accessory | Warm-gold choker with dark-blue drop | `ACCESSORY`, lower row cell 2 | DG-047 representative test | `assets/neck_accessories/neck_accessory_002_gold_blue_drop_choker.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-049 | neck accessory | Black ribbon bow | `ACCESSORY`, lower row cell 3 | DG-047 | `assets/neck_accessories/neck_accessory_003_black_ribbon_bow.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-050 | neck accessory | Fine silver chain with dark round pendant | `ACCESSORY`, lower row cell 4 | DG-047 | `assets/neck_accessories/neck_accessory_004_silver_dark_round_pendant.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-051 | neck accessory | Silver V-chain with long navy pendant | `ACCESSORY`, lower row cell 5 | DG-047 | `assets/neck_accessories/neck_accessory_005_silver_navy_long_pendant.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-052 | neck accessory | Fine silver chain with pale circular charm | `ACCESSORY`, lower row cell 6 | DG-047 | `assets/neck_accessories/neck_accessory_006_silver_pale_circle_charm.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-053 | neck accessory | Gold chain with long teardrop pendant | `ACCESSORY`, lower row cell 7 | DG-047 | `assets/neck_accessories/neck_accessory_007_gold_teardrop_pendant.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-054 | neck accessory | Violet ribbon bow | `ACCESSORY`, lower row cell 8 | DG-047 | `assets/neck_accessories/neck_accessory_008_violet_ribbon_bow.png` | `prompts/09_head_and_neck_accessories.md` | pending |

### Eyes

The 24 eye pairs below are distinct visible cells in the dedicated facial-trait sheet. Color adjectives are intentionally conservative; exact liner, iris, pupil, catchlight, and gradient detail must follow the cited cell.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-055 | eyes | Dark neutral eye pair, cell r1c1 | `FACE`, eyes r1c1 | Approved face anchors | `assets/eyes/eyes_001_sheet_r1c1_dark_neutral.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-056 | eyes | Dark eye pair, cell r1c2 | `FACE`, eyes r1c2 | DG-055 representative test | `assets/eyes/eyes_002_sheet_r1c2_dark.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-057 | eyes | Dark eye pair, cell r1c3 | `FACE`, eyes r1c3 | DG-055 | `assets/eyes/eyes_003_sheet_r1c3_dark.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-058 | eyes | Deep-olive eye pair, cell r1c4 | `FACE`, eyes r1c4 | DG-055 | `assets/eyes/eyes_004_sheet_r1c4_deep_olive.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-059 | eyes | Deep-blue eye pair, cell r1c5 | `FACE`, eyes r1c5 | DG-055 | `assets/eyes/eyes_005_sheet_r1c5_deep_blue.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-060 | eyes | Violet eye pair, cell r1c6 | `FACE`, eyes r1c6 | DG-055 | `assets/eyes/eyes_006_sheet_r1c6_violet.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-061 | eyes | Near-black eye pair, cell r1c7 | `FACE`, eyes r1c7 | DG-055 | `assets/eyes/eyes_007_sheet_r1c7_near_black.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-062 | eyes | Dark-brown eye pair, cell r1c8 | `FACE`, eyes r1c8 | DG-055 | `assets/eyes/eyes_008_sheet_r1c8_dark_brown.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-063 | eyes | Gold eye pair, cell r2c1 | `FACE`, eyes r2c1 | DG-055 | `assets/eyes/eyes_009_sheet_r2c1_gold.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-064 | eyes | Yellow-green eye pair, cell r2c2 | `FACE`, eyes r2c2 | DG-055 | `assets/eyes/eyes_010_sheet_r2c2_yellow_green.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-065 | eyes | Cyan eye pair, cell r2c3 | `FACE`, eyes r2c3 | DG-055 | `assets/eyes/eyes_011_sheet_r2c3_cyan.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-066 | eyes | Emerald eye pair, cell r2c4 | `FACE`, eyes r2c4 | DG-055 | `assets/eyes/eyes_012_sheet_r2c4_emerald.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-067 | eyes | Crimson eye pair, cell r2c5 | `FACE`, eyes r2c5 | DG-055 | `assets/eyes/eyes_013_sheet_r2c5_crimson.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-068 | eyes | Magenta eye pair, cell r2c6 | `FACE`, eyes r2c6 | DG-055 | `assets/eyes/eyes_014_sheet_r2c6_magenta.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-069 | eyes | Charcoal eye pair, cell r2c7 | `FACE`, eyes r2c7 | DG-055 | `assets/eyes/eyes_015_sheet_r2c7_charcoal.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-070 | eyes | Black eye pair, cell r2c8 | `FACE`, eyes r2c8 | DG-055 | `assets/eyes/eyes_016_sheet_r2c8_black.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-071 | eyes | Dark neutral eye pair, cell r3c1 | `FACE`, eyes r3c1 | DG-055 | `assets/eyes/eyes_017_sheet_r3c1_dark_neutral.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-072 | eyes | Gray eye pair, cell r3c2 | `FACE`, eyes r3c2 | DG-055 | `assets/eyes/eyes_018_sheet_r3c2_gray.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-073 | eyes | Rose eye pair, cell r3c3 | `FACE`, eyes r3c3 | DG-055 | `assets/eyes/eyes_019_sheet_r3c3_rose.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-074 | eyes | Pink eye pair, cell r3c4 | `FACE`, eyes r3c4 | DG-055 | `assets/eyes/eyes_020_sheet_r3c4_pink.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-075 | eyes | Amber eye pair, cell r3c5 | `FACE`, eyes r3c5 | DG-055 | `assets/eyes/eyes_021_sheet_r3c5_amber.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-076 | eyes | Orange-gold eye pair, cell r3c6 | `FACE`, eyes r3c6 | DG-055 | `assets/eyes/eyes_022_sheet_r3c6_orange_gold.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-077 | eyes | Charcoal eye pair, cell r3c7 | `FACE`, eyes r3c7 | DG-055 | `assets/eyes/eyes_023_sheet_r3c7_charcoal.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-078 | eyes | Black eye pair, cell r3c8 | `FACE`, eyes r3c8 | DG-055 | `assets/eyes/eyes_024_sheet_r3c8_black.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |

### Eyebrows

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-079 | eyebrows | Matched pair, reference cell r1c1 | `FACE`, eyebrows r1c1 | Approved face anchors | `assets/eyebrows/eyebrows_001_sheet_r1c1.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-080 | eyebrows | Matched pair, reference cell r1c2 | `FACE`, eyebrows r1c2 | DG-079 representative test | `assets/eyebrows/eyebrows_002_sheet_r1c2.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-081 | eyebrows | Matched pair, reference cell r1c3 | `FACE`, eyebrows r1c3 | DG-079 | `assets/eyebrows/eyebrows_003_sheet_r1c3.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-082 | eyebrows | Matched pair, reference cell r1c4 | `FACE`, eyebrows r1c4 | DG-079 | `assets/eyebrows/eyebrows_004_sheet_r1c4.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-083 | eyebrows | Matched pair, reference cell r2c1 | `FACE`, eyebrows r2c1 | DG-079 | `assets/eyebrows/eyebrows_005_sheet_r2c1.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-084 | eyebrows | Matched pair, reference cell r2c2 | `FACE`, eyebrows r2c2 | DG-079 | `assets/eyebrows/eyebrows_006_sheet_r2c2.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-085 | eyebrows | Matched pair, reference cell r2c3 | `FACE`, eyebrows r2c3 | DG-079 | `assets/eyebrows/eyebrows_007_sheet_r2c3.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-086 | eyebrows | Matched pair, reference cell r2c4 | `FACE`, eyebrows r2c4 | DG-079 | `assets/eyebrows/eyebrows_008_sheet_r2c4.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-087 | eyebrows | Matched pair, reference cell r3c1 | `FACE`, eyebrows r3c1 | DG-079 | `assets/eyebrows/eyebrows_009_sheet_r3c1.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-088 | eyebrows | Matched pair, reference cell r3c2 | `FACE`, eyebrows r3c2 | DG-079 | `assets/eyebrows/eyebrows_010_sheet_r3c2.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-089 | eyebrows | Matched pair, reference cell r3c3 | `FACE`, eyebrows r3c3 | DG-079 | `assets/eyebrows/eyebrows_011_sheet_r3c3.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-090 | eyebrows | Matched pair, reference cell r3c4 | `FACE`, eyebrows r3c4 | DG-079 | `assets/eyebrows/eyebrows_012_sheet_r3c4.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-091 | eyebrows | Matched pair, reference cell r4c1 | `FACE`, eyebrows r4c1 | DG-079 | `assets/eyebrows/eyebrows_013_sheet_r4c1.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-092 | eyebrows | Matched pair, reference cell r4c2 | `FACE`, eyebrows r4c2 | DG-079 | `assets/eyebrows/eyebrows_014_sheet_r4c2.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-093 | eyebrows | Matched pair, reference cell r4c3 | `FACE`, eyebrows r4c3 | DG-079 | `assets/eyebrows/eyebrows_015_sheet_r4c3.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-094 | eyebrows | Matched pair, reference cell r4c4 | `FACE`, eyebrows r4c4 | DG-079 | `assets/eyebrows/eyebrows_016_sheet_r4c4.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |

### Mouths

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-095 | mouth | Fine closed neutral mouth, cell r1c1 | `FACE`, mouths r1c1 | Approved mouth anchor | `assets/mouths/mouth_001_closed_neutral.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-096 | mouth | Small pink open smile, cell r1c2 | `FACE`, mouths r1c2 | DG-095 representative test | `assets/mouths/mouth_002_small_open_smile.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-097 | mouth | Small dark open/fang mouth, cell r1c3 | `FACE`, mouths r1c3 | DG-095 | `assets/mouths/mouth_003_small_dark_open.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-098 | mouth | Wide pink open smile, cell r1c4 | `FACE`, mouths r1c4 | DG-095 | `assets/mouths/mouth_004_wide_open_smile.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-099 | mouth | Fine short mouth line, cell r2c1 | `FACE`, mouths r2c1 | DG-095 | `assets/mouths/mouth_005_short_line.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-100 | mouth | Small soft curve, cell r2c2 | `FACE`, mouths r2c2 | DG-095 | `assets/mouths/mouth_006_soft_curve.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-101 | mouth | Fine flat line, cell r2c3 | `FACE`, mouths r2c3 | DG-095 | `assets/mouths/mouth_007_flat_line.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-102 | mouth | Small downturned/open mouth, cell r2c4 | `FACE`, mouths r2c4 | DG-095 | `assets/mouths/mouth_008_small_downturned.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-103 | mouth | Tiny neutral mark, cell r3c1 | `FACE`, mouths r3c1 | DG-095 | `assets/mouths/mouth_009_tiny_neutral.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-104 | mouth | Tiny curved mark, cell r3c2 | `FACE`, mouths r3c2 | DG-095 | `assets/mouths/mouth_010_tiny_curve.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-105 | mouth | Pink open pout, cell r3c3 | `FACE`, mouths r3c3 | DG-095 | `assets/mouths/mouth_011_pink_open_pout.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |
| DG-106 | mouth | Tiny dark round mouth, cell r3c4 | `FACE`, mouths r3c4 | DG-095 | `assets/mouths/mouth_012_tiny_round.png` | `prompts/06_eyes_eyebrows_mouths.md` | pending |

### Expression marks

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-107 | expression mark | Pink blush strokes | `FACE`, expression marks r1c1 | Approved face anchors | `assets/expression_marks/expression_mark_001_pink_blush_strokes.png` | `prompts/07_expression_marks.md` | pending |
| DG-108 | expression mark | Yellow stress/attention marks | `FACE`, expression marks r1c2 | DG-107 representative test | `assets/expression_marks/expression_mark_002_yellow_stress_marks.png` | `prompts/07_expression_marks.md` | pending |
| DG-109 | expression mark | Dark vertical gloom lines | `FACE`, expression marks r1c3 | DG-107 | `assets/expression_marks/expression_mark_003_dark_gloom_lines.png` | `prompts/07_expression_marks.md` | pending |
| DG-110 | expression mark | Gold sparkle/star | `FACE`, expression marks r1c4 | DG-107 | `assets/expression_marks/expression_mark_004_gold_sparkle.png` | `prompts/07_expression_marks.md` | pending |
| DG-111 | expression mark | Cyan sweat drop | `FACE`, expression marks r2c1 | DG-107 | `assets/expression_marks/expression_mark_005_cyan_sweat_drop.png` | `prompts/07_expression_marks.md` | pending |
| DG-112 | expression mark | Pink anger cross | `FACE`, expression marks r2c2 | DG-107 | `assets/expression_marks/expression_mark_006_pink_anger_cross.png` | `prompts/07_expression_marks.md` | pending |
| DG-113 | expression mark | Yellow-green square emphasis mark | `FACE`, expression marks r2c3 | DG-107 | `assets/expression_marks/expression_mark_007_yellow_green_emphasis.png` | `prompts/07_expression_marks.md` | pending |
| DG-114 | expression mark | Pink curved motion/surprise mark | `FACE`, expression marks r2c4 | DG-107 | `assets/expression_marks/expression_mark_008_pink_curved_mark.png` | `prompts/07_expression_marks.md` | pending |

### Hair front

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-115 | hair front | Gold-blonde parted bangs and face-framing strands | `HAIR`, lower row cell 1 | Matching DG-029 and approved face opening | `assets/hair_front/hair_front_001_gold_parted_bangs.png` | `prompts/05_hair_front.md` | pending |
| DG-116 | hair front | Black side-swept bangs and face-framing strands | `HAIR`, lower row cell 2 | DG-115 representative test; matching DG-030 | `assets/hair_front/hair_front_002_black_side_swept.png` | `prompts/05_hair_front.md` | pending |
| DG-117 | hair front | White-silver straight bangs and face-framing strands | `HAIR`, lower row cell 3 | Matching DG-031 | `assets/hair_front/hair_front_003_silver_straight_bangs.png` | `prompts/05_hair_front.md` | pending |
| DG-118 | hair front | Violet parted bangs and face-framing strands | `HAIR`, lower row cell 4 | Matching DG-032 | `assets/hair_front/hair_front_004_violet_parted_bangs.png` | `prompts/05_hair_front.md` | pending |
| DG-119 | hair front | Deep-blue pointed bangs and face-framing strands | `HAIR`, lower row cell 5 | Matching DG-033 | `assets/hair_front/hair_front_005_blue_pointed_bangs.png` | `prompts/05_hair_front.md` | pending |
| DG-120 | hair front | Pink soft bangs and face-framing strands | `HAIR`, lower row cell 6 | Matching DG-034 | `assets/hair_front/hair_front_006_pink_soft_bangs.png` | `prompts/05_hair_front.md` | pending |
| DG-121 | hair front | Teal open-center face-framing strands | `HAIR`, lower row cell 7 | Matching DG-035 | `assets/hair_front/hair_front_007_teal_open_center.png` | `prompts/05_hair_front.md` | pending |
| DG-122 | hair front | Red short bangs and face-framing strands | `HAIR`, lower row cell 8 | Matching DG-036 | `assets/hair_front/hair_front_008_red_short_bangs.png` | `prompts/05_hair_front.md` | pending |

### Head accessories

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-123 | head accessory | Gold pointed crown | `ACCESSORY`, upper group cell 1 | Approved head/hair composite | `assets/head_accessories/head_accessory_001_gold_pointed_crown.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-124 | head accessory | Large gold halo ring | `ACCESSORY`, upper group cell 2; compatibility example | DG-123 representative test | `assets/head_accessories/head_accessory_002_large_gold_halo.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-125 | head accessory | Green laurel wreath | `ACCESSORY`, upper group cell 3 | DG-123 | `assets/head_accessories/head_accessory_003_green_laurel.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-126 | head accessory | Balanced black curved horn set | `ACCESSORY`, upper group cells 4–5 as one pair | DG-123 | `assets/head_accessories/head_accessory_004_black_curved_horns.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-127 | head accessory | Silver winged circlet | `ACCESSORY`, upper group cell 6 | DG-123 | `assets/head_accessories/head_accessory_005_silver_winged_circlet.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-128 | head accessory | Silver ornate tiara | `ACCESSORY`, upper group cell 7 | DG-123 | `assets/head_accessories/head_accessory_006_silver_ornate_tiara.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-129 | head accessory | Silver forehead circlet with central drop | `ACCESSORY`, upper group cell 8 | DG-123 | `assets/head_accessories/head_accessory_007_silver_drop_circlet.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-130 | head accessory | Translucent white veil | `ACCESSORY`, upper group cell 9 | DG-123 | `assets/head_accessories/head_accessory_008_translucent_white_veil.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-131 | head accessory | Pale-blue spiked crown/tiara | `ACCESSORY`, upper group cell 10 | DG-123 | `assets/head_accessories/head_accessory_009_pale_blue_spiked_tiara.png` | `prompts/09_head_and_neck_accessories.md` | pending |
| DG-132 | head accessory | Gold low-profile circlet | `ACCESSORY`, upper group cell 11 | DG-123 | `assets/head_accessories/head_accessory_010_gold_low_circlet.png` | `prompts/09_head_and_neck_accessories.md` | pending |

### Hand objects

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-133 | hand object | Gnarled wood staff with blue flame/crystal | `HAND`, r1c1 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_001_arcane_staff_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-134 | hand object | Purple crystal orb | `HAND`, r1c2 | DG-005 viewer-left palm-up | `assets/hand_objects/hand_object_002_violet_orb_pose_004_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-135 | hand object | Slender dark wand | `HAND`, r1c3 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_003_dark_wand_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-136 | hand object | Silver straight sword | `HAND`, r1c4 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_004_silver_sword_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-137 | hand object | Dark spellbook with gold star emblem | `HAND`, r1c5 | DG-005 viewer-left palm-up | `assets/hand_objects/hand_object_005_star_spellbook_pose_004_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-138 | hand object | Warm-gold hanging lantern | `HAND`, r1c6 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_006_gold_lantern_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-139 | hand object | Gold staff with blue gem | `HAND`, r2c1 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_007_gold_blue_gem_staff_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-140 | hand object | Blue crescent-moon staff | `HAND`, r2c2 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_008_blue_crescent_staff_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-141 | hand object | Violet short blade/dagger | `HAND`, r2c3 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_009_violet_blade_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-142 | hand object | Horned skull scepter | `HAND`, r2c4 | DG-003 viewer-left vertical grip | `assets/hand_objects/hand_object_010_horned_skull_scepter_pose_002_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-143 | hand object | Round dark compass/watch talisman | `HAND`, r2c5 | DG-005 viewer-left palm-up | `assets/hand_objects/hand_object_011_round_talisman_pose_004_left.png` | `prompts/10_hand_objects.md` | pending |
| DG-144 | hand object | Brown closed tome | `HAND`, r2c6 | DG-005 viewer-left palm-up | `assets/hand_objects/hand_object_012_brown_tome_pose_004_left.png` | `prompts/10_hand_objects.md` | pending |

### Front auras

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-145 | front aura | Orange rising foreground flame | `AURA`, lower row cell 7 | Rear-aura representative and composite tests | `assets/front_auras/aura_front_001_orange_rising_flame.png` | `prompts/12_auras.md` | pending |
| DG-146 | front aura | Gold vertical foreground light pillars | `AURA`, lower row cell 8 | DG-145 representative test | `assets/front_auras/aura_front_002_gold_light_pillars.png` | `prompts/12_auras.md` | pending |

## Global-finish source gate

`16_global_finish` exists in the canonical layer stack and validator, but no distinct global-finish artwork is identifiable in the compressed repository reference sheets and no dedicated global-finish prompt defines a visual design. No `global_finish_001` asset is invented in this backlog. Before the representative global-finish test, the repository needs either an explicit reference cell or a narrowly defined finish treatment that remains a separate transparent layer.

## Execution rule

After DG-002 is registered and DG-003–DG-006 are normalized, produce the first entry of each remaining category in canonical layer order. Run cross-category composites before continuing each category's later IDs. Hand objects may be produced only against the approved pose named in their dependency column.
