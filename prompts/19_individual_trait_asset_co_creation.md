# Prompt — Individual Trait Asset Co-Creation and Submission

Use this prompt with an external image-generation AI to create Demigods asset candidates. Each generated image must still contain exactly one isolated asset, but several separate PNGs may be generated and uploaded as a batch. Repository intake assigns missing IDs and filenames, performs corrections and QA, and decides which candidates qualify for production.

## Practical candidate mode

Candidate creation may proceed before Pose 001 is approved and may occur out of backlog order. When an approved base or pose is unavailable, use the locked coordinate guide and label the file `prealignment_candidate`; final repository alignment and compatibility testing will happen later. Such work may be useful and retained, but it cannot be registered as production-ready until the required base/pose composite passes.

These candidate-stage corrections are allowed when recorded:

- canvas-preserving X/Y translation without scaling or resampling;
- alpha-edge cleanup and removal of stray pixels;
- sRGB profile tagging or RGB/RGBA mode normalization that does not alter dimensions;
- canonical renaming and category-folder relocation;
- small painted cleanup that does not redesign the referenced trait;
- generation and upload of multiple separate PNGs in one batch.

Native size, one isolated asset per PNG, genuine transparency for character traits, and no baked unrelated traits remain required because files without those properties cannot function as modular layers.

## Asset assignment block

Complete the fields you know. Use `ASSIGN DURING REPOSITORY INTAKE` for an unknown backlog ID, digest, filename, dependency, or final path. The category, visual description, and supporting reference must still be identifiable.

```text
BACKLOG ID: [DG-###]
CATEGORY: [exact canonical category]
VISUAL DESCRIPTION: [repository-supported description only]
SOURCE REFERENCE FILE: [exact path or attached file]
SOURCE REFERENCE CELL: [row/column or named region]
SOURCE REFERENCE SHA-256: [exact digest when available]
APPROVED BASE/POSE FILE: [exact file when available; otherwise LOCKED RIG GUIDE / PREALIGNMENT]
POSE/COMPATIBILITY DEPENDENCY: [approved pose, intended pose, or ASSIGN DURING REPOSITORY INTAKE]
INTENDED PRODUCTION PATH: [assets/<category>/<canonical filename>.png]
CANDIDATE FILENAME: [<canonical stem>_candidate_attempt_001.png]
PROMPT FILE: [repository prompt governing this category]
```

If the visual design itself is unsupported or ambiguous, ask for a clearer reference. Missing repository metadata does not block candidate creation; use the intake placeholder above. Do not invent a new design, named character, or unrelated trait.

## Instructions for the image-generation AI

```text
Create exactly one isolated Demigods asset candidate from the supplied Asset Assignment Block and attached repository reference.

NATIVE OUTPUT:
- exactly 1254 × 1254 pixels, generated natively at that size
- PNG in sRGB
- character-compatible trait: RGBA with genuine transparent alpha
- background only: RGB or fully opaque RGBA, full bleed
- keep the entire 1254 × 1254 canvas; never crop to visible content
- exactly one asset and one variation in the image
- return the PNG only, without explanatory text or a contact sheet

PROHIBITED PROCESSING:
- do not resize, upscale, downscale, or resample a finished candidate to satisfy 1254 × 1254; generate it natively
- use undersized catalog cells as visual references for a fresh native render, not as pixels to enlarge into the output
- never remove a background from a flattened preview and call the extraction production-ready
- never bake the approved avatar, pose guide, reference sheet, or another trait into the output
- never hide a defect with blur, glow, darkness, transparency, cropping, or decorative effects

LOCKED RIG:
- canvas center X: 627
- top of head Y: 141
- head center: [627,343]
- eye line Y: 367
- mouth center: [627,441]
- shoulder line Y: 569
- waist center: [627,808]
- viewer-left hand anchor: [404,772]
- viewer-right hand anchor: [850,772]
- foot baseline Y: 1139
- maximum character bounds: [233,129,1021,1139]
- perfectly front-facing with shared scale and proportions

ALIGNMENT:
- use the supplied approved base/pose when available; otherwise use the locked coordinate guide for a prealignment candidate
- aim for the exact full-canvas scale, center line, landmark positions, and silhouette relationship
- output only the assigned trait pixels at their final full-canvas coordinates
- preserve transparent padding everywhere else
- keep the intended front-facing orientation; repository intake may apply recorded canvas-only translation when needed
- do not change the body, face, pose, hands, identity, proportions, or clothing beneath the requested layer
- hand objects should use the intended hand pose when known and must pass an approved-pose composite before registration

LIGHTING AND STYLE:
- upper-left key light at approximately 45 degrees
- highlights on upper-left-facing surfaces
- lower-right form shadows
- subtle cool right rim where appropriate
- premium anime-chibi fantasy game-art rendering
- clean silhouettes, controlled cel shading, refined painterly detail, coherent line weight, crisp anti-aliased edges
- match the approved collection palette and contrast; do not introduce an unsupported style

ISOLATION:
- exactly the requested category and design only
- no named character and no complete character
- no body, skin, face, hair, clothing, accessory, object, aura, shadow, or effect unless it is the requested trait
- no background, floor, scenery, contact shadow, checkerboard, matte, halo, border, frame, label, caption, watermark, signature, guide, UI, or presentation card
- no readable letters, words, numbers, runes, pseudo-writing, or typographic symbols unless the repository reference explicitly requires an approved non-readable ornament
- no duplicate variation, alternate color, before/after view, inset, zoom, or contact-sheet cell

CATEGORY-SPECIFIC ISOLATION:
- rear aura: effect layer only, behind the body; no body or front effect
- back accessory: requested wings/cape/back object only; no hair, outfit, or body
- hair back: rear hair mass only; no bangs/front hair, face, scalp, or accessory
- outfit: garment pixels only; no body/skin/head/hair; opaque modest fabric with clear edges and no skin-tone garment ambiguity
- neck accessory: neck item only; no neck/body/outfit/hair
- eyes: eye artwork only at eye line Y 367; no face, eyebrows, hair, or expression marks
- eyebrows: eyebrow artwork only; no eyes, face, hair, or expression marks
- mouth: mouth artwork only at center [627,441]; no face, nose, eyes, or expression marks
- expression marks: requested marks only; no facial features or face fill
- hair front: bangs/front hair only; no rear hair, face, scalp, or head accessory
- head accessory: requested head item only, aligned to head center [627,343] and top-of-head Y 141; no hair or head
- hand object: object only, aligned to the explicitly named approved hand pose and hand anchor; no hand, arm, body, or extra object
- front aura: foreground effect only; no rear aura, body, object, or background
- global finish: generate only when an explicit repository reference defines it; never invent a generic filter or color grade

ANATOMY AND CONTENT SAFETY:
- do not generate nudity, erotic styling, lingerie, swimwear, underwear presentation, exposed torso/hips, or emphasized anatomical contours
- do not add fingers, hands, limbs, faces, or body fragments to an isolated trait
- garments must remain clearly separate opaque clothing layers

FINAL SELF-CHECK BEFORE RETURNING:
- one PNG only
- exact native 1254 × 1254 canvas
- correct RGB/RGBA contract for the category
- genuine transparency for character traits
- requested design only
- best achievable full-canvas position against every relevant locked anchor; final intake may translate without resampling
- no unrelated or baked-in pixels
- no text, watermark, checkerboard, crop, or contact sheet
- no invented requirement
```

## Candidate upload instructions

Do not upload an unreviewed candidate anywhere under `assets/` and do not edit `assets/asset_manifest.json`.

You may upload one candidate or a batch of separate candidate PNGs. Every file must still contain exactly one asset:

- backgrounds: `images/background_candidates/native_candidates/`
- Pose 001 or pose variants: `images/pose_candidates/`
- all other trait categories: `images/trait_candidates/<category>/`

Use the candidate filename when known. Otherwise use a descriptive temporary name; repository intake will assign the canonical name. Keep failed attempts with `_attempt_###`; reserve the unsuffixed `_candidate.png` name for the current preferred review candidate.

Include this information in the commit message or upload description:

```text
Backlog ID:
Category:
Reference path and cell:
Approved pose dependency:
Intended production path:
Image generator used:
Postprocessing performed, if any:
```

## Repository review performed after upload

The repository maintainer will:

1. verify complete PNG decoding, format, dimensions, mode, alpha/opacity, bounds, naming, and SHA-256;
2. verify source provenance and reject rescaling while documenting any allowed candidate-stage cleanup;
3. overlay the locked rig and inspect composition, identity, anatomy, lighting, isolation, and compatibility;
4. composite the candidate with its approved base/pose and relevant neighboring layers;
5. reject defects with exact reasons or request explicit human visual approval for one candidate or a named batch;
6. move only an approved candidate into its canonical production directory;
7. register exact provenance and SHA-256 in the manifest;
8. update the backlog and production ledger;
9. run JSON, compilation, regression, configuration, asset, provenance, manifest, generator, and output audits when applicable; and
10. commit and push the audited milestone to `main`.

Candidate batches may be created ahead of dependencies. Production promotion remains dependency-aware: representative assets and cross-category composites must pass before a category is mass-registered.
