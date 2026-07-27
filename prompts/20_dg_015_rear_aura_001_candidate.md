# Prompt — DG-015 Rear Aura 001 Blue Floor Ring Candidate

Governing category prompt: `prompts/12_auras.md`. Co-creation rules: `prompts/19_individual_trait_asset_co_creation.md`.

## Locked next asset

| Field | Value |
|---|---|
| Backlog ID | DG-015 |
| Category | `rear_auras` (layer 02, behind the character) |
| Visual description | Blue elliptical floor / halo ring |
| Source reference | `images/reference_sheets/back_accessories_and_aura_effects_catalog.webp`, lower "aura effects" row, cell 1 |
| Reference SHA-256 | `2acac934db9a854dadc29ce9800a9f581dfa0812462fe27b642a2e9f7394fe52` |
| Intended production path | `assets/rear_auras/aura_rear_001_blue_floor_ring.png` |
| Candidate filename | `aura_rear_001_blue_floor_ring_candidate_attempt_001.png` |
| Candidate upload folder | `images/trait_candidates/rear_auras/` |
| Role | Rear-aura representative test — unblocks DG-016 through DG-020 |

The reference cell is a 128 × 96 catalog preview. It is sufficient to identify the design and nothing more. Render this natively at 1254 × 1254; never crop, upscale, or extract pixels from the preview.

## Attachments

- `assets/base_bodies/base_body_001_neutral_master.png` — SHA-256 `b344cffec9385725ccbf375b165a3b2b5fbea7af4edabce53741f47980cf83a3` (invisible placement, scale, and lighting reference only)
- `docs/rig/rig_guide_1254.png` — SHA-256 `3433da2ceede664fba1e4f21112c3bbd0fc3ac786870584e8c92cffb1f6baf5c`
- The aura catalog sheet above, for the cell-1 design only

## Geometry note that decides pass or fail

This asset is gated by `python scripts/rig_gate_report.py --trait <file>`, which enforces the locked maximum bounds `[233, 129, 1021, 1139]` on **every pixel whose alpha is not exactly zero**. A wide, faint glow that trails off at alpha 1–2 still counts as a visible pixel and will fail the gate.

Therefore the ring is a floor ring whose *near* edge rests on the foot baseline rather than a ring drawn around the feet in full perspective. The entire effect — ring, inner fill, and glow falloff — must have faded to fully zero alpha before it reaches those bounds.

## Image-generation request

```text
Create exactly one isolated Demigods rear aura, rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested aura on full transparency — never the body, face, feet, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG:
- 1254 x 1254, fully transparent background, no checkerboard and no backdrop
- canvas center X 627
- foot baseline Y 1139
- every pixel with any non-zero alpha must fall inside X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic; zero yaw, pitch, roll, tilt, or perspective distortion of the canvas

TARGET:
Create one blue elliptical floor halo ring lying flat on the ground plane beneath the character, seen from the collection's fixed front-facing camera so the ring reads as a horizontal ellipse much wider than it is tall.

- one continuous closed elliptical ring band; do not draw a disc, a sphere, a vertical halo, or concentric multiple rings
- horizontally centered on X 627, symmetrical left to right
- outer ellipse width approximately 600 px, spanning roughly X 327 to X 927
- outer ellipse height approximately 170 px
- the LOWEST visible pixel of the ring and its glow sits at approximately Y 1136 and must never cross Y 1139, so the near edge of the ring meets the foot baseline
- ring band thickness approximately 40-55 px, slightly thicker at the near (lower) edge
- palette: pale cornflower blue and periwinkle band, brightening to a pale blue-white inner edge, matching the reference cell
- the ellipse interior is mostly open: a very faint pale blue luminous wash at low alpha, not a solid fill
- luminous soft-light rendering with smooth alpha falloff; the glow must reach fully zero alpha well inside the locked bounds
- no solid black, white, or colored backdrop anywhere
- this effect IS explicitly a floor circle, so the flat ground-plane ring is correct and required
- do not clip the ring or its glow at any canvas edge

LIGHTING:
- soft upper-left key light at approximately 45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- the ring is self-luminous, so keep its own light consistent and even; do not cast it onto anything else

ISOLATION: the final asset contains ONLY the rear aura floor ring; exclude the character, body, feet, legs, skin, clothing, hair, objects, scenery, and any contact or drop shadow.

OUTPUT: one transparent 1254 x 1254 PNG. filename: aura_rear_001_blue_floor_ring.png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, a solid filled disc, a vertical or tilted halo, concentric or multiple rings, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, contact shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Mandatory candidate workflow

1. Upload the result to `images/trait_candidates/rear_auras/` as `aura_rear_001_blue_floor_ring_candidate_attempt_001.png`. Do not place it under `assets/` and do not edit `assets/asset_manifest.json`.
2. Run the gate:

   ```bash
   python scripts/rig_gate_report.py --trait images/trait_candidates/rear_auras/aura_rear_001_blue_floor_ring_candidate_attempt_001.png
   ```

   It must report a genuinely transparent background and `max_bounds` within `[233,129,1021,1139]`.
3. Composite the candidate over `assets/base_bodies/base_body_001_neutral_master.png` and confirm the ring sits at the feet, stays behind the body in the layer stack, and does not read as a shadow.
4. Obtain explicit human visual approval.
5. Only then register the exact bytes, update `docs/trait-production-backlog.md` DG-015 to `registered`, and run `python scripts/report_production_status.py --write`.

Keep every rejected attempt with its `_attempt_###` suffix and record the failure reason, as with backgrounds 002 and 004.
