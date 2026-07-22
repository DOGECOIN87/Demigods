# Prompt — DG-010 Native 1254 Background 004 Candidate

Continue production on `DOGECOIN87/Demigods` from the latest `main`. Direct updates to `main` are authorized for small, fully audited milestones.

## Locked next asset

- Backlog ID: `DG-010`
- Category: `backgrounds`
- Visual direction: crescent-star dreamscape
- Exact reference: `images/background_candidates/background_004_crescent_star_dreamscape_reference.jpg`
- Reference SHA-256: `7ef8cedff521095601e1225f6ad87f8024930c05d9e458dda138e92ae16c6d3e`
- Reference state: 1024 × 1024 RGB JPEG, preserved byte-for-byte, never a production asset
- Dependency: DG-009 Background 003 is registered
- Candidate path: `images/background_candidates/native_candidates/background_004_crescent_star_dreamscape_candidate.png`
- Intended production path: `assets/backgrounds/background_004_crescent_star_dreamscape.png`
- Shared background specification: `prompts/17_native_1254_backgrounds.md`

Do not merely return another prompt when image generation is available. Produce exactly one candidate image in the current attempt.

## Image-generation request

Attach only the exact Background 004 JPEG above and submit this request:

```text
Create exactly one new full-bleed Demigods Background 004 as a genuinely native 1254 × 1254 pixel PNG. Use the attached 1024 × 1024 crescent-star dreamscape JPEG only as visual-direction and composition reference. Rebuild the complete scene natively from scratch. Do not resize, upscale, resample, trace, tile, extend, convert, patch, or copy the reference.

PRESERVE:
- dreamy navy-to-violet night sky
- soft layered lavender, mauve, indigo, and warm-cream clouds
- one large luminous gold-white crescent moon in the upper-middle composition
- elegant hanging gold stars suspended from the upper edge
- scattered small starlight points
- one centered floating celestial platform surrounded by clouds
- whimsical premium anime-fantasy game-art mood, clean depth, and polished edges

COMPOSITION AND COMPATIBILITY:
- keep the scene symmetrical and front-facing with a stable centered composition
- keep the avatar staging corridor within X 233–1021 and Y 129–1139 readable and uncluttered
- place the floating platform behind the future avatar, centered under the feet, with its usable top aligned visually near the locked foot baseline Y 1139
- keep clouds behind or outside the central body silhouette; do not cover the central face, torso, hands, or feet region with foreground cloud masses
- use upper-left moonlight as the key direction, lower-right form shadows, restrained warm gold accents, and controlled contrast

PLATFORM ORNAMENT:
- use only smooth concentric rings, dots, simple radial lines, diamonds, circles, and starbursts
- no alphabet-like marks, runes, pseudo-writing, equations, sigils, compass letters, or readable symbols
- keep the platform structurally coherent and free of dangling ornaments that could be mistaken for a foreground trait

ISOLATION:
- exactly one background scene only
- no character, person, face, creature, humanoid silhouette, statue, foreground avatar, UI, frame, border, caption, watermark, signature, contact sheet, or unrelated scenery
- no readable letters, words, numbers, labels, typography, or franchise references
- do not add buildings, furniture, weapons, vegetation, extra moons, planets, portals, or objects absent from the approved visual direction

OUTPUT:
- exactly 1254 × 1254 pixels
- PNG in sRGB
- RGB or fully opaque RGBA
- fill every canvas pixel; no transparency, empty border, crop, or presentation frame
- exactly one image and no explanatory text
```

For this background request, the generic `scenery` exclusion in `prompts/01_universal_avoid_block.md` applies only to unrelated or additional scenery; the requested dreamscape itself is the isolated asset. Every other applicable exclusion remains locked.

## Mandatory candidate workflow

1. State the ID, category, reference, prompt, dependency, candidate path, and intended production path.
2. Generate exactly one native candidate from the exact JPEG only.
3. Keep it outside `assets/backgrounds/` until every gate passes.
4. Run complete PNG decode, format, 1254 × 1254 dimensions, RGB/opaque-RGBA, opacity, full-bleed, naming, source-integrity, and SHA-256 checks.
5. Manually inspect reference fidelity, centered platform placement, avatar staging clearance, perspective, lighting, cloud overlap, symbol removal, and isolation.
6. Reject any failed candidate with its exact reason. Never resize, conceal, patch, or register a defect.
7. Display a passing candidate and obtain explicit human visual approval.
8. Only after approval, copy the exact approved bytes to the intended production path and register the exact SHA-256, dimensions, mode, prompt, QA report, candidate provenance, reference hash, native dimensions, and empty postprocessing list in `assets/asset_manifest.json`.
9. Update `docs/trait-production-backlog.md`, `docs/production_status.md`, the background-candidate ledger, and the asset QA report.
10. Run JSON validation, Python compilation, all regression tests, configuration validation, asset/provenance validation, manifest consistency, generator preflight, and output verification when outputs exist. Report the expected missing-`base_bodies` preflight failure accurately.
11. Commit the audited milestone and push directly to `main`; verify the remote commit and keep Issue #4 open.

After Background 004 is registered, the exact next asset is DG-011 Background 005, not a character-aligned trait.
