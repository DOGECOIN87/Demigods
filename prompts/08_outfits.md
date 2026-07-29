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

## Collars must be open

A standing collar has to be drawn as an **open tube**, not a sealed cone. The
neck opening must be genuinely transparent so the base body's neck reads through
it, and the inside face of the collar must be painted where it would be visible.

`outfit_002` and `outfit_003` were rendered with sealed collars: the opening is
opaque, leaving only 16.3% and 15.6% of the neck visible, so the head reads as
sitting on a tube rather than joining a body. This cannot be repaired after the
fact — removing the painted interior does not reveal the collar's inner face,
because that face was never drawn. Both need a re-render. See
`docs/qa/outfit_chroma_key_cleanup_2026-07-29.md`.

Target at least ~25% of the neck band (jaw Y 457 to shoulder Y 569) visible.

## Never resample after keying without re-contracting

If a keyed layer is rescaled or refit, run the alpha edge contract **after** the
resample. Contracting first does not survive it: the resample blends the still
contaminated neighbouring pixels into a new soft edge and the fringe returns.
That ordering mistake put green key spill on four of the five registered
outfits.

## Promotion gate

Before moving a candidate to `assets/outfits/`:

1. confirm native 1254 × 1254 RGBA with genuine transparent corners;
2. composite it over its declared approved pose;
3. inspect neck, both shoulders, elbows, wrists, every finger, waist, knees, and
   feet at 200% zoom;
4. reject any body pixels, checkerboard pixels, pose drift, or hand collision;
5. confirm the neck opening is transparent and the neck is visible through it;
6. check for green key spill with
   `python scripts/clean_chroma_key.py <file> --out-dir /tmp` and reject if the
   reported green count is materially above zero;
7. add a `requires` rule tying the final outfit filename to its exact base-pose
   filename in `config/compatibility.json`.
