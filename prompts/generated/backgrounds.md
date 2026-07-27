# backgrounds — 10 assets to produce

Layer 01. Generated from the backlog; do not hand-edit.

**Gate every candidate:** `python scripts/rig_gate_report.py n/a — backgrounds are opaque, not gated by the rig <file>`

Then composite over `assets/base_bodies/base_body_001_neutral_master.png` and confirm placement before requesting approval.

---

## DG-011 — background_005_solar_sky_temple

Dependency: DG-010  
Path: `assets/backgrounds/background_005_solar_sky_temple.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: White-and-gold open-air solar temple with sky, clouds, star motif, and ceremonial platform.
- source reference: BG/background_005_solar_sky_temple_reference.jpg
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_005_solar_sky_temple.png. No text, no alternate versions.
```

## DG-012 — background_006_moonlit_marble_balcony

Dependency: DG-011  
Path: `assets/backgrounds/background_006_moonlit_marble_balcony.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Moonlit pale-marble balcony with arches, mountains, stars, and cool floor shadows.
- source reference: BG/background_006_moonlit_marble_balcony_reference.jpg
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_006_moonlit_marble_balcony.png. No text, no alternate versions.
```

## DG-013 — background_007_golden_celestial_gateway

Dependency: DG-012  
Path: `assets/backgrounds/background_007_golden_celestial_gateway.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Layered white-stone golden gateway with portal light, star emblem, stairs, and plants.
- source reference: BG/background_007_golden_celestial_gateway_reference.jpg
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_007_golden_celestial_gateway.png. No text, no alternate versions.
```

## DG-014 — background_008_violet_void_portal

Dependency: DG-013  
Path: `assets/backgrounds/background_008_violet_void_portal.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Circular violet void portal with floating platform, rocks, crystals, and smoke.
- source reference: BG/background_008_violet_void_portal_reference.jpg
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_008_violet_void_portal.png. No text, no alternate versions.
```

## DG-158 — background_009_luminous_world_tree

Dependency: Staging review  
Path: `assets/backgrounds/background_009_luminous_world_tree.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Luminous world-tree grove with fireflies, moss floor, and green canopy.
- source reference: BG2 world tree
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_009_luminous_world_tree.png. No text, no alternate versions.
```

## DG-159 — background_010_infinite_arcane_library

Dependency: Staging review  
Path: `assets/backgrounds/background_010_infinite_arcane_library.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Infinite arcane library with floating books, arched window, and starfield.
- source reference: BG2 infinite library
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_010_infinite_arcane_library.png. No text, no alternate versions.
```

## DG-160 — background_011_ember_ruins

Dependency: Staging review  
Path: `assets/backgrounds/background_011_ember_ruins.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Ember ruins with broken arches, cracked lava ground, and smoke sky.
- source reference: BG2 ember ruins
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_011_ember_ruins.png. No text, no alternate versions.
```

## DG-161 — background_012_clockwork_sanctum

Dependency: Staging review  
Path: `assets/backgrounds/background_012_clockwork_sanctum.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Clockwork sanctum with brass gears, lanterns, and a raised circular platform.
- source reference: BG2 clockwork sanctum
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_012_clockwork_sanctum.png. No text, no alternate versions.
```

## DG-162 — background_013_crystal_spire_peak

Dependency: Needs a floor plane  
Path: `assets/backgrounds/background_013_crystal_spire_peak.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Crystal spire peak above cloud sea with violet and cyan crystals.
- source reference: BG2 crystal spire
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_013_crystal_spire_peak.png. No text, no alternate versions.
```

## DG-163 — background_014_skybound_isles

Dependency: Needs a floor plane  
Path: `assets/backgrounds/background_014_skybound_isles.png`

```text
Create exactly one full-bleed Demigods full-bleed background, rendered NATIVELY at exactly 1254 x 1254 pixels.

ATTACH: the matching reference image.

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

BACKGROUND CONTRACT:
- fill every canvas pixel; no transparency and no empty border
- preserve a clear central staging region within X 233-1021 and Y 129-1139
- provide a believable floor surface at foot baseline Y 1139 that a character
  can stand on and a floor-ring aura can sit on
- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is
  applied afterward by scripts/apply_background_depth.py, and requesting it here
  double-treats the image irreversibly
- rebuild natively from the reference; never upscale, trace, tile, or patch it

SUBJECT: Skybound isles with waterfalls, a lit bridge, and cloud vista.
- source reference: BG2 skybound isles
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: full canvas, RGB or fully opaque RGBA, no transparency.

OUTPUT: one opaque 1254 x 1254 PNG named background_014_skybound_isles.png. No text, no alternate versions.
```

