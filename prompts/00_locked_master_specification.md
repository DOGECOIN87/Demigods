# Locked Master Specification

## Canvas
- 2048 × 2048 px, sRGB.
- Character-compatible traits use true transparent alpha.
- No rendered checkerboard, border, labels, guides, watermark, poster, or presentation layout.

## Shared master-rig coordinates
- Canvas center: X 1024.
- Top of head: Y 230.
- Head center: X 1024, Y 560.
- Eye line: Y 600.
- Mouth center: X 1024, Y 720.
- Shoulder line: Y 930.
- Waist center: X 1024, Y 1320.
- Viewer-left hand anchor: X 660, Y 1260.
- Viewer-right hand anchor: X 1388, Y 1260.
- Foot baseline: Y 1860.
- Maximum character bounds: X 380–1668, Y 210–1860.

## Camera and geometry
- Perfectly front-facing, orthographic appearance.
- Zero yaw, pitch, roll, tilt, and perspective distortion.
- No pose or scale variation outside approved hand-pose templates.
- Preserve all shared coordinates across every compatible asset.

## Lighting
- Soft upper-left key light at approximately 45 degrees.
- Highlights on upper-left-facing surfaces.
- Form shadows on lower-right-facing surfaces.
- Subtle cool rim light from the right.
- Soft neutral ambient fill.
- Identical contrast and shadow softness across assets.
- No cast ground shadow on transparent traits.

## Visual quality
- Premium anime-chibi fantasy game-art style.
- Clean silhouettes, controlled cel shading, refined painterly rendering.
- Crisp anti-aliased edges and coherent line weight.
- Details remain legible at NFT display size.

## Isolation
- Exactly one requested asset per output.
- No unrelated traits, backgrounds, names, labels, or merged categories.
- Do not crop any part of the requested asset.
