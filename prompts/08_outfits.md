# Prompt — Pose-Aware Outfit Family

Generate outfits as a family of pose-specific layers. A neutral-pose outfit is
not compatible with a grip or palm-up pose unless a separate fitted variant has
passed the composite gate.

## Required inputs

- `[OUTFIT FAMILY ID]`
- `[DESCRIPTION]`
- `[POSE ID]` and its exact approved file from `assets/base_bodies/`
- `[ARM GEOMETRY]` copied from the matrix below

| Pose | Approved base | Arm geometry |
|---|---|---|
| 001 | `base_body_001_neutral_master.png` | both arms lowered; both hands relaxed/open |
| 002 | `base_pose_002_viewer_left_vertical_grip.png` | viewer-left grip; viewer-right relaxed/open |
| 003 | `base_pose_003_viewer_right_vertical_grip.png` | viewer-right grip; viewer-left relaxed/open |
| 004 | `base_pose_004_viewer_left_palm_up.png` | viewer-left palm-up; viewer-right relaxed/open |
| 005 | `base_pose_005_centered_two_hand_grip.png` | both forearms centered; joined two-hand grip |

## Generation prompt

```text
[INSERT LOCKED MASTER SPECIFICATION]

EDIT TARGET AND PLACEMENT REFERENCE:
Use the exact approved [POSE ID] base image as the immutable body, pose,
silhouette, and placement reference. Do not infer arm geometry from another
pose.

TARGET ASSET:
Create one fitted outfit variant from family [OUTFIT FAMILY ID]:
[DESCRIPTION].

Pose lock:
- match the reference neck, shoulders, torso, waist, hips, knees, ankles, and
  foot baseline exactly
- match this arm geometry exactly: [ARM GEOMETRY]
- preserve both wrist positions, hand silhouettes, finger silhouettes, and the
  clear space needed by hand-object layers
- terminate cuffs before wrists; no sleeve, strap, sash, mantle, or ornament may
  cross a hand
- for pose 005, keep the torso region behind the joined hands low-profile

Fit:
- tailor the garment to the approved chibi proportions, never adult proportions
- use believable neck openings, armholes, sleeve bends, waist tension, hems,
  and footwear contact
- include 4–8 px hidden overlap beneath neck and hand occlusion boundaries
- keep back garments in `back_accessories` unless structurally inseparable

Isolation:
- final asset contains outfit pixels only
- remove the body, head, face, hair, skin, hands, held object, aura, and scenery
- retain the full 1254 × 1254 coordinates
- export genuine RGBA transparency; never render a checkerboard

OUTPUT:
One transparent PNG.

FILENAME:
outfit_[FAMILY]_[THEME]_[COLOR]_pose_[POSE].png

[INSERT UNIVERSAL AVOID BLOCK]
```

## Diversity contract

A wardrobe set must vary at least three of these between families: silhouette,
construction, material, cultural/fantasy influence, value structure, and
palette. Recolors of one cut do not count as new outfits.

Recommended coverage includes cloth robes, fitted tailoring, light armor,
utility/workwear, ceremonial clothing, and layered travel clothing. Keep every
design opaque and age-neutral.

## Promotion gate

Before moving a candidate to `assets/outfits/`:

1. confirm native 1254 × 1254 RGBA with genuine transparent corners;
2. composite it over its declared approved pose;
3. inspect neck, both shoulders, elbows, wrists, every finger, waist, knees, and
   feet at 200% zoom;
4. reject any body pixels, checkerboard pixels, pose drift, or hand collision;
5. add a `requires` rule tying the final outfit filename to its exact base-pose
   filename in `config/compatibility.json`.
