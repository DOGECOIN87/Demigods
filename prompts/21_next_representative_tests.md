# Prompts — Remaining assets as of 2026-07-27

Ready-to-run prompts for everything still missing. Per-category templates live in `prompts/ready_to_run_trait_prompts.md`; this file fills in the specific assets that are next in dependency order, plus the two groups with extra constraints.

Every prompt below inherits the shared contract from the generated template file: native 1254 × 1254, paint on transparency, **never** key a background out, bright partial alpha, zero stray pixels.

## Priority order

| Asset | Why it is next | Route |
|---|---|---|
| DG-021 silver feathered wings | back-accessory representative test; unblocks DG-022–028 | generator |
| DG-037 celestial robe | outfit representative test; unblocks DG-038–046 | generator |
| DG-151–157 textured rings | extend a registered family; seating already solved | generator |
| Backgrounds 005–008 | 4 of 8 registered; each adds directly to combination space | generator + depth pass |
| DG-029–036 hair back | representative test registered; needs correct proportions | generator |

Combination space is currently **120 of 777**. A single 8-member category multiplies it by 8, so outfits and eyes move the number fastest.

---

## DG-021 — Back accessory 001, silver feathered wings

Representative test for the whole back-accessory category. Reference: `AURA` sheet, upper row cell 1.

Intended path: `assets/back_accessories/back_accessory_001_silver_feathered_wings.png`

```text
Create exactly one isolated Demigods back accessory, rendered NATIVELY at exactly 1254 x 1254 pixels, RGBA PNG with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — a 1024 x 1024 result is an automatic rejection:
- exactly 1254 x 1254, generated natively at that size
- never upscale, downscale, or resample to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND. Paint directly onto an empty transparent canvas. Do not render on black, white, or any backdrop and then key it to transparency — that leaves the backdrop in the colour channels and produces a gray matte fringe, which is an automatic rejection.

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value; a pixel at alpha 30 still reads as pale silver, never dark gray
- composited over pure WHITE the layer must not darken the background
- no gray, black, or neutral fringe in any soft edge

SUBJECT: one balanced symmetrical pair of pale silver feathered wings, seen from the front, sitting BEHIND the character.
- wings spread upward and outward from the shoulder-blade anchors, around shoulder line Y 569
- layered flight feathers with clean separation; crisp anti-aliased edges, no blur
- pale silver-white with cool blue-gray shadow in the feather underlayers
- soft upper-left key light at ~45 degrees, lower-right form shadows
- a hidden central overlap behind the torso so no seam shows when the body composites over it
- symmetrical left to right about X 627
- keep every visible pixel within X 233-1021 and Y 129-1139
- do not clip the wingtips at any canvas edge

PROPORTION: wings legitimately exceed the body width — 1.6x to 2.0x is correct for this category. Do not shrink them to the body silhouette.

STRAY PIXELS: every pixel outside the wings must be exactly alpha 0. No alpha-1 dust anywhere on the canvas.

ISOLATION: the final asset contains ONLY the wings. No body, head, hair, outfit, hands, aura, scenery, or contact shadow.

OUTPUT: one transparent 1254 x 1254 PNG. No text, no alternate versions, no contact sheet.
```

Gate: `python scripts/rig_gate_report.py --trait <file>` — **no** `--max-width-ratio`; a ceiling would false-fail the category. Then composite over the base master to confirm the torso hides the central overlap.

---

## DG-037 — Outfit 001, white-silver celestial ceremonial robe

Representative test for the outfit category. Reference: `OUTFIT` sheet, row 1 cell 1.

Intended path: `assets/outfits/outfit_001_celestial_robe_white_silver.png`

```text
Create exactly one isolated Demigods outfit, rendered NATIVELY at exactly 1254 x 1254 pixels, RGBA PNG with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — a 1024 x 1024 result is an automatic rejection:
- exactly 1254 x 1254, generated natively at that size
- never upscale, downscale, or resample to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND. Paint directly onto an empty transparent canvas, never keyed out of a rendered backdrop.

SUBJECT: one white-and-silver celestial ceremonial robe, worn shape only, no body inside it.
- fitted to the attached base body exactly: neck opening at the collar, shoulders at Y 569, waist at X 627 Y 808, hem clear of foot baseline Y 1139
- flowing floor-length robe with a structured bodice, soft draped skirt, and silver trim at collar, cuffs and hem
- subtle celestial ornament: fine silver star or constellation embroidery, non-readable, no letters or runes
- opaque fabric throughout with clear edges; no skin-tone fabric that could read as bare body
- clean openings where the head, neck and hands emerge, matching the base body silhouette
- hidden overlap beneath the neck and hands so no seam shows when those layers composite
- soft upper-left key light at ~45 degrees, lower-right form shadows, subtle cool right rim
- symmetrical about X 627, perfectly front-facing, zero perspective

PROPORTION: a garment hugs the figure. Total width must stay within about 1.15x the base body width — this is clothing, not a cape. Keep capes and mantles as a separate back-accessory layer.

CONTENT: modest ceremonial clothing only. No nudity, lingerie, swimwear, exposed torso or hips, or emphasized anatomical contours.

STRAY PIXELS: every pixel outside the garment must be exactly alpha 0.

ISOLATION: the final asset contains ONLY the garment. No body, skin, head, face, hair, hands, held objects, aura, or scenery.

OUTPUT: one transparent 1254 x 1254 PNG. No text, no alternate versions, no contact sheet.
```

Gate: `python scripts/rig_gate_report.py --trait <file> --max-width-ratio 1.15`, then composite over the base master and confirm the head, neck and hand openings line up.

---

## DG-151–157 — Textured floor rings

Seven rings from `images/reference_sheets/floor_ring_aura_variants_sheet.png`. The geometry is **already solved** by the four registered neon rings — these differ only in surface treatment, so the seating must match exactly or the family will not stack.

| ID | Cell | Design | Path stem |
|---|---|---|---|
| DG-151 | row 1 cell 2 | Orange fire ring | `aura_rear_011_fire_ring` |
| DG-152 | row 1 cell 3 | Blue lightning ring | `aura_rear_012_lightning_ring` |
| DG-153 | row 2 cell 2 | Violet flame ring | `aura_rear_013_violet_flame_ring` |
| DG-154 | row 3 cell 1 | Pale-blue ice crystal ring | `aura_rear_014_ice_crystal_ring` |
| DG-155 | row 3 cell 3 | Black smoke void ring | `aura_rear_015_smoke_void_ring` |
| DG-156 | row 4 cell 2 | Violet cosmic sparkle ring | `aura_rear_016_cosmic_sparkle_ring` |
| DG-157 | row 4 cell 3 | Cyan water splash ring | `aura_rear_017_water_splash_ring` |

Substitute the design per row:

```text
Create exactly one isolated Demigods rear aura, rendered NATIVELY at exactly 1254 x 1254 pixels, RGBA PNG with genuine transparent alpha.

ATTACH: assets/rear_auras/aura_rear_001_blue_floor_ring.png (EXACT geometry and placement reference) + assets/base_bodies/base_body_001_neutral_master.png + the floor-ring variants sheet

CANVAS: exactly 1254 x 1254 natively. Never upscale or resample. A 1024 x 1024 result is an automatic rejection.

DO NOT REMOVE A BACKGROUND. Paint on transparency. A keyed-out backdrop leaves a gray matte fringe and is an automatic rejection.

GEOMETRY — match the attached blue ring exactly:
- a horizontal ellipse lying flat on the ground plane, centred on X 627
- outer extent spanning X 293 to X 960, from Y 1035 down to Y 1221
- the ring is SEATED ON THE FEET: the far arc passes behind the ankles, the near arc in front of the toes, so the character stands INSIDE it
- the near arc falls below foot baseline Y 1139 — this is correct and required
- nothing may touch the final canvas row; keep at least 30 px clear of the bottom edge
- interior stays open and transparent; no filled disc

SURFACE TREATMENT: [SPECIFY — e.g. licking orange flames rising from the ring band / crackling blue lightning arcing along the ellipse / faceted pale-blue ice shards standing along the ring / churning black smoke / violet sparkles and stars / cyan water splashing outward].
- the treatment follows the ellipse; it must not become a sphere, a vertical halo, or a scattered cloud
- luminous where the design is energy; every partial-alpha pixel keeps a bright colour value
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS: every pixel outside the ring and its effect must be exactly alpha 0. No alpha-1 dust.

ISOLATION: only the ring effect. No character, feet, legs, scenery, or contact shadow.

OUTPUT: one transparent 1254 x 1254 PNG.
```

Gate: `python scripts/rig_gate_report.py --floor-aura <file>` — **not** `--trait`, which rejects the near arc below Y 1139 by design.

---

## Backgrounds 005–008

Use `prompts/17_native_1254_backgrounds.md` unchanged, attaching the matching reference from `images/background_candidates/`.

| ID | Reference | Path stem |
|---|---|---|
| DG-011 | `background_005_solar_sky_temple_reference.jpg` | `background_005_solar_sky_temple` |
| DG-012 | `background_006_moonlit_marble_balcony_reference.jpg` | `background_006_moonlit_marble_balcony` |
| DG-013 | `background_007_golden_celestial_gateway_reference.jpg` | `background_007_golden_celestial_gateway` |
| DG-014 | `background_008_violet_void_portal_reference.jpg` | `background_008_violet_void_portal` |

**Generate fully sharp and unvignetted.** The depth treatment is applied afterward so all eight match:

```bash
python scripts/apply_background_depth.py <new background> --blur 2.5 --vignette 0.22 --vignette-power 2.4
```

Requesting blur or vignette from the generator on top of that pass double-treats the image and destroys detail that cannot be recovered.

Each background must also preserve a clear central staging region within X 233–1021, Y 129–1139, and a floor surface at foot baseline Y 1139 that the seated floor rings can sit on.

---

## DG-029–036 — Remaining hair-back colours

`hair_back_003` is registered as the representative test, but it was refitted rather than rendered at correct proportions. Render these natively to the target instead of repeating the refit:

- total width about **1.2 ×** the base body width — roughly 530 px, spanning about X 360 to X 890
- the top must reach **Y 132 or above**, so a hair rim shows above the head crown at Y 141 rather than a bald gap
- length falling to roughly **Y 720**, behind the shoulders, clear of the arms

Use the Layer 04 template in `prompts/ready_to_run_trait_prompts.md` with the colour and style from the `HAIR` sheet cell, and add the three measurements above.

The eight `HAIR` upper-row cells are **distinct cuts, not one design recoloured** — see the backlog note. Each must follow its own cell.

Gate: `python scripts/rig_gate_report.py --trait <file> --max-width-ratio 1.35` and confirm the reported crown offset is positive.
