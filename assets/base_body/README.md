# Base Avatar Assets

This folder contains the approved visual anchor for the shared Demigods master rig.

## Approved visual reference

- `base_body_001_neutral_master.webp`
- Visual status: approved and locked
- Production status: **QA blocked — do not use for generation or compositing**
- Orientation: perfectly front-facing
- Pose: neutral, symmetrical stance
- Outfit: opaque beige training uniform with clearly defined neckline, armholes, waistband, and shorts hems
- Lighting: upper-left key light; lower-right form shadows; subtle right rim light
- Intended background: transparent

The approved visual design must not be redesigned or replaced merely because another generation appears better.

## Binary-integrity warning

The repository WebP is damaged and cannot be converted into a valid production PNG. It is a 256 × 256 file whose decoded frame contains severe missing and corrupted lower-body data. Historical upload chunks also recover only a truncated partial PNG containing the upper-head region.

See the complete findings in:

`docs/qa/base_body_001_integrity_report.md`

The damaged WebP remains archival only. Production now proceeds from the intact 1254 × 1254 RGBA candidate at `images/pose_candidates/base_pose_001_relaxed_open_candidate.png` after manual identity, rig, clothing, lighting, anatomy, and isolation QA.

Do not upscale the damaged WebP, use truncated-image recovery as a production asset, regenerate the avatar from memory, or reconstruct it from the reference sheets.

## Production rules

All interchangeable traits must preserve the approved avatar's head position, eye line, shoulder width, hand anchors, scale, center line, and foot baseline. Hair, outfits, facial overlays, accessories, objects, and effects must be exported as separate transparent layers rather than merged into the base asset.
