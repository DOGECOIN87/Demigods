# Prompt — Native 2048 Relaxed-Open Master Candidate

This prompt creates exactly one visual-review candidate. It does not approve, register, or promote an asset to production.

## Hard execution gate

- Prefer the intact original approved 2048 × 2048 master whenever it becomes available. Intake that file directly instead of regenerating it.
- Use this prompt only when an operator has explicitly authorized a recreated review candidate.
- The image engine must render natively at exactly 2048 × 2048. Do not upscale, resize, resample, trace, or patch any undersized reference.
- If exact native dimensions or true transparency cannot be produced, stop and report the limitation. Do not create a substitute production file.
- Keep every unapproved result outside `assets/` and `registered_production_assets`.

## Ready-to-run image prompt

Attach only `images/pose_candidates/base_pose_001_relaxed_open_candidate.png` as the visual reference, then use:

```text
Create exactly one full-body Demigods relaxed-open base-avatar review candidate.

REFERENCE ROLE:
Use the attached relaxed-open candidate only for the character's approved anime-chibi visual direction, face identity, warm skin palette, large-head proportions, neutral friendly expression, and general silhouette. It is a 1254 × 1254 non-production reference. Do not resize, upscale, trace, copy pixels from, or treat it as the output source. Ignore any reference detail that conflicts with the locked requirements below.

OUTPUT CONTRACT:
- render natively at exactly 2048 × 2048 pixels
- PNG in RGBA mode with genuine transparent alpha
- one centered, fully visible character only
- no baked checkerboard, white background, floor, contact shadow, halo, glow, text, frame, labels, or interface
- filename: base_pose_001_relaxed_open_candidate_2048.png

LOCKED CANVAS AND RIG:
- canvas center: X 1024
- top of head: Y 230
- head center: X 1024, Y 560
- eye line: Y 600
- mouth center: X 1024, Y 720
- shoulder line: Y 930
- waist center: X 1024, Y 1320
- viewer-left hand anchor: X 660, Y 1260
- viewer-right hand anchor: X 1388, Y 1260
- foot baseline: Y 1860
- keep all visible character pixels within X 380–1668 and Y 210–1860

CHARACTER LOCK:
- premium anime-chibi fantasy game-avatar rendering
- perfectly front-facing and orthographic, with zero yaw, pitch, roll, tilt, or perspective distortion
- symmetrical relaxed neutral stance
- large smooth bald head, large warm-brown eyes, small nose, and gentle closed-mouth smile
- preserve the reference's head-to-body relationship, facial spacing, limb proportions, hand scale, and foot scale
- two anatomically coherent arms, two legs, two hands with five fingers each, and two feet with five toes each
- both arms lowered and relaxed; both hands open at the shared waist-level anchors

WARDROBE LOCK:
- fully clothed at all times
- opaque warm-beige athletic training uniform
- separate sleeveless crew-neck top and knee-length shorts
- clearly visible fabric neckline, armholes, waistband, seams, and shorts hems
- subtle textile texture so the garments read unmistakably as clothing
- full torso and hip coverage
- no bodysuit, underwear, swimwear, cropped top, exposed midriff, exposed hips, or skin-tone garment ambiguity

LIGHTING AND FINISH:
- soft upper-left key light at approximately 45 degrees
- highlights on upper-left-facing surfaces
- form shadows on lower-right-facing surfaces
- subtle cool rim light from the right
- soft neutral ambient fill
- clean silhouette, controlled cel shading, refined painterly finish, crisp anti-aliased edges, and coherent line weight
- no ground shadow on transparent pixels

ISOLATION:
No hair, facial-hair layer, jewelry, handheld object, head accessory, neck accessory, back accessory, wings, aura, scenery, additional character, alternate pose, or contact-sheet layout.

AVOID:
repository screenshots, website interfaces, browser chrome, code windows, contact sheets, trait sheets, infographics, multiple assets, multiple variations, multiple characters, labels, captions, typography, frames, display cards, rendered checkerboards, fake transparency, gray studio backdrops, floor shadows, outer halos, merged trait categories, unrelated hair, unrelated clothing, scenery, character names, franchise names, side views, three-quarter views, action poses, camera tilt, perspective distortion, scale drift, changed rig anchors, cropped edges, incomplete assets, blurry edges, pixelation, inconsistent lighting, front-right key light, swimwear styling, underwear styling, exposed torso, exposed hips, skin-tone garments without visible fabric edges, emphasized anatomical contours, extra fingers, missing fingers, duplicated limbs, malformed hands, or asymmetrical placement.

Return one transparent PNG only. Do not return explanatory text, a preview sheet, or alternate versions.
```

## Mandatory QA and promotion gate

Save the first output outside `assets/`, then run binary intake without `--register`:

```bash
python scripts/intake_approved_base.py /path/to/base_pose_001_relaxed_open_candidate_2048.png \
  --report docs/qa/base_pose_001_candidate_intake_report.json
```

A binary pass is necessary but not sufficient. Before any production registration, manually compare the result against the selected visual reference and `00_locked_master_specification.md`. Confirm exact identity, proportions, anchors, clothing, anatomy, lighting, alpha isolation, and foot baseline.

If either review fails, leave the file unregistered and record the blocker. Never repair a failed dimension check by resizing.

Only after a human explicitly approves this candidate as the collection master may it be registered. Then derive poses 002–005 sequentially from that approved native 2048 master, changing only the required arms and hands. Pose 003's viewer-right vertical grip must mirror pose 002's grip height at the common waist-level anchor. Produce and QA one pose per request.
