# Demigods Background Candidates

These eight user-supplied images define the approved visual direction for the first background set. Their exact uploaded bytes are preserved here as references. Re-uploaded duplicates were excluded by SHA-256.

They are **not production layers**:

- each source is a 1024 × 1024 RGB JPEG; no embedded ICC profile was added or removed
- the locked production canvas is 1254 × 1254
- production backgrounds must be full-bleed PNGs and fully opaque
- none is stored in `assets/backgrounds/` or registered in `registered_production_assets`
- never resize, upscale, or merely convert these JPEGs and call the results production assets
- original attachment filenames, byte counts, dimensions, modes, formats, preservation state, and exact hashes are recorded in `assets/asset_manifest.json`

## Inventory

| ID | Visual direction | Reference file | SHA-256 | Intended production path |
|---|---|---|---|---|
| 001 | Celestial blue-and-gold throne hall | `background_001_celestial_throne_hall_reference.jpg` | `b92287aaa4fe36fd4c1b8102367a51b635c8f912d91aca9db37e91aa4c20a8e8` | `assets/backgrounds/background_001_celestial_throne_hall.png` |
| 002 | Violet gothic sanctum | `background_002_violet_gothic_sanctum_reference.jpg` | `ed6a2f8893e6d5b53e9bccec21daa2dafd06a469b8c4621d759cbfeabef6dfde` | `assets/backgrounds/background_002_violet_gothic_sanctum.png` |
| 003 | Moonlit arcane library | `background_003_arcane_library_reference.jpg` | `afc64910b8f1c44f49f33294a71f8228961025ae8a8f7f46b40def2a268e2785` | `assets/backgrounds/background_003_arcane_library.png` |
| 004 | Crescent-star dreamscape | `background_004_crescent_star_dreamscape_reference.jpg` | `7ef8cedff521095601e1225f6ad87f8024930c05d9e458dda138e92ae16c6d3e` | `assets/backgrounds/background_004_crescent_star_dreamscape.png` |
| 005 | Solar sky temple | `background_005_solar_sky_temple_reference.jpg` | `ccb3a8265fb4294752b15d0ef3fcc320b52ce77ddad2cf03abdfe1d5eed46e15` | `assets/backgrounds/background_005_solar_sky_temple.png` |
| 006 | Moonlit marble balcony | `background_006_moonlit_marble_balcony_reference.jpg` | `8bd53a70cac05a4dbed40bcff596e70121e4d5d693150054b3f8e29b5608d4ed` | `assets/backgrounds/background_006_moonlit_marble_balcony.png` |
| 007 | Golden celestial gateway | `background_007_golden_celestial_gateway_reference.jpg` | `b9ca9d7afc28f1314cbe0dc33b7dc6226df9233a1c25d42f8d1bdd85d9c221b5` | `assets/backgrounds/background_007_golden_celestial_gateway.png` |
| 008 | Violet void portal | `background_008_violet_void_portal_reference.jpg` | `cb20d17670e3d95b932979613a01dbf8e17f33fae52c46f8656f96d2f905aa29` | `assets/backgrounds/background_008_violet_void_portal.png` |

## Production gate

Use `prompts/17_native_1254_backgrounds.md` to create one native 1254 × 1254 background at a time. Each result must pass complete decode, dimensions, opacity, composition, lighting, text/glyph removal, and manual visual QA before its exact final SHA-256 is registered.

Native review candidates remain under `images/background_candidates/native_candidates/` until approval. Background 001 passed QA and was registered at `assets/backgrounds/background_001_celestial_throne_hall.png` with SHA-256 `2a82caf4833bc1f86f6d9ed1b7ba8a04c2344860a12b74f36f26c7cdeb4750d9`. Its source JPEG remains unchanged.

## Background 002 review candidates

| Attempt | Candidate | SHA-256 | Binary QA | Manual status |
|---|---|---|---|---|
| 001 | `native_candidates/background_002_violet_gothic_sanctum_candidate_attempt_001.png` | `7ef25fa04d6430b5e1a7ca688cc5755f28df5c4b9da6ec5d80d12507a1f0d2b0` | Pass — native 1254 × 1254 RGB, fully opaque | QA-failed: several altar pinnacles terminate in explicit cross-shaped finials. |
| 002 | `native_candidates/background_002_violet_gothic_sanctum_candidate.png` | `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc` | Pass — native 1254 × 1254 RGB, fully opaque | Approved and registered byte-for-byte at the intended production path. |

Attempt 001 remains outside production. Approved attempt 002 is stored byte-for-byte at `assets/backgrounds/background_002_violet_gothic_sanctum.png` and registered with SHA-256 `ba15e3dd980aed77a939a87b59652af495629733fddb1316f77cfabe2c259bdc`. The preserved Background 002 JPEG remains byte-for-byte unchanged at SHA-256 `ed6a2f8893e6d5b53e9bccec21daa2dafd06a469b8c4621d759cbfeabef6dfde`.

## Background 003 review candidate

| Attempt | Candidate | SHA-256 | Binary QA | Manual status |
|---|---|---|---|---|
| 001 | `native_candidates/background_003_arcane_library_candidate.png` | `dfd632fd80b6279a35f74cb767fbdf1d5662f57bbad7f6db799d972edb9928f0` | Pass — native 1254 × 1254 RGB, fully opaque | Approved and registered byte-for-byte at the intended production path. |

The approved candidate is stored byte-for-byte at `assets/backgrounds/background_003_arcane_library.png` and registered with SHA-256 `dfd632fd80b6279a35f74cb767fbdf1d5662f57bbad7f6db799d972edb9928f0`. The preserved Background 003 JPEG remains byte-for-byte unchanged at SHA-256 `afc64910b8f1c44f49f33294a71f8228961025ae8a8f7f46b40def2a268e2785`.

## Background 004 review candidates

| Attempt | Candidate | SHA-256 | Binary QA | Manual status |
|---|---|---|---|---|
| 001 | `native_candidates/background_004_crescent_star_dreamscape_candidate_attempt_001.png` | `0ce22870e010f729a3a8819035f1deef072476a0e47729d2632c4d79547b08f5` | Pass — native 1254 × 1254 RGB, fully opaque | QA-failed: platform surface is substantially above foot baseline Y 1139, placing the future feet below the platform. |
| 002 | `native_candidates/background_004_crescent_star_dreamscape_candidate_attempt_002.png` | `702f8f7c5f5dee986bcb3bc66ec3f63006ff0730c4c641d86f1d9078e28f784d` | Pass — native 1254 × 1254 RGB, fully opaque | QA-failed: coordinate `[627,1139]` lands below the front rim on the vertical platform fascia rather than the walking surface. |
| 003 | `native_candidates/background_004_crescent_star_dreamscape_candidate.png` | `e2e2f183c4c28231e36114b1c80d2844774edd682e11b1d76b9dd0e77c58c2d9` | Pass — native 1254 × 1254 RGB, fully opaque | Candidate: coordinate overlay and repository manual QA passed; explicit human visual approval pending. |

All three were generated independently from the exact preserved Background 004 JPEG. None was resized, patched, derived from a prior attempt, or stored under `assets/backgrounds/`. The reference remains byte-for-byte unchanged at SHA-256 `7ef8cedff521095601e1225f6ad87f8024930c05d9e458dda138e92ae16c6d3e`.

## Unassigned uploaded material

An additional 784 × 1168 moonlit-balcony JPEG uploaded under `assets/backgrounds/` is preserved at `unassigned/grok_1784705110324_reference_unassigned.jpg` with SHA-256 `b06d020a9bf96cfaf6566ef7a79a7e406203a84f0becf1d1f7d19b93050a72b1`. It is not one of the eight canonical references, has no backlog assignment, and is not a production asset.
