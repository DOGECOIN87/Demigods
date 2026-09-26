# Demigods 1-of-1s

The collection's one-of-one tier, working toward 77 pieces. Each piece is a complete, flattened character-and-environment illustration, not a modular layer, so `generate_777.py` never reads these files.

| Nos. | Pieces | Where |
|---|---|---|
| 001–007 | 7 legendaries | registered in `assets/legendary/` |
| 008–056 | 49 one-of-ones | this folder |
| 057–077 | 21 not yet generated | prompts in [`prompts/24_one_of_one_completion_pack.md`](../../prompts/24_one_of_one_completion_pack.md) |

## State of this folder

- The 49 files were uploaded to the top of `images/` on 2026-09-25 and 2026-09-26, then moved here byte-for-byte and renamed with the approved titles. `sources.json` records each file's original upload name, upload commit and SHA-256.
- All 49 pass `python scripts/validate_legendary.py --dir images/one_of_ones --expect 49`: complete decode, PNG, native 1254 × 1254, fully opaque RGB, and 49 distinct digests. None matches a registered legendary.
- A by-eye check of the bottom corners found no generator watermark. No full-size check for stray text has been done yet.
- None is registered in `assets/asset_manifest.json`. Registering them changes the supply split in `config/collection.json`, currently 770 generative + 7 legendary, and that is a separate decision.

## Roster

| No. | Title | File | Uploaded as |
|---|---|---|---|
| 001 | Sovereign of the Solar Court | [`assets/legendary/legendary_001_sovereign_of_the_solar_court.png`](../../assets/legendary/legendary_001_sovereign_of_the_solar_court.png) | registered legendary |
| 002 | Oracle of the Waning Crescent | [`assets/legendary/legendary_002_oracle_of_the_waning_crescent.png`](../../assets/legendary/legendary_002_oracle_of_the_waning_crescent.png) | registered legendary |
| 003 | Heir of the Celestial Throne | [`assets/legendary/legendary_003_heir_of_the_celestial_throne.png`](../../assets/legendary/legendary_003_heir_of_the_celestial_throne.png) | registered legendary |
| 004 | Keeper of the Arcane Index | [`assets/legendary/legendary_004_keeper_of_the_arcane_index.png`](../../assets/legendary/legendary_004_keeper_of_the_arcane_index.png) | registered legendary |
| 005 | Warden of the Violet Void | [`assets/legendary/legendary_005_warden_of_the_violet_void.png`](../../assets/legendary/legendary_005_warden_of_the_violet_void.png) | registered legendary |
| 006 | Tempest Sovereign | [`assets/legendary/legendary_006_tempest_sovereign.png`](../../assets/legendary/legendary_006_tempest_sovereign.png) | registered legendary |
| 007 | Verdant Archivist | [`assets/legendary/legendary_007_verdant_archivist.png`](../../assets/legendary/legendary_007_verdant_archivist.png) | registered legendary |
| 008 | Pirate Captain | [`one_of_one_008_pirate_captain.png`](one_of_one_008_pirate_captain.png) | `06159dcf-7a3f-4212-a40a-4b00d15a059c.png` |
| 009 | Crystal Bird Mage | [`one_of_one_009_crystal_bird_mage.png`](one_of_one_009_crystal_bird_mage.png) | `12933e13-8141-4610-bc1b-c1ece30e67ae.png` |
| 010 | Blacksmith | [`one_of_one_010_blacksmith.png`](one_of_one_010_blacksmith.png) | `13b7a459-449c-4179-bdbd-4dd710c2512b.png` |
| 011 | Clockwork Astronomer | [`one_of_one_011_clockwork_astronomer.png`](one_of_one_011_clockwork_astronomer.png) | `1be65bf5-b010-4537-b7ce-bb5695973f0b.png` |
| 012 | Chess King | [`one_of_one_012_chess_king.png`](one_of_one_012_chess_king.png) | `1fc61bfc-2430-413b-9d47-89893ad22ad2.png` |
| 013 | Dragon General | [`one_of_one_013_dragon_general.png`](one_of_one_013_dragon_general.png) | `244fac5f-f452-412c-af2b-5e262a8b6070.png` |
| 014 | Mushroom Forager | [`one_of_one_014_mushroom_forager.png`](one_of_one_014_mushroom_forager.png) | `26b1799e-c3e7-4dbe-acbc-b1a90bc20e84.png` |
| 015 | Deep-Sea Diver | [`one_of_one_015_deep_sea_diver.png`](one_of_one_015_deep_sea_diver.png) | `2d249232-17c3-4ec1-8f59-f4693a3dfdc0.png` |
| 016 | Bamboo Fan Lady | [`one_of_one_016_bamboo_fan_lady.png`](one_of_one_016_bamboo_fan_lady.png) | `3134d2ff-147e-46da-b4d3-60cef09438f5.png` |
| 017 | Justice Judge | [`one_of_one_017_justice_judge.png`](one_of_one_017_justice_judge.png) | `38cfa65b-b06a-4d9a-9ba9-3af7fb0d8f47.png` |
| 018 | Oak Druid | [`one_of_one_018_oak_druid.png`](one_of_one_018_oak_druid.png) | `3ad68636-6dd5-4f68-9eb1-21a542c1f02a.png` |
| 019 | Void Portal Mage | [`one_of_one_019_void_portal_mage.png`](one_of_one_019_void_portal_mage.png) | `3fe452a3-b039-411c-9743-dd3e9a56be9a.png` |
| 020 | Winter Bell Mage | [`one_of_one_020_winter_bell_mage.png`](one_of_one_020_winter_bell_mage.png) | `47acb7a2-3f7c-415f-98e6-866cb1e6cbd2.png` |
| 021 | Lion Gladiator | [`one_of_one_021_lion_gladiator.png`](one_of_one_021_lion_gladiator.png) | `4fb29b56-7c6a-4ef0-9615-a5e32f18860a.png` |
| 022 | Sakura Samurai | [`one_of_one_022_sakura_samurai.png`](one_of_one_022_sakura_samurai.png) | `52886e8e-770d-4930-a3ce-e19a3677f66a.png` |
| 023 | Aurora Ice Mage | [`one_of_one_023_aurora_ice_mage.png`](one_of_one_023_aurora_ice_mage.png) | `5b7d3259-a0c1-466c-9c5f-44e36c4a9391.png` |
| 024 | Black Opal Knight | [`one_of_one_024_black_opal_knight.png`](one_of_one_024_black_opal_knight.png) | `616d5fe8-cae6-434f-9cd9-1a45173a2cee.png` |
| 025 | Lava Knight | [`one_of_one_025_lava_knight.png`](one_of_one_025_lava_knight.png) | `6d20e785-07d6-4622-8390-1e0e33d81d73.png` |
| 026 | Peacock Noble | [`one_of_one_026_peacock_noble.png`](one_of_one_026_peacock_noble.png) | `6e2be519-f600-4b87-8d8a-fa1893fac1dd.png` |
| 027 | Star Cartographer | [`one_of_one_027_star_cartographer.png`](one_of_one_027_star_cartographer.png) | `73d1a496-ef9e-4a0b-a64a-5be905da6a5a.png` |
| 028 | Dream Weaver | [`one_of_one_028_dream_weaver.png`](one_of_one_028_dream_weaver.png) | `793fa724-744a-456b-82b5-45a54e29949d.png` |
| 029 | Coral Jellyfish | [`one_of_one_029_coral_jellyfish.png`](one_of_one_029_coral_jellyfish.png) | `85466ed9-e8e6-470d-8833-1c46fc9018e2.png` |
| 030 | Swan Knight | [`one_of_one_030_swan_knight.png`](one_of_one_030_swan_knight.png) | `85b70876-f9fa-4e32-9aa1-e18edb0d990d.png` |
| 031 | Thunder Drummer | [`one_of_one_031_thunder_drummer.png`](one_of_one_031_thunder_drummer.png) | `89f803b5-f42c-40fb-a622-d68d42f8f9f9.png` |
| 032 | Crystal Paladin | [`one_of_one_032_crystal_paladin.png`](one_of_one_032_crystal_paladin.png) | `8c0e95d3-91f2-4986-87fb-210e263b27d8.png` |
| 033 | Amethyst Mage | [`one_of_one_033_amethyst_mage.png`](one_of_one_033_amethyst_mage.png) | `91eb8b2f-f752-49f6-9f51-bfdd770b4ff4.png` |
| 034 | Eclipse Reaper | [`one_of_one_034_eclipse_reaper.png`](one_of_one_034_eclipse_reaper.png) | `9858c541-0036-4594-bec6-7bd6a4d416f4.png` |
| 035 | Jester | [`one_of_one_035_jester.png`](one_of_one_035_jester.png) | `9c3125b9-4223-420a-819c-492fe547ef7f.png` |
| 036 | Naval Admiral | [`one_of_one_036_naval_admiral.png`](one_of_one_036_naval_admiral.png) | `a3f6ce85-9d39-4c50-804d-0179f9c00b2a.png` |
| 037 | Star Shepherd | [`one_of_one_037_star_shepherd.png`](one_of_one_037_star_shepherd.png) | `abbb6688-88f0-4be4-af2c-5d9b63addadc.png` |
| 038 | Lotus Monk | [`one_of_one_038_lotus_monk.png`](one_of_one_038_lotus_monk.png) | `b272a6c3-12bf-4b6f-aea5-4ff1644f94ca.png` |
| 039 | Desert Hourglass | [`one_of_one_039_desert_hourglass.png`](one_of_one_039_desert_hourglass.png) | `b317d51a-2427-426a-9f97-a4cc1f4ffb3b.png` |
| 040 | Crimson King | [`one_of_one_040_crimson_king.png`](one_of_one_040_crimson_king.png) | `b76a0aa7-bcab-4ba0-a2f8-97095bfe3463.png` |
| 041 | Frost King | [`one_of_one_041_frost_king.png`](one_of_one_041_frost_king.png) | `b9cde825-27a7-4a70-a068-5438a880d7de.png` |
| 042 | Rose Letter | [`one_of_one_042_rose_letter.png`](one_of_one_042_rose_letter.png) | `bcdc2e81-552f-4e4a-af01-76bf73d60279.png` |
| 043 | Moth Wings | [`one_of_one_043_moth_wings.png`](one_of_one_043_moth_wings.png) | `c09d634a-02e0-40fc-a176-52109ab34f3d.png` |
| 044 | Dream Knight | [`one_of_one_044_dream_knight.png`](one_of_one_044_dream_knight.png) | `c3505d43-a1d1-40e4-819f-c1829b8d53e4.png` |
| 045 | Lantern Festival | [`one_of_one_045_lantern_festival.png`](one_of_one_045_lantern_festival.png) | `c373163c-3b87-4252-aa1c-2f93f99b6af8.png` |
| 046 | Ink Calligrapher | [`one_of_one_046_ink_calligrapher.png`](one_of_one_046_ink_calligrapher.png) | `c809670f-01bd-4425-81d5-d6a199904ef5.png` |
| 047 | Storm Lancer | [`one_of_one_047_storm_lancer.png`](one_of_one_047_storm_lancer.png) | `c8129056-0977-41ae-92fd-5f32167bd4e3.png` |
| 048 | Falconer | [`one_of_one_048_falconer.png`](one_of_one_048_falconer.png) | `d719e236-1478-45dd-8112-bb2edd428522.png` |
| 049 | Eclipse Swordsman | [`one_of_one_049_eclipse_swordsman.png`](one_of_one_049_eclipse_swordsman.png) | `d74d58f7-a934-4249-a182-19d5002fb04c.png` |
| 050 | Key Keeper | [`one_of_one_050_key_keeper.png`](one_of_one_050_key_keeper.png) | `d92fecf2-8ddf-4528-93a3-035694270779.png` |
| 051 | Void Librarian | [`one_of_one_051_void_librarian.png`](one_of_one_051_void_librarian.png) | `dc95575f-7537-4029-a530-19e7bf112610.png` |
| 052 | Alchemist | [`one_of_one_052_alchemist.png`](one_of_one_052_alchemist.png) | `e0fd64d2-621f-478a-8ca2-31d4d904670a.png` |
| 053 | Moon Rabbit | [`one_of_one_053_moon_rabbit.png`](one_of_one_053_moon_rabbit.png) | `ee60e87e-5a6f-48ac-b219-c3f134bff943.png` |
| 054 | Moon Archer | [`one_of_one_054_moon_archer.png`](one_of_one_054_moon_archer.png) | `efa0b432-ce29-492b-8c22-b71a4751006d.png` |
| 055 | Galaxy Astronomer | [`one_of_one_055_galaxy_astronomer.png`](one_of_one_055_galaxy_astronomer.png) | `f55efd26-9e50-46a2-9606-94894dd8a09c.png` |
| 056 | Constellation Scholar | [`one_of_one_056_constellation_scholar.png`](one_of_one_056_constellation_scholar.png) | `file_00000000866081f590a8a9f6b7f21797.png` |
| 057 | Kitsune Shrine Keeper | not yet generated; save as `one_of_one_057_kitsune_shrine_keeper.png` | — |
| 058 | Honey Warden | not yet generated; save as `one_of_one_058_honey_warden.png` | — |
| 059 | Windcaller | not yet generated; save as `one_of_one_059_windcaller.png` | — |
| 060 | Marble Sculptor | not yet generated; save as `one_of_one_060_marble_sculptor.png` | — |
| 061 | Rainbow Herald | not yet generated; save as `one_of_one_061_rainbow_herald.png` | — |
| 062 | Hearthkeeper | not yet generated; save as `one_of_one_062_hearthkeeper.png` | — |
| 063 | Harvest Sovereign | not yet generated; save as `one_of_one_063_harvest_sovereign.png` | — |
| 064 | Pomegranate Princess | not yet generated; save as `one_of_one_064_pomegranate_princess.png` | — |
| 065 | Valkyrie | not yet generated; save as `one_of_one_065_valkyrie.png` | — |
| 066 | Raven Seer | not yet generated; save as `one_of_one_066_raven_seer.png` | — |
| 067 | Cat Temple Guardian | not yet generated; save as `one_of_one_067_cat_temple_guardian.png` | — |
| 068 | Feathered Serpent Priest | not yet generated; save as `one_of_one_068_feathered_serpent_priest.png` | — |
| 069 | Djinn Lamp Keeper | not yet generated; save as `one_of_one_069_djinn_lamp_keeper.png` | — |
| 070 | Chromatic Painter | not yet generated; save as `one_of_one_070_chromatic_painter.png` | — |
| 071 | Wind-Up Toymaker | not yet generated; save as `one_of_one_071_wind_up_toymaker.png` | — |
| 072 | Confectioner | not yet generated; save as `one_of_one_072_confectioner.png` | — |
| 073 | Hedge Witch | not yet generated; save as `one_of_one_073_hedge_witch.png` | — |
| 074 | Stained Glass Artisan | not yet generated; save as `one_of_one_074_stained_glass_artisan.png` | — |
| 075 | Autumn Stag Prince | not yet generated; save as `one_of_one_075_autumn_stag_prince.png` | — |
| 076 | Wandering Bard | not yet generated; save as `one_of_one_076_wandering_bard.png` | — |
| 077 | Owl Sage | not yet generated; save as `one_of_one_077_owl_sage.png` | — |
