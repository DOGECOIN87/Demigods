# Approved Base Avatar Intake

Use this workflow only when the exact intact approved master-avatar artwork is available.

## Required source

The source must be:

- the exact previously approved artwork
- PNG format
- 1254 × 1254 pixels
- RGBA
- genuine transparent background
- full uncropped avatar
- unchanged placement, proportions, outfit, lighting, and expression

Do not substitute a regenerated approximation, screenshot, reference sheet, damaged WebP, upscaled preview, or recovered partial image.

## Automated intake QA

Run:

```bash
python scripts/intake_approved_base.py /path/to/approved_master.png
```

This produces `base_source_intake_report.json` and checks:

- complete PNG structure verification and full decoding
- exact dimensions
- RGBA mode
- genuine non-opaque alpha
- visible artwork exists
- visible pixels do not touch canvas edges
- inclusive visible bounds remain inside `[233,129,1021,1139]`
- first visible head pixel is exactly Y 141
- final visible foot pixel is exactly Y 1139
- alpha silhouette remains centered on X 627 within the one-pixel antialiasing tolerance
- SHA-256 provenance hash

A passing automated report does not constitute visual approval. Eye, mouth, shoulder, waist, and hand anchors still require a manual coordinate overlay.

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

`assets/base_bodies/base_body_001_neutral_master.png`

It refuses to overwrite an existing production PNG.

The singular `assets/base_body/` directory remains a source-reference area and is not a production layer.

After registration:

1. Run `python scripts/validate_assets.py assets --manifest assets/asset_manifest.json --repository-root .`.
2. Compare the production PNG against the locked anchors.
3. Add a `registered_production_assets` entry to `assets/asset_manifest.json` only after binary and manual visual QA both pass:

   ```json
   {
     "id": "base_body_001",
     "category": "base_bodies",
     "path": "assets/base_bodies/base_body_001_neutral_master.png",
     "status": "production_ready",
     "sha256": "<exact lowercase SHA-256 of the accepted PNG>",
     "dimensions": [1254, 1254]
   }
   ```

   The base-body portion of the registry remains empty until a candidate passes automated rig geometry and manual approval. The already registered Background 001 is independent; this example does not authorize automatic base promotion.
4. Run `python scripts/validate_manifest_consistency.py --manifest assets/asset_manifest.json --repository-root .`.
5. Determine whether the same artwork satisfies `base_pose_001_relaxed_open.png`.
6. Register the same artwork at `assets/base_bodies/base_pose_001_relaxed_open.png` only when it already qualifies.
7. Update `assets/asset_manifest.json` and `docs/production_status.md`.
8. Commit the PNG, intake report, validation result, manifest, and status change together.
9. Verify the files on `main` before proceeding to pose 002.
