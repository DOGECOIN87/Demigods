# Demigods - dressed-body prompts for the 31 missing outfit renders

Prepared 2026-09-25. Companion to `prompts/manual_outfit_pose_pack_2026-09-25.md`, which asked for isolated outfit layers. The owner switched to renders with the body intact: the base pose and its outfit painted as one bald, faceless figure. Twenty arrived that day and are registered (`docs/qa/dressed_bodies_2026-09-25.md`); these prompts are for the thirty-one still missing.

## Where the wardrobe stands

| Family | Pose 001 | Pose 002 | Pose 003 | Pose 004 | Pose 005 |
|---|---|---|---|---|---|
| 001 Celestial Scholar | layer, to replace | **missing** | **missing** | **missing** | **missing** |
| 002 Storm Guardian | **missing** | layer, to replace | **missing** | **missing** | **missing** |
| 003 Verdant Alchemist | **missing** | **missing** | layer, to replace | **missing** | **missing** |
| 004 Lunar Oracle | **missing** | **missing** | **missing** | layer, to replace | **missing** |
| 005 Sun Temple | **missing** | **missing** | **missing** | **missing** | **missing** (layer withdrawn) |
| 006 Black layered hooded robe | dressed | dressed | dressed | **missing** (withdrawn) | dressed |
| 007 Brown leather long coat | dressed | dressed | dressed | dressed | dressed |
| 008 Olive ragged cloak | dressed | dressed | dressed | dressed | dressed |
| 009 Navy high-collar coat | dressed | dressed | dressed | dressed | dressed |
| 010 Celestial Robe, white and gold | **missing** (layer withdrawn) | **missing** | **missing** | **missing** | **missing** |

- **dressed** - registered dressed body, rendered with the base pose hidden (`hides` in `config/compatibility.json`).
- **layer, to replace** - the original single-pose garment layer drawn over the bare base. It stays in the collection until its dressed render lands; it still shows the base's cream undergarment at the waist in places (`docs/handoff/outfit-refit-brief.md`).
- **missing** - nothing in this pose yet. On 2026-09-25 the owner withdrew the sun temple and white-and-gold robe layers and the black robe's Pose 004 render, which did not render properly (`docs/qa/trait_reduction_2026-09-25.md`); a new render of any of them is welcome.

The collection generates today without any of these: the registered traits allow about 1.5 trillion rule-valid combinations. Each render added here adds an outfit to a pose and evens out the wardrobe.

## How to generate one

1. Pick a prompt below and attach its three images in the stated order, as files: the base pose from `assets/base_bodies/`, the approved example from `assets/outfits/`, and the design reference.
2. Generate one image per prompt. Keep every attempt; do not edit, crop or resize the output.
3. Save the original PNG under `images/trait_candidates/outfits_dressed/` and add an entry to `sources.json` there (source, sha256, outfit, outfit_slug, outfit_label, pose, target), or hand the files to whoever runs intake.
4. Run `python scripts/intake_dressed_bodies.py images/trait_candidates/outfits_dressed/sources.json` and look at the two sheets it writes under `docs/qa/`. Workflow: `docs/workflows/dressed_body_intake.md`.

## What the intake checks, so a render is not wasted

- **Head size and place.** Face, hair and headwear are shared layers drawn to one head. The fit reduces the head to the shared chin height and the body separately to the baseline, so a render drawn a little large or long-legged still fits - but it only ever reduces. A head drawn smaller than Image 1's cannot be enlarged, and a head of a different shape is rejected by the face check, where the mouth lands on the chin or the eye patches on the ears.
- **Fist and palm.** Hand objects are seated on the base's fist (Pose 002) and palm (Pose 004). A hand drawn elsewhere keeps the render, but every hand object is excluded from it.
- **Background.** Transparent is best. Pure black works for light and mid-tone outfits; dark outfits must be transparent.
- **Face.** No painted features at all. The shared face layers cover only the eyes, brows and mouth they draw.

# The thirty-one prompts

### Outfit 001 Celestial Scholar - Pose 001 (neutral, both hands open)

```text
Create ONE full-body character render: the Demigods Celestial Scholar outfit (family 001) worn by the collection's base figure in Pose 001 (neutral, both hands open), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png (repository: assets/base_bodies/base_body_001_neutral_master.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_001.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_001_celestial_scholar_pose_001.png (repository: assets/outfits/outfit_001_celestial_scholar_pose_001.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. An indigo half-cape with gold stars covers the VIEWER-RIGHT shoulder only, fastened by a gold star clasp with a blue gem; a gold waist sash is knotted on VIEWER-RIGHT with its end hanging. A gold crescent sits on the viewer-left chest; keep the reference's arrangement of embroidered panels.
Where skin shows: Both arms are bare below the armholes, and the viewer-left shoulder is bare; the half-cape covers only the viewer-right shoulder. The neck shows above the small open collar. The reference shows pale outlines of absent arms - those are extraction defects, not design. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 001
All left and right directions mean the viewer's left and right. Both arms are lowered and held slightly away from the body, both hands relaxed and open, exactly as Image 1, with clear gaps between the hands and the hips. No fist, no palm-up gesture, nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_001_celestial_scholar_pose_001.png
```

### Outfit 001 Celestial Scholar - Pose 002 (viewer-left vertical grip)

```text
Create ONE full-body character render: the Demigods Celestial Scholar outfit (family 001) worn by the collection's base figure in Pose 002 (viewer-left vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_002.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_001_celestial_scholar_pose_001.png (repository: assets/outfits/outfit_001_celestial_scholar_pose_001.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. An indigo half-cape with gold stars covers the VIEWER-RIGHT shoulder only, fastened by a gold star clasp with a blue gem; a gold waist sash is knotted on VIEWER-RIGHT with its end hanging. A gold crescent sits on the viewer-left chest; keep the reference's arrangement of embroidered panels.
Where skin shows: Both arms are bare below the armholes, and the viewer-left shoulder is bare; the half-cape covers only the viewer-right shoulder. The neck shows above the small open collar. The reference shows pale outlines of absent arms - those are extraction defects, not design. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 002
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is - staffs, swords and lanterns are added later as separate layers seated on that fist, and a fist drawn 20 px inward leaves every one of them hanging beside the hand. Keep the fist's grip clear of sleeves, capes and sashes. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_001_celestial_scholar_pose_002.png
```

### Outfit 001 Celestial Scholar - Pose 003 (viewer-right vertical grip)

```text
Create ONE full-body character render: the Demigods Celestial Scholar outfit (family 001) worn by the collection's base figure in Pose 003 (viewer-right vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png (repository: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_003.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_001_celestial_scholar_pose_001.png (repository: assets/outfits/outfit_001_celestial_scholar_pose_001.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. An indigo half-cape with gold stars covers the VIEWER-RIGHT shoulder only, fastened by a gold star clasp with a blue gem; a gold waist sash is knotted on VIEWER-RIGHT with its end hanging. A gold crescent sits on the viewer-left chest; keep the reference's arrangement of embroidered panels.
Where skin shows: Both arms are bare below the armholes, and the viewer-left shoulder is bare; the half-cape covers only the viewer-right shoulder. The neck shows above the small open collar. The reference shows pale outlines of absent arms - those are extraction defects, not design. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 003
All left and right directions mean the viewer's left and right. The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the LEFT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is, and keep its grip clear of fabric. Do not mirror Pose 002; asymmetric garment details stay on their own side. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_001_celestial_scholar_pose_003.png
```

### Outfit 001 Celestial Scholar - Pose 004 (viewer-left palm up)

```text
Create ONE full-body character render: the Demigods Celestial Scholar outfit (family 001) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_001_celestial_scholar_pose_001.png (repository: assets/outfits/outfit_001_celestial_scholar_pose_001.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. An indigo half-cape with gold stars covers the VIEWER-RIGHT shoulder only, fastened by a gold star clasp with a blue gem; a gold waist sash is knotted on VIEWER-RIGHT with its end hanging. A gold crescent sits on the viewer-left chest; keep the reference's arrangement of embroidered panels.
Where skin shows: Both arms are bare below the armholes, and the viewer-left shoulder is bare; the half-cape covers only the viewer-right shoulder. The neck shows above the small open collar. The reference shows pale outlines of absent arms - those are extraction defects, not design. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm exactly where Image 1's palm is - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of fabric. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_001_celestial_scholar_pose_004.png
```

### Outfit 001 Celestial Scholar - Pose 005 (centered two-hand grip)

```text
Create ONE full-body character render: the Demigods Celestial Scholar outfit (family 001) worn by the collection's base figure in Pose 005 (centered two-hand grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png (repository: assets/base_bodies/base_pose_005_centered_two_hand_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_005.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_001_celestial_scholar_pose_001.png (repository: assets/outfits/outfit_001_celestial_scholar_pose_001.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Ivory sleeveless tunic with a small open standing collar, gold crescent and constellation embroidery, a pointed ivory front tabard, indigo full-length trousers, and navy boots with gold edging and star ornaments. An indigo half-cape with gold stars covers the VIEWER-RIGHT shoulder only, fastened by a gold star clasp with a blue gem; a gold waist sash is knotted on VIEWER-RIGHT with its end hanging. A gold crescent sits on the viewer-left chest; keep the reference's arrangement of embroidered panels.
Where skin shows: Both arms are bare below the armholes, and the viewer-left shoulder is bare; the half-cape covers only the viewer-right shoulder. The neck shows above the small open collar. The reference shows pale outlines of absent arms - those are extraction defects, not design. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 005
All left and right directions mean the viewer's left and right. Both forearms angle inward across the lower torso and end in TWO STACKED GRIPPING HANDS at the centre, exactly as Image 1, with the same hand on top. Not side fists, not clasped palms, not a different arm crossing. No sash end, cape edge or ornament may paint over the hands. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_001_celestial_scholar_pose_005.png
```

### Outfit 002 Storm Guardian - Pose 001 (neutral, both hands open)

```text
Create ONE full-body character render: the Demigods Storm Guardian outfit (family 002) worn by the collection's base figure in Pose 001 (neutral, both hands open), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png (repository: assets/base_bodies/base_body_001_neutral_master.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_001.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_002_storm_guardian_pose_002.png (repository: assets/outfits/outfit_002_storm_guardian_pose_002.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Charcoal patterned sleeveless armour with bronze edging, an open raised collar with a teal inset, a single layered bronze pauldron with a circular shoulder boss on VIEWER-RIGHT, a teal waist sash with short teal hip panels, a brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze-and-brown plated shin guards over boots. Practical and compact: no weapon, shield or gloves.
Where skin shows: The viewer-left shoulder and both arms are bare below the armour and the short viewer-right pauldron. The neck shows inside the raised open collar; the collar must not close into a solid cap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 001
All left and right directions mean the viewer's left and right. Both arms are lowered and held slightly away from the body, both hands relaxed and open, exactly as Image 1, with clear gaps between the hands and the hips. No fist, no palm-up gesture, nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_002_storm_guardian_pose_001.png
```

### Outfit 002 Storm Guardian - Pose 002 (viewer-left vertical grip)

```text
Create ONE full-body character render: the Demigods Storm Guardian outfit (family 002) worn by the collection's base figure in Pose 002 (viewer-left vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_002.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_002_storm_guardian_pose_002.png (repository: assets/outfits/outfit_002_storm_guardian_pose_002.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Charcoal patterned sleeveless armour with bronze edging, an open raised collar with a teal inset, a single layered bronze pauldron with a circular shoulder boss on VIEWER-RIGHT, a teal waist sash with short teal hip panels, a brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze-and-brown plated shin guards over boots. Practical and compact: no weapon, shield or gloves.
Where skin shows: The viewer-left shoulder and both arms are bare below the armour and the short viewer-right pauldron. The neck shows inside the raised open collar; the collar must not close into a solid cap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 002
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is - staffs, swords and lanterns are added later as separate layers seated on that fist, and a fist drawn 20 px inward leaves every one of them hanging beside the hand. Keep the fist's grip clear of sleeves, capes and sashes. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_002_storm_guardian_pose_002.png
```

### Outfit 002 Storm Guardian - Pose 003 (viewer-right vertical grip)

```text
Create ONE full-body character render: the Demigods Storm Guardian outfit (family 002) worn by the collection's base figure in Pose 003 (viewer-right vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png (repository: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_003.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_002_storm_guardian_pose_002.png (repository: assets/outfits/outfit_002_storm_guardian_pose_002.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Charcoal patterned sleeveless armour with bronze edging, an open raised collar with a teal inset, a single layered bronze pauldron with a circular shoulder boss on VIEWER-RIGHT, a teal waist sash with short teal hip panels, a brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze-and-brown plated shin guards over boots. Practical and compact: no weapon, shield or gloves.
Where skin shows: The viewer-left shoulder and both arms are bare below the armour and the short viewer-right pauldron. The neck shows inside the raised open collar; the collar must not close into a solid cap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 003
All left and right directions mean the viewer's left and right. The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the LEFT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is, and keep its grip clear of fabric. Do not mirror Pose 002; asymmetric garment details stay on their own side. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_002_storm_guardian_pose_003.png
```

### Outfit 002 Storm Guardian - Pose 004 (viewer-left palm up)

```text
Create ONE full-body character render: the Demigods Storm Guardian outfit (family 002) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_002_storm_guardian_pose_002.png (repository: assets/outfits/outfit_002_storm_guardian_pose_002.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Charcoal patterned sleeveless armour with bronze edging, an open raised collar with a teal inset, a single layered bronze pauldron with a circular shoulder boss on VIEWER-RIGHT, a teal waist sash with short teal hip panels, a brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze-and-brown plated shin guards over boots. Practical and compact: no weapon, shield or gloves.
Where skin shows: The viewer-left shoulder and both arms are bare below the armour and the short viewer-right pauldron. The neck shows inside the raised open collar; the collar must not close into a solid cap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm exactly where Image 1's palm is - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of fabric. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_002_storm_guardian_pose_004.png
```

### Outfit 002 Storm Guardian - Pose 005 (centered two-hand grip)

```text
Create ONE full-body character render: the Demigods Storm Guardian outfit (family 002) worn by the collection's base figure in Pose 005 (centered two-hand grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png (repository: assets/base_bodies/base_pose_005_centered_two_hand_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_005.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_002_storm_guardian_pose_002.png (repository: assets/outfits/outfit_002_storm_guardian_pose_002.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
Charcoal patterned sleeveless armour with bronze edging, an open raised collar with a teal inset, a single layered bronze pauldron with a circular shoulder boss on VIEWER-RIGHT, a teal waist sash with short teal hip panels, a brown utility belt with a bronze hexagonal buckle, dark trousers, and bronze-and-brown plated shin guards over boots. Practical and compact: no weapon, shield or gloves.
Where skin shows: The viewer-left shoulder and both arms are bare below the armour and the short viewer-right pauldron. The neck shows inside the raised open collar; the collar must not close into a solid cap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 005
All left and right directions mean the viewer's left and right. Both forearms angle inward across the lower torso and end in TWO STACKED GRIPPING HANDS at the centre, exactly as Image 1, with the same hand on top. Not side fists, not clasped palms, not a different arm crossing. No sash end, cape edge or ornament may paint over the hands. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_002_storm_guardian_pose_005.png
```

### Outfit 003 Verdant Alchemist - Pose 001 (neutral, both hands open)

```text
Create ONE full-body character render: the Demigods Verdant Alchemist outfit (family 003) worn by the collection's base figure in Pose 001 (neutral, both hands open), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png (repository: assets/base_bodies/base_body_001_neutral_master.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_001.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_003_verdant_alchemist_pose_003.png (repository: assets/outfits/outfit_003_verdant_alchemist_pose_003.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An olive fitted embroidered vest with warm brass buttons over a cream linen shirt, and a brown bandolier running from the VIEWER-LEFT shoulder to the VIEWER-RIGHT waist carrying four small green and blue potion vials. A brown double belt with a square brass buckle, a small pouch on the viewer-right hip and a hanging vial on the viewer-left; rust shorts over dark leggings; brown lace-up boots.
Where skin shows: Hands and neck only. The shirt sleeves cover both arms to the wrists, their rolled cuffs ending at each wrist. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 001
All left and right directions mean the viewer's left and right. Both arms are lowered and held slightly away from the body, both hands relaxed and open, exactly as Image 1, with clear gaps between the hands and the hips. No fist, no palm-up gesture, nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_003_verdant_alchemist_pose_001.png
```

### Outfit 003 Verdant Alchemist - Pose 002 (viewer-left vertical grip)

```text
Create ONE full-body character render: the Demigods Verdant Alchemist outfit (family 003) worn by the collection's base figure in Pose 002 (viewer-left vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_002.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_003_verdant_alchemist_pose_003.png (repository: assets/outfits/outfit_003_verdant_alchemist_pose_003.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An olive fitted embroidered vest with warm brass buttons over a cream linen shirt, and a brown bandolier running from the VIEWER-LEFT shoulder to the VIEWER-RIGHT waist carrying four small green and blue potion vials. A brown double belt with a square brass buckle, a small pouch on the viewer-right hip and a hanging vial on the viewer-left; rust shorts over dark leggings; brown lace-up boots.
Where skin shows: Hands and neck only. The shirt sleeves cover both arms to the wrists, their rolled cuffs ending at each wrist. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 002
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is - staffs, swords and lanterns are added later as separate layers seated on that fist, and a fist drawn 20 px inward leaves every one of them hanging beside the hand. Keep the fist's grip clear of sleeves, capes and sashes. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_003_verdant_alchemist_pose_002.png
```

### Outfit 003 Verdant Alchemist - Pose 003 (viewer-right vertical grip)

```text
Create ONE full-body character render: the Demigods Verdant Alchemist outfit (family 003) worn by the collection's base figure in Pose 003 (viewer-right vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png (repository: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_003.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_003_verdant_alchemist_pose_003.png (repository: assets/outfits/outfit_003_verdant_alchemist_pose_003.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An olive fitted embroidered vest with warm brass buttons over a cream linen shirt, and a brown bandolier running from the VIEWER-LEFT shoulder to the VIEWER-RIGHT waist carrying four small green and blue potion vials. A brown double belt with a square brass buckle, a small pouch on the viewer-right hip and a hanging vial on the viewer-left; rust shorts over dark leggings; brown lace-up boots.
Where skin shows: Hands and neck only. The shirt sleeves cover both arms to the wrists, their rolled cuffs ending at each wrist. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 003
All left and right directions mean the viewer's left and right. The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the LEFT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is, and keep its grip clear of fabric. Do not mirror Pose 002; asymmetric garment details stay on their own side. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_003_verdant_alchemist_pose_003.png
```

### Outfit 003 Verdant Alchemist - Pose 004 (viewer-left palm up)

```text
Create ONE full-body character render: the Demigods Verdant Alchemist outfit (family 003) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_003_verdant_alchemist_pose_003.png (repository: assets/outfits/outfit_003_verdant_alchemist_pose_003.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An olive fitted embroidered vest with warm brass buttons over a cream linen shirt, and a brown bandolier running from the VIEWER-LEFT shoulder to the VIEWER-RIGHT waist carrying four small green and blue potion vials. A brown double belt with a square brass buckle, a small pouch on the viewer-right hip and a hanging vial on the viewer-left; rust shorts over dark leggings; brown lace-up boots.
Where skin shows: Hands and neck only. The shirt sleeves cover both arms to the wrists, their rolled cuffs ending at each wrist. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm exactly where Image 1's palm is - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of fabric. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_003_verdant_alchemist_pose_004.png
```

### Outfit 003 Verdant Alchemist - Pose 005 (centered two-hand grip)

```text
Create ONE full-body character render: the Demigods Verdant Alchemist outfit (family 003) worn by the collection's base figure in Pose 005 (centered two-hand grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png (repository: assets/base_bodies/base_pose_005_centered_two_hand_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_005.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_003_verdant_alchemist_pose_003.png (repository: assets/outfits/outfit_003_verdant_alchemist_pose_003.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An olive fitted embroidered vest with warm brass buttons over a cream linen shirt, and a brown bandolier running from the VIEWER-LEFT shoulder to the VIEWER-RIGHT waist carrying four small green and blue potion vials. A brown double belt with a square brass buckle, a small pouch on the viewer-right hip and a hanging vial on the viewer-left; rust shorts over dark leggings; brown lace-up boots.
Where skin shows: Hands and neck only. The shirt sleeves cover both arms to the wrists, their rolled cuffs ending at each wrist. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 005
All left and right directions mean the viewer's left and right. Both forearms angle inward across the lower torso and end in TWO STACKED GRIPPING HANDS at the centre, exactly as Image 1, with the same hand on top. Not side fists, not clasped palms, not a different arm crossing. No sash end, cape edge or ornament may paint over the hands. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_003_verdant_alchemist_pose_005.png
```

### Outfit 004 Lunar Oracle - Pose 001 (neutral, both hands open)

```text
Create ONE full-body character render: the Demigods Lunar Oracle outfit (family 004) worn by the collection's base figure in Pose 001 (neutral, both hands open), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png (repository: assets/base_bodies/base_body_001_neutral_master.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_001.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_004_lunar_oracle_pose_004.png (repository: assets/outfits/outfit_004_lunar_oracle_pose_004.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on the VIEWER-RIGHT chest, a layered lavender-and-plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. A silver rope belt is knotted with two crescent charms hanging on VIEWER-RIGHT. Keep the reference's wrap direction, panel shapes and lavender lining.
Where skin shows: Both shoulders and both arms are bare through clean sleeveless openings. The neck shows above the wrap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 001
All left and right directions mean the viewer's left and right. Both arms are lowered and held slightly away from the body, both hands relaxed and open, exactly as Image 1, with clear gaps between the hands and the hips. No fist, no palm-up gesture, nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_004_lunar_oracle_pose_001.png
```

### Outfit 004 Lunar Oracle - Pose 002 (viewer-left vertical grip)

```text
Create ONE full-body character render: the Demigods Lunar Oracle outfit (family 004) worn by the collection's base figure in Pose 002 (viewer-left vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_002.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_004_lunar_oracle_pose_004.png (repository: assets/outfits/outfit_004_lunar_oracle_pose_004.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on the VIEWER-RIGHT chest, a layered lavender-and-plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. A silver rope belt is knotted with two crescent charms hanging on VIEWER-RIGHT. Keep the reference's wrap direction, panel shapes and lavender lining.
Where skin shows: Both shoulders and both arms are bare through clean sleeveless openings. The neck shows above the wrap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 002
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is - staffs, swords and lanterns are added later as separate layers seated on that fist, and a fist drawn 20 px inward leaves every one of them hanging beside the hand. Keep the fist's grip clear of sleeves, capes and sashes. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_004_lunar_oracle_pose_002.png
```

### Outfit 004 Lunar Oracle - Pose 003 (viewer-right vertical grip)

```text
Create ONE full-body character render: the Demigods Lunar Oracle outfit (family 004) worn by the collection's base figure in Pose 003 (viewer-right vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png (repository: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_003.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_004_lunar_oracle_pose_004.png (repository: assets/outfits/outfit_004_lunar_oracle_pose_004.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on the VIEWER-RIGHT chest, a layered lavender-and-plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. A silver rope belt is knotted with two crescent charms hanging on VIEWER-RIGHT. Keep the reference's wrap direction, panel shapes and lavender lining.
Where skin shows: Both shoulders and both arms are bare through clean sleeveless openings. The neck shows above the wrap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 003
All left and right directions mean the viewer's left and right. The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the LEFT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is, and keep its grip clear of fabric. Do not mirror Pose 002; asymmetric garment details stay on their own side. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_004_lunar_oracle_pose_003.png
```

### Outfit 004 Lunar Oracle - Pose 004 (viewer-left palm up)

```text
Create ONE full-body character render: the Demigods Lunar Oracle outfit (family 004) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_004_lunar_oracle_pose_004.png (repository: assets/outfits/outfit_004_lunar_oracle_pose_004.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on the VIEWER-RIGHT chest, a layered lavender-and-plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. A silver rope belt is knotted with two crescent charms hanging on VIEWER-RIGHT. Keep the reference's wrap direction, panel shapes and lavender lining.
Where skin shows: Both shoulders and both arms are bare through clean sleeveless openings. The neck shows above the wrap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm exactly where Image 1's palm is - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of fabric. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_004_lunar_oracle_pose_004.png
```

### Outfit 004 Lunar Oracle - Pose 005 (centered two-hand grip)

```text
Create ONE full-body character render: the Demigods Lunar Oracle outfit (family 004) worn by the collection's base figure in Pose 005 (centered two-hand grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png (repository: assets/base_bodies/base_pose_005_centered_two_hand_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_005.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_004_lunar_oracle_pose_004.png (repository: assets/outfits/outfit_004_lunar_oracle_pose_004.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A deep plum sleeveless wrap tunic with narrow silver embroidered borders, a silver crescent and small star on the VIEWER-RIGHT chest, a layered lavender-and-plum petal-panel skirt over plum trousers, and purple boots with silver crescent details and silver edges. A silver rope belt is knotted with two crescent charms hanging on VIEWER-RIGHT. Keep the reference's wrap direction, panel shapes and lavender lining.
Where skin shows: Both shoulders and both arms are bare through clean sleeveless openings. The neck shows above the wrap. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 005
All left and right directions mean the viewer's left and right. Both forearms angle inward across the lower torso and end in TWO STACKED GRIPPING HANDS at the centre, exactly as Image 1, with the same hand on top. Not side fists, not clasped palms, not a different arm crossing. No sash end, cape edge or ornament may paint over the hands. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background, because the collection separates the figure from black by brightness and dark fabric would be cut away with it. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_004_lunar_oracle_pose_005.png
```

### Outfit 005 Sun Temple - Pose 001 (neutral, both hands open)

```text
Create ONE full-body character render: the Demigods Sun Temple outfit (family 005) worn by the collection's base figure in Pose 001 (neutral, both hands open), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png (repository: assets/base_bodies/base_body_001_neutral_master.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_001.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_005_sun_temple_pose_005.png (repository: assets/outfits/outfit_005_sun_temple_pose_005.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An ivory short-sleeved ceremonial tunic with a small open standing collar, orange and terracotta embroidered vertical bands with matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Loose ivory trousers with orange geometric cuffs, ivory shin wraps with terracotta criss-cross ties, and complete orange-and-ivory footwear. Warm ivory, terracotta and a restrained gold.
Where skin shows: Short sleeves cover the shoulder caps and upper arms and end above the elbows; forearms and hands are bare. The neck shows above the small open collar. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 001
All left and right directions mean the viewer's left and right. Both arms are lowered and held slightly away from the body, both hands relaxed and open, exactly as Image 1, with clear gaps between the hands and the hips. No fist, no palm-up gesture, nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_005_sun_temple_pose_001.png
```

### Outfit 005 Sun Temple - Pose 002 (viewer-left vertical grip)

```text
Create ONE full-body character render: the Demigods Sun Temple outfit (family 005) worn by the collection's base figure in Pose 002 (viewer-left vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_002.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_005_sun_temple_pose_005.png (repository: assets/outfits/outfit_005_sun_temple_pose_005.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An ivory short-sleeved ceremonial tunic with a small open standing collar, orange and terracotta embroidered vertical bands with matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Loose ivory trousers with orange geometric cuffs, ivory shin wraps with terracotta criss-cross ties, and complete orange-and-ivory footwear. Warm ivory, terracotta and a restrained gold.
Where skin shows: Short sleeves cover the shoulder caps and upper arms and end above the elbows; forearms and hands are bare. The neck shows above the small open collar. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 002
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is - staffs, swords and lanterns are added later as separate layers seated on that fist, and a fist drawn 20 px inward leaves every one of them hanging beside the hand. Keep the fist's grip clear of sleeves, capes and sashes. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_005_sun_temple_pose_002.png
```

### Outfit 005 Sun Temple - Pose 003 (viewer-right vertical grip)

```text
Create ONE full-body character render: the Demigods Sun Temple outfit (family 005) worn by the collection's base figure in Pose 003 (viewer-right vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png (repository: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_003.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_005_sun_temple_pose_005.png (repository: assets/outfits/outfit_005_sun_temple_pose_005.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An ivory short-sleeved ceremonial tunic with a small open standing collar, orange and terracotta embroidered vertical bands with matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Loose ivory trousers with orange geometric cuffs, ivory shin wraps with terracotta criss-cross ties, and complete orange-and-ivory footwear. Warm ivory, terracotta and a restrained gold.
Where skin shows: Short sleeves cover the shoulder caps and upper arms and end above the elbows; forearms and hands are bare. The neck shows above the small open collar. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 003
All left and right directions mean the viewer's left and right. The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the LEFT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is, and keep its grip clear of fabric. Do not mirror Pose 002; asymmetric garment details stay on their own side. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_005_sun_temple_pose_003.png
```

### Outfit 005 Sun Temple - Pose 004 (viewer-left palm up)

```text
Create ONE full-body character render: the Demigods Sun Temple outfit (family 005) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_005_sun_temple_pose_005.png (repository: assets/outfits/outfit_005_sun_temple_pose_005.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An ivory short-sleeved ceremonial tunic with a small open standing collar, orange and terracotta embroidered vertical bands with matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Loose ivory trousers with orange geometric cuffs, ivory shin wraps with terracotta criss-cross ties, and complete orange-and-ivory footwear. Warm ivory, terracotta and a restrained gold.
Where skin shows: Short sleeves cover the shoulder caps and upper arms and end above the elbows; forearms and hands are bare. The neck shows above the small open collar. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm exactly where Image 1's palm is - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of fabric. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_005_sun_temple_pose_004.png
```

### Outfit 005 Sun Temple - Pose 005 (centered two-hand grip)

```text
Create ONE full-body character render: the Demigods Sun Temple outfit (family 005) worn by the collection's base figure in Pose 005 (centered two-hand grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png (repository: assets/base_bodies/base_pose_005_centered_two_hand_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_005.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_005_sun_temple_pose_005.png (repository: assets/outfits/outfit_005_sun_temple_pose_005.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
An ivory short-sleeved ceremonial tunic with a small open standing collar, orange and terracotta embroidered vertical bands with matching geometric sleeve and hem borders, a terracotta waist sash, and a long patterned central panel ending in fringe. Loose ivory trousers with orange geometric cuffs, ivory shin wraps with terracotta criss-cross ties, and complete orange-and-ivory footwear. Warm ivory, terracotta and a restrained gold.
Where skin shows: Short sleeves cover the shoulder caps and upper arms and end above the elbows; forearms and hands are bare. The neck shows above the small open collar. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 005
All left and right directions mean the viewer's left and right. Both forearms angle inward across the lower torso and end in TWO STACKED GRIPPING HANDS at the centre, exactly as Image 1, with the same hand on top. Not side fists, not clasped palms, not a different arm crossing. No sash end, cape edge or ornament may paint over the hands. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_005_sun_temple_pose_005.png
```

### Outfit 010 Celestial Robe, white and gold - Pose 001 (neutral, both hands open)

```text
Create ONE full-body character render: the Demigods Celestial Robe, white and gold outfit (family 010) worn by the collection's base figure in Pose 001 (neutral, both hands open), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_body_001_neutral_master.png (repository: assets/base_bodies/base_body_001_neutral_master.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_001.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_010_celestial_robe_white_gold.png (repository: assets/outfits/outfit_010_celestial_robe_white_gold.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A silver-white and ivory ceremonial coat-robe with a high OPEN collar, pale blue-grey facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with a star clasp and its end hanging on VIEWER-RIGHT, long split robe panels over white trousers, and complete white-and-gold star-trimmed boots. Keep the long vertical pale-blue front panels and the airy white-and-gold values.
Where skin shows: Hands and neck only. The sleeves cover the shoulders and arms to the wrists. The neck rises through the open collar, whose inside shows real fabric depth. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 001
All left and right directions mean the viewer's left and right. Both arms are lowered and held slightly away from the body, both hands relaxed and open, exactly as Image 1, with clear gaps between the hands and the hips. No fist, no palm-up gesture, nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_010_celestial_robe_white_gold_pose_001.png
```

### Outfit 010 Celestial Robe, white and gold - Pose 002 (viewer-left vertical grip)

```text
Create ONE full-body character render: the Demigods Celestial Robe, white and gold outfit (family 010) worn by the collection's base figure in Pose 002 (viewer-left vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_002.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_010_celestial_robe_white_gold.png (repository: assets/outfits/outfit_010_celestial_robe_white_gold.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A silver-white and ivory ceremonial coat-robe with a high OPEN collar, pale blue-grey facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with a star clasp and its end hanging on VIEWER-RIGHT, long split robe panels over white trousers, and complete white-and-gold star-trimmed boots. Keep the long vertical pale-blue front panels and the airy white-and-gold values.
Where skin shows: Hands and neck only. The sleeves cover the shoulders and arms to the wrists. The neck rises through the open collar, whose inside shows real fabric depth. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 002
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is - staffs, swords and lanterns are added later as separate layers seated on that fist, and a fist drawn 20 px inward leaves every one of them hanging beside the hand. Keep the fist's grip clear of sleeves, capes and sashes. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_010_celestial_robe_white_gold_pose_002.png
```

### Outfit 010 Celestial Robe, white and gold - Pose 003 (viewer-right vertical grip)

```text
Create ONE full-body character render: the Demigods Celestial Robe, white and gold outfit (family 010) worn by the collection's base figure in Pose 003 (viewer-right vertical grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_003_viewer_right_vertical_grip.png (repository: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_003.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_010_celestial_robe_white_gold.png (repository: assets/outfits/outfit_010_celestial_robe_white_gold.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A silver-white and ivory ceremonial coat-robe with a high OPEN collar, pale blue-grey facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with a star clasp and its end hanging on VIEWER-RIGHT, long split robe panels over white trousers, and complete white-and-gold star-trimmed boots. Keep the long vertical pale-blue front panels and the airy white-and-gold values.
Where skin shows: Hands and neck only. The sleeves cover the shoulders and arms to the wrists. The neck rises through the open collar, whose inside shows real fabric depth. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 003
All left and right directions mean the viewer's left and right. The hand on the RIGHT SIDE OF THE IMAGE is a vertical gripping fist held low at the side; the hand on the LEFT SIDE OF THE IMAGE is relaxed and open. Put the fist exactly where Image 1's fist is, and keep its grip clear of fabric. Do not mirror Pose 002; asymmetric garment details stay on their own side. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_010_celestial_robe_white_gold_pose_003.png
```

### Outfit 010 Celestial Robe, white and gold - Pose 004 (viewer-left palm up)

```text
Create ONE full-body character render: the Demigods Celestial Robe, white and gold outfit (family 010) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_010_celestial_robe_white_gold.png (repository: assets/outfits/outfit_010_celestial_robe_white_gold.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A silver-white and ivory ceremonial coat-robe with a high OPEN collar, pale blue-grey facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with a star clasp and its end hanging on VIEWER-RIGHT, long split robe panels over white trousers, and complete white-and-gold star-trimmed boots. Keep the long vertical pale-blue front panels and the airy white-and-gold values.
Where skin shows: Hands and neck only. The sleeves cover the shoulders and arms to the wrists. The neck rises through the open collar, whose inside shows real fabric depth. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm exactly where Image 1's palm is - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of fabric. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_010_celestial_robe_white_gold_pose_004.png
```

### Outfit 010 Celestial Robe, white and gold - Pose 005 (centered two-hand grip)

```text
Create ONE full-body character render: the Demigods Celestial Robe, white and gold outfit (family 010) worn by the collection's base figure in Pose 005 (centered two-hand grip), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_005_centered_two_hand_grip.png (repository: assets/base_bodies/base_pose_005_centered_two_hand_grip.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_007_brown_leather_long_coat_pose_005.png (repository: assets/outfits/). An approved render in this same pose, showing only the finished format: a bald, faceless figure wearing a complete outfit at exactly this scale. Do not copy its coat.
Image 3: outfit_010_celestial_robe_white_gold.png (repository: assets/outfits/outfit_010_celestial_robe_white_gold.png). The outfit design: garments, colours, materials and ornaments. Its fit, pose and extraction are not authoritative.

FIGURE
Paint Image 1's figure wearing the outfit. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair. Face, hair and headwear are added later as separate layers, so a painted feature would show through them.

OUTFIT
A silver-white and ivory ceremonial coat-robe with a high OPEN collar, pale blue-grey facing and lining, delicate gold constellation embroidery and scrollwork, full sleeves with flared gold-embroidered cuffs, a gold waist sash with a star clasp and its end hanging on VIEWER-RIGHT, long split robe panels over white trousers, and complete white-and-gold star-trimmed boots. Keep the long vertical pale-blue front panels and the airy white-and-gold values.
Where skin shows: Hands and neck only. The sleeves cover the shoulders and arms to the wrists. The neck rises through the open collar, whose inside shows real fabric depth. Everything else is covered: no undershirt, tank or shorts may show at the neckline, sides, waist, hips or thighs.

POSE 005
All left and right directions mean the viewer's left and right. Both forearms angle inward across the lower torso and end in TWO STACKED GRIPPING HANDS at the centre, exactly as Image 1, with the same hand on top. Not side fists, not clasped palms, not a different arm crossing. No sash end, cape edge or ornament may paint over the hands. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. If your generator cannot output transparency, use a flat pure black (#000000) background instead - nothing else: no gradient, vignette, floor or shadow. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_010_celestial_robe_white_gold_pose_005.png
```

### Outfit 006 Black layered hooded robe - Pose 004 (viewer-left palm up)

The first render of this pose drew the palm 16 px inside the base's, so every palm object hung off it; it was withdrawn. The palm is the point of this prompt.

```text
Create ONE full-body character render: the Demigods Black layered hooded robe outfit (family 006) worn by the collection's base figure in Pose 004 (viewer-left palm up), painted with the body intact.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/base_pose_004_viewer_left_palm_up.png). The exact figure, pose, scale and placement. It governs every contour: head, ears, neck, shoulders, arms, hands, legs and feet.
Image 2: outfit_006_black_layered_hooded_robe_pose_001.png (repository: assets/outfits/). The same robe, approved, in another pose: its design, fabric planes and finish exactly as the collection has them.
Image 3: outfit_007_brown_leather_long_coat_pose_004.png (repository: assets/outfits/). An approved render in this same pose. Its open palm sits exactly where it must; do not copy its coat.

FIGURE
Paint Image 1's figure wearing the robe. Keep Image 1's head, ears, neck, arms, hands, legs, stance and proportions exactly: the same head size and position (top of the head near Y 140, head centred on X 627, about 353 px across the ears, chin near Y 461), the same arm and hand positions, and the soles on Image 1's baseline near Y 1140. Do not lengthen the legs or the body, and do not enlarge or shrink the figure. The head stays bald and faceless: smooth skin and ears only - no eyes, eyebrows, nose, mouth or hair.

OUTFIT
Deep black and charcoal layered long robe with a collapsed hood behind the open neckline, an overlapping inner tunic, restrained silver-grey seams and angular ornaments, a dark belt with metal buckle and hanging strap, long pointed split robe panels, full sleeves with broad dark cuffs, black trousers and complete black boots. Preserve the many distinct black fabric planes through controlled shading; keep the hood down and off the head.
Where skin shows: hands and neck only. The sleeves cover the shoulders and arms to the wrists. Everything else is covered.

POSE 004
All left and right directions mean the viewer's left and right. The hand on the LEFT SIDE OF THE IMAGE is open and turned palm-up at the low side position; the hand on the RIGHT SIDE OF THE IMAGE is relaxed and open. Put the palm EXACTLY where Image 1's palm is, fingertips included - an orb, a book or a talisman is added later seated on it - and keep the space around it clear of the sleeve. Nothing held.

CANVAS AND STYLE
One 1254 x 1254 PNG with a TRANSPARENT background. This outfit is dark: do not substitute a black background. One figure, front-facing and orthographic, in the collection's anime-chibi fantasy game-art style: clean coherent outlines, refined cel and painterly shading, soft upper-left key light with lower-right form shadows and a subtle cool right rim light.

AVOID
Eyes, eyebrows, nose, mouth, hair, hats, jewellery at the neck, held objects, weapons, wings, auras, glows, ground shadows, floors, scenery, text, labels, borders, a second figure or view, a checkerboard painted into the image, a changed camera, a mirrored pose, a stretched or shortened body, a larger or smaller head, and anything cropped at the canvas edge.

OUTPUT
Exactly one PNG named: outfit_006_black_layered_hooded_robe_pose_004.png
```
