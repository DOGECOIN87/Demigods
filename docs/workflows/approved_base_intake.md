# Approved Base Avatar Intake

Use this workflow only when the exact intact approved master-avatar artwork is available.

## Required source

The source must be:

- the exact previously approved artwork
- PNG format
- 2048 × 2048 pixels
- RGBA
- genuine transparent background
- full uncropped avatar
- unchanged placement, proportions, outfit, lighting, and expression

Do not substitute a regenerated approximation, screenshot, reference sheet, damaged WebP, upscaled preview, or recovered partial image.

## Binary QA

Run:

```bash
python scripts/intake_approved_base.py /path/to/approved_master.png
```

This produces `base_source_intake_report.json` and checks:

- complete decoding
- PNG format
- exact dimensions
- RGBA mode
- non-opaque alpha
- visible artwork exists
- visible pixels do not touch canvas edges
- SHA-256 provenance hash

A passing binary report does not constitute visual approval.

## Manual visual QA

Before registration, compare the candidate directly against the approved visual reference and locked specifications. Confirm:

- exact head and face shape
- exact body proportions
- exact shoulder width
- exact arm and leg lengths
- exact hand scale and five-finger anatomy
- exact foot placement and baseline
- exact neutral beige full-coverage outfit
- exact front-facing camera
- exact upper-left lighting
- no backdrop, floor shadow, or unintended glow
- relaxed-open arm and hand state, when registering pose 001

## Registration

After binary and manual QA both pass, run:

```bash
python scripts/intake_approved_base.py /path/to/approved_master.png \
  --register \
  --report docs/qa/base_body_001_intake_report.json
```

The script writes:

`assets/base_body/base_body_001_neutral_master.png`

It refuses to overwrite an existing production PNG.

After registration:

1. Run `python scripts/validate_assets.py assets/base_body`.
2. Compare the production PNG against the locked anchors.
3. Determine whether the same artwork satisfies `base_pose_001_relaxed_open.png`.
4. Update `assets/asset_manifest.json`.
5. Commit the PNG, intake report, validation result, and manifest change together.
6. Verify the files on `main` before proceeding to pose 002.
