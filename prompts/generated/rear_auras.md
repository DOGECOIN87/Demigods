# rear_auras — 11 assets to produce

Layer 02. Generated from the backlog; do not hand-edit.

**Gate every candidate:** `python scripts/rig_gate_report.py --floor-aura for ground rings, --trait for body-centred glows <file>`

Then composite over `assets/base_bodies/base_body_001_neutral_master.png` and confirm placement before requesting approval.

---

## DG-016 — aura_rear_002_violet_radial_glow

Dependency: DG-015 representative test  
Path: `assets/rear_auras/aura_rear_002_violet_radial_glow.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Soft violet circular radial glow.
- source reference: AURA, lower row cell 2
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_002_violet_radial_glow.png. No text, no alternate versions.
```

## DG-017 — aura_rear_003_blue_crystalline_burst

Dependency: DG-015  
Path: `assets/rear_auras/aura_rear_003_blue_crystalline_burst.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Blue crystalline energy burst.
- source reference: AURA, lower row cell 3
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_003_blue_crystalline_burst.png. No text, no alternate versions.
```

## DG-018 — aura_rear_004_violet_void_flame

Dependency: DG-015  
Path: `assets/rear_auras/aura_rear_004_violet_void_flame.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Dark violet rising void flame.
- source reference: AURA, lower row cell 4
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_004_violet_void_flame.png. No text, no alternate versions.
```

## DG-019 — aura_rear_005_lavender_lightning

Dependency: DG-015  
Path: `assets/rear_auras/aura_rear_005_lavender_lightning.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Pale-lavender vertical lightning wisps.
- source reference: AURA, lower row cell 5
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_005_lavender_lightning.png. No text, no alternate versions.
```

## DG-151 — aura_rear_011_fire_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_011_fire_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Orange fire ring (generator).
- source reference: RING, cell 6
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_011_fire_ring.png. No text, no alternate versions.
```

## DG-152 — aura_rear_012_lightning_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_012_lightning_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Blue lightning ring (generator).
- source reference: RING, cell 7
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_012_lightning_ring.png. No text, no alternate versions.
```

## DG-153 — aura_rear_013_violet_flame_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_013_violet_flame_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Violet flame ring (generator).
- source reference: RING, cell 8
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_013_violet_flame_ring.png. No text, no alternate versions.
```

## DG-154 — aura_rear_014_ice_crystal_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_014_ice_crystal_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Pale-blue ice crystal ring (generator).
- source reference: RING, cell 9
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_014_ice_crystal_ring.png. No text, no alternate versions.
```

## DG-155 — aura_rear_015_smoke_void_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_015_smoke_void_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Black smoke void ring (generator).
- source reference: RING, cell 10
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_015_smoke_void_ring.png. No text, no alternate versions.
```

## DG-156 — aura_rear_016_cosmic_sparkle_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_016_cosmic_sparkle_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Violet cosmic sparkle ring (generator).
- source reference: RING, cell 11
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_016_cosmic_sparkle_ring.png. No text, no alternate versions.
```

## DG-157 — aura_rear_017_water_splash_ring

Dependency: DG-015 seating and gate mode  
Path: `assets/rear_auras/aura_rear_017_water_splash_ring.png`

```text
Create exactly one isolated Demigods rear aura / effect behind the character, rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

SUBJECT: Cyan water splash ring (generator).
- source reference: RING, cell 12
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: no width ceiling; auras vary by design.

OUTPUT: one transparent 1254 x 1254 PNG named aura_rear_017_water_splash_ring.png. No text, no alternate versions.
```

