# Demigods Trait Production Backlog

Last updated: 2026-07-27

This is the ordered production-registration queue for the 1254 × 1254 modular collection. Candidate generation may happen in parallel or out of order under `prompts/19_individual_trait_asset_co_creation.md`, but registration still follows dependencies and QA. The backlog inventories only assets supported by repository prompts, dedicated reference catalogs, or the eight preserved background references. Character names from the flattened concept sheets are not used as production trait names.

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
| `RING` | `images/reference_sheets/floor_ring_aura_variants_sheet.png` |
| `BG2` | `images/background_candidates_round_two/` |

The broader and theme-composite sheets in `images/reference_sheets/index.md` corroborate the visual system, but their tiny flattened composite cells are not treated as additional production assets where the same design is already represented in a dedicated catalog. This avoids double-counting baked character combinations as isolated traits.

## Phase A — Base body and pose family

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-001 | base body | Neutral bald, fully clothed shared mannequin master | `POSE` relaxed-open identity reference | Pose 001 must independently qualify | `assets/base_bodies/base_body_001_neutral_master.png` | `prompts/16_native_1254_pose_001_candidate.md` | registered |
| DG-002 | base pose | Both hands relaxed and open | native master `base_body_001_neutral_master.png` | fulfilled by approved neutral master | `assets/base_bodies/base_body_001_neutral_master.png` | `prompts/16_native_1254_pose_001_candidate.md` | registered |
| DG-003 | base pose | Viewer-left vertical grip; viewer-right relaxed | native master `base_body_001_neutral_master.png` | DG-002 | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | `prompts/03_hand_poses.md` | registered |
| DG-004 | base pose | Viewer-right vertical grip; viewer-left relaxed | native master `base_body_001_neutral_master.png` | DG-002 and grip height from DG-003 | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | `prompts/03_hand_poses.md` | registered |
| DG-005 | base pose | Viewer-left palm-up; viewer-right relaxed | native master `base_body_001_neutral_master.png` | DG-002 | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | `prompts/03_hand_poses.md` | registered |
| DG-006 | base pose | Centered two-handed grip | native master `base_body_001_neutral_master.png` | DG-002 | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | `prompts/03_hand_poses.md` | registered |

## Phase B — Native backgrounds 001–008

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-007 | background | Symmetrical white-marble celestial throne hall with navy drapery, gold ornament, blue carpet, and distant throne | `BG/background_001_celestial_throne_hall_reference.jpg` | None | `assets/backgrounds/background_001_celestial_throne_hall.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-008 | background | Violet gothic sanctum with tall nave, stained glass, dark stone, candles, and central altar | `BG/background_002_violet_gothic_sanctum_reference.jpg` | DG-007 sequential approval | `assets/backgrounds/background_002_violet_gothic_sanctum.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-009 | background | Moonlit arcane library with bookcases, arched window, cyan lights, desks, and abstract floor circle | `BG/background_003_arcane_library_reference.jpg` | DG-008 | `assets/backgrounds/background_003_arcane_library.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-010 | background | Navy-violet cloud dreamscape with crescent, hanging gold stars, and floating platform | `BG/background_004_crescent_star_dreamscape_reference.jpg` | DG-009 | `assets/backgrounds/background_004_crescent_star_dreamscape.png` | `prompts/18_native_1254_background_004_candidate.md` | registered |
| DG-011 | background | White-and-gold open-air solar temple with sky, clouds, star motif, and ceremonial platform | `BG/background_005_solar_sky_temple_reference.jpg` | DG-010 | `assets/backgrounds/background_005_solar_sky_temple.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-012 | background | Moonlit pale-marble balcony with arches, mountains, stars, and cool floor shadows | `BG/background_006_moonlit_marble_balcony_reference.jpg` | DG-011 | `assets/backgrounds/background_006_moonlit_marble_balcony.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-013 | background | Layered white-stone golden gateway with portal light, star emblem, stairs, and plants | `BG/background_007_golden_celestial_gateway_reference.jpg` | DG-012 | `assets/backgrounds/background_007_golden_celestial_gateway.png` | `prompts/17_native_1254_backgrounds.md` | registered |
| DG-014 | background | Circular violet void portal with floating platform, rocks, crystals, and smoke | `BG/background_008_violet_void_portal_reference.jpg` | DG-013 | `assets/backgrounds/background_008_violet_void_portal.png` | `prompts/17_native_1254_backgrounds.md` | registered |

## Phase B2 — Second background wave (added 2026-07-27)

Six further directions supplied by the maintainer, preserved in
`images/background_candidates_round_two/`. They sit in their own directory
because `validate_assets.py` pins `images/background_candidates/` to exactly
eight 1024 × 1024 files and verifies them byte for byte; five of these are
784 × 1168, so adding them there would have meant weakening that guarantee.

They also broaden the palette usefully — the registered four are all navy,
violet and gold, while this wave adds green, ember and warm brass.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-158 | background | Luminous world-tree grove with fireflies, moss floor, and green canopy | `BG2` world tree | Staging review | `assets/backgrounds/background_009_luminous_world_tree.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-159 | background | Infinite arcane library with floating books, arched window, and starfield | `BG2` infinite library | Staging review | `assets/backgrounds/background_010_infinite_arcane_library.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-160 | background | Ember ruins with broken arches, cracked lava ground, and smoke sky | `BG2` ember ruins | Staging review | `assets/backgrounds/background_011_ember_ruins.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-161 | background | Clockwork sanctum with brass gears, lanterns, and a raised circular platform | `BG2` clockwork sanctum | Staging review | `assets/backgrounds/background_012_clockwork_sanctum.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-162 | background | Crystal spire peak above cloud sea with violet and cyan crystals | `BG2` crystal spire | **Needs a floor plane** | `assets/backgrounds/background_013_crystal_spire_peak.png` | `prompts/17_native_1254_backgrounds.md` | pending |
| DG-163 | background | Skybound isles with waterfalls, a lit bridge, and cloud vista | `BG2` skybound isles | **Needs a floor plane** | `assets/backgrounds/background_014_skybound_isles.png` | `prompts/17_native_1254_backgrounds.md` | pending |

### Staging review — read before rendering these

Every background must give the character a surface to stand on at foot baseline
Y 1139, because the registered floor-ring auras are seated there and the feet
must not float.

- **DG-158, DG-159, DG-160, DG-161** have usable ground. DG-161 is the strongest:
  its raised circular platform sits almost exactly where the rig needs one.
- **DG-162 and DG-163 do not.** Both are aerial vistas — a spire summit and a
  cloud-level island view — with no floor plane at the bottom of frame. Rendered
  as-is the character would stand on empty sky and the floor ring would hang in
  the air. Each needs a foreground ledge, platform, or path introduced at the
  foot baseline during the native render. That is a composition change from the
  reference, and it must be deliberate.

### Preview findings (2026-07-27)

A preview sheet was built by bottom-cropping each reference to square, scaling to
1254, applying the standard grade, and compositing the registered layers:
`docs/qa/composites/sheet_100_new_backgrounds_preview_2026-07-27.png`. These are
**previews only** — resampled references, never production assets.

- The grade integrates all six cleanly with the registered four. Measured edge
  energy inside the staging region is **1.9** for the new six against **2.0** for
  the registered four, so they are marginally calmer, not busier. An initial
  impression that they would compete more with the character was wrong.
- They are darker and moodier than the registered set, which increases figure
  separation rather than reducing it.
- The staging concern is confirmed. `docs/qa/composites/new_backgrounds_staging_check_2026-07-27.png`
  shows DG-161 clockwork resting correctly on floorboards, while DG-162 crystal
  spire leaves the ring hovering over broken terrain and DG-163 skybound isles
  leaves it hanging in open void. Bottom-cropping the reference does not create a
  floor; the native render has to introduce one.

All six references are portrait 784 × 1168 or square 1024 × 1024. Production is
1254 × 1254, so each must be **recomposed** natively, not cropped or letterboxed.
The portrait framing in particular will not survive a straight crop: the vertical
subject has to be rebuilt for a square frame.

Generate sharp and unvignetted; apply `scripts/apply_background_depth.py` after,
as with 001–004.

## Phase C — Representative test assets, then remaining backlog in canonical layer order

External co-created candidates may be generated in batches before Pose 001 is approved. They must follow `prompts/19_individual_trait_asset_co_creation.md` and remain under `images/trait_candidates/<category>/` until repository QA, dependency composites, and human approval pass.

### Rear auras

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-015 | rear aura | Blue elliptical floor/halo ring; classify behind body unless stress test requires front split | `AURA`, lower row cell 1 | Locked pose family | `assets/rear_auras/aura_rear_001_blue_floor_ring.png` | `prompts/12_auras.md` | registered |
| DG-016 | rear aura | Soft violet circular radial glow | `AURA`, lower row cell 2 | DG-015 representative test | `assets/rear_auras/aura_rear_002_violet_radial_glow.png` | `prompts/12_auras.md` | pending |
| DG-017 | rear aura | Blue crystalline energy burst | `AURA`, lower row cell 3 | DG-015 | `assets/rear_auras/aura_rear_003_blue_crystalline_burst.png` | `prompts/12_auras.md` | pending |
| DG-018 | rear aura | Dark violet rising void flame | `AURA`, lower row cell 4 | DG-015 | `assets/rear_auras/aura_rear_004_violet_void_flame.png` | `prompts/12_auras.md` | pending |
| DG-019 | rear aura | Pale-lavender vertical lightning wisps | `AURA`, lower row cell 5 | DG-015 | `assets/rear_auras/aura_rear_005_lavender_lightning.png` | `prompts/12_auras.md` | pending |
| DG-020 | rear aura | Soft gold radiant glow | `AURA`, lower row cell 6 | DG-015 | `assets/rear_auras/aura_rear_006_gold_radiance.png` | `prompts/12_auras.md` | registered |

#### Floor-ring aura family — `RING` sheet (added 2026-07-27)

`images/reference_sheets/floor_ring_aura_variants_sheet.png` supplies twelve floor rings sharing one elliptical form. Cell 1 is the blue double ring already covered by DG-015, so the remaining eleven extend the category. Unlike the compressed catalog previews, this sheet is full resolution and its designs are unambiguous.

The neon variants are the *same geometry* in a different palette, so they are rendered by `scripts/build_aura_floor_ring.py --palette <name>` and are pixel-identical in form to DG-015. The textured variants carry organic detail that a distance field cannot express and go to the image generator.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-147 | rear aura | Green neon double ring (procedural `--palette green`) | `RING`, cell 2 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_007_green_neon_ring.png` | `scripts/build_aura_floor_ring.py` | registered |
| DG-148 | rear aura | Gold neon double ring (procedural `--palette gold`) | `RING`, cell 3 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_008_gold_neon_ring.png` | `scripts/build_aura_floor_ring.py` | registered |
| DG-149 | rear aura | Pink neon double ring (procedural `--palette pink`) | `RING`, cell 4 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_009_pink_neon_ring.png` | `scripts/build_aura_floor_ring.py` | registered |
| DG-150 | rear aura | White-silver neon double ring (procedural `--palette white`) | `RING`, cell 5 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_010_white_neon_ring.png` | `scripts/build_aura_floor_ring.py` | registered |
| DG-151 | rear aura | Orange fire ring (generator) | `RING`, cell 6 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_011_fire_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |
| DG-152 | rear aura | Blue lightning ring (generator) | `RING`, cell 7 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_012_lightning_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |
| DG-153 | rear aura | Violet flame ring (generator) | `RING`, cell 8 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_013_violet_flame_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |
| DG-154 | rear aura | Pale-blue ice crystal ring (generator) | `RING`, cell 9 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_014_ice_crystal_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |
| DG-155 | rear aura | Black smoke void ring (generator) | `RING`, cell 10 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_015_smoke_void_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |
| DG-156 | rear aura | Violet cosmic sparkle ring (generator) | `RING`, cell 11 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_016_cosmic_sparkle_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |
| DG-157 | rear aura | Cyan water splash ring (generator) | `RING`, cell 12 | DG-015 seating and gate mode | `assets/rear_auras/aura_rear_017_water_splash_ring.png` | `prompts/19_individual_trait_asset_co_creation.md` | pending |

All eleven are ground-plane effects and are gated with `rig_gate_report.py --floor-aura`. The generator variants must match DG-015's seating exactly so the family stacks consistently: same ellipse, same foot-baseline placement, differing only in surface treatment.

#### Production route per aura cell (assessed 2026-07-27)

The aura catalog's lower row splits cleanly into geometric and organic designs. Geometric cells are rendered analytically by repository scripts, which removes the matte-fringe and stray-pixel failures that background removal introduces. Organic cells still need an image generator driven by `prompts/19`.

Backlog IDs sit in the second column here: this is a routing reference, not a
backlog table, and the ledger parser treats a `DG-` value in the first column as
a schema row.

| Cell reading | Backlog ID | Route | Script |
|---|---|---|---|
| Elliptical ring band | DG-015 | procedural | `scripts/build_aura_floor_ring.py` |
| Violet circle with **radiating spoke texture**, not a plain gradient | DG-016 | generator, or procedural spokes plus hand finish | — |
| Angular crystalline shards | DG-017 | generator | — |
| Rising flame with organic curl | DG-018 | generator | — |
| Branching lightning wisps | DG-019 | generator | — |
| Smooth pale-gold falloff, no internal structure | DG-020 | procedural | `scripts/build_aura_radiance.py` |

DG-016 was initially assessed as a plain radial gradient. Inspection of the cell at magnification shows radiating internal structure, so it is **not** a straight companion to DG-020 and should not be routed as one.

Ground-plane effects (DG-015) are gated with `rig_gate_report.py --floor-aura`; body-centered effects (DG-016, DG-020) use `--trait` and stay inside the locked character bounds.

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
| DG-031 | hair back | Long wavy white-silver rear hair | `HAIR`, upper row cell 3 | representative hair-back test (this asset) | `assets/hair_back/hair_back_003_silver_long_wavy.png` | `prompts/04_hair_back.md` | **registered** |
| DG-032 | hair back | Long wavy violet rear hair | `HAIR`, upper row cell 4 | DG-029 | `assets/hair_back/hair_back_004_violet_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-033 | hair back | Long wavy deep-blue rear hair | `HAIR`, upper row cell 5 | DG-029 | `assets/hair_back/hair_back_005_blue_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-034 | hair back | Long wavy pink rear hair | `HAIR`, upper row cell 6 | DG-029 | `assets/hair_back/hair_back_006_pink_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-035 | hair back | Long wavy teal rear hair | `HAIR`, upper row cell 7 | DG-029 | `assets/hair_back/hair_back_007_teal_long_wavy.png` | `prompts/04_hair_back.md` | pending |
| DG-036 | hair back | Long wavy red rear hair | `HAIR`, upper row cell 8 | DG-029 | `assets/hair_back/hair_back_008_red_long_wavy.png` | `prompts/04_hair_back.md` | pending |

#### No recoloring shortcut for the hair-back family (assessed 2026-07-27)

DG-029 through DG-036 are described as "long wavy [colour] rear hair", which invites recolouring the registered silver DG-031 into the remaining seven. **Do not.** The eight upper-row cells are distinct cuts, not one design in eight colours: measured ink heights across the row span 20–27 px on a ~24 px cell, a 29% spread, and cell 3 (silver) is visibly shorter and straighter than cell 4 (violet), while cells 1, 7, and 8 differ again in layering and volume.

The sheet is 128 × 96, so each cell is roughly 15 × 25 px — enough to establish that the silhouettes differ, not enough to approve micro-detail. Each colour must be rendered natively from its own cited cell, as the general reference-preview rule at the top of this file already requires.

#### Interim hair recolours — DG-169 to DG-175 (added 2026-07-27)

A 50-token random sample showed **identical hair on every token**: `hair_back`
held one registered asset, making hair the most repetitive element in the
collection — more so than the robes. These seven recolours reduce that until
painted hair lands.

Produced by `scripts/build_hair_recolour.py` from the registered DG-031 silver
layer. Luminance is normalised across the source's actual opaque range (78–185)
and remapped through a three-stop palette, so strand separation, wave structure
and the upper-left key light all survive; only hue and value shift. Alpha is
copied through untouched, so the gate result is identical to the source.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-169 | hair back | Gold-blonde recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_011_recolour_gold.png` | `scripts/build_hair_recolour.py` | registered |
| DG-170 | hair back | Black recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_012_recolour_black.png` | `scripts/build_hair_recolour.py` | registered |
| DG-171 | hair back | Violet recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_013_recolour_violet.png` | `scripts/build_hair_recolour.py` | registered |
| DG-172 | hair back | Deep-blue recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_014_recolour_blue.png` | `scripts/build_hair_recolour.py` | registered |
| DG-173 | hair back | Pink recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_015_recolour_pink.png` | `scripts/build_hair_recolour.py` | registered |
| DG-174 | hair back | Teal recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_016_recolour_teal.png` | `scripts/build_hair_recolour.py` | registered |
| DG-175 | hair back | Red recolour of the registered silver layer | DG-031 recolour | DG-031 | `assets/hair_back/hair_back_017_recolour_red.png` | `scripts/build_hair_recolour.py` | registered |

**Scope, stated plainly: colour varies, silhouette does not.** All seven share
DG-031's exact shape, so the collection gains seven hair *colours* and still has
one hair *cut*.

This does **not** contradict the no-recolouring finding recorded under the
hair-back family. That finding says the eight `HAIR` sheet cells are distinct
cuts and must each be rendered natively — which remains true, and DG-029 to
DG-036 stay `pending` and are not satisfied by these. Numbered from
`hair_back_011` so 001–008 remain reserved for the painted cuts.

### Outfits

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-037 | outfit | White-silver celestial ceremonial robe | `OUTFIT`, row 1 cell 1 | DG-045; pale, high contrast risk, produce late | `assets/outfits/outfit_001_celestial_robe_white_silver.png` | `prompts/08_outfits.md` | pending |
| DG-038 | outfit | Black long coat with split cape tails | `OUTFIT`, row 1 cell 2 | DG-045 | `assets/outfits/outfit_002_black_split_tail_coat.png` | `prompts/08_outfits.md` | pending |
| DG-039 | outfit | Plum-gray long mage robe | `OUTFIT`, row 1 cell 3 | DG-045 | `assets/outfits/outfit_003_plum_gray_mage_robe.png` | `prompts/08_outfits.md` | pending |
| DG-040 | outfit | Black ragged hooded cloak outfit | `OUTFIT`, row 1 cell 4 | DG-045 representative test | `assets/outfits/outfit_004_black_ragged_hooded_cloak.png` | `prompts/08_outfits.md` | pending |
| DG-041 | outfit | White and blue armored ceremonial mantle | `OUTFIT`, row 1 cell 5 | DG-045; pale, high contrast risk, produce late | `assets/outfits/outfit_005_white_blue_armored_mantle.png` | `prompts/08_outfits.md` | pending |
| DG-042 | outfit | Black layered hooded long robe | `OUTFIT`, row 2 cell 1 | DG-045 representative test | `assets/outfits/outfit_006_black_layered_hooded_robe.png` | `prompts/08_outfits.md` | pending |
| DG-043 | outfit | Brown leather long coat/robe | `OUTFIT`, row 2 cell 2 | DG-045 | `assets/outfits/outfit_007_brown_leather_long_coat.png` | `prompts/08_outfits.md` | pending |
| DG-044 | outfit | Olive-green ragged cloak outfit | `OUTFIT`, row 2 cell 3 | DG-045 | `assets/outfits/outfit_008_olive_ragged_cloak.png` | `prompts/08_outfits.md` | pending |
| DG-045 | outfit | Deep-navy high-collar long coat | `OUTFIT`, row 2 cell 4 | Outfit representative test; highest contrast margin | `assets/outfits/outfit_009_navy_high_collar_coat.png` | `prompts/08_outfits.md` | pending |
| DG-046 | outfit | Silver-white high-collar ceremonial robe | `OUTFIT`, row 2 cell 5; naming example in `docs/naming-and-export.md` | DG-045; pale, high contrast risk, produce late | `assets/outfits/outfit_010_celestial_robe_white_gold.png` | `prompts/08_outfits.md` | pending |

#### Painted robes — DG-199 to DG-204 (added 2026-07-27)

Six painted robes supplied by the collection owner, replacing the five interim
procedural coats (DG-164 to DG-168) that previously held this category. Those
coats existed only to clear the release blocker and have been **removed** — the
files, their registrations and their backlog rows — because they were flat,
near-identical and did not read as designed clothing. Their build script,
`scripts/build_outfit.py`, is kept for reference.

Each reference arrived as a native 1254 x 1254 **RGB** file: the transparency
checker was painted into the pixels and there was no alpha channel. They were
also drawn at full humanoid proportions, about 1100 px collar to hem, against a
rig whose entire body below the chin is 606 px. `scripts/intake_painted_outfit.py`
removes the backdrop by flood fill from the canvas border — a brightness
threshold would eat the white-and-gold robes, whose fabric is as bright as the
backdrop — un-premultiplies the edge against the backdrop white so no pale rim
survives against a dark background, and refits the garment to the rig.

The collar seats at Y 442 and the hem at Y 1108. Y 442 was found by sweeping
scale and offset for the placement leaving zero bare skin in the shoulder band:
the more obvious seat at Y 480 put the hem in the right place but left a rim of
shoulder showing outside the pauldrons on every robe and every pose.

Rescaling during intake was **waived by the collection owner** for this batch. It
is recorded in each manifest entry's `postprocessing` as
`rig_refit_collar_y_442_hem_y_1108` so it stays visible.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-199 | outfit | White and gold ceremonial robe, layered pauldrons and sash | `images/outfit_references/robe_ref_001_white_gold.png` | Owner-supplied render | `assets/outfits/outfit_001_white_gold_painted.png` | `prompts/22_outfit_prompts.md` | registered |
| DG-200 | outfit | Black and gold high-collar robe, thorn filigree | `images/outfit_references/robe_ref_002_black_gold.png` | DG-199 | `assets/outfits/outfit_002_black_gold_painted.png` | `prompts/22_outfit_prompts.md` | registered |
| DG-201 | outfit | Navy and gold star-mantle robe, tasselled sash | `images/outfit_references/robe_ref_003_navy_gold_star.png` | DG-199 | `assets/outfits/outfit_003_navy_gold_star_painted.png` | `prompts/22_outfit_prompts.md` | registered |
| DG-202 | outfit | Crimson and gold flame-trim robe, chained belt | `images/outfit_references/robe_ref_004_crimson_gold.png` | DG-199 | `assets/outfits/outfit_004_crimson_gold_painted.png` | `prompts/22_outfit_prompts.md` | registered |
| DG-203 | outfit | Purple and black robe, amethyst-set gold trim | `images/outfit_references/robe_ref_005_purple_black_gold.png` | DG-199 | `assets/outfits/outfit_005_purple_black_gold_painted.png` | `prompts/22_outfit_prompts.md` | registered |
| DG-204 | outfit | White and navy star robe, sapphire drops | `images/outfit_references/robe_ref_006_white_navy_star.png` | DG-199 | `assets/outfits/outfit_006_white_navy_star_painted.png` | `prompts/22_outfit_prompts.md` | registered |

These are distinct painted designs, not recolours of one another, so the category
gains six *designs* rather than six colours. They do not correspond to cells in
the `OUTFIT` sheet, so **DG-037 to DG-046 stay `pending`** and are not satisfied
by these.

**Known limit — the sleeves defeat the pose variants.** An outfit composites over
the base body, so its sleeves replace whatever the arms were doing, and these are
painted with one arm position. Measured as the share of each pose's silhouette
difference from the neutral master that the garment covers, alongside whether the
hands still emerge from the cuffs — which is what actually makes a pose read:

| Base pose | Arm hidden, painted robe | Arm hidden, removed procedural coat | Hands visible |
|---|---|---|---|
| 001 neutral master | 0.0% | 0.0% | yes |
| 004 viewer-left palm-up | 58.6% | 33.6% | yes, 1284 px |
| 003 viewer-right vertical grip | 63.6% | 44.6% | yes, 806 px |
| 002 viewer-left vertical grip | 64.7% | 44.3% | yes, 1210 px |
| 005 centered two-hand grip | 82.8% | 61.2% | **no** |

The middle column is the finding that matters: **this was already true** under the
removed procedural coats and had not been measured. A sleeve covering an arm is
not a fault, though. On poses 002 to 004 the hands still emerge from the bell
cuffs and the fist, open hand or upturned palm reads, so those poses survive.

Pose 005 does not. Its clasped fists sit at X 580-705, Y 685-815 — in front of the
torso rather than at the cuffs — so every robe buries them, and a pose-005 token
is visually identical to a pose-001 token.

Compositing the hands back over the robe was tried and does not work: the fists
overlap the torso at the same skin tone with no enclosing outline, so an
edge-aware flood fill from the fist centres leaks into the torso and returns a
skin-coloured slab. The sleeves have to be painted for the pose.

Per-pose variants are queued as DG-205 to DG-228 with generation prompts in
`prompts/23_per_pose_outfit_variants.md`. The six pose-005 variants are the
priority; the eighteen for poses 002 to 004 are refinement.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-205 | outfit | White and gold robe, sleeves painted for the centered two-hand grip | DG-199 + `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | DG-199 | `assets/outfits/outfit_001_white_gold_pose005.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-206 | outfit | Black and gold robe, sleeves painted for the centered two-hand grip | DG-200 + `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | DG-199 | `assets/outfits/outfit_002_black_gold_pose005.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-207 | outfit | Navy and gold star robe, sleeves painted for the centered two-hand grip | DG-201 + `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | DG-199 | `assets/outfits/outfit_003_navy_gold_star_pose005.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-208 | outfit | Crimson and gold robe, sleeves painted for the centered two-hand grip | DG-202 + `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | DG-199 | `assets/outfits/outfit_004_crimson_gold_pose005.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-209 | outfit | Purple and black robe, sleeves painted for the centered two-hand grip | DG-203 + `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | DG-199 | `assets/outfits/outfit_005_purple_black_gold_pose005.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-210 | outfit | White and navy star robe, sleeves painted for the centered two-hand grip | DG-204 + `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` | DG-199 | `assets/outfits/outfit_006_white_navy_star_pose005.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-211 | outfit | White and gold robe, sleeves painted for the viewer-left vertical grip | DG-199 + `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | DG-205 | `assets/outfits/outfit_001_white_gold_pose002.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-212 | outfit | Black and gold robe, sleeves painted for the viewer-left vertical grip | DG-200 + `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | DG-205 | `assets/outfits/outfit_002_black_gold_pose002.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-213 | outfit | Navy and gold star robe, sleeves painted for the viewer-left vertical grip | DG-201 + `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | DG-205 | `assets/outfits/outfit_003_navy_gold_star_pose002.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-214 | outfit | Crimson and gold robe, sleeves painted for the viewer-left vertical grip | DG-202 + `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | DG-205 | `assets/outfits/outfit_004_crimson_gold_pose002.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-215 | outfit | Purple and black robe, sleeves painted for the viewer-left vertical grip | DG-203 + `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | DG-205 | `assets/outfits/outfit_005_purple_black_gold_pose002.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-216 | outfit | White and navy star robe, sleeves painted for the viewer-left vertical grip | DG-204 + `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` | DG-205 | `assets/outfits/outfit_006_white_navy_star_pose002.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-217 | outfit | White and gold robe, sleeves painted for the viewer-right vertical grip | DG-199 + `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | DG-205 | `assets/outfits/outfit_001_white_gold_pose003.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-218 | outfit | Black and gold robe, sleeves painted for the viewer-right vertical grip | DG-200 + `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | DG-205 | `assets/outfits/outfit_002_black_gold_pose003.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-219 | outfit | Navy and gold star robe, sleeves painted for the viewer-right vertical grip | DG-201 + `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | DG-205 | `assets/outfits/outfit_003_navy_gold_star_pose003.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-220 | outfit | Crimson and gold robe, sleeves painted for the viewer-right vertical grip | DG-202 + `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | DG-205 | `assets/outfits/outfit_004_crimson_gold_pose003.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-221 | outfit | Purple and black robe, sleeves painted for the viewer-right vertical grip | DG-203 + `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | DG-205 | `assets/outfits/outfit_005_purple_black_gold_pose003.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-222 | outfit | White and navy star robe, sleeves painted for the viewer-right vertical grip | DG-204 + `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` | DG-205 | `assets/outfits/outfit_006_white_navy_star_pose003.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-223 | outfit | White and gold robe, sleeves painted for the viewer-left palm-up | DG-199 + `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | DG-205 | `assets/outfits/outfit_001_white_gold_pose004.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-224 | outfit | Black and gold robe, sleeves painted for the viewer-left palm-up | DG-200 + `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | DG-205 | `assets/outfits/outfit_002_black_gold_pose004.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-225 | outfit | Navy and gold star robe, sleeves painted for the viewer-left palm-up | DG-201 + `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | DG-205 | `assets/outfits/outfit_003_navy_gold_star_pose004.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-226 | outfit | Crimson and gold robe, sleeves painted for the viewer-left palm-up | DG-202 + `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | DG-205 | `assets/outfits/outfit_004_crimson_gold_pose004.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-227 | outfit | Purple and black robe, sleeves painted for the viewer-left palm-up | DG-203 + `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | DG-205 | `assets/outfits/outfit_005_purple_black_gold_pose004.png` | `prompts/23_per_pose_outfit_variants.md` | pending |
| DG-228 | outfit | White and navy star robe, sleeves painted for the viewer-left palm-up | DG-204 + `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` | DG-205 | `assets/outfits/outfit_006_white_navy_star_pose004.png` | `prompts/23_per_pose_outfit_variants.md` | pending |

Each variant binds to its pose through `config/compatibility.json`, which
`generate_777.py` already honours: the variant requires its base pose, and the
base robe excludes the poses that have variants, so a sleeve can never be paired
with the wrong arms. Rules are added only as variants register — a rule naming a
missing file fails `validate_config.py`.

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

> **GATED on the faceless base bodies.**
> The registered bases carried a fully painted face, and the layer stack
> composites `eyes`, `eyebrows` and `mouths` over it, so an isolation-compliant
> layer left the baked lashes and outline visible. The features have been erased
> from all five bases — candidates are in
> `images/trait_candidates/base_bodies/`, built by
> `scripts/build_faceless_base.py`. Produce nothing in these three categories
> until those candidates are promoted into `assets/base_bodies/` and
> re-registered; after that the isolation rule holds as written, with no skin
> padding and no occlusion requirement. See
> `docs/qa/face_layer_conflict_2026-07-27.md`.

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

#### Procedural mouths — DG-237 to DG-248 (added 2026-07-27)

`mouths` held one asset — DG-198, recovered from the base master — so every token
in the collection shared a mouth. It was the thinnest category in the library and
the asset catalogue showed it as a single cell.

Built by `scripts/build_mouths.py` from signed distance fields at 4× supersampling
inside a 152 × 86 band on the locked anchor (627, 441). Closed mouths are tapered
strokes along a quadratic Bezier; open mouths are filled shapes whose outline
band comes from the same field, with a darker interior and a tongue where the
design calls for one. Ink is `(136, 65, 33)`, sampled from the darkest pixels of
DG-198, so the procedural mouths and the painted one read as the same hand.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-237 | mouth | Fine closed smile | mouth anchor (627, 441) | DG-198 | `assets/mouths/mouth_014_fine_closed_smile.png` | `scripts/build_mouths.py` | registered |
| DG-238 | mouth | Fine flat line | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_015_flat_line.png` | `scripts/build_mouths.py` | registered |
| DG-239 | mouth | Small downturned mouth | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_016_small_downturned.png` | `scripts/build_mouths.py` | registered |
| DG-240 | mouth | Asymmetric smirk, one corner raised | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_017_smirk_asymmetric.png` | `scripts/build_mouths.py` | registered |
| DG-241 | mouth | Cat mouth, omega curve | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_018_cat_mouth.png` | `scripts/build_mouths.py` | registered |
| DG-242 | mouth | Wavy unsure line | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_019_wavy_unsure.png` | `scripts/build_mouths.py` | registered |
| DG-243 | mouth | Parted line, two strokes with a centre gap | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_020_parted_line.png` | `scripts/build_mouths.py` | registered |
| DG-244 | mouth | Small open smile, flat-topped with tongue | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_021_small_open_smile.png` | `scripts/build_mouths.py` | registered |
| DG-245 | mouth | Wide open smile, flat-topped with tongue | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_022_wide_open_smile.png` | `scripts/build_mouths.py` | registered |
| DG-246 | mouth | Tiny dark round mouth | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_023_tiny_round.png` | `scripts/build_mouths.py` | registered |
| DG-247 | mouth | Tall pink open pout | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_024_pink_open_pout.png` | `scripts/build_mouths.py` | registered |
| DG-248 | mouth | Wide open mouth with two fangs | mouth anchor (627, 441) | DG-237 | `assets/mouths/mouth_025_wide_open_fangs.png` | `scripts/build_mouths.py` | registered |

Every one centres on X 626–627 against the locked axis and passes the rig gate.

A first pass drew the downturned mouth with a 3 px arc, which reads as a straight
line at face scale and was indistinguishable from `flat_line`. It now drops 7 px,
matching the smile's rise — the smallest arc that reads as a frown.

**These are shapes built to the sheet's descriptions, not the sheet's paintings.**
The twelve `FACE` mouth cells are distinct artwork, so **DG-095 to DG-106 stay
`pending`** and are not satisfied by these. Numbered from 014 so 001–012 remain
free for the sheet cells and 013 stays with the recovered mouth.

#### Recovered face layers and recolours — DG-176 to DG-198 (added 2026-07-27)

Removing the baked face from the base bodies left the collection with no face at
all, which is worse than the conflict it fixed. The erased artwork is the
approved design, so rather than draw replacements it was lifted back out of the
pre-removal master as trait layers by `scripts/extract_face_layers.py`.

The recovery is a difference matte, not a cut-out. The faceless base is a
measured reconstruction of the skin behind each feature, so the original is
exactly the feature composited over that skin; solving that composite for
coverage and colour gives real soft edges where the artist feathered the lashes.
Compositing the three recovered layers back over the faceless base reproduces
the original master to a worst-case channel error of 5. Fringe luminance
correlates with alpha at −0.22, so the matte is genuinely un-premultiplied
rather than keyed from black.

`scripts/build_face_recolours.py` then varies the colour. Hue and saturation
move; **value and alpha do not**, so every painted gradient, the pupil, the lash
weight and the upper-left key light survive. The sclera, the catchlights and the
skin-toned eyelid are held out. Eye palettes are gated on measured contrast —
RGB distance from skin, and hue separation from every registered background
sampled behind the head — by `build_face_recolours.py --check-contrast`.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-176 | eyes | Recovered painted eye pair from the base master, brown | base master face | Approved face anchors | `assets/eyes/eyes_025_base_master_brown.png` | `scripts/extract_face_layers.py` | registered |
| DG-177 | eyes | Gold recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_026_recolour_gold.png` | `scripts/build_face_recolours.py` | registered |
| DG-178 | eyes | Olive recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_027_recolour_olive.png` | `scripts/build_face_recolours.py` | registered |
| DG-179 | eyes | Lime recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_028_recolour_lime.png` | `scripts/build_face_recolours.py` | registered |
| DG-180 | eyes | Jade recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_029_recolour_jade.png` | `scripts/build_face_recolours.py` | registered |
| DG-181 | eyes | Spring-green recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_030_recolour_spring.png` | `scripts/build_face_recolours.py` | registered |
| DG-182 | eyes | Emerald recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_031_recolour_emerald.png` | `scripts/build_face_recolours.py` | registered |
| DG-183 | eyes | Teal recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_032_recolour_teal.png` | `scripts/build_face_recolours.py` | registered |
| DG-184 | eyes | Orchid recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_033_recolour_orchid.png` | `scripts/build_face_recolours.py` | registered |
| DG-185 | eyes | Magenta recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_034_recolour_magenta.png` | `scripts/build_face_recolours.py` | registered |
| DG-186 | eyes | Rose recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_035_recolour_rose.png` | `scripts/build_face_recolours.py` | registered |
| DG-187 | eyes | Grey recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_036_recolour_grey.png` | `scripts/build_face_recolours.py` | registered |
| DG-188 | eyes | Charcoal recolour of the recovered eye pair | DG-176 recolour | DG-176 | `assets/eyes/eyes_037_recolour_charcoal.png` | `scripts/build_face_recolours.py` | registered |
| DG-189 | eyebrows | Recovered painted eyebrow pair from the base master, brown | base master face | Approved face anchors | `assets/eyebrows/eyebrows_017_base_master_brown.png` | `scripts/extract_face_layers.py` | registered |
| DG-190 | eyebrows | Silver recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_018_recolour_silver.png` | `scripts/build_face_recolours.py` | registered |
| DG-191 | eyebrows | Gold recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_019_recolour_gold.png` | `scripts/build_face_recolours.py` | registered |
| DG-192 | eyebrows | Black recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_020_recolour_black.png` | `scripts/build_face_recolours.py` | registered |
| DG-193 | eyebrows | Violet recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_021_recolour_violet.png` | `scripts/build_face_recolours.py` | registered |
| DG-194 | eyebrows | Blue recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_022_recolour_blue.png` | `scripts/build_face_recolours.py` | registered |
| DG-195 | eyebrows | Pink recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_023_recolour_pink.png` | `scripts/build_face_recolours.py` | registered |
| DG-196 | eyebrows | Teal recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_024_recolour_teal.png` | `scripts/build_face_recolours.py` | registered |
| DG-197 | eyebrows | Red recolour of the recovered eyebrow pair | DG-189 recolour | DG-189 | `assets/eyebrows/eyebrows_025_recolour_red.png` | `scripts/build_face_recolours.py` | registered |
| DG-198 | mouth | Recovered painted closed smile from the base master | base master face | Approved mouth anchor | `assets/mouths/mouth_013_base_master_closed_smile.png` | `scripts/extract_face_layers.py` | registered |

**Scope, stated plainly: colour varies, shape does not.** All thirteen eye
assets share one painted eye design and all nine eyebrows share one brow shape,
so the collection gains twelve eye *colours* and one eye *design*.

The 24 `FACE` sheet eye cells, 16 eyebrow cells and 12 mouth cells are distinct
paintings, so **DG-055 to DG-106 stay `pending` and are not satisfied by these**.
Numbered from 025, 017 and 013 upward so the sheet cells keep 001–024, 001–016
and 001–012.

Eyebrow palettes are matched to the registered hair colours rather than to the
eye palettes, since a brow reads as hair and not as eye.

### Expression marks

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-107 | expression mark | Pink blush strokes | `FACE`, expression marks r1c1 | Approved face anchors | `assets/expression_marks/expression_mark_001_pink_blush_strokes.png` | `prompts/07_expression_marks.md` | registered |
| DG-108 | expression mark | Yellow stress/attention marks | `FACE`, expression marks r1c2 | DG-107 representative test | `assets/expression_marks/expression_mark_002_yellow_stress_marks.png` | `prompts/07_expression_marks.md` | registered |
| DG-109 | expression mark | Dark vertical gloom lines | `FACE`, expression marks r1c3 | DG-107 | `assets/expression_marks/expression_mark_003_dark_gloom_lines.png` | `prompts/07_expression_marks.md` | registered |
| DG-110 | expression mark | Gold sparkle/star | `FACE`, expression marks r1c4 | DG-107 | `assets/expression_marks/expression_mark_004_gold_sparkle.png` | `prompts/07_expression_marks.md` | registered |
| DG-111 | expression mark | Cyan sweat drop | `FACE`, expression marks r2c1 | DG-107 | `assets/expression_marks/expression_mark_005_cyan_sweat_drop.png` | `prompts/07_expression_marks.md` | registered |
| DG-112 | expression mark | Pink anger cross | `FACE`, expression marks r2c2 | DG-107 | `assets/expression_marks/expression_mark_006_pink_anger_cross.png` | `prompts/07_expression_marks.md` | registered |
| DG-113 | expression mark | Yellow-green square emphasis mark | `FACE`, expression marks r2c3 | DG-107 | `assets/expression_marks/expression_mark_007_yellow_green_emphasis.png` | `prompts/07_expression_marks.md` | registered |
| DG-114 | expression mark | Pink curved motion/surprise mark | `FACE`, expression marks r2c4 | DG-107 | `assets/expression_marks/expression_mark_008_pink_curved_mark.png` | `prompts/07_expression_marks.md` | registered |

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

#### Interim procedural fringe — DG-229 to DG-236 (added 2026-07-27)

`hair_front` held nothing, and measurement showed the consequence was worse than
an empty category usually is: **`hair_back` covers 0% of the scalp** at every row
from Y 150 to Y 340. All eight registered back layers are wisps either side of
the skull, and the base master is deliberately bald, so every token in the
collection rendered as a bald head — see the thumbnails in
`docs/qa/composites/face_tokens_thumbnail_2026-07-27.png`. That is the same class
of defect as the outfit blocker, which was "reads as unclothed".

These eight clear it. `scripts/build_hair_front.py` takes the cap from the base
body's own alpha, so it follows the skull exactly and cannot drift from it, and
draws the fringe as tapered distance fields evaluated supersampled inside the
hair band only. Palettes match the registered `hair_back` colours so a token can
pair front and back.

Two measurements set the geometry. The cap hands over to the fringe along a
**curve** — high at the centre, low at the temples — because cropping it at a
single Y drew a hard horizontal line straight across the face. And the locks tip
at Y 285-306, clearing the recovered eyebrows at Y 292-343: `hair_front` sits at
layer 12, above `eyebrows` at 09, so a longer fringe would hide a whole category.

| ID | Category | Visual description | Source reference | Dependency | Intended production path | Prompt | Status |
|---|---|---|---|---|---|---|---|
| DG-229 | hair front | Procedural centre-parted fringe, black | base body dome | Release-visible defect | `assets/hair_front/hair_front_001_fringe_black.png` | `scripts/build_hair_front.py` | registered |
| DG-230 | hair front | Procedural centre-parted fringe, blue | base body dome | DG-229 | `assets/hair_front/hair_front_002_fringe_blue.png` | `scripts/build_hair_front.py` | registered |
| DG-231 | hair front | Procedural centre-parted fringe, gold | base body dome | DG-229 | `assets/hair_front/hair_front_003_fringe_gold.png` | `scripts/build_hair_front.py` | registered |
| DG-232 | hair front | Procedural centre-parted fringe, pink | base body dome | DG-229 | `assets/hair_front/hair_front_004_fringe_pink.png` | `scripts/build_hair_front.py` | registered |
| DG-233 | hair front | Procedural centre-parted fringe, red | base body dome | DG-229 | `assets/hair_front/hair_front_005_fringe_red.png` | `scripts/build_hair_front.py` | registered |
| DG-234 | hair front | Procedural centre-parted fringe, silver | base body dome | DG-229 | `assets/hair_front/hair_front_006_fringe_silver.png` | `scripts/build_hair_front.py` | registered |
| DG-235 | hair front | Procedural centre-parted fringe, teal | base body dome | DG-229 | `assets/hair_front/hair_front_007_fringe_teal.png` | `scripts/build_hair_front.py` | registered |
| DG-236 | hair front | Procedural centre-parted fringe, violet | base body dome | DG-229 | `assets/hair_front/hair_front_008_fringe_violet.png` | `scripts/build_hair_front.py` | registered |

**Scope, stated plainly: colour varies, shape does not.** All eight share one
fringe silhouette, so the collection gains eight fringe *colours* and one fringe
*cut*. They are simpler than the painted hair — no strand separation, no wave
structure — and are honest placeholders that stop the collection rendering bald.

The eight `HAIR` sheet lower-row cells are distinct cuts, so **DG-115 to DG-122
stay `pending`** and are not satisfied by these. Numbered from 001 in a naming
scheme that keeps `fringe` in the filename, so a painted cut can take the sheet
name without collision.

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

Phase A is complete: DG-001–DG-006 are registered, so the base family is locked. Produce the first entry of each remaining category in canonical layer order as that category's representative test — DG-015 (rear aura), DG-021 (back accessory), and DG-037 (outfit) are next. Run cross-category composites before continuing each category's later IDs. Hand objects may be produced only against the approved pose named in their dependency column.

DG-031 already serves as the hair-back representative test, so the remaining hair-back colors may proceed without waiting on DG-029.

Every status change in these tables must be followed by `python scripts/report_production_status.py --write`. CI fails when a row marked `registered` has no matching manifest entry, or when the generated ledger in `docs/production_status.md` is stale.
