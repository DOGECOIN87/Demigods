# Base Body 001 — Binary Integrity Report

Date: 2026-07-20

## Scope

This report records the QA inspection of the approved visual reference at:

`assets/base_body/base_body_001_neutral_master.webp`

The inspection was performed before attempting to register or produce:

`base_pose_001_relaxed_open.png`

## Result

**QA status: BLOCKED**

The approved visual concept remains locked, but the binary currently stored in the repository is not a valid production source. It cannot be safely converted into the required 2048 × 2048 RGBA PNG without reconstructing or redesigning missing image data.

## Current WebP findings

- Repository path: `assets/base_body/base_body_001_neutral_master.webp`
- File size: 29,280 bytes
- SHA-256: `6509e99119f51cee3f19c9b038a0bfae7facebfc0601a35f62d287d654eefe65`
- Container identifies it as a 256 × 256 WebP with alpha.
- Pillow fails while loading it with: `OSError: failed to read next frame`.
- FFmpeg can decode one frame, but the decoded frame contains severe lower-body corruption and missing image data.
- The file therefore fails the required dimensions, integrity, placement, and anatomy QA checks.

## Historical recovery attempt

The deleted temporary upload files were recovered from commit history:

- `.asset-upload/base_body.part00` — 10,032 bytes
- `.asset-upload/base_body.part01` — 10,000 bytes

Concatenating and base64-decoding those files produces a 15,024-byte PNG whose header declares 2048 × 2048 dimensions. The PNG is truncated and only contains a partial upper-head region. Pillow can load it only with truncated-image recovery enabled.

Recovered partial-image findings:

- Declared size: 2048 × 2048
- SHA-256: `4157f4b4645d833469e8aa857c1ad0319769cb5145be5981e3758b4fea69a243`
- Alpha extrema: `(0, 253)`
- Visible alpha bounding box: `(903, 238, 1375, 603)`
- The body, arms, hands, legs, and feet are absent from the recovered data.

The historical chunks are therefore not an intact source file and cannot be used to reconstruct the approved avatar.

## Repository-wide inspection

All current repository image files were inspected. The remaining images are low-resolution reference-sheet previews ranging from approximately 102–256 pixels in width. They are visual guides only and are not an intact production source for the approved master avatar.

Rebuilding the avatar from those previews would constitute a redesign or approximation and would violate the locked-avatar rules.

## Required resolution

Production must remain paused at `base_pose_001_relaxed_open.png` until one of the following is supplied and explicitly approved:

1. The original intact approved avatar as a 2048 × 2048 RGBA PNG on genuine transparency; or
2. An intact lossless source file containing the exact approved avatar at sufficient resolution and placement.

Do not upscale the damaged WebP, approve the truncated historical PNG, regenerate the avatar from memory, or reconstruct it from the reference sheets.
