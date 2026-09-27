# Demigods - hand objects painted with the hand holding them

Prepared 2026-09-26. The owner wants every handheld item drawn with the hand actually holding it, so no hand overlay is needed during token generation. Updated the same day: the hand is painted without a wrist (see below). Copying the base's fist onto the existing objects was tried and rejected: a closed fist laid over a shaft does not read as a grip. All twelve items need new renders where the hand and the object are painted together.

## How to generate one

1. Attach the two images in the stated order, as files.
2. Generate one image per prompt. Keep every attempt; do not edit, crop or resize the output.
3. Save the original PNG under `images/trait_candidates/hand_objects/` and hand it to intake. Normalization follows `docs/workflows/generator_source_transform.md` (reduction only).

## What makes a render usable

- **The object really passes through the hand.** Staffs, blades and scepters enter the top of the fist and leave the bottom in one straight line, with the fingers wrapped over them. The palm items rest in or hang from the hand with the fingers touching them.
- **The hand stays the body's size.** Renders that drew the hand large had to be shrunk to fit the body, which shrank the item too; the owner rejected those (003, 004, 007). Each prompt gives the hand's and the object's size in pixels.
- **The hand is the base pose's hand, in place.** The layer shares the body's canvas, so the painted hand has to land on the base's own hand at the same size, or it shows as a second hand.
- **No wrist.** Paint the hand only up to the base of the palm, with a soft edge that has no outline; the body layer supplies the wrist and forearm. Painted wrists never lined up with the body's arm (sideways stumps, outlines drawn across the wrist, the hand turned the wrong way), so the owner asked for renders without them. A render that still shows a painted wrist is rejected and generated again; wrists are not trimmed off.
- **Transparent background.** Nothing else on the canvas.

# Fist grip - Pose 002 (8 items)

### Hand object 001 Arcane staff - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods arcane staff held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_001_arcane_staff_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 246 px wide and 841 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a tall twisted dark-brown wooden staff whose top splits into gnarled roots cradling a blue-violet flame crystal. The fingers wrap fully around the shaft: the shaft enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the shaft is visible through the hand, and there is no gap between hand and shaft. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 003 Dark wand - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods dark wand held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_003_dark_wand_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 191 px wide and 789 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a long slim dark wooden wand-staff tipped with a small violet crystal. The fingers wrap fully around the shaft: the shaft enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the shaft is visible through the hand, and there is no gap between hand and shaft. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 004 Silver sword - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods silver sword held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_004_silver_sword_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 191 px wide and 780 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a silver longsword with a slim blade, a silver crossguard set with a blue gem, a navy cord-wrapped grip and a round blue-gem pommel. The fingers wrap fully around the sword grip: the sword grip enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the sword grip is visible through the hand, and there is no gap between hand and sword grip. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 006 Gold lantern - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods gold lantern held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_006_gold_lantern_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 174 px wide and 398 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a warm-gold hanging lantern with glowing amber panels and a round top ring. The fist closes around the lantern's top ring: the ring passes through the curled fingers, the thumb presses over it, and the lantern hangs straight down below the hand, clear of the legs and the canvas bottom. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 007 Gold staff with blue gem - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods gold staff with blue gem held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_007_gold_blue_gem_staff_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 195 px wide and 639 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a slim gold staff with an ornate gold head holding a large blue gem and a pointed gold foot. The fingers wrap fully around the shaft: the shaft enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the shaft is visible through the hand, and there is no gap between hand and shaft. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 008 Blue crescent staff - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods blue crescent staff held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_008_blue_crescent_staff_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 253 px wide and 816 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a blue staff with a gold crescent-moon head set with a blue gem, gold collars and a pointed gold foot. The fingers wrap fully around the shaft: the shaft enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the shaft is visible through the hand, and there is no gap between hand and shaft. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 009 Violet blade - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods violet blade held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_009_violet_blade_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 226 px wide and 768 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a large violet crystal blade with a curved gold crossguard set with a violet gem, a purple cord-wrapped grip and a gold pommel. The fingers wrap fully around the blade grip: the blade grip enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the blade grip is visible through the hand, and there is no gap between hand and blade grip. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 010 Horned skull scepter - Pose 002 (viewer-left vertical grip)

```text
Create ONE isolated trait layer: the Demigods horned skull scepter held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_002_viewer_left_vertical_grip.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_010_horned_skull_scepter_pose_002_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1, centred near X 438, Y 772, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. It is a gripping hand, not a solid fist: the curled fingers and thumb close around the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the fist is about 72 px wide, while the object keeps Image 2's full size, about 203 px wide and 622 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a slim dark scepter topped by a horned bone skull with a violet gem, with a pointed dark foot. The fingers wrap fully around the shaft: the shaft enters the top of the fist between thumb and index finger and leaves the bottom below the little finger, in one straight continuous line at Image 2's angle. The thumb crosses in front of it, the curled fingers overlap it, and the knuckles face the viewer. No part of the shaft is visible through the hand, and there is no gap between hand and shaft. The top of the object stays on the outer left of the body and never enters the face or torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

# Palm up - Pose 004 (4 items)

### Hand object 002 Violet crystal orb - Pose 004 (viewer-left palm up)

```text
Create ONE isolated trait layer: the Demigods violet crystal orb held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_002_violet_orb_pose_004_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1: open, palm up, the palm centred near X 438, Y 748, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. Five relaxed fingers that curl slightly to hold the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the open hand is about 98 px wide, while the object keeps Image 2's full size, about 180 px wide and 220 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a faceted violet crystal orb about 150 px across in a small ornate silver cradle, resting upright in the cupped palm. The fingers curl up around the cradle; the orb rises above the hand, stays below Y 560 and clear of the torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 005 Star spellbook - Pose 004 (viewer-left palm up)

```text
Create ONE isolated trait layer: the Demigods star spellbook held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_005_star_spellbook_pose_004_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1: open, palm up, the palm centred near X 438, Y 748, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. Five relaxed fingers that curl slightly to hold the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the open hand is about 98 px wide, while the object keeps Image 2's full size, about 230 px wide and 161 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a closed navy leather spellbook with gold corner guards and a gold eight-point star on the cover, lying on the open palm, cover facing the viewer and tilted slightly upward. The fingers curl up against its lower edge and the thumb rests on its side; the book stays clear of the torso and face. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 011 Round talisman - Pose 004 (viewer-left palm up)

```text
Create ONE isolated trait layer: the Demigods round talisman held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_011_round_talisman_pose_004_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1: open, palm up, the palm centred near X 438, Y 748, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. Five relaxed fingers that curl slightly to hold the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the open hand is about 98 px wide, while the object keeps Image 2's full size, about 170 px wide and 229 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint a round bronze-and-navy talisman with a gold compass star and small crescent. The disc alone is about 160 px across, clearly wider than the whole hand, and no blue glow outlines it. The hand stays open and palm up as in Image 1, never a closed fist. Its top ring lies across the palm with the fingers curled over it and the thumb pinning it; the disc hangs below the hand, clear of the legs. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```

### Hand object 012 Brown tome - Pose 004 (viewer-left palm up)

```text
Create ONE isolated trait layer: the Demigods brown tome held in the collection figure's viewer-left hand, with the hand painted actually holding it.

ATTACH THESE IMAGES IN THIS ORDER
Image 1: base_pose_004_viewer_left_palm_up.png (repository: assets/base_bodies/). The exact figure, scale and placement. Use it only as an invisible alignment guide: its viewer-left hand sets the hand's position, size and skin.
Image 2: hand_object_012_brown_tome_pose_004_left.png (repository: assets/hand_objects/, as it was at commit 788454a, before the in-hand versions replaced it). The object design: shape, colours, materials, ornaments and length. Its relation to the hand is wrong and must not be copied.

OUTPUT
One 1254 x 1254 transparent PNG. Only two things are painted: the viewer-left hand, from the fingertips back to the base of the palm (no wrist), and the object it holds. No arm, body, head, clothing, background or shadow.

HAND
Paint Image 1's viewer-left hand where it is in Image 1: open, palm up, the palm centred near X 438, Y 748, at the same size, skin tone, line weight and shading, so it sits exactly over the body's own hand. Paint NO wrist: stop at the base of the palm, just below Image 1's wrist line, and leave that edge soft, with no outline, rim light or cap along it; the body's own wrist and forearm continue the hand there. The hand keeps Image 1's angle to the arm and never turns sideways. Five relaxed fingers that curl slightly to hold the object.

SIZE
The hand stays small, exactly Image 1's size: on the 1254 x 1254 canvas the open hand is about 98 px wide, while the object keeps Image 2's full size, about 310 px wide and 133 px tall. Do not enlarge the hand to show the grip, and do not shrink the object to fit the hand.

OBJECT AND GRIP
Paint an open brown leather tome with cream pages and a gold compass emblem, resting open on the upturned palm, pages up and toward the viewer. The fingertips curl up at its near edge and the thumb holds the page edge; the tome stays clear of the torso. Hand and object read as one piece: a believable contact shadow where they touch, and every finger in front of the object painted over it.

STYLE
Premium anime-chibi fantasy game art, perfectly front-facing orthographic view, soft upper-left key light with form shadows toward the lower right, subtle cool rim light from the right on the object only, none on the hand. Keep glows inside soft alpha falloff with no rectangular backdrop.

AVOID:
wrist, wrist stump, forearm stub, an outlined or capped edge where the hand stops, a hand turned sideways, body, forearm, sleeve, second hand, a hand pasted on top of the object, a closed fist with nothing inside it, the object floating beside, behind or in front of the hand, extra fingers, missing fingers, malformed hands, a hand placed anywhere other than Image 1's hand, scenery, floor shadows, labels, frames, checkerboard, fake transparency, cropped edges, multiple objects, perspective distortion.
```
