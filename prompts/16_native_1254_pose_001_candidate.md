# Prompt — Native 1254 Relaxed-Open Master Candidate

This prompt creates exactly one visual-review candidate. It does not approve, register, or promote an asset to production.

## Hard execution gate

- Use the existing 1254 × 1254 Pose 001 candidate as the visual reference. It now meets the locked canvas-size requirement but remains unapproved until manual rig, clothing, anatomy, lighting, identity, and isolation QA pass.
- Use this prompt only when an operator has explicitly authorized a recreated review candidate.
- The image engine must render natively at exactly 1254 × 1254. Do not resize or resample the output after rendering.
- If exact native dimensions or true transparency cannot be produced, stop and report the limitation. Do not create a substitute production file.
- Keep every unapproved result outside `assets/` and `registered_production_assets`.

## Ready-to-run image prompt

Attach only `images/pose_candidates/base_pose_001_relaxed_open_candidate.png` as the visual reference, then use:

```text
Create exactly one full-body Demigods relaxed-open base-avatar review candidate.

REFERENCE ROLE:
Use the attached relaxed-open candidate only for the character's approved anime-chibi visual direction, face identity, warm skin palette, large-head proportions, neutral friendly expression, and general silhouette. It is a 1254 × 1254 non-production reference. Do not resize, upscale, trace, copy pixels from, or treat it as the output source. Ignore any reference detail that conflicts with the locked requirements below.

OUTPUT CONTRACT:
- render natively at exactly 1254 × 1254 pixels
- PNG in RGBA mode with genuine transparent alpha
- one centered, fully visible character only
- no baked checkerboard, white background, floor, contact shadow, halo, glow, text, frame, labels, or interface
- filename: base_pose_001_relaxed_open_candidate_1254.png

LOCKED CANVAS AND RIG:
- canvas center: X 627
- top of head: Y 141
- head center: X 627, Y 343
- eye line: Y 367
- mouth center: X 627, Y 441
- shoulder line: Y 569
- waist center: X 627, Y 808
- viewer-left hand anchor: X 404, Y 772
- viewer-right hand anchor: X 850, Y 772
- foot baseline: Y 1139
- keep all visible character pixels within X 233–1021 and Y 129–1139

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
python scripts/intake_approved_base.py /path/to/base_pose_001_relaxed_open_candidate_1254.png \
  --report docs/qa/base_pose_001_candidate_intake_report.json
```

A binary pass is necessary but not sufficient. Before any production registration, manually compare the result against the selected visual reference and `00_locked_master_specification.md`. Confirm exact identity, proportions, anchors, clothing, anatomy, lighting, alpha isolation, and foot baseline.

If either review fails, leave the file unregistered and record the blocker. Never repair a failed dimension check by resizing.

Only after a human explicitly approves this candidate as the collection master may it be registered. Then derive poses 002–005 sequentially from that approved native 1254 master, changing only the required arms and hands. Pose 003's viewer-right vertical grip must mirror pose 002's grip height at the common waist-level anchor. Produce and QA one pose per request.
