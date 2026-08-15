# Locked Master Specification

## Canvas
- Every registered production asset is 1254 × 1254 px, sRGB, and uses true transparent alpha.
- Native 1254 × 1254 RGBA output is preferred. When a generator cannot emit the locked canvas, it may return one isolated RGBA source-art PNG with genuine alpha, generous clean transparent margin, and no frame-edge contact; it must then follow `docs/workflows/generator_source_transform.md` before it can be reviewed.
- Source transformation is reduction-only. It never upscales, invents missing pixels, or bypasses the final 1254 × 1254, alpha, rig, composite, and provenance gates.
- No rendered checkerboard, border, labels, guides, watermark, poster, or presentation layout.

## Shared master-rig coordinates
- Canvas center: X 627.
- Top of head: Y 141.
- Head center: X 627, Y 343.
- Eye line: Y 367.
- Mouth center: X 627, Y 441.
- Shoulder line: Y 569.
- Waist center: X 627, Y 808.
- Viewer-left hand anchor: X 404, Y 772.
- Viewer-right hand anchor: X 850, Y 772.
- Foot baseline: Y 1139.
- Maximum character bounds: X 233–1021, Y 129–1139.

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
