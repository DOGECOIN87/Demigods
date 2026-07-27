# back_accessories — 8 assets to produce

Layer 03. Generated from the backlog; do not hand-edit.

**Gate every candidate:** `python scripts/rig_gate_report.py --trait <file>`

Then composite over `assets/base_bodies/base_body_001_neutral_master.png` and confirm placement before requesting approval.

---

## DG-021 — back_accessory_001_silver_feathered_wings

Dependency: Locked pose family  
Path: `assets/back_accessories/back_accessory_001_silver_feathered_wings.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Pale silver feathered wing pair.
- source reference: AURA, upper row cell 1
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_001_silver_feathered_wings.png. No text, no alternate versions.
```

## DG-022 — back_accessory_002_black_violet_bat_wings

Dependency: DG-021 representative test  
Path: `assets/back_accessories/back_accessory_002_black_violet_bat_wings.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Black-violet bat wing pair.
- source reference: AURA, upper row cell 2
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_002_black_violet_bat_wings.png. No text, no alternate versions.
```

## DG-023 — back_accessory_003_cyan_fairy_wings

Dependency: DG-021  
Path: `assets/back_accessories/back_accessory_003_cyan_fairy_wings.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Translucent cyan fairy wing pair.
- source reference: AURA, upper row cell 3
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_003_cyan_fairy_wings.png. No text, no alternate versions.
```

## DG-024 — back_accessory_004_navy_formal_cape

Dependency: DG-021  
Path: `assets/back_accessories/back_accessory_004_navy_formal_cape.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Deep navy formal cape.
- source reference: AURA, upper row cell 4
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_004_navy_formal_cape.png. No text, no alternate versions.
```

## DG-025 — back_accessory_005_black_violet_ragged_cloak

Dependency: DG-021  
Path: `assets/back_accessories/back_accessory_005_black_violet_ragged_cloak.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Black-purple ragged cloak.
- source reference: AURA, upper row cell 5
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_005_black_violet_ragged_cloak.png. No text, no alternate versions.
```

## DG-026 — back_accessory_006_pale_blue_crystal_wings

Dependency: DG-021  
Path: `assets/back_accessories/back_accessory_006_pale_blue_crystal_wings.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Pale-blue crystalline wing/mantle pair.
- source reference: AURA, upper row cell 6
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_006_pale_blue_crystal_wings.png. No text, no alternate versions.
```

## DG-027 — back_accessory_007_gold_luminous_wings

Dependency: DG-021  
Path: `assets/back_accessories/back_accessory_007_gold_luminous_wings.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Luminous gold feathered wing pair.
- source reference: AURA, upper row cell 7
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_007_gold_luminous_wings.png. No text, no alternate versions.
```

## DG-028 — back_accessory_008_olive_silver_spiked_wings

Dependency: DG-021  
Path: `assets/back_accessories/back_accessory_008_olive_silver_spiked_wings.png`

```text
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view

SUBJECT: Olive-silver mechanical/spiked wing pair.
- source reference: AURA, upper row cell 8
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no ceiling — wings and capes run 1.6-2.0x body width by design.

OUTPUT: one transparent 1254 x 1254 PNG named back_accessory_008_olive_silver_spiked_wings.png. No text, no alternate versions.
```

