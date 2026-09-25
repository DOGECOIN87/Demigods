> Repository companion to the manual-generation download pack delivered on 2026-09-25. The `prompts/` and `references/` paths below refer to that extracted pack. Original repository source links are listed in the Reference origins table. The latest sleeveless Olive Cloak reference is also checkpointed at `incoming/manual_prompt_reference_2026-09-25/outfit_008_olive_ragged_cloak_sleeveless_latest.png`; it is a design reference only, not a newly approved outfit. All 50 prompts are reproduced in full below.

# Demigods — 50 outfit and pose prompts

10 outfits × 5 approved poses = 50 separate outfit PNGs.

Every prompt is fully filled in and can be copied on its own. The pack includes 5 approved base-pose images, 10 outfit design references, 50 individual TXT prompts, one compiled Markdown document and an output/reference index. The images in `references/` are source references, not newly generated or newly approved production assets.

## Start here

1. Extract the ZIP. Choose an outfit folder under `prompts/` and open `pose_001.txt`.
2. Upload the two PNG references named at the top, in the stated order: exact base pose first, outfit design second. Attach the actual files; pasting filenames alone is not enough.
3. Copy the entire TXT prompt into your image generator and generate one PNG. Save the original transparent file with the output name at the bottom. Keep each attempt separate until one is approved.
4. Composite that result over its matching base at X=0, Y=0, without resizing either image. Check on both light and dark backgrounds using the checklist below.
5. Once Pose 001 is acceptable, generate the same outfit's Pose 005 as an early hand-overlap check, then Poses 002, 003 and 004. Use each pose's own prompt and own base. You may add the approved Pose 001 outfit as a third design reference to keep the family consistent.
6. Repeat for all ten outfits. A family is complete only when all five variants pass. A neutral outfit, a mirrored copy or a renamed PNG does not count as another pose.

**Start with `prompts/001_celestial_scholar/pose_001.txt`.** Send back original PNGs rather than screenshots when they are ready for fit review.

Prompts can guide the generator but cannot guarantee pixel-perfect fit or reliable alpha. Each result remains a candidate until its actual composite has been inspected. If your generator cannot produce native 1254 × 1254 RGBA, keep the original output separately as source art and flag the limitation. Do not upscale or stretch it to claim compatibility. The repository's separate source-transform workflow must be followed before any non-native result can be reviewed as production art.

## Pose key

Left and right always mean the viewer's left and right. The two side grips are low at the sides, not arms raised in the air.

| Pose | Gesture | Exact Image 1 |
|---|---|---|
| 001 | Neutral — both hands open | `base_body_001_neutral_master.png` |
| 002 | Viewer-left vertical grip | `base_pose_002_viewer_left_vertical_grip.png` |
| 003 | Viewer-right vertical grip | `base_pose_003_viewer_right_vertical_grip.png` |
| 004 | Viewer-left palm up | `base_pose_004_viewer_left_palm_up.png` |
| 005 | Centered two-hand grip | `base_pose_005_centered_two_hand_grip.png` |

## Outfit key

| Outfit | Design | Arm coverage |
|---|---|---|
| 001 | Celestial Scholar | Sleeveless; arms visible below designed shoulder cover |
| 002 | Storm Guardian | Sleeveless; arms visible below designed shoulder cover |
| 003 | Verdant Alchemist | Full sleeves; hands and neck visible |
| 004 | Lunar Oracle | Sleeveless; arms visible below designed shoulder cover |
| 005 | Sun Temple | Short sleeves; forearms and hands visible |
| 006 | Black Layered Hooded Robe | Full sleeves; hands and neck visible |
| 007 | Brown Leather Long Coat | Full sleeves; hands and neck visible |
| 008 | Olive Ragged Cloak | Sleeveless; arms visible below designed shoulder cover |
| 009 | Navy High-Collar Coat | Full sleeves; hands and neck visible |
| 010 | Celestial Robe — White and Gold | Full sleeves; hands and neck visible |

The Alchemist keeps its rolled-cuff styling, but the sleeves are fitted through the wrists to honor the existing hands-and-neck-only exposure rule. The latest Olive Cloak intentionally exposes the arms below its capelet; do not revert to the older full-sleeved catalog version.

## Check every generated PNG

- Actual file: 1254 × 1254, RGBA, genuine transparent background and corners. A visible checkerboard painted into the image is a failure.
- Placement: unchanged base coordinates, front-facing camera, original avatar scale and large empty head area. The collar must not rise into the face region. Both complete soles sit on the approved Y=1139 baseline.
- Coverage: no cream tank or shorts visible at the neckline, sides, waist, hips, crotch or thighs; no shoulder crescents where the design has sleeves.
- Exposure: the base's original neck, exposed arms, hands and fingers remain visible exactly where the design allows. No skin is baked into the outfit PNG.
- Pose 005: bare-arm outfits have exact forearm and hand apertures. Full-sleeve outfits draw sleeves over the forearms and have exact hand apertures. Neither type may use a broad triangular cutout that exposes the tank/shorts.
- Detail: inspect neck, shoulders, elbows, cuffs, every finger, waist, hips, knees, ankles, toes and soles at 200–400% on light and dark composites. Check the whole figure at normal size as well.
- Design: identical family colors, motifs, garment construction and asymmetry in all five poses. No stretched lapels, narrowed sashes, broken piping, smeared contour fills or added accessories.
- Edges: no detached pixels, pale arm outlines, green key fringe, gray/white halo, floor shadow or cropped footwear.

After visual approval, each filename must be bound to its exact base pose in the collection's compatibility rules and pass the existing intake/manifest checks. Merely generating these files does not register them.

## Important reference details

The base-pose image is the placement authority. Older written shoulder and waist coordinates do not reliably describe the visible anatomy; these prompts deliberately use the image contours for those positions. Shared stable anchors are canvas 1254 × 1254, center X=627, head top near Y=141 and foot baseline Y=1139.

All original design files are included unchanged, so their defects remain visible. Use their construction and colors, not their existing alpha or fit, as the model:

- Scholar: ignore the pale outlines of absent arms.
- Sun Temple: discard the baked-in neck, forearms and hands. Poses 001–004 need continuous garment fabric where its source's centered hands used to be. Pose 005 needs alpha apertures following the exact base.
- Standing collars: keep a true transparent neck opening with visible inner fabric facing; do not copy a flat white, gray or skin-colored neck patch.
- Olive Cloak: use the latest sleeveless file supplied here, including complete boot toes and soles.
- Structured coats and robes: redraw their fit at the base's width; keep lapels, sash width, trim and motif proportions intact.

## Reference origins

Repository sources are pinned to commit `d5c31dd39428732d193d9161624f4ce0beecf6c2`. Pose files come from `assets/base_bodies/`. The latest Olive Cloak is the user-supplied “Olive cloak boot-edge cleanup.png,” copied byte-for-byte with a simpler pack filename.

| Outfit | Image 2 in the pack | Origin |
|---|---|---|
| 001 | `outfit_001_celestial_scholar_pose_001.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_001_celestial_scholar_pose_001.png) |
| 002 | `outfit_002_storm_guardian_pose_002.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_002_storm_guardian_pose_002.png) |
| 003 | `outfit_003_verdant_alchemist_pose_003.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_003_verdant_alchemist_pose_003.png) |
| 004 | `outfit_004_lunar_oracle_pose_004.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_004_lunar_oracle_pose_004.png) |
| 005 | `outfit_005_sun_temple_pose_005.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_005_sun_temple_pose_005.png) |
| 006 | `outfit_006_black_layered_hooded_robe.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_006_black_layered_hooded_robe.png) |
| 007 | `outfit_007_brown_leather_long_coat.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_007_brown_leather_long_coat.png) |
| 008 | `outfit_008_olive_ragged_cloak_sleeveless_latest.png` | Latest user-provided sleeveless olive-cloak reference. Overrides the older catalog. |
| 009 | `outfit_009_navy_high_collar_coat.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_009_navy_high_collar_coat.png) |
| 010 | `outfit_010_celestial_robe_white_gold.png` | [Repository source](https://github.com/DOGECOIN87/Demigods/blob/d5c31dd39428732d193d9161624f4ce0beecf6c2/assets/outfits/outfit_010_celestial_robe_white_gold.png) |

The reference filenames and SHA-256 checksums are recorded in `reference_manifest.json`. `prompt_index.json` maps all 50 outputs to their exact prompts and two reference files. No failed generation candidates are included as fit references.

Prepared 2026-09-25 for manual generation.


# All 50 standalone prompts

## Outfit 001 — Celestial Scholar

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Celestial Scholar, outfit family 001, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_001_celestial_scholar_pose_001.png
Pack path: references/outfits/outfit_001_celestial_scholar_pose_001.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. Retain the indigo half-cape on VIEWER-RIGHT, its gold stars, the gold star clasp with blue gem, and the gold waist sash with its knot and hanging end on VIEWER-RIGHT. Preserve the crescent on the viewer-left chest and the source's arrangement of embroidered panels.

EXPOSED AREAS AND SOURCE CORRECTIONS
Keep both arms exposed below the designed armholes and short shoulder cape; leave the viewer-left shoulder exposed. The cape covers only its intended viewer-right shoulder area. Remove the pale arm-outline remnants visible in Image 2; they are extraction defects.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Fit the sleeveless armholes to the lowered arms. The viewer-right cape and sash must clear the relaxed right hand; leave the left arm and open hand unobstructed.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_001_celestial_scholar_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Celestial Scholar, outfit family 001, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_001_celestial_scholar_pose_001.png
Pack path: references/outfits/outfit_001_celestial_scholar_pose_001.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. Retain the indigo half-cape on VIEWER-RIGHT, its gold stars, the gold star clasp with blue gem, and the gold waist sash with its knot and hanging end on VIEWER-RIGHT. Preserve the crescent on the viewer-left chest and the source's arrangement of embroidered panels.

EXPOSED AREAS AND SOURCE CORRECTIONS
Keep both arms exposed below the designed armholes and short shoulder cape; leave the viewer-left shoulder exposed. The cape covers only its intended viewer-right shoulder area. Remove the pale arm-outline remnants visible in Image 2; they are extraction defects.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Keep the cape and sash on VIEWER-RIGHT while fitting the VIEWER-LEFT gripping arm. Do not mirror the garment to create this variant.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_001_celestial_scholar_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Celestial Scholar, outfit family 001, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_001_celestial_scholar_pose_001.png
Pack path: references/outfits/outfit_001_celestial_scholar_pose_001.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. Retain the indigo half-cape on VIEWER-RIGHT, its gold stars, the gold star clasp with blue gem, and the gold waist sash with its knot and hanging end on VIEWER-RIGHT. Preserve the crescent on the viewer-left chest and the source's arrangement of embroidered panels.

EXPOSED AREAS AND SOURCE CORRECTIONS
Keep both arms exposed below the designed armholes and short shoulder cape; leave the viewer-left shoulder exposed. The cape covers only its intended viewer-right shoulder area. Remove the pale arm-outline remnants visible in Image 2; they are extraction defects.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Keep the cape and sash on VIEWER-RIGHT, the same side as the gripping hand. Shape their drape to clear that arm, wrist and fist without moving the star clasp to the opposite side.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_001_celestial_scholar_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Celestial Scholar, outfit family 001, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_001_celestial_scholar_pose_001.png
Pack path: references/outfits/outfit_001_celestial_scholar_pose_001.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. Retain the indigo half-cape on VIEWER-RIGHT, its gold stars, the gold star clasp with blue gem, and the gold waist sash with its knot and hanging end on VIEWER-RIGHT. Preserve the crescent on the viewer-left chest and the source's arrangement of embroidered panels.

EXPOSED AREAS AND SOURCE CORRECTIONS
Keep both arms exposed below the designed armholes and short shoulder cape; leave the viewer-left shoulder exposed. The cape covers only its intended viewer-right shoulder area. Remove the pale arm-outline remnants visible in Image 2; they are extraction defects.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Keep the VIEWER-LEFT palm and its surrounding object space clear. The half-cape stays on VIEWER-RIGHT; no new fabric may span the left forearm.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_001_celestial_scholar_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Celestial Scholar, outfit family 001, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_001_celestial_scholar_pose_001.png
Pack path: references/outfits/outfit_001_celestial_scholar_pose_001.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. Retain the indigo half-cape on VIEWER-RIGHT, its gold stars, the gold star clasp with blue gem, and the gold waist sash with its knot and hanging end on VIEWER-RIGHT. Preserve the crescent on the viewer-left chest and the source's arrangement of embroidered panels.

EXPOSED AREAS AND SOURCE CORRECTIONS
Keep both arms exposed below the designed armholes and short shoulder cape; leave the viewer-left shoulder exposed. The cape covers only its intended viewer-right shoulder area. Remove the pale arm-outline remnants visible in Image 2; they are extraction defects.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Cut precise alpha openings for both exposed inward forearms and stacked hands. The waist sash and pointed tabard continue visually behind those openings; preserve the viewer-right knot. No gold trim, cape edge or star ornament may paint over the hands.
For this exposed-arm design, the outfit layer must have exact transparent openings following the bare inward forearms AND both stacked hands. Fabric remains everywhere around their contours, including between and beside the arms where the base garment would otherwise show. Never use a simple V-shaped or rectangular hole.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_001_celestial_scholar_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 002 — Storm Guardian

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Storm Guardian, outfit family 002, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_002_storm_guardian_pose_002.png
Pack path: references/outfits/outfit_002_storm_guardian_pose_002.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Charcoal patterned sleeveless armor with bronze edging, an open raised collar with teal inset, a single layered bronze pauldron on VIEWER-RIGHT, teal waist sash and short teal hip panels, brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze/brown plated shin guards and boots. Preserve the pauldron's circular shoulder detail and articulated plates. Keep the design practical and compact; add no weapon, shield or gloves.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose the viewer-left shoulder and both arms below the armor and the short viewer-right pauldron. Retain a real transparent neck aperture; the raised collar must not become a solid cap.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Fit the armor and single viewer-right pauldron to the lowered arms. Keep both relaxed hands and fingers entirely clear.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_002_storm_guardian_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Storm Guardian, outfit family 002, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_002_storm_guardian_pose_002.png
Pack path: references/outfits/outfit_002_storm_guardian_pose_002.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Charcoal patterned sleeveless armor with bronze edging, an open raised collar with teal inset, a single layered bronze pauldron on VIEWER-RIGHT, teal waist sash and short teal hip panels, brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze/brown plated shin guards and boots. Preserve the pauldron's circular shoulder detail and articulated plates. Keep the design practical and compact; add no weapon, shield or gloves.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose the viewer-left shoulder and both arms below the armor and the short viewer-right pauldron. Retain a real transparent neck aperture; the raised collar must not become a solid cap.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Leave the VIEWER-LEFT gripping arm exposed; the pauldron remains on VIEWER-RIGHT. Fit the left armhole without turning it into a sleeve or mirroring the armor.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_002_storm_guardian_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Storm Guardian, outfit family 002, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_002_storm_guardian_pose_002.png
Pack path: references/outfits/outfit_002_storm_guardian_pose_002.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Charcoal patterned sleeveless armor with bronze edging, an open raised collar with teal inset, a single layered bronze pauldron on VIEWER-RIGHT, teal waist sash and short teal hip panels, brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze/brown plated shin guards and boots. Preserve the pauldron's circular shoulder detail and articulated plates. Keep the design practical and compact; add no weapon, shield or gloves.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose the viewer-left shoulder and both arms below the armor and the short viewer-right pauldron. Retain a real transparent neck aperture; the raised collar must not become a solid cap.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
The VIEWER-RIGHT pauldron follows the right shoulder while the exposed right arm ends in the exact reference fist. Its lowest plate must stop before the elbow/forearm clearance; retain the left bare shoulder.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_002_storm_guardian_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Storm Guardian, outfit family 002, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_002_storm_guardian_pose_002.png
Pack path: references/outfits/outfit_002_storm_guardian_pose_002.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Charcoal patterned sleeveless armor with bronze edging, an open raised collar with teal inset, a single layered bronze pauldron on VIEWER-RIGHT, teal waist sash and short teal hip panels, brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze/brown plated shin guards and boots. Preserve the pauldron's circular shoulder detail and articulated plates. Keep the design practical and compact; add no weapon, shield or gloves.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose the viewer-left shoulder and both arms below the armor and the short viewer-right pauldron. Retain a real transparent neck aperture; the raised collar must not become a solid cap.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Expose the VIEWER-LEFT palm-up arm. Keep the left armhole open and the right pauldron on its original side; no belt pouch or armor edge may cross the palm.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_002_storm_guardian_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Storm Guardian, outfit family 002, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_002_storm_guardian_pose_002.png
Pack path: references/outfits/outfit_002_storm_guardian_pose_002.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Charcoal patterned sleeveless armor with bronze edging, an open raised collar with teal inset, a single layered bronze pauldron on VIEWER-RIGHT, teal waist sash and short teal hip panels, brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze/brown plated shin guards and boots. Preserve the pauldron's circular shoulder detail and articulated plates. Keep the design practical and compact; add no weapon, shield or gloves.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose the viewer-left shoulder and both arms below the armor and the short viewer-right pauldron. Retain a real transparent neck aperture; the raised collar must not become a solid cap.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Leave both inward forearms and stacked hands visible through exact alpha apertures. Keep the bronze buckle and teal sash behind the hand shapes without expanding the holes into the exposed torso/hip fabric. Retain the single viewer-right pauldron.
For this exposed-arm design, the outfit layer must have exact transparent openings following the bare inward forearms AND both stacked hands. Fabric remains everywhere around their contours, including between and beside the arms where the base garment would otherwise show. Never use a simple V-shaped or rectangular hole.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_002_storm_guardian_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 003 — Verdant Alchemist

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Verdant Alchemist, outfit family 003, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_003_verdant_alchemist_pose_003.png
Pack path: references/outfits/outfit_003_verdant_alchemist_pose_003.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Olive fitted embroidered vest over a cream linen shirt, warm brass buttons, and a brown diagonal bandolier running from VIEWER-LEFT shoulder to VIEWER-RIGHT waist with four small green/blue potion vials. Retain the brown double-belt construction, square brass buckle, small viewer-right hip pouch and viewer-left hanging vial, rust shorts over dark leggings, and brown lace-up boots. Preserve the shirt's rolled-cuff styling; fit the sleeves to cover the arms through the wrists, consistent with this outfit's hands-and-neck-only exposure rule.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Shirt sleeves must cover both shoulders, upper arms and forearms, with rolled cuffs ending immediately before each wrist/hand boundary. Do not copy the source's sleeve shortfall or any dull skin-colored neck fill.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Redraw both cream sleeves along the lowered arms, carrying the rolled-cuff detail down to the wrists. Do not leave the forearms exposed because the reference shirt is too short.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_003_verdant_alchemist_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Verdant Alchemist, outfit family 003, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_003_verdant_alchemist_pose_003.png
Pack path: references/outfits/outfit_003_verdant_alchemist_pose_003.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Olive fitted embroidered vest over a cream linen shirt, warm brass buttons, and a brown diagonal bandolier running from VIEWER-LEFT shoulder to VIEWER-RIGHT waist with four small green/blue potion vials. Retain the brown double-belt construction, square brass buckle, small viewer-right hip pouch and viewer-left hanging vial, rust shorts over dark leggings, and brown lace-up boots. Preserve the shirt's rolled-cuff styling; fit the sleeves to cover the arms through the wrists, consistent with this outfit's hands-and-neck-only exposure rule.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Shirt sleeves must cover both shoulders, upper arms and forearms, with rolled cuffs ending immediately before each wrist/hand boundary. Do not copy the source's sleeve shortfall or any dull skin-colored neck fill.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Adapt the VIEWER-LEFT sleeve and rolled cuff to the left grip's exact wrist angle. Keep the opposite cuff clear of every relaxed right-hand finger; retain the bandolier direction.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_003_verdant_alchemist_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Verdant Alchemist, outfit family 003, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_003_verdant_alchemist_pose_003.png
Pack path: references/outfits/outfit_003_verdant_alchemist_pose_003.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Olive fitted embroidered vest over a cream linen shirt, warm brass buttons, and a brown diagonal bandolier running from VIEWER-LEFT shoulder to VIEWER-RIGHT waist with four small green/blue potion vials. Retain the brown double-belt construction, square brass buckle, small viewer-right hip pouch and viewer-left hanging vial, rust shorts over dark leggings, and brown lace-up boots. Preserve the shirt's rolled-cuff styling; fit the sleeves to cover the arms through the wrists, consistent with this outfit's hands-and-neck-only exposure rule.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Shirt sleeves must cover both shoulders, upper arms and forearms, with rolled cuffs ending immediately before each wrist/hand boundary. Do not copy the source's sleeve shortfall or any dull skin-colored neck fill.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Adapt the VIEWER-RIGHT sleeve and rolled cuff to the right grip. The diagonal vial strap still runs viewer-left shoulder to viewer-right waist; keep its lower end clear of the right hand.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_003_verdant_alchemist_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Verdant Alchemist, outfit family 003, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_003_verdant_alchemist_pose_003.png
Pack path: references/outfits/outfit_003_verdant_alchemist_pose_003.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Olive fitted embroidered vest over a cream linen shirt, warm brass buttons, and a brown diagonal bandolier running from VIEWER-LEFT shoulder to VIEWER-RIGHT waist with four small green/blue potion vials. Retain the brown double-belt construction, square brass buckle, small viewer-right hip pouch and viewer-left hanging vial, rust shorts over dark leggings, and brown lace-up boots. Preserve the shirt's rolled-cuff styling; fit the sleeves to cover the arms through the wrists, consistent with this outfit's hands-and-neck-only exposure rule.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Shirt sleeves must cover both shoulders, upper arms and forearms, with rolled cuffs ending immediately before each wrist/hand boundary. Do not copy the source's sleeve shortfall or any dull skin-colored neck fill.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Rotate and bend the VIEWER-LEFT sleeve and rolled cuff to the palm-up wrist. Expose the full upturned palm and all fingers. Keep the small waist vials away from the palm's object space.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_003_verdant_alchemist_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Verdant Alchemist, outfit family 003, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_003_verdant_alchemist_pose_003.png
Pack path: references/outfits/outfit_003_verdant_alchemist_pose_003.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Olive fitted embroidered vest over a cream linen shirt, warm brass buttons, and a brown diagonal bandolier running from VIEWER-LEFT shoulder to VIEWER-RIGHT waist with four small green/blue potion vials. Retain the brown double-belt construction, square brass buckle, small viewer-right hip pouch and viewer-left hanging vial, rust shorts over dark leggings, and brown lace-up boots. Preserve the shirt's rolled-cuff styling; fit the sleeves to cover the arms through the wrists, consistent with this outfit's hands-and-neck-only exposure rule.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Shirt sleeves must cover both shoulders, upper arms and forearms, with rolled cuffs ending immediately before each wrist/hand boundary. Do not copy the source's sleeve shortfall or any dull skin-colored neck fill.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Draw both shirt sleeves bending inward over the forearms, with convincing elbow compression and rolled cuffs stopping before the stacked hands. Cut alpha only for the exposed hands/wrist openings, not for the covered forearms. Let the hands occlude any belt or bandolier part directly behind them.
For this full-sleeve design, draw clothing over the inward forearms and leave exact transparent openings for the exposed stacked hands at the cuff boundaries. Do not cut out the clothed forearms. Do not merge two cuffs into a mitten or erase the waist fabric around the hands.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_003_verdant_alchemist_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 004 — Lunar Oracle

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Lunar Oracle, outfit family 004, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_004_lunar_oracle_pose_004.png
Pack path: references/outfits/outfit_004_lunar_oracle_pose_004.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on VIEWER-RIGHT chest, a layered lavender/plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. Retain the silver rope belt with its knot and two hanging crescent charms on VIEWER-RIGHT. Keep the wrap direction, layered panel shapes and lavender lining from Image 2.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose both shoulders and both arms through clean sleeveless openings. Keep the neck opening transparent above the actual wrap/inner garment. Do not copy green fringe or stray extraction pixels from the design reference.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Shape the wrap armholes around the lowered arms. Silver cords and crescent charms remain on VIEWER-RIGHT and must not cross the relaxed right hand.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_004_lunar_oracle_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Lunar Oracle, outfit family 004, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_004_lunar_oracle_pose_004.png
Pack path: references/outfits/outfit_004_lunar_oracle_pose_004.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on VIEWER-RIGHT chest, a layered lavender/plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. Retain the silver rope belt with its knot and two hanging crescent charms on VIEWER-RIGHT. Keep the wrap direction, layered panel shapes and lavender lining from Image 2.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose both shoulders and both arms through clean sleeveless openings. Keep the neck opening transparent above the actual wrap/inner garment. Do not copy green fringe or stray extraction pixels from the design reference.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Leave the VIEWER-LEFT gripping arm uncovered. Keep the wrap direction, chest crescent and belt charms on their original sides; do not mirror the costume.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_004_lunar_oracle_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Lunar Oracle, outfit family 004, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_004_lunar_oracle_pose_004.png
Pack path: references/outfits/outfit_004_lunar_oracle_pose_004.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on VIEWER-RIGHT chest, a layered lavender/plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. Retain the silver rope belt with its knot and two hanging crescent charms on VIEWER-RIGHT. Keep the wrap direction, layered panel shapes and lavender lining from Image 2.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose both shoulders and both arms through clean sleeveless openings. Keep the neck opening transparent above the actual wrap/inner garment. Do not copy green fringe or stray extraction pixels from the design reference.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Keep the VIEWER-RIGHT gripping arm and fist fully clear of the hanging crescent charms. Preserve the charms' viewer-right placement while letting the garment drape naturally behind the arm.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_004_lunar_oracle_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Lunar Oracle, outfit family 004, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_004_lunar_oracle_pose_004.png
Pack path: references/outfits/outfit_004_lunar_oracle_pose_004.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on VIEWER-RIGHT chest, a layered lavender/plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. Retain the silver rope belt with its knot and two hanging crescent charms on VIEWER-RIGHT. Keep the wrap direction, layered panel shapes and lavender lining from Image 2.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose both shoulders and both arms through clean sleeveless openings. Keep the neck opening transparent above the actual wrap/inner garment. Do not copy green fringe or stray extraction pixels from the design reference.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Expose the complete VIEWER-LEFT palm-up silhouette. The tunic remains sleeveless; no silver cord, wrap edge or charm crosses the palm or wrist.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_004_lunar_oracle_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Lunar Oracle, outfit family 004, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_004_lunar_oracle_pose_004.png
Pack path: references/outfits/outfit_004_lunar_oracle_pose_004.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on VIEWER-RIGHT chest, a layered lavender/plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. Retain the silver rope belt with its knot and two hanging crescent charms on VIEWER-RIGHT. Keep the wrap direction, layered panel shapes and lavender lining from Image 2.

EXPOSED AREAS AND SOURCE CORRECTIONS
Expose both shoulders and both arms through clean sleeveless openings. Keep the neck opening transparent above the actual wrap/inner garment. Do not copy green fringe or stray extraction pixels from the design reference.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Create exact alpha apertures for both inward forearms and the stacked hands. The silver cord belt and petal panels pass visually behind the hands; do not leave a broad triangular hole showing the base's cream shorts. Keep the crescent charms on viewer-right.
For this exposed-arm design, the outfit layer must have exact transparent openings following the bare inward forearms AND both stacked hands. Fabric remains everywhere around their contours, including between and beside the arms where the base garment would otherwise show. Never use a simple V-shaped or rectangular hole.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_004_lunar_oracle_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 005 — Sun Temple

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Sun Temple, outfit family 005, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_005_sun_temple_pose_005.png
Pack path: references/outfits/outfit_005_sun_temple_pose_005.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory short-sleeved ceremonial tunic with an open small standing collar, orange/terracotta embroidered vertical bands, matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Include loose ivory trousers, orange geometric trouser cuffs, ivory shin wraps with terracotta crisscross ties, and complete orange/ivory footwear. Preserve the warm ivory, terracotta and restrained gold palette and the source's geometric motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Short sleeves cover the entire shoulder caps and upper arms, ending above the elbows as designed. Leave both forearms and hands exposed. Image 2 contains baked-in skin, forearms, hands and neck: use it for garment design only and remove ALL of that body content from the output.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Redraw the short sleeves for the lowered-arm neutral base. Replace the source's central forearm/hand region with continuous garment fabric, sash and central panel: this pose has no hands in front of the waist.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_005_sun_temple_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Sun Temple, outfit family 005, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_005_sun_temple_pose_005.png
Pack path: references/outfits/outfit_005_sun_temple_pose_005.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory short-sleeved ceremonial tunic with an open small standing collar, orange/terracotta embroidered vertical bands, matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Include loose ivory trousers, orange geometric trouser cuffs, ivory shin wraps with terracotta crisscross ties, and complete orange/ivory footwear. Preserve the warm ivory, terracotta and restrained gold palette and the source's geometric motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Short sleeves cover the entire shoulder caps and upper arms, ending above the elbows as designed. Leave both forearms and hands exposed. Image 2 contains baked-in skin, forearms, hands and neck: use it for garment design only and remove ALL of that body content from the output.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Fit the VIEWER-LEFT short sleeve to the left grip pose and keep the left forearm bare. Fill the source's old central hand/arm area with the continuing tunic and sash; the hands belong at Image 1's side positions.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_005_sun_temple_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Sun Temple, outfit family 005, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_005_sun_temple_pose_005.png
Pack path: references/outfits/outfit_005_sun_temple_pose_005.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory short-sleeved ceremonial tunic with an open small standing collar, orange/terracotta embroidered vertical bands, matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Include loose ivory trousers, orange geometric trouser cuffs, ivory shin wraps with terracotta crisscross ties, and complete orange/ivory footwear. Preserve the warm ivory, terracotta and restrained gold palette and the source's geometric motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Short sleeves cover the entire shoulder caps and upper arms, ending above the elbows as designed. Leave both forearms and hands exposed. Image 2 contains baked-in skin, forearms, hands and neck: use it for garment design only and remove ALL of that body content from the output.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Fit the VIEWER-RIGHT short sleeve to the right grip pose and keep the right forearm bare. Restore continuous tunic/sash/panel fabric where the source's central hands were; do not copy those hands.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_005_sun_temple_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Sun Temple, outfit family 005, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_005_sun_temple_pose_005.png
Pack path: references/outfits/outfit_005_sun_temple_pose_005.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory short-sleeved ceremonial tunic with an open small standing collar, orange/terracotta embroidered vertical bands, matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Include loose ivory trousers, orange geometric trouser cuffs, ivory shin wraps with terracotta crisscross ties, and complete orange/ivory footwear. Preserve the warm ivory, terracotta and restrained gold palette and the source's geometric motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Short sleeves cover the entire shoulder caps and upper arms, ending above the elbows as designed. Leave both forearms and hands exposed. Image 2 contains baked-in skin, forearms, hands and neck: use it for garment design only and remove ALL of that body content from the output.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Fit the VIEWER-LEFT short sleeve and expose the whole upturned forearm, palm and fingers. Restore fabric through the source's old central-hand region. Keep the geometric sleeve border away from the palm.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_005_sun_temple_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Sun Temple, outfit family 005, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_005_sun_temple_pose_005.png
Pack path: references/outfits/outfit_005_sun_temple_pose_005.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Ivory short-sleeved ceremonial tunic with an open small standing collar, orange/terracotta embroidered vertical bands, matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Include loose ivory trousers, orange geometric trouser cuffs, ivory shin wraps with terracotta crisscross ties, and complete orange/ivory footwear. Preserve the warm ivory, terracotta and restrained gold palette and the source's geometric motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Short sleeves cover the entire shoulder caps and upper arms, ending above the elbows as designed. Leave both forearms and hands exposed. Image 2 contains baked-in skin, forearms, hands and neck: use it for garment design only and remove ALL of that body content from the output.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Use Image 1's exact inward forearm contours and stacked-hand outlines to make genuine alpha apertures. Do not retain or repaint the skin already present in Image 2. The terracotta sash and patterned center panel must remain visible everywhere outside those precise apertures, with no cream tank/shorts showing around them.
For this exposed-arm design, the outfit layer must have exact transparent openings following the bare inward forearms AND both stacked hands. Fabric remains everywhere around their contours, including between and beside the arms where the base garment would otherwise show. Never use a simple V-shaped or rectangular hole.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_005_sun_temple_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 006 — Black Layered Hooded Robe

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Black Layered Hooded Robe, outfit family 006, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_006_black_layered_hooded_robe.png
Pack path: references/outfits/outfit_006_black_layered_hooded_robe.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep black and charcoal layered long robe with a collapsed hood behind the open neckline, an overlapping inner tunic, restrained silver-gray seams and angular ornaments, a dark belt with metal buckle and hanging strap, long pointed split robe panels, full sleeves with broad dark cuffs, black trousers and complete black boots. Preserve the many distinct black fabric planes through controlled shading; keep the hood down and off the head.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps continuously, then cover each arm through the wrist. The neck opening and cuff centers are transparent where skin will show; visible inner fabric facings remain painted.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Redraw both long sleeves along the lowered arms. Keep the broad cuffs before the open hands, with no peach shoulder crescents or sleeve gaps.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_006_black_layered_hooded_robe_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Black Layered Hooded Robe, outfit family 006, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_006_black_layered_hooded_robe.png
Pack path: references/outfits/outfit_006_black_layered_hooded_robe.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep black and charcoal layered long robe with a collapsed hood behind the open neckline, an overlapping inner tunic, restrained silver-gray seams and angular ornaments, a dark belt with metal buckle and hanging strap, long pointed split robe panels, full sleeves with broad dark cuffs, black trousers and complete black boots. Preserve the many distinct black fabric planes through controlled shading; keep the hood down and off the head.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps continuously, then cover each arm through the wrist. The neck opening and cuff centers are transparent where skin will show; visible inner fabric facings remain painted.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Adapt the VIEWER-LEFT robe sleeve and cuff to the grip wrist while retaining the relaxed right sleeve. The wide cuff must clear the whole left fist and its object channel.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_006_black_layered_hooded_robe_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Black Layered Hooded Robe, outfit family 006, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_006_black_layered_hooded_robe.png
Pack path: references/outfits/outfit_006_black_layered_hooded_robe.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep black and charcoal layered long robe with a collapsed hood behind the open neckline, an overlapping inner tunic, restrained silver-gray seams and angular ornaments, a dark belt with metal buckle and hanging strap, long pointed split robe panels, full sleeves with broad dark cuffs, black trousers and complete black boots. Preserve the many distinct black fabric planes through controlled shading; keep the hood down and off the head.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps continuously, then cover each arm through the wrist. The neck opening and cuff centers are transparent where skin will show; visible inner fabric facings remain painted.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Adapt the VIEWER-RIGHT robe sleeve and cuff to the grip wrist while retaining the relaxed left sleeve. Keep the whole right fist and its object channel clear.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_006_black_layered_hooded_robe_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Black Layered Hooded Robe, outfit family 006, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_006_black_layered_hooded_robe.png
Pack path: references/outfits/outfit_006_black_layered_hooded_robe.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep black and charcoal layered long robe with a collapsed hood behind the open neckline, an overlapping inner tunic, restrained silver-gray seams and angular ornaments, a dark belt with metal buckle and hanging strap, long pointed split robe panels, full sleeves with broad dark cuffs, black trousers and complete black boots. Preserve the many distinct black fabric planes through controlled shading; keep the hood down and off the head.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps continuously, then cover each arm through the wrist. The neck opening and cuff centers are transparent where skin will show; visible inner fabric facings remain painted.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Shape the VIEWER-LEFT sleeve for the palm-up wrist, with visible inner cuff facing where appropriate. The flared cuff must not hang across the upturned palm or object space.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_006_black_layered_hooded_robe_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Black Layered Hooded Robe, outfit family 006, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_006_black_layered_hooded_robe.png
Pack path: references/outfits/outfit_006_black_layered_hooded_robe.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep black and charcoal layered long robe with a collapsed hood behind the open neckline, an overlapping inner tunic, restrained silver-gray seams and angular ornaments, a dark belt with metal buckle and hanging strap, long pointed split robe panels, full sleeves with broad dark cuffs, black trousers and complete black boots. Preserve the many distinct black fabric planes through controlled shading; keep the hood down and off the head.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps continuously, then cover each arm through the wrist. The neck opening and cuff centers are transparent where skin will show; visible inner fabric facings remain painted.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Draw both full sleeves bending inward in front of the torso. Sleeve fabric covers the forearms; leave exact transparent apertures for the stacked hands only. Preserve readable separation between sleeves, robe front and belt, without turning the center into a black mitten or opening oversized holes.
For this full-sleeve design, draw clothing over the inward forearms and leave exact transparent openings for the exposed stacked hands at the cuff boundaries. Do not cut out the clothed forearms. Do not merge two cuffs into a mitten or erase the waist fabric around the hands.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_006_black_layered_hooded_robe_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 007 — Brown Leather Long Coat

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Brown Leather Long Coat, outfit family 007, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_007_brown_leather_long_coat.png
Pack path: references/outfits/outfit_007_brown_leather_long_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Warm brown leather long coat with broad open lapels and raised collar, layered brown vest, a clearly fabric cream inner shirt at the chest, bronze buttons and buckles, a wide brown belt with square buckle, the existing viewer-right hip pouch, long split coat tails, full sleeves with strapped cuffs, brown trousers and sturdy brown boots. Preserve the source's leather seams, buttons, thigh strap and restrained highlights. Add no tools, scissors, weapons or extra pouches.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps and arms fully to the wrists. Keep the cream inner shirt as actual fabric below the neckline, but remove skin-colored filler from the neck aperture; retain open collar depth and inside faces.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Fit the full leather sleeves to both lowered arms, with cuffs immediately before the relaxed hands. Keep the coat fronts, belt and lapels undistorted.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_007_brown_leather_long_coat_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Brown Leather Long Coat, outfit family 007, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_007_brown_leather_long_coat.png
Pack path: references/outfits/outfit_007_brown_leather_long_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Warm brown leather long coat with broad open lapels and raised collar, layered brown vest, a clearly fabric cream inner shirt at the chest, bronze buttons and buckles, a wide brown belt with square buckle, the existing viewer-right hip pouch, long split coat tails, full sleeves with strapped cuffs, brown trousers and sturdy brown boots. Preserve the source's leather seams, buttons, thigh strap and restrained highlights. Add no tools, scissors, weapons or extra pouches.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps and arms fully to the wrists. Keep the cream inner shirt as actual fabric below the neckline, but remove skin-colored filler from the neck aperture; retain open collar depth and inside faces.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Redraw the VIEWER-LEFT sleeve around the grip arm and angle the strapped cuff to the wrist. Preserve the viewer-right pouch and original lapel construction.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_007_brown_leather_long_coat_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Brown Leather Long Coat, outfit family 007, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_007_brown_leather_long_coat.png
Pack path: references/outfits/outfit_007_brown_leather_long_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Warm brown leather long coat with broad open lapels and raised collar, layered brown vest, a clearly fabric cream inner shirt at the chest, bronze buttons and buckles, a wide brown belt with square buckle, the existing viewer-right hip pouch, long split coat tails, full sleeves with strapped cuffs, brown trousers and sturdy brown boots. Preserve the source's leather seams, buttons, thigh strap and restrained highlights. Add no tools, scissors, weapons or extra pouches.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps and arms fully to the wrists. Keep the cream inner shirt as actual fabric below the neckline, but remove skin-colored filler from the neck aperture; retain open collar depth and inside faces.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Redraw the VIEWER-RIGHT sleeve around the grip arm; keep the strapped cuff and viewer-right hip pouch clear of the right fist. Preserve all lapel and belt proportions.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_007_brown_leather_long_coat_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Brown Leather Long Coat, outfit family 007, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_007_brown_leather_long_coat.png
Pack path: references/outfits/outfit_007_brown_leather_long_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Warm brown leather long coat with broad open lapels and raised collar, layered brown vest, a clearly fabric cream inner shirt at the chest, bronze buttons and buckles, a wide brown belt with square buckle, the existing viewer-right hip pouch, long split coat tails, full sleeves with strapped cuffs, brown trousers and sturdy brown boots. Preserve the source's leather seams, buttons, thigh strap and restrained highlights. Add no tools, scissors, weapons or extra pouches.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps and arms fully to the wrists. Keep the cream inner shirt as actual fabric below the neckline, but remove skin-colored filler from the neck aperture; retain open collar depth and inside faces.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Articulate the VIEWER-LEFT leather elbow and cuff for the palm-up wrist. Keep the cuff strap behind the wrist boundary and expose all palm/finger contours.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_007_brown_leather_long_coat_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Brown Leather Long Coat, outfit family 007, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_007_brown_leather_long_coat.png
Pack path: references/outfits/outfit_007_brown_leather_long_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Warm brown leather long coat with broad open lapels and raised collar, layered brown vest, a clearly fabric cream inner shirt at the chest, bronze buttons and buckles, a wide brown belt with square buckle, the existing viewer-right hip pouch, long split coat tails, full sleeves with strapped cuffs, brown trousers and sturdy brown boots. Preserve the source's leather seams, buttons, thigh strap and restrained highlights. Add no tools, scissors, weapons or extra pouches.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover both shoulder caps and arms fully to the wrists. Keep the cream inner shirt as actual fabric below the neckline, but remove skin-colored filler from the neck aperture; retain open collar depth and inside faces.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Bend both leather sleeves inward with natural elbow folds. End strapped cuffs before the stacked hands and cut precise hand apertures; the covered forearms stay leather. Keep lapels and belt continuous behind the arms without stretched buckles, smeared seams or a pouch crossing the hands.
For this full-sleeve design, draw clothing over the inward forearms and leave exact transparent openings for the exposed stacked hands at the cuff boundaries. Do not cut out the clothed forearms. Do not merge two cuffs into a mitten or erase the waist fabric around the hands.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_007_brown_leather_long_coat_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 008 — Olive Ragged Cloak

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Olive Ragged Cloak, outfit family 008, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_008_olive_ragged_cloak_sleeveless_latest.png
Pack path: references/outfits/outfit_008_olive_ragged_cloak_sleeveless_latest.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Use the LATEST SLEEVELESS olive travel-cloak design in Image 2: an open collapsed hood, short ragged shoulder capelet, layered olive leaf-tail panels, sleeveless cream linen tunic, orange-brown rope fastening and waist belt with hanging ends on VIEWER-RIGHT, the existing small pendant, brown trousers, and warm brown lace-up boots with folded tops. Preserve the complete rounded toes and soles. Keep all ragged edges deliberate and fabric-like.

EXPOSED AREAS AND SOURCE CORRECTIONS
Both arms remain exposed below the shoulder capelet and the sleeveless tunic armholes. The cream shapes along the arm openings are fabric edging only; do not add cream sleeves or skin. This latest sleeveless reference overrides the older full-sleeved olive-cloak catalog.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Fit the sleeveless tunic and short capelet around the lowered arms. Keep ragged panels and rope ends clear of both open hands; retain intact boot toes and soles.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_008_olive_ragged_cloak_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Olive Ragged Cloak, outfit family 008, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_008_olive_ragged_cloak_sleeveless_latest.png
Pack path: references/outfits/outfit_008_olive_ragged_cloak_sleeveless_latest.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Use the LATEST SLEEVELESS olive travel-cloak design in Image 2: an open collapsed hood, short ragged shoulder capelet, layered olive leaf-tail panels, sleeveless cream linen tunic, orange-brown rope fastening and waist belt with hanging ends on VIEWER-RIGHT, the existing small pendant, brown trousers, and warm brown lace-up boots with folded tops. Preserve the complete rounded toes and soles. Keep all ragged edges deliberate and fabric-like.

EXPOSED AREAS AND SOURCE CORRECTIONS
Both arms remain exposed below the shoulder capelet and the sleeveless tunic armholes. The cream shapes along the arm openings are fabric edging only; do not add cream sleeves or skin. This latest sleeveless reference overrides the older full-sleeved olive-cloak catalog.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Leave the VIEWER-LEFT gripping arm exposed, with no invented sleeve. Keep the capelet above the forearms and the viewer-right rope ends away from the opposite relaxed hand.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_008_olive_ragged_cloak_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Olive Ragged Cloak, outfit family 008, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_008_olive_ragged_cloak_sleeveless_latest.png
Pack path: references/outfits/outfit_008_olive_ragged_cloak_sleeveless_latest.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Use the LATEST SLEEVELESS olive travel-cloak design in Image 2: an open collapsed hood, short ragged shoulder capelet, layered olive leaf-tail panels, sleeveless cream linen tunic, orange-brown rope fastening and waist belt with hanging ends on VIEWER-RIGHT, the existing small pendant, brown trousers, and warm brown lace-up boots with folded tops. Preserve the complete rounded toes and soles. Keep all ragged edges deliberate and fabric-like.

EXPOSED AREAS AND SOURCE CORRECTIONS
Both arms remain exposed below the shoulder capelet and the sleeveless tunic armholes. The cream shapes along the arm openings are fabric edging only; do not add cream sleeves or skin. This latest sleeveless reference overrides the older full-sleeved olive-cloak catalog.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Leave the VIEWER-RIGHT gripping arm exposed. Keep the rope ends and leaf-tail panels on their original sides while clearing the right fist and wrist.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_008_olive_ragged_cloak_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Olive Ragged Cloak, outfit family 008, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_008_olive_ragged_cloak_sleeveless_latest.png
Pack path: references/outfits/outfit_008_olive_ragged_cloak_sleeveless_latest.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Use the LATEST SLEEVELESS olive travel-cloak design in Image 2: an open collapsed hood, short ragged shoulder capelet, layered olive leaf-tail panels, sleeveless cream linen tunic, orange-brown rope fastening and waist belt with hanging ends on VIEWER-RIGHT, the existing small pendant, brown trousers, and warm brown lace-up boots with folded tops. Preserve the complete rounded toes and soles. Keep all ragged edges deliberate and fabric-like.

EXPOSED AREAS AND SOURCE CORRECTIONS
Both arms remain exposed below the shoulder capelet and the sleeveless tunic armholes. The cream shapes along the arm openings are fabric edging only; do not add cream sleeves or skin. This latest sleeveless reference overrides the older full-sleeved olive-cloak catalog.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Leave the VIEWER-LEFT forearm and upturned palm fully exposed. Do not let the capelet, leaf tails or rope cross the palm's object space, and do not invent a sleeve.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_008_olive_ragged_cloak_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Olive Ragged Cloak, outfit family 008, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_008_olive_ragged_cloak_sleeveless_latest.png
Pack path: references/outfits/outfit_008_olive_ragged_cloak_sleeveless_latest.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Use the LATEST SLEEVELESS olive travel-cloak design in Image 2: an open collapsed hood, short ragged shoulder capelet, layered olive leaf-tail panels, sleeveless cream linen tunic, orange-brown rope fastening and waist belt with hanging ends on VIEWER-RIGHT, the existing small pendant, brown trousers, and warm brown lace-up boots with folded tops. Preserve the complete rounded toes and soles. Keep all ragged edges deliberate and fabric-like.

EXPOSED AREAS AND SOURCE CORRECTIONS
Both arms remain exposed below the shoulder capelet and the sleeveless tunic armholes. The cream shapes along the arm openings are fabric edging only; do not add cream sleeves or skin. This latest sleeveless reference overrides the older full-sleeved olive-cloak catalog.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Cut exact alpha apertures for the inward bare forearms and stacked hands. Rope belt, cream tunic and leaf panels continue everywhere around those openings; do not reveal a triangle of the base's cream shorts. Keep the sleeveless design and complete footwear.
For this exposed-arm design, the outfit layer must have exact transparent openings following the bare inward forearms AND both stacked hands. Fabric remains everywhere around their contours, including between and beside the arms where the base garment would otherwise show. Never use a simple V-shaped or rectangular hole.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_008_olive_ragged_cloak_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 009 — Navy High-Collar Coat

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Navy High-Collar Coat, outfit family 009, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_009_navy_high_collar_coat.png
Pack path: references/outfits/outfit_009_navy_high_collar_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep navy tailored long coat with a high OPEN standing collar, pale metallic piping with gold accents, asymmetrical fitted front, gold star brooch and short chain on VIEWER-RIGHT chest, full sleeves with structured star-trimmed cuffs, long split tails with blue constellation-patterned lining, navy trousers, and navy boots with gold star details and trim. Preserve the original asymmetrical lapel and long viewer-right front panel; keep the costume navy rather than turning it into the white/gold robe.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Redraw shoulder caps and sleeves at the base body's real width. The high collar is an open tube with visible inner facing and a transparent neck aperture; never fill that aperture with a flat white or gray neck substitute.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Fit full sleeves to the lowered arms. Retain the asymmetrical front and unbroken pale piping, with cuffs stopping before the relaxed hands.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_009_navy_high_collar_coat_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Navy High-Collar Coat, outfit family 009, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_009_navy_high_collar_coat.png
Pack path: references/outfits/outfit_009_navy_high_collar_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep navy tailored long coat with a high OPEN standing collar, pale metallic piping with gold accents, asymmetrical fitted front, gold star brooch and short chain on VIEWER-RIGHT chest, full sleeves with structured star-trimmed cuffs, long split tails with blue constellation-patterned lining, navy trousers, and navy boots with gold star details and trim. Preserve the original asymmetrical lapel and long viewer-right front panel; keep the costume navy rather than turning it into the white/gold robe.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Redraw shoulder caps and sleeves at the base body's real width. The high collar is an open tube with visible inner facing and a transparent neck aperture; never fill that aperture with a flat white or gray neck substitute.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Tailor the VIEWER-LEFT sleeve and structured cuff to the grip wrist. Keep the star brooch and long front panel on VIEWER-RIGHT; never mirror the coat.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_009_navy_high_collar_coat_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Navy High-Collar Coat, outfit family 009, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_009_navy_high_collar_coat.png
Pack path: references/outfits/outfit_009_navy_high_collar_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep navy tailored long coat with a high OPEN standing collar, pale metallic piping with gold accents, asymmetrical fitted front, gold star brooch and short chain on VIEWER-RIGHT chest, full sleeves with structured star-trimmed cuffs, long split tails with blue constellation-patterned lining, navy trousers, and navy boots with gold star details and trim. Preserve the original asymmetrical lapel and long viewer-right front panel; keep the costume navy rather than turning it into the white/gold robe.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Redraw shoulder caps and sleeves at the base body's real width. The high collar is an open tube with visible inner facing and a transparent neck aperture; never fill that aperture with a flat white or gray neck substitute.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Tailor the VIEWER-RIGHT sleeve and structured cuff to the grip wrist. Keep the right front panel and star trim clear of the fist; preserve the asymmetrical lapel.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_009_navy_high_collar_coat_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Navy High-Collar Coat, outfit family 009, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_009_navy_high_collar_coat.png
Pack path: references/outfits/outfit_009_navy_high_collar_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep navy tailored long coat with a high OPEN standing collar, pale metallic piping with gold accents, asymmetrical fitted front, gold star brooch and short chain on VIEWER-RIGHT chest, full sleeves with structured star-trimmed cuffs, long split tails with blue constellation-patterned lining, navy trousers, and navy boots with gold star details and trim. Preserve the original asymmetrical lapel and long viewer-right front panel; keep the costume navy rather than turning it into the white/gold robe.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Redraw shoulder caps and sleeves at the base body's real width. The high collar is an open tube with visible inner facing and a transparent neck aperture; never fill that aperture with a flat white or gray neck substitute.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Rotate the VIEWER-LEFT structured cuff to the palm-up wrist, showing inner facing where visible. Keep the cuff and piping clear of every palm/finger contour and object space.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_009_navy_high_collar_coat_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Navy High-Collar Coat, outfit family 009, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_009_navy_high_collar_coat.png
Pack path: references/outfits/outfit_009_navy_high_collar_coat.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Deep navy tailored long coat with a high OPEN standing collar, pale metallic piping with gold accents, asymmetrical fitted front, gold star brooch and short chain on VIEWER-RIGHT chest, full sleeves with structured star-trimmed cuffs, long split tails with blue constellation-patterned lining, navy trousers, and navy boots with gold star details and trim. Preserve the original asymmetrical lapel and long viewer-right front panel; keep the costume navy rather than turning it into the white/gold robe.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Redraw shoulder caps and sleeves at the base body's real width. The high collar is an open tube with visible inner facing and a transparent neck aperture; never fill that aperture with a flat white or gray neck substitute.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Draw both navy sleeves bending inward and crossing in front of the coat at Image 1's exact arm locations. Leave alpha apertures for stacked hands, with covered forearms remaining navy. Preserve the star brooch, lapel and piping behind the sleeves; do not warp them to close gaps.
For this full-sleeve design, draw clothing over the inward forearms and leave exact transparent openings for the exposed stacked hands at the cuff boundaries. Do not cut out the clothed forearms. Do not merge two cuffs into a mitten or erase the waist fabric around the hands.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_009_navy_high_collar_coat_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

## Outfit 010 — Celestial Robe — White and Gold

### Pose 001 — Neutral — both hands open

```text
Create ONE isolated outfit layer: Celestial Robe — White and Gold, outfit family 010, Pose 001 (Neutral — both hands open).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png
Pack path: references/poses/base_body_001_neutral_master.png
Image 2: outfit_010_celestial_robe_white_gold.png
Pack path: references/outfits/outfit_010_celestial_robe_white_gold.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Silver-white/ivory ceremonial coat-robe with a high OPEN collar, pale blue-gray facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with star clasp and hanging end on VIEWER-RIGHT, long split robe panels, white trousers, and complete white/gold star-trimmed boots. Retain the front's long vertical pale-blue panels and airy white/gold value structure; preserve all existing gold motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover shoulder caps and arms continuously to the wrists. The collar must show real interior fabric depth around a genuine transparent neck opening; remove any flat gray/white fill where the base neck should appear.

POSE 001 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both arms are lowered and slightly away from the body, with both hands relaxed/open exactly as Image 1. Preserve every fingertip and the clear gaps between hands and hips. Do not create gripping hands or a palm-up gesture.
Fit both ivory sleeves to the lowered arms; keep the flared cuffs before the relaxed hands. Preserve the gold sash width and undistorted vertical facing panels.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_010_celestial_robe_white_gold_pose_001.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 002 — Viewer-left vertical grip

```text
Create ONE isolated outfit layer: Celestial Robe — White and Gold, outfit family 010, Pose 002 (Viewer-left vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png
Pack path: references/poses/base_pose_002_viewer_left_vertical_grip.png
Image 2: outfit_010_celestial_robe_white_gold.png
Pack path: references/outfits/outfit_010_celestial_robe_white_gold.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Silver-white/ivory ceremonial coat-robe with a high OPEN collar, pale blue-gray facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with star clasp and hanging end on VIEWER-RIGHT, long split robe panels, white trousers, and complete white/gold star-trimmed boots. Retain the front's long vertical pale-blue panels and airy white/gold value structure; preserve all existing gold motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover shoulder caps and arms continuously to the wrists. The collar must show real interior fabric depth around a genuine transparent neck opening; remove any flat gray/white fill where the base neck should appear.

POSE 002 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the RIGHT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not add a held object.
Adapt the VIEWER-LEFT sleeve and gold-embroidered cuff to the grip wrist. Keep the sash clasp and hanging end on VIEWER-RIGHT and all fingers unobstructed.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_010_celestial_robe_white_gold_pose_002.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 003 — Viewer-right vertical grip

```text
Create ONE isolated outfit layer: Celestial Robe — White and Gold, outfit family 010, Pose 003 (Viewer-right vertical grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png
Pack path: references/poses/base_pose_003_viewer_right_vertical_grip.png
Image 2: outfit_010_celestial_robe_white_gold.png
Pack path: references/outfits/outfit_010_celestial_robe_white_gold.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Silver-white/ivory ceremonial coat-robe with a high OPEN collar, pale blue-gray facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with star clasp and hanging end on VIEWER-RIGHT, long split robe panels, white trousers, and complete white/gold star-trimmed boots. Retain the front's long vertical pale-blue panels and airy white/gold value structure; preserve all existing gold motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover shoulder caps and arms continuously to the wrists. The collar must show real interior fabric depth around a genuine transparent neck opening; remove any flat gray/white fill where the base neck should appear.

POSE 003 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist; the hand on the LEFT SIDE OF THE IMAGE is relaxed/open. Match the reference's exact shoulder, elbow, wrist and finger positions. The grip is low at the side, not a raised arm. Do not mirror Pose 002 or add a held object.
Adapt the VIEWER-RIGHT sleeve and cuff to the grip wrist. Keep the viewer-right sash end clear of the fist without mirroring or narrowing the sash.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_010_celestial_robe_white_gold_pose_003.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 004 — Viewer-left palm up

```text
Create ONE isolated outfit layer: Celestial Robe — White and Gold, outfit family 010, Pose 004 (Viewer-left palm up).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png
Pack path: references/poses/base_pose_004_viewer_left_palm_up.png
Image 2: outfit_010_celestial_robe_white_gold.png
Pack path: references/outfits/outfit_010_celestial_robe_white_gold.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Silver-white/ivory ceremonial coat-robe with a high OPEN collar, pale blue-gray facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with star clasp and hanging end on VIEWER-RIGHT, long split robe panels, white trousers, and complete white/gold star-trimmed boots. Retain the front's long vertical pale-blue panels and airy white/gold value structure; preserve all existing gold motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover shoulder caps and arms continuously to the wrists. The collar must show real interior fabric depth around a genuine transparent neck opening; remove any flat gray/white fill where the base neck should appear.

POSE 004 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the reference's low side position; the RIGHT hand remains relaxed/open. Follow the actual elbow/forearm angle and expose the entire left palm and fingers. Do not raise the arm, make a fist or add an object.
Shape the VIEWER-LEFT sleeve and flared cuff for the palm-up wrist. Expose the full palm and every finger; show pale-blue cuff lining only on fabric surfaces, never across the skin opening.
Keep the exact skin/hand areas from Image 1 transparent. Match the target pose directly, even when another pose looks similar; a filename change or mirrored copy does not create a fitted variant.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_010_celestial_robe_white_gold_pose_004.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```

### Pose 005 — Centered two-hand grip

```text
Create ONE isolated outfit layer: Celestial Robe — White and Gold, outfit family 010, Pose 005 (Centered two-hand grip).

ATTACH THESE TWO REFERENCE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png
Pack path: references/poses/base_pose_005_centered_two_hand_grip.png
Image 2: outfit_010_celestial_robe_white_gold.png
Pack path: references/outfits/outfit_010_celestial_robe_white_gold.png
Image 1 is the immutable body geometry, pose, scale and pixel-placement reference. Image 2 supplies clothing design, palette, materials and ornament placement only; its pose, fit and extraction defects are not authoritative. If an already composite-approved Pose 001 version of this same outfit is attached as Image 3, use it only to maintain garment design and rendering consistency. Image 1 still controls all geometry.

DESIGN TO PRESERVE
Silver-white/ivory ceremonial coat-robe with a high OPEN collar, pale blue-gray facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with star clasp and hanging end on VIEWER-RIGHT, long split robe panels, white trousers, and complete white/gold star-trimmed boots. Retain the front's long vertical pale-blue panels and airy white/gold value structure; preserve all existing gold motifs.

EXPOSED AREAS AND SOURCE CORRECTIONS
Show hands and neck only. Cover shoulder caps and arms continuously to the wrists. The collar must show real interior fabric depth around a genuine transparent neck opening; remove any flat gray/white fill where the base neck should appear.

POSE 005 — EXACT REQUIREMENTS
All left/right directions mean the viewer's left/right.
Both forearms angle inward across the lower torso, ending in TWO STACKED GRIPPING HANDS at the center exactly as Image 1. Preserve which hand is above and the precise wrist, thumb and finger contours. Do not use side-positioned hands, two separate side fists, clasped palms, or a different arm crossing. Do not add an object.
Paint both ivory sleeves bending inward over the forearms, with clear folds and gold trim following the sleeves. Cut exact apertures for the stacked hands; do not erase the clothed forearms. The gold sash and pale-blue front panels continue behind the hands/sleeves without narrowed sash ends, enlarged holes or distorted scrollwork.
For this full-sleeve design, draw clothing over the inward forearms and leave exact transparent openings for the exposed stacked hands at the cuff boundaries. Do not cut out the clothed forearms. Do not merge two cuffs into a mitten or erase the waist fabric around the hands.

CANVAS, PLACEMENT AND STYLE
Return one native 1254 x 1254 pixel sRGB RGBA PNG with genuine transparent alpha. Preserve Image 1's entire canvas and original avatar scale even though the head/body will be absent in the output. Keep the large empty head area; do not zoom the garment to fill the square, auto-center its visible bounding box, crop, shift, rotate, mirror, upscale or stretch it. Canvas center is X=627; the approved figure's head starts near Y=141 and its feet end at Y=1139. Keep the footwear on that same baseline, with no pixels below Y=1139, and the garment within X=233..1021 and Y=129..1139. Image 1's actual anatomical contours govern neck, shoulder, elbow, waist, hip, knee, ankle and wrist positions; do not substitute generic coordinate labels or adult proportions. The collar belongs at the reference neck, roughly Y=475..500, not near the top of the canvas.
Use the same front-facing orthographic anime-chibi fantasy game-art style as the references: clean coherent outlines, refined cel/painterly shading, readable detail, soft upper-left key light, lower-right form shadows and subtle cool right rim light. No perspective or camera change.

FIT AND ALPHA
This outfit will be composited OVER the unchanged base body. Paint clothing and footwear only. Where skin must remain visible, use true transparent alpha so the original base shows through; never repaint skin or draw a replacement hand. Keep neck and wrist openings anatomically exact, with painted inner collar/cuff faces only where they are actual visible fabric. No sleeve, cape, sash, charm or trim may cross an exposed hand or finger.
Tailor new fabric to the full width of Image 1's torso, waist, hips and legs so none of the base's cream tank or shorts peeks out. Preserve the designed garment construction while redrawing the fit: do not stretch lapels, narrow belts, warp embroidery, repeat edge pixels or smear outlines. Fit footwear around both reference feet and toes, including complete soles. Opaque fabric covers the base; intentional skin openings follow skin precisely, not broad guessed cutouts. Copy no stray outlines, color-key fringe, detached specks or known coverage defects from Image 2.

AVOID
Body, head, face, hair, painted neck, painted arms, painted hands, extra fingers, mannequin, gloves added to hide hand errors, held objects, aura, scenery, floor shadow, glow/halo, labels, text, guides, borders, contact sheets, multiple variations in one image, fake checkerboard, solid background, copied extraction defects, undergarment leaks, exposed torso/hips, missing soles, clipped footwear, wrong pose, changed camera, scale drift, mirrored asymmetry and added accessories.

OUTPUT
Exactly one isolated transparent PNG named:
outfit_010_celestial_robe_white_gold_pose_005.png
The file contains only this outfit, including its matching trousers/legwear and footwear, at the unchanged reference coordinates. No full-character preview inside the PNG. If native 1254 x 1254 RGBA output is unavailable, state that limitation; do not silently substitute a resized or flattened image.
```
