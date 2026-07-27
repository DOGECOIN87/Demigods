# DEMIGODS — ready-to-run Grok trait prompts

One self-contained prompt per layer category, in back-to-front stack order. Each renders a single isolated transparent 1254x1254 trait aligned to the registered base body. Fill the `[SPECIFY ...]` slot (and `[NUM]`/`[COLOR]` in the filename) per asset.

**Every prompt:** attach `assets/base_bodies/base_body_001_neutral_master.png` + `docs/rig/rig_guide_1254.png` (hand objects also attach the matching pose). After generating, gate partial trait layers with `python scripts/rig_gate_report.py --trait <file>`, then confirm placement with a composite over the base master. Use `--pose-variant --tolerance 2` only for full-figure base poses; it measures head and leg bands and will false-fail a partial layer.

---

## Layer 02 — rear aura / effect (behind the character)

```
Create exactly one isolated Demigods rear aura / effect (behind the character), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one rear aura or effect: [SPECIFY — e.g. blue floor halo ring / violet radial glow / lightning wisps / rising void flame / sacred light].
- centered to the master rig, framing the character silhouette without covering the face zone
- luminous with soft transparent alpha falloff; no solid black, white, or colored fill
- include a floor disc ONLY if the effect is explicitly a floor circle
- do not clip glow or particles at the canvas edges

ISOLATION: the final asset contains ONLY the rear aura / effect (behind the character); exclude the character, clothing, objects, and scenery.

OUTPUT: one transparent 1254 x 1254 PNG. filename: aura_[NUM]_[TYPE]_[COLOR]_rear.png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 03 — back accessory (wings / cape / cloak / mantle / crest)

```
Create exactly one isolated Demigods back accessory (wings / cape / cloak / mantle / crest), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one back accessory: [SPECIFY — e.g. silver feathered wings / black-violet bat wings / navy formal cape / ragged cloak].
- align to the shared upper-back and shoulder-blade anchors, positioned BEHIND the body
- render as seen from the front while sitting behind the character
- wings are a balanced symmetrical pair unless deliberately asymmetric
- preserve a hidden central overlap behind the torso; respect the foot baseline

ISOLATION: the final asset contains ONLY the back accessory (wings / cape / cloak / mantle / crest); exclude the mannequin, body, head, hair, outfit, hands, and background.

OUTPUT: one transparent 1254 x 1254 PNG. filename: back_accessory_[NUM]_[TYPE]_[COLOR].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 04 — hair-back layer (rear hair only)

```
Create exactly one isolated Demigods hair-back layer (rear hair only), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create only the REAR portion of one hairstyle: [SPECIFY — length and shape, e.g. long wavy, straight, twin braids].
- back-hair layer only, positioned behind the head and shoulders
- align to the master scalp centered at X 627, Y 343; keep the head interior transparent
- exclude bangs and face-framing front strands (those are the separate front-hair layer)
- include hidden overlap behind the scalp to prevent seams
- Color: [COLOR]

ISOLATION: the final asset contains ONLY the hair-back layer (rear hair only); exclude bangs, front strands, face, ears, body, clothes, and accessories.

OUTPUT: one transparent 1254 x 1254 PNG. filename: hair_back_[NUM]_[COLOR]_[STYLE].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 06 — outfit (clothing only)

```
Create exactly one isolated Demigods outfit (clothing only), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one isolated outfit: [SPECIFY — theme, garments, colors, e.g. royal white-gold robe / dark prince armor / celestial dress].
- align to the shared neck, shoulders, torso, waist, wrists, hips, knees, and foot baseline
- preserve the exact approved body proportions; leave clean openings for head, neck, and hands
- include hidden overlap beneath hands, hair, and neck layers to prevent seams
- keep capes / wings / back effects as SEPARATE layers unless structurally inseparable

ISOLATION: the final asset contains ONLY the outfit (clothing only); exclude the body, head, face, hair, hands, held objects, aura, and scenery.

OUTPUT: one transparent 1254 x 1254 PNG. filename: outfit_[NUM]_[THEME]_[COLOR].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 07 — neck accessory (necklace / choker / collar / bow / pendant)

```
Create exactly one isolated Demigods neck accessory (necklace / choker / collar / bow / pendant), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one isolated neck accessory: [SPECIFY — type, material, color].
- align to the approved neck and upper-chest anchor
- preserve hidden overlap beneath hair and above the outfit

ISOLATION: the final asset contains ONLY the neck accessory (necklace / choker / collar / bow / pendant); exclude skin, outfit, head, face, and hair.

OUTPUT: one transparent 1254 x 1254 PNG. filename: neck_accessory_[NUM]_[TYPE]_[COLOR].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 08 — eye set (matched pair)

```
Create exactly one isolated Demigods eye set (matched pair), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one matched eye-set trait: [SPECIFY — iris color, pupil, style, e.g. galaxy blue / soul-flame violet / silver runic].
- both eyes aligned to Y 367 using the identical approved spacing and scale
- include eye lines, lashes, sclera, irises, pupils, internal highlights, and shading
- use the shared upper-left catchlight logic

ISOLATION: the final asset contains ONLY the eye set (matched pair); exclude eyebrows, nose, mouth, face, skin, blush, hair, and expression marks.

OUTPUT: one transparent 1254 x 1254 PNG. filename: eyes_[NUM]_[COLOR]_[STYLE].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 09 — eyebrow pair

```
Create exactly one isolated Demigods eyebrow pair, rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one matched eyebrow pair expressing [SPECIFY MOOD — e.g. calm, fierce, gentle, surprised].
- use the approved eyebrow anchor positions and line weight, just above the eye line (Y 367)
- remain compatible with all approved eye sets

ISOLATION: the final asset contains ONLY the eyebrow pair; exclude eyes, face, forehead, hair, nose, mouth, and blush.

OUTPUT: one transparent 1254 x 1254 PNG. filename: eyebrows_[NUM]_[MOOD].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 10 — mouth

```
Create exactly one isolated Demigods mouth, rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one isolated mouth: [SPECIFY — e.g. soft smile / confident smirk / open cheer / calm neutral / tiny pout / fang grin].
- center to the mouth anchor at X 627, Y 441 using the approved scale
- include only the mouth (and minimal chin shading if needed)

ISOLATION: the final asset contains ONLY the mouth; exclude eyes, eyebrows, nose, face, skin, blush, and hair.

OUTPUT: one transparent 1254 x 1254 PNG. filename: mouth_[NUM]_[TYPE].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 11 — expression mark overlay

```
Create exactly one isolated Demigods expression mark overlay, rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one isolated expression overlay: [SPECIFY — blush / sweat drop / anger mark / sparkles / stress lines / tears].
- align to the appropriate face zone (cheeks, temple, or above the head)
- include only the requested effect on clean transparent space; readable at small size

ISOLATION: the final asset contains ONLY the expression mark overlay; exclude face features, hair, body, and any full-character aura.

OUTPUT: one transparent 1254 x 1254 PNG. filename: expression_[NUM]_[TYPE].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 12 — hair-front layer (bangs / front strands only)

```
Create exactly one isolated Demigods hair-front layer (bangs / front strands only), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create only the FRONT portion of one hairstyle: [SPECIFY — bang shape and parting].
- bangs and front face-framing strands only; align to the shared scalp, forehead, temple, and ear anchors
- preserve the approved face opening; do not change head dimensions
- include hidden overlap beneath the top hairline to prevent seams
- Color: [COLOR]  (match the paired hair-back layer)

ISOLATION: the final asset contains ONLY the hair-front layer (bangs / front strands only); exclude rear hair, scalp, face, skin, eyes, eyebrows, mouth, ears, clothing, crowns, horns, halos, and jewelry.

OUTPUT: one transparent 1254 x 1254 PNG. filename: hair_front_[NUM]_[COLOR]_[STYLE].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 13 — head accessory (crown / halo / horns / tiara / laurel / circlet / veil)

```
Create exactly one isolated Demigods head accessory (crown / halo / horns / tiara / laurel / circlet / veil), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one isolated head accessory: [SPECIFY — type, material, color].
- center to the approved head anchor at X 627, Y 343; sit on top of or around the head
- preserve hidden overlap where it enters or sits behind hair
- use a balanced pair for horns or side ornaments; keep halos and open metalwork transparent inside

ISOLATION: the final asset contains ONLY the head accessory (crown / halo / horns / tiara / laurel / circlet / veil); exclude hair, scalp, face, eyes, body, clothing, neck accessory, and aura.

OUTPUT: one transparent 1254 x 1254 PNG. filename: head_accessory_[NUM]_[TYPE]_[MATERIAL].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 14 — hand-held object

```
Create exactly one isolated Demigods hand-held object, rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png + the matching pose file (e.g. assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png)

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one isolated hand-held object: [SPECIFY — staff / orb / book / sword / wand / lantern / relic]. Assigned hand: [VIEWER-LEFT X404,Y772 / VIEWER-RIGHT X850,Y772 / BOTH].
- align the grip/contact point exactly to the assigned hand anchor, matching the chosen pose's grip angle
- include the object only, plus a minimal grip overlay ONLY if technically necessary
- contain any glow within transparent alpha falloff; keep the whole object uncropped

ISOLATION: the final asset contains ONLY the hand-held object; exclude the body, arm, outfit, face, and background.

OUTPUT: one transparent 1254 x 1254 PNG. filename: hand_object_[NUM]_[TYPE]_pose_[POSE]_[SIDE].png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```

## Layer 15 — front aura / effect (in front of the character)

```
Create exactly one isolated Demigods front aura / effect (in front of the character), rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish

TARGET:
Create one front aura or effect: [SPECIFY — sparkles / floating stars / embers / petals / energy motes].
- centered to the master rig, sitting in FRONT of the character but never covering the eyes or mouth
- luminous with soft transparent alpha falloff; no solid backdrop
- do not clip particles at the canvas edges

ISOLATION: the final asset contains ONLY the front aura / effect (in front of the character); exclude the character, clothing, objects, and scenery.

OUTPUT: one transparent 1254 x 1254 PNG. filename: aura_[NUM]_[TYPE]_[COLOR]_front.png

AVOID:
photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, merged trait categories, unrelated traits, scenery, character or franchise names, blurry or low-detail rendering, inconsistent or front-right lighting.

Return one transparent PNG only. No text or alternate versions.
```
