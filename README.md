# Demigods 777 — Modular Generative Asset System

Production specifications, category prompts, reference images, validation tools, and generation rules for a 777-piece interchangeable chibi-fantasy collection.

## Current production status

**Phase 1 uses a locked 1254 × 1254 canvas. The former resolution blocker is removed; Pose 001 is awaiting manual production approval.**

- Live ledger: `docs/production_status.md`
- QA report: `docs/qa/base_body_001_integrity_report.md`
- Intake workflow: `docs/workflows/approved_base_intake.md`
- Tracked blocker: [Issue #4](https://github.com/DOGECOIN87/Demigods/issues/4)

The approved visual design remains locked. Use the intact 1254 × 1254 RGBA Pose 001 candidate for review; do not reconstruct the avatar from the damaged repository WebP.

## Core requirements

- Every non-background trait is a separate transparent PNG.
- Every character-compatible asset uses one locked 1254 × 1254 master canvas and shared proportionally rebased rig.
- All assets are perfectly front-facing with identical scale, anchors, proportions, and crop.
- Key light comes from the upper-left; form shadows fall toward the lower-right.
- Character names are not part of the trait system.
- Trait categories remain isolated: no baked-in unrelated layers.
- The generator creates exactly 777 unique approved outputs from the valid combination space.

## Repository structure

```text
assets/                   Canonical full-canvas production categories and source references
prompts/                  Reusable image-generation and extraction prompts
docs/                     Layer order, naming, rig, QA, workflow, and production status
images/reference_sheets/  Visual guides from the design process; never production assets
images/background_candidates/  Exact user-supplied background references awaiting native production renders
config/                   Collection and compatibility configuration
metadata/                 Token metadata schema
scripts/                  Intake, validation, configuration, generation, and output-verification tools
tests/                    Automated validator, configuration, generator, and output tests
.github/workflows/        Continuous production validation
```

## Canonical base-body paths

Production-ready neutral bodies and pose variants belong in `assets/base_bodies/`:

```text
assets/base_bodies/base_body_001_neutral_master.png
assets/base_bodies/base_pose_001_relaxed_open.png
assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png
assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png
assets/base_bodies/base_pose_004_viewer_left_palm_up.png
assets/base_bodies/base_pose_005_centered_two_hand_grip.png
```

The singular `assets/base_body/` folder is a source-reference area and is excluded from production-layer discovery.

## Validation

Install dependencies and run the automated tests:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Audit the locked collection geometry and compatibility rules:

```bash
python scripts/validate_config.py \
  --collection config/collection.json \
  --compatibility config/compatibility.json \
  --assets assets \
  --json-report config_validation_report.json
```

The configuration preflight rejects changed locked anchors, malformed rules, missing trait references, duplicate relationships, impossible same-layer requirements, and requires/excludes contradictions.

Audit the repository during the current empty-library preproduction phase:

```bash
python scripts/validate_assets.py assets \
  --manifest assets/asset_manifest.json \
  --repository-root . \
  --allow-empty \
  --json-report asset_validation_report.json
```

The asset validator performs complete binary decoding and checks PNG format, dimensions, RGBA and alpha behavior, visible bounds, folder/category agreement, three-digit numbering, SHA-256 values, blocked-reference consistency, and byte-for-byte provenance for all eight background candidates.

Verify provenance for every registered production asset before treating it as usable:

```bash
python scripts/validate_manifest_consistency.py \
  --manifest assets/asset_manifest.json \
  --repository-root . \
  --json-report manifest_consistency_report.json
```

The registry remains empty until the existing Pose 001 candidate passes manual visual QA and is explicitly promoted. Once an asset is registered, the checker requires its file to exist at the declared production path, remain `production_ready`, match its declared SHA-256 and dimensions, and pass category-aware PNG QA.

## Exact-777 generation

After the production library is complete:

```bash
python scripts/generate_777.py --preflight-only
python scripts/generate_777.py --seed <FINAL_SEED> --dry-run --output output/dry_run
python scripts/generate_777.py --seed <FINAL_SEED> --output output/final
```

The generator rejects invalid assets and stale output directories, rejects duplicate signatures, creates token IDs `0001` through `0777`, writes matching metadata, and records deterministic trait and image provenance hashes.

Audit a dry run before rendering:

```bash
python scripts/validate_output.py output/dry_run \
  --allow-dry-run \
  --json-report dry_run_validation_report.json
```

Independently verify the final render before release:

```bash
python scripts/validate_output.py output/final \
  --json-report final_output_validation_report.json
```

The output verifier requires the exact `0001`–`0777` image and metadata sets, recomputes every image hash and trait signature, validates metadata layer order and source paths, confirms final images are complete opaque RGBA PNGs, and independently recomputes both collection provenance hashes.

## Recommended workflow

1. Complete manual QA and approve the 1254 × 1254 Pose 001 master candidate.
2. Lock the rig coordinates and lighting.
3. Approve hand-pose variants sequentially.
4. Create one isolated test asset from every category.
5. Composite cross-category stress-test characters.
6. Correct collisions, clipping, hidden overlaps, and layer order.
7. Produce remaining assets one item per output.
8. Validate and commit every accepted asset or small verified milestone.
9. Define only necessary compatibility exclusions.
10. Dry-run, verify, render, and independently verify exactly 777 unique tokens.

## Important clarification

The trait library may contain far more than 777 mathematical combinations. The collection generator samples exactly 777 validated unique combinations rather than forcing the product of category counts to equal 777.
