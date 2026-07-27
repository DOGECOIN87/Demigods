# neck_accessories — 8 assets to produce

Layer 07. Generated from the backlog; do not hand-edit.

**Gate every candidate:** `python scripts/rig_gate_report.py --trait <file>`

Then composite over `assets/base_bodies/base_body_001_neutral_master.png` and confirm placement before requesting approval.

---

## DG-047 — neck_accessory_001_black_choker

Dependency: Approved Pose 001 and outfit test  
Path: `assets/neck_accessories/neck_accessory_001_black_choker.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Plain black curved choker.
- source reference: ACCESSORY, lower row cell 1
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_001_black_choker.png. No text, no alternate versions.
```

## DG-048 — neck_accessory_002_gold_blue_drop_choker

Dependency: DG-047 representative test  
Path: `assets/neck_accessories/neck_accessory_002_gold_blue_drop_choker.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Warm-gold choker with dark-blue drop.
- source reference: ACCESSORY, lower row cell 2
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_002_gold_blue_drop_choker.png. No text, no alternate versions.
```

## DG-049 — neck_accessory_003_black_ribbon_bow

Dependency: DG-047  
Path: `assets/neck_accessories/neck_accessory_003_black_ribbon_bow.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Black ribbon bow.
- source reference: ACCESSORY, lower row cell 3
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_003_black_ribbon_bow.png. No text, no alternate versions.
```

## DG-050 — neck_accessory_004_silver_dark_round_pendant

Dependency: DG-047  
Path: `assets/neck_accessories/neck_accessory_004_silver_dark_round_pendant.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Fine silver chain with dark round pendant.
- source reference: ACCESSORY, lower row cell 4
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_004_silver_dark_round_pendant.png. No text, no alternate versions.
```

## DG-051 — neck_accessory_005_silver_navy_long_pendant

Dependency: DG-047  
Path: `assets/neck_accessories/neck_accessory_005_silver_navy_long_pendant.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Silver V-chain with long navy pendant.
- source reference: ACCESSORY, lower row cell 5
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_005_silver_navy_long_pendant.png. No text, no alternate versions.
```

## DG-052 — neck_accessory_006_silver_pale_circle_charm

Dependency: DG-047  
Path: `assets/neck_accessories/neck_accessory_006_silver_pale_circle_charm.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Fine silver chain with pale circular charm.
- source reference: ACCESSORY, lower row cell 6
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_006_silver_pale_circle_charm.png. No text, no alternate versions.
```

## DG-053 — neck_accessory_007_gold_teardrop_pendant

Dependency: DG-047  
Path: `assets/neck_accessories/neck_accessory_007_gold_teardrop_pendant.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Gold chain with long teardrop pendant.
- source reference: ACCESSORY, lower row cell 7
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_007_gold_teardrop_pendant.png. No text, no alternate versions.
```

## DG-054 — neck_accessory_008_violet_ribbon_bow

Dependency: DG-047  
Path: `assets/neck_accessories/neck_accessory_008_violet_ribbon_bow.png`

```text
Create exactly one isolated Demigods neck accessory, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Violet ribbon bow.
- source reference: ACCESSORY, lower row cell 8
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: small layer; sits at the collar.

OUTPUT: one transparent 1254 x 1254 PNG named neck_accessory_008_violet_ribbon_bow.png. No text, no alternate versions.
```

