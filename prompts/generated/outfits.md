# outfits — 10 assets to produce

Layer 06. Generated from the backlog; do not hand-edit.

**Gate every candidate:** `python scripts/rig_gate_report.py --trait --max-width-ratio 1.15 --min-skin-contrast 70 <file>`

Then composite over `assets/base_bodies/base_body_001_neutral_master.png` and confirm placement before requesting approval.


## Release-blocking category

`outfits` is listed in `generate_777.REQUIRED_CATEGORIES`, so `generate_777.py`
refuses to run while the category is empty. It is required because the base
bodies wear only a skin-toned mannequin garment — tank top `(252,218,182)` and
shorts `(247,211,174)` against cheek skin `(253,199,163)`. At full resolution
that garment reads fine; at marketplace thumbnail size the contrast disappears
and the chibi figures read as unclothed.

## The contrast gate

```bash
python scripts/rig_gate_report.py --trait <file> \
  --max-width-ratio 1.15 --min-skin-contrast 70
```

`skin_contrast` is the **mean RGB distance between the layer's opaque pixels and
the reference skin colour `(253,199,163)`**. The mannequin garment measures about
**27**; a deep navy robe measures about **274**. Any candidate below **70** must
be rejected: pale, skin-adjacent garments make the character appear unclothed at
thumbnail size, which is the exact failure this category exists to prevent.

## Production order

Produce in this order rather than by ID:

1. **DG-045** — `outfit_009_navy_high_collar_coat` — category representative test
2. **DG-040** — `outfit_004_black_ragged_hooded_cloak`
3. **DG-042** — `outfit_006_black_layered_hooded_robe`

The remaining mid-tone designs may follow in any order. Leave the three pale
designs until last, because they carry the highest contrast risk and are the
likeliest to need several attempts:

- **DG-037** — `outfit_001_celestial_robe_white_silver`
- **DG-041** — `outfit_005_white_blue_armored_mantle`
- **DG-046** — `outfit_010_celestial_robe_white_gold`

DG-045 leads because deep navy gives the largest possible margin over skin tone,
so it clears the release blocker with the fewest rejected rounds. There is no
reason to gate the release behind the hardest cases in the set.

**Register three or four approved outfits before rendering the collection.** The
gate only needs one, but a single robe across all 777 tokens produces excessive
visual repetition — and fixing that later means re-rendering the whole set.

## Workflow for every outfit candidate

1. Upload the candidate to `images/trait_candidates/outfits/`.
2. Run the outfit gate with `--max-width-ratio 1.15` and `--min-skin-contrast 70`.
3. Composite it over `assets/base_bodies/base_body_001_neutral_master.png`.
4. Check the neck, head and hand openings, garment coverage, and whether any
   mannequin garment shows through.
5. Downscale the composite to **210 px** and confirm the character still clearly
   reads as clothed. This is the test the category exists to pass.
6. Obtain human approval.
7. Register the asset.
8. Run `python scripts/report_production_status.py --write`.

---

## DG-037 — outfit_001_celestial_robe_white_silver

Dependency: DG-045; pale, high contrast risk, produce late  
Path: `assets/outfits/outfit_001_celestial_robe_white_silver.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: White-silver celestial ceremonial robe.
- source reference: OUTFIT, row 1 cell 1
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_001_celestial_robe_white_silver.png. No text, no alternate versions.
```

## DG-038 — outfit_002_black_split_tail_coat

Dependency: DG-045  
Path: `assets/outfits/outfit_002_black_split_tail_coat.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Black long coat with split cape tails.
- source reference: OUTFIT, row 1 cell 2
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_002_black_split_tail_coat.png. No text, no alternate versions.
```

## DG-039 — outfit_003_plum_gray_mage_robe

Dependency: DG-045  
Path: `assets/outfits/outfit_003_plum_gray_mage_robe.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Plum-gray long mage robe.
- source reference: OUTFIT, row 1 cell 3
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_003_plum_gray_mage_robe.png. No text, no alternate versions.
```

## DG-040 — outfit_004_black_ragged_hooded_cloak

Dependency: DG-045 representative test  
Path: `assets/outfits/outfit_004_black_ragged_hooded_cloak.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Black ragged hooded cloak outfit.
- source reference: OUTFIT, row 1 cell 4
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_004_black_ragged_hooded_cloak.png. No text, no alternate versions.
```

## DG-041 — outfit_005_white_blue_armored_mantle

Dependency: DG-045; pale, high contrast risk, produce late  
Path: `assets/outfits/outfit_005_white_blue_armored_mantle.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: White and blue armored ceremonial mantle.
- source reference: OUTFIT, row 1 cell 5
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_005_white_blue_armored_mantle.png. No text, no alternate versions.
```

## DG-042 — outfit_006_black_layered_hooded_robe

Dependency: DG-045 representative test  
Path: `assets/outfits/outfit_006_black_layered_hooded_robe.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Black layered hooded long robe.
- source reference: OUTFIT, row 2 cell 1
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_006_black_layered_hooded_robe.png. No text, no alternate versions.
```

## DG-043 — outfit_007_brown_leather_long_coat

Dependency: DG-045  
Path: `assets/outfits/outfit_007_brown_leather_long_coat.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Brown leather long coat/robe.
- source reference: OUTFIT, row 2 cell 2
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_007_brown_leather_long_coat.png. No text, no alternate versions.
```

## DG-044 — outfit_008_olive_ragged_cloak

Dependency: DG-045  
Path: `assets/outfits/outfit_008_olive_ragged_cloak.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Olive-green ragged cloak outfit.
- source reference: OUTFIT, row 2 cell 3
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_008_olive_ragged_cloak.png. No text, no alternate versions.
```

## DG-045 — outfit_009_navy_high_collar_coat

Dependency: Outfit representative test; highest contrast margin  
Path: `assets/outfits/outfit_009_navy_high_collar_coat.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Deep-navy high-collar long coat.
- source reference: OUTFIT, row 2 cell 4
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_009_navy_high_collar_coat.png. No text, no alternate versions.
```

## DG-046 — outfit_010_celestial_robe_white_gold

Dependency: DG-045; pale, high contrast risk, produce late  
Path: `assets/outfits/outfit_010_celestial_robe_white_gold.png`

```text
Create exactly one isolated Demigods outfit (clothing only), rendered NATIVELY at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

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

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.

SUBJECT: Silver-white high-collar ceremonial robe.
- source reference: OUTFIT, row 2 cell 5; naming example in docs/naming-and-export.md
- render this design only; do not substitute or embellish beyond the reference

PROPORTION: a garment hugs the figure AND must clear skin tone (253,199,163) by 70+.

OUTPUT: one transparent 1254 x 1254 PNG named outfit_010_celestial_robe_white_gold.png. No text, no alternate versions.
```

